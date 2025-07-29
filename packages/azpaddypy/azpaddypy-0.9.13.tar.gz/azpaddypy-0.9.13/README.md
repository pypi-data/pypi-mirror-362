# azpaddypy

## Overview

`azpaddypy` provides robust, production-grade tools for managing Azure resources, with a focus on multi-tenant SaaS applications. The CosmosPromptManager enables efficient, tenant-aware prompt storage and retrieval using Azure Cosmos DB.

## CosmosPromptManager: Multi-Tenant Prompt Management

### Key Features
- **Multi-Tenancy**: All prompt operations are tenant-aware. Use `tenant_id` for isolation and performance.
- **Partition Key Logic**: Uses `tenant_id` as the Cosmos DB partition key when provided, falling back to `prompt_name` for global/shared prompts.
- **Batch Operations**: Batch methods (`get_prompts_batch`, `save_prompts_batch`, `delete_prompts_batch`) are implemented as sequential single operations. For large-scale batch, consider Cosmos DB stored procedures.
- **Retry Logic**: All operations use exponential backoff for resilience.
- **Async Support**: Async methods are available for high-throughput scenarios.
- **Comprehensive Logging**: Standardized logging and error handling throughout.

### Best Practices
- **Always provide `tenant_id`** for tenant-specific operations in multi-tenant SaaS.
- Use global prompts (no `tenant_id`) only for shared defaults.
- For large-scale batch operations, use Cosmos DB stored procedures for efficiency.
- For performance, ensure your Cosmos DB container uses `/tenant_id` as the partition key.

### Example Usage

```python
from azpaddypy.tools.cosmos_prompt_manager import CosmosPromptManager

# Initialize manager (see full example for AzureCosmosDB setup)
prompt_manager = CosmosPromptManager(
    cosmos_client=cosmos_client,
    database_name="prompts",
    container_name="prompts"
)

# Save a tenant-specific prompt
prompt_manager.save_prompt(
    prompt_name="answering_user_prompt",
    prompt_data="Your prompt template here...",
    tenant_id="tenant_abc123"
)

# Retrieve a tenant-specific prompt
prompt = prompt_manager.get_prompt(
    prompt_name="answering_user_prompt",
    tenant_id="tenant_abc123"
)

# List all prompts for a tenant
prompt_names = prompt_manager.list_prompts(tenant_id="tenant_abc123")

# Batch save prompts (sequential, not true batch)
prompts_to_save = [
    {"prompt_name": "prompt1", "prompt_data": "template1"},
    {"prompt_name": "prompt2", "prompt_data": "template2"}
]
prompt_manager.save_prompts_batch(prompts_to_save, tenant_id="tenant_abc123")

# Batch delete prompts
prompt_manager.delete_prompts_batch(["prompt1", "prompt2"], tenant_id="tenant_abc123")
```

### Partition Key Strategy
- For best performance and scalability, use `/tenant_id` as the partition key in your Cosmos DB container.
- This ensures tenant data is isolated and queries are efficient.

### Batch Operation Caveats
- The `*_batch` methods perform sequential single operations, not true Cosmos DB batch.
- For high-volume batch, use Cosmos DB stored procedures or `read_many_items`.

### Error Handling & Logging
- All operations use retry logic with exponential backoff.
- Errors are logged with context for troubleshooting.

### Async Usage
- Async methods are available for high-throughput scenarios.
- See the code for details on async context management.

## Configuration Management
- The configuration system is fully multi-tenant ready.
- All settings (checkboxes, dropdowns, etc.) in the admin UI are tenant-specific when a tenant is selected.
- Configurations are saved and loaded per tenant, with fallback to global defaults.

## License
MIT 