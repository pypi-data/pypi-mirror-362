"""
Azure Cosmos DB Prompt Management Tool (Multi-Tenant Ready)

This module provides a robust, multi-tenant prompt management system using Azure Cosmos DB
for storing and retrieving prompts with real-time updates and optimized performance.

Features:
- Multi-tenant support: all operations are tenant-aware via tenant_id partition key
- Partition key logic: uses tenant_id as partition key when available, falls back to prompt_name for global prompts
- Batch operations: implemented as sequential single operations (no true Cosmos batch)
- Configurable consistency levels (eventual, bounded, strong)
- Real-time updates across all instances
- Async support for high-throughput applications
- Retry logic with exponential backoff for resilience
- Comprehensive error handling and logging
- Backward compatibility with existing system
- Standardized azpaddypy logging and error handling

Best Practices:
- For multi-tenant SaaS, always provide tenant_id for isolation and performance
- Use global prompts (no tenant_id) only for shared defaults
- For large-scale batch operations, consider Cosmos DB stored procedures for efficiency
"""

import json
import time
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any, Union, Literal
from contextlib import asynccontextmanager
from functools import wraps

from azure.core.exceptions import ResourceNotFoundError
from azure.cosmos import CosmosClient
from azure.cosmos.aio import CosmosClient as AsyncCosmosClient

from ..resources.cosmosdb import AzureCosmosDB
from ..mgmt.logging import AzureLogger

