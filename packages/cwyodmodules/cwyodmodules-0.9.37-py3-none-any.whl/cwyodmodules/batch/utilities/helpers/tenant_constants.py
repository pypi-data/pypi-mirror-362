"""Constants for tenant management."""

# Global tenant UUID (nil UUID)
GLOBAL_TENANT_ID = "00000000-0000-0000-0000-000000000000"
GLOBAL_TENANT_NAME = "global"

# Legacy global tenant string (for backward compatibility during migration)
LEGACY_GLOBAL_TENANT_ID = "global"

def is_global_tenant(tenant_id: str) -> bool:
    """Check if tenant_id represents the global tenant."""
    return tenant_id in [GLOBAL_TENANT_ID, LEGACY_GLOBAL_TENANT_ID]

def normalize_tenant_id(tenant_id: str) -> str:
    """Normalize tenant_id to use UUID format."""
    if tenant_id == LEGACY_GLOBAL_TENANT_ID:
        return GLOBAL_TENANT_ID
    return tenant_id 