def retry_with_exponential_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0
):
    """
    Decorator for retry logic with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds for the first retry
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff calculation
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        # Last attempt failed, raise the exception
                        break
                    
                    # Calculate delay for next attempt
                    delay = min(base_delay * (exponential_base ** attempt), max_delay)
                    
                                    # Log the retry attempt
                if args and hasattr(args[0], 'logger'):
                    args[0].logger.warning(
                        f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s",
                        extra={
                            "error": str(e), 
                            "attempt": attempt + 1,
                            "function": func.__name__
                        }
                    )
                    
                    time.sleep(delay)
            
            # All attempts failed
            raise last_exception
            
        return wrapper
    return decorator


class CosmosPromptManager:
    """
    Azure Cosmos DB-based prompt management tool with optimized performance,
    batch operations, and configurable consistency levels.
    
    This tool follows the azpaddypy pattern for Azure resource management with
    proper logging, error handling, and configuration management. It leverages
    Cosmos DB's integrated cache for optimal performance without additional 
    local caching layers.
    
    Features:
    - Optimized Cosmos DB integrated cache usage
    - Batch operations for multiple prompts
    - Configurable consistency levels (eventual, bounded, strong)
    - Async support for high-throughput scenarios
    - Retry logic with exponential backoff
    - Comprehensive error handling and logging
    """

    def __init__(
        self,
        cosmos_client: AzureCosmosDB,
        database_name: str = "prompts",
        container_name: str = "prompts",
        service_name: str = "azure_cosmos_prompt_manager",
        service_version: str = "1.0.0",
        logger: Optional[AzureLogger] = None,
        max_retries: int = 3,
        base_retry_delay: float = 1.0,
    ):
        """
        Initialize CosmosPromptManager.
        
        Args:
            cosmos_client: AzureCosmosDB client instance
            database_name: Name of the Cosmos DB database
            container_name: Name of the Cosmos DB container
            service_name: Service name for logging
            service_version: Service version for logging
            logger: Optional AzureLogger instance
            max_retries: Maximum number of retry attempts for failed operations
            base_retry_delay: Base delay in seconds for retry logic
        
        Multi-Tenancy:
            All prompt operations are tenant-aware. If tenant_id is provided, it is used as the partition key.
            If not, prompt_name is used (for global/shared prompts).
        """
        self.cosmos_client = cosmos_client
        self.database_name = database_name
        self.container_name = container_name
        self.service_name = service_name
        self.service_version = service_version
        self.max_retries = max_retries
        self.base_retry_delay = base_retry_delay

        if logger:
            self.logger = logger
        else:
            self.logger = AzureLogger(
                service_name=service_name,
                service_version=service_version,
                enable_console_logging=True,
            )

        self.logger.info(
            f"Cosmos Prompt Manager initialized for service '{service_name}' v{service_version}",
            extra={
                "database_name": database_name,
                "container_name": container_name,
                "max_retries": max_retries,
                "base_retry_delay": base_retry_delay,
            }
        )

    def _create_prompt_document(self, prompt_name: str, prompt_data: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create Cosmos DB document from prompt data.
        
        Args:
            prompt_name: Name of the prompt
            prompt_data: Either a string template or dictionary with prompt data
            
        Returns:
            Dictionary formatted for Cosmos DB storage
        """
        # If prompt_data is a dict, merge it; otherwise, treat it as prompt_template content
        if isinstance(prompt_data, dict):
            # prompt_data is already a dictionary, merge with context
            context = {
                "id": prompt_name,
                "prompt_name": prompt_name,
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
            merged_data = {**prompt_data, **context}
        else:
            # prompt_data is a string or other type, treat as prompt_template
            merged_data = {
                "id": prompt_name,
                "prompt_name": prompt_name,
                "description": f"Autogenerated prompt for {prompt_name}",
                "version": "1.0.0",
                "prompt_template": prompt_data,
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
        return merged_data

    def _get_cache_staleness_ms(self, consistency_level: Literal["eventual", "bounded", "strong"]) -> int:
        """
        Get cache staleness in milliseconds based on consistency level.
        
        Args:
            consistency_level: Desired consistency level
            
        Returns:
            Cache staleness in milliseconds
        """
        staleness_config = {
            "eventual": 30000,    # 30 seconds for non-critical prompts
            "bounded": 5000,      # 5 seconds for normal prompts
            "strong": 0           # 0 milliseconds for critical prompts (no cache)
        }
        return staleness_config.get(consistency_level, 5000)

    def get_prompt(
        self, 
        prompt_name: str,
        tenant_id: Optional[str] = None,
        consistency_level: Literal["eventual", "bounded", "strong"] = "bounded",
        max_integrated_cache_staleness_in_ms: Optional[int] = None
    ) -> Optional[str]:
        """
        Retrieve a prompt template from Cosmos DB, tenant-aware.
        
        Args:
            prompt_name: Name of the prompt
            tenant_id: Optional tenant ID for tenant-specific prompt
            consistency_level: Consistency level for the read operation
            max_integrated_cache_staleness_in_ms: Optional override for cache staleness
        
        Returns:
            Prompt template string if found, None otherwise
        
        Notes:
            - Uses tenant_id as partition key if provided, else prompt_name
            - If tenant_id is provided, verifies the document's tenant_id matches
        """
        @retry_with_exponential_backoff(max_retries=self.max_retries)
        def _get_with_retry():
            attributes = {
                "prompt_name": prompt_name,
                "consistency_level": consistency_level,
            }
            if tenant_id is not None:
                attributes["tenant_id"] = tenant_id
                
            with self.logger.create_span(
                "CosmosPromptManager.get_prompt", 
                attributes=attributes
            ):
                # Determine cache staleness
                if max_integrated_cache_staleness_in_ms is None:
                    staleness_ms = self._get_cache_staleness_ms(consistency_level)
                else:
                    staleness_ms = max_integrated_cache_staleness_in_ms
                
                # Read from Cosmos DB with optimized cache settings
                doc = self.cosmos_client.read_item(
                    database_name=self.database_name,
                    container_name=self.container_name,
                    item_id=prompt_name,
                    partition_key=tenant_id if tenant_id else prompt_name,
                    max_integrated_cache_staleness_in_ms=staleness_ms
                )
                
                # Check if document was found
                if doc is None:
                    self.logger.warning(f"Prompt not found in Cosmos DB: {prompt_name}")
                    return None
                
                # If tenant_id is provided, verify it matches the document's tenant_id
                if tenant_id and doc.get("tenant_id") != tenant_id:
                    self.logger.warning(f"Prompt {prompt_name} found, but tenant_id does not match.")
                    return None

                prompt_template = doc.get("prompt_template", "")
                return prompt_template
        
        return _get_with_retry()

    def get_prompts_batch(
        self, 
        prompt_names: List[str],
        tenant_id: Optional[str] = None,
        consistency_level: Literal["eventual", "bounded", "strong"] = "bounded"
    ) -> Dict[str, Optional[str]]:
        """
        Retrieve multiple prompt templates from Cosmos DB, tenant-aware.
        
        Args:
            prompt_names: List of prompt names to retrieve
            tenant_id: Optional tenant ID for tenant-specific prompts
            consistency_level: Consistency level for the read operations
        
        Returns:
            Dictionary with prompt names as keys and prompt templates as values
        
        Notes:
            - This is not a true Cosmos DB batch; it performs sequential single gets
            - For large-scale batch, consider using stored procedures or read_many_items
        """
        # This is a simplified implementation. A true batch operation
        # would use a stored procedure or read_many_items if available.
        prompts = {}
        for name in prompt_names:
            prompts[name] = self.get_prompt(name, tenant_id, consistency_level)
        return prompts

    def save_prompt(self, prompt_name: str, prompt_data: Union[str, Dict[str, Any]], tenant_id: Optional[str] = None) -> bool:
        """
        Save or update a prompt in Cosmos DB, tenant-aware.
        
        Args:
            prompt_name: Name of the prompt
            prompt_data: Either a string template or dictionary with prompt data
            tenant_id: Optional tenant ID to associate with the prompt
        
        Returns:
            True if successful, False otherwise
        
        Notes:
            - Uses tenant_id as partition key if provided, else prompt_name
            - Adds tenant_id to the document if provided
            - Uses retry logic for resilience
        """
        prompt_document = self._create_prompt_document(prompt_name, prompt_data)
        if tenant_id:
            prompt_document["tenant_id"] = tenant_id

        @retry_with_exponential_backoff(max_retries=self.max_retries)
        def _save_with_retry():
            attributes = {"prompt_name": prompt_name}
            if tenant_id is not None:
                attributes["tenant_id"] = tenant_id
                
            with self.logger.create_span(
                "CosmosPromptManager.save_prompt",
                attributes=attributes
            ):
                self.cosmos_client.upsert_item(
                    database_name=self.database_name,
                    container_name=self.container_name,
                    item=prompt_document,
                )
            return True
        return _save_with_retry()

    def save_prompts_batch(
        self, 
        prompts: List[Dict[str, Any]],
        tenant_id: Optional[str] = None
    ) -> Dict[str, bool]:
        """
        Save or update multiple prompts in Cosmos DB, tenant-aware.
        
        Args:
            prompts: List of dictionaries, each containing 'prompt_name' and 'prompt_data'
            tenant_id: Optional tenant ID to associate with all prompts in the batch
        
        Returns:
            Dictionary with prompt names as keys and success status as values
        
        Notes:
            - This is not a true Cosmos DB batch; it performs sequential single upserts
            - For large-scale batch, consider using stored procedures
            - Invalid prompt dicts are skipped with a warning
        """
        results = {}
        for prompt in prompts:
            prompt_name = prompt.get("prompt_name")
            prompt_data = prompt.get("prompt_data")
            if prompt_name and prompt_data:
                results[prompt_name] = self.save_prompt(prompt_name, prompt_data, tenant_id)
            else:
                self.logger.warning("Invalid prompt format in batch, skipping.", extra={"prompt": prompt})
        return results

    def list_prompts(self, tenant_id: Optional[str] = None) -> List[str]:
        """
        List all prompt names from Cosmos DB, optionally filtered by tenant_id.
        
        Args:
            tenant_id: Optional tenant ID to filter prompts
        
        Returns:
            List of prompt names
        
        Notes:
            - Uses a SQL query with tenant_id filter if provided
            - Returns only the prompt IDs
        """
        with self.logger.create_span(
            "CosmosPromptManager.list_prompts",
            attributes={"tenant_id": tenant_id} if tenant_id else {}
        ):
            query = "SELECT c.id FROM c"
            params = []
            if tenant_id:
                query += " WHERE c.tenant_id = @tenant_id"
                params.append({"name": "@tenant_id", "value": tenant_id})

            items = self.cosmos_client.query_items(
                database_name=self.database_name,
                container_name=self.container_name,
                query=query,
                parameters=params,
                enable_cross_partition_query=True,
            )
            return [item["id"] for item in items]

    def delete_prompt(self, prompt_name: str, tenant_id: Optional[str] = None) -> bool:
        """
        Delete a prompt from Cosmos DB, tenant-aware.
        
        Args:
            prompt_name: Name of the prompt to delete
            tenant_id: Optional tenant ID for validation before deletion
        
        Returns:
            True if successful, False otherwise
        
        Notes:
            - If tenant_id is provided, validates ownership before deletion
            - Uses tenant_id as partition key if provided, else prompt_name
            - Uses retry logic for resilience
        """
        @retry_with_exponential_backoff(max_retries=self.max_retries)
        def _delete_with_retry():
            attributes = {"prompt_name": prompt_name}
            if tenant_id is not None:
                attributes["tenant_id"] = tenant_id
                
            with self.logger.create_span(
                "CosmosPromptManager.delete_prompt",
                attributes=attributes
            ):
                if tenant_id:
                    # If tenant_id is provided, read the item first to validate ownership
                    item = self.get_prompt_details(prompt_name, tenant_id)
                    if not item:
                        self.logger.warning(f"Prompt '{prompt_name}' not found for tenant '{tenant_id}'. Deletion aborted.")
                        return False

                self.cosmos_client.delete_item(
                    database_name=self.database_name,
                    container_name=self.container_name,
                    item_id=prompt_name,
                    partition_key=tenant_id if tenant_id else prompt_name,
                )
            return True
        return _delete_with_retry()

    def get_prompt_details(self, prompt_name: str, tenant_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get full details of a prompt from Cosmos DB, tenant-aware.
        
        Args:
            prompt_name: Name of the prompt
            tenant_id: Optional tenant ID to filter prompts
        
        Returns:
            Dictionary with prompt details if found, otherwise None
        
        Notes:
            - Uses tenant_id as partition key if provided, else prompt_name
            - If tenant_id is provided, verifies the document's tenant_id matches
        """
        attributes = {"prompt_name": prompt_name}
        if tenant_id is not None:
            attributes["tenant_id"] = tenant_id
            
        with self.logger.create_span(
            "CosmosPromptManager.get_prompt_details",
            attributes=attributes
        ):
            doc = self.cosmos_client.read_item(
                database_name=self.database_name,
                container_name=self.container_name,
                item_id=prompt_name,
                partition_key=tenant_id if tenant_id else prompt_name,
            )
            if doc and (not tenant_id or doc.get("tenant_id") == tenant_id):
                return doc
            return None

    def get_all_prompt_details(self, tenant_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get full details of all prompts, optionally filtered by tenant_id.
        
        Args:
            tenant_id: Optional tenant ID to filter prompts
        
        Returns:
            List of dictionaries with prompt details
        
        Notes:
            - Uses a SQL query with tenant_id filter if provided
            - Returns all fields for each prompt
        """
        with self.logger.create_span(
            "CosmosPromptManager.get_all_prompt_details",
            attributes={"tenant_id": tenant_id} if tenant_id else {}
        ):
            query = "SELECT * FROM c"
            params = []
            if tenant_id:
                query += " WHERE c.tenant_id = @tenant_id"
                params.append({"name": "@tenant_id", "value": tenant_id})

            items = self.cosmos_client.query_items(
                database_name=self.database_name,
                container_name=self.container_name,
                query=query,
                parameters=params,
                enable_cross_partition_query=True,
            )
            return list(items)

    def delete_prompts_batch(self, prompt_names: List[str], tenant_id: Optional[str] = None) -> Dict[str, bool]:
        """
        Delete multiple prompts from Cosmos DB in a single batch, tenant-aware.
        
        Args:
            prompt_names: List of prompt names to delete
            tenant_id: Optional tenant ID for validation before deletion
        
        Returns:
            Dictionary with prompt names as keys and success status as values
        
        Notes:
            - This is not a true Cosmos DB batch; it performs sequential single deletes
            - For large-scale batch, consider using stored procedures
        """
        results = {}
        for prompt_name in prompt_names:
            results[prompt_name] = self.delete_prompt(prompt_name, tenant_id)
        return results

    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on the prompt manager.
        
        Returns:
            Dictionary with health check results
        """
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": {
                "name": self.service_name,
                "version": self.service_version
            },
            "checks": {}
        }
        
        try:
            # Test database connection
            start_time = time.time()
            self.cosmos_client.get_database(self.database_name)
            connection_time = time.time() - start_time
            
            health_status["checks"]["database_connection"] = {
                "status": "healthy",
                "response_time_ms": int(connection_time * 1000)
            }
            
            # Test container access
            start_time = time.time()
            container = self.cosmos_client.get_container(self.database_name, self.container_name)
            container_time = time.time() - start_time
            
            health_status["checks"]["container_access"] = {
                "status": "healthy",
                "response_time_ms": int(container_time * 1000)
            }
            
            # Test basic operations
            start_time = time.time()
            prompts = self.list_prompts()
            list_time = time.time() - start_time
            
            health_status["checks"]["basic_operations"] = {
                "status": "healthy",
                "response_time_ms": int(list_time * 1000),
                "prompt_count": len(prompts)
            }
            
            self.logger.info("Health check completed successfully")
            
        except Exception as e:
            health_status["status"] = "unhealthy"
            health_status["error"] = str(e)
            health_status["checks"]["error"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            self.logger.error(f"Health check failed: {e}", exc_info=True)
        
        return health_status

    @asynccontextmanager
    async def async_context(self):
        """
        Asynchronous context manager for Cosmos DB client.
        """
        async with self.cosmos_client.async_client_context() as client:
            yield self

    async def get_prompt_async(
        self, 
        prompt_name: str,
        tenant_id: Optional[str] = None,
        consistency_level: Literal["eventual", "bounded", "strong"] = "bounded"
    ) -> Optional[str]:
        """
        Asynchronously get a prompt template from Cosmos DB.
        
        Args:
            prompt_name: Name of the prompt
            tenant_id: Optional tenant ID to filter prompts
            consistency_level: Consistency level for the read operation
            
        Returns:
            Prompt template if found, None otherwise
        """
        async with self.cosmos_client.async_client_context() as client:
            container = client.get_database_client(self.database_name).get_container_client(self.container_name)
            
            staleness_ms = self._get_cache_staleness_ms(consistency_level)
            
            options = {}
            if staleness_ms > 0:
                options['max_integrated_cache_staleness_in_ms'] = staleness_ms
            
            try:
                doc = await container.read_item(
                    item=prompt_name,
                    partition_key=tenant_id if tenant_id else prompt_name,
                    **options
                )
                
                if doc and (not tenant_id or doc.get("tenant_id") == tenant_id):
                    return doc.get("prompt_template", "")
                
                return None
            except Exception as e:
                self.logger.error(f"Error in async prompt retrieval {prompt_name}: {e}", exc_info=True)
                return None


def create_cosmos_prompt_manager(
    cosmos_client: AzureCosmosDB,
    database_name: str = "prompts",
    container_name: str = "prompts",
    service_name: str = "azure_cosmos_prompt_manager",
    service_version: str = "1.0.0",
    logger: Optional[AzureLogger] = None,
    max_retries: int = 3,
    base_retry_delay: float = 1.0,
) -> CosmosPromptManager:
    """
    Factory function to create an instance of CosmosPromptManager with enhanced features.
    
    Args:
        cosmos_client: AzureCosmosDB client instance
        database_name: Name of the Cosmos DB database
        container_name: Name of the Cosmos DB container
        service_name: Service name for logging
        service_version: Service version for logging
        logger: Optional AzureLogger instance
        max_retries: Maximum number of retry attempts
        base_retry_delay: Base delay in seconds for retry logic
        
    Returns:
        Configured CosmosPromptManager instance with enhanced features
    """
    return CosmosPromptManager(
        cosmos_client=cosmos_client,
        database_name=database_name,
        container_name=container_name,
        service_name=service_name,
        service_version=service_version,
        logger=logger,
        max_retries=max_retries,
        base_retry_delay=base_retry_delay,
    ) 