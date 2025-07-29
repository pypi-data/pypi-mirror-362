from .postgres_db import PostgresDB
from .tenant_constants import GLOBAL_TENANT_ID, normalize_tenant_id
from mgmt_config import logger

class TenantHelper:
    def __init__(self):
        self.db = PostgresDB()

    def ensure_tenant_exists(self, tenant_id, tenant_name=None):
        """Ensure a tenant exists in the database, creating it if it doesn't exist."""
        try:
            # Normalize tenant_id to use UUID format
            normalized_tenant_id = normalize_tenant_id(tenant_id)
            
            # Check if tenant exists
            existing_tenant = self.get_tenant_by_id(normalized_tenant_id)
            if existing_tenant:
                logger.info(f"Tenant {normalized_tenant_id} already exists")
                return existing_tenant
            
            # Create tenant if it doesn't exist
            if tenant_name is None:
                tenant_name = f"tenant_{normalized_tenant_id[:8]}"  # Use first 8 chars as name
            
            query = "INSERT INTO tenants (tenant_id, tenant_name) VALUES (%s, %s) ON CONFLICT (tenant_id) DO NOTHING RETURNING tenant_id, tenant_name"
            result = self.db.execute_query(query, (normalized_tenant_id, tenant_name), fetch="one", commit=True)
            
            if result:
                logger.info(f"Created tenant: {tenant_name} with ID: {normalized_tenant_id}")
            else:
                # If no result, tenant might have been created by another process
                result = self.get_tenant_by_id(normalized_tenant_id)
                
            return result
        except Exception as e:
            logger.error(f"Error ensuring tenant exists {tenant_id}: {e}")
            raise

    def create_tenant(self, tenant_name):
        """Create a new tenant."""
        try:
            query = "INSERT INTO tenants (tenant_name) VALUES (%s) RETURNING tenant_id, tenant_name"
            result = self.db.execute_query(query, (tenant_name,), fetch="one", commit=True)
            logger.info(f"Created tenant: {tenant_name} with ID: {result['tenant_id'] if result else 'Unknown'}")
            return result
        except Exception as e:
            logger.error(f"Error creating tenant {tenant_name}: {e}")
            raise

    def get_tenants(self):
        """Get all tenants."""
        try:
            query = "SELECT tenant_id, tenant_name FROM tenants ORDER BY tenant_name"
            result = self.db.execute_query(query, fetch="all")
            logger.info(f"Found {len(result) if result else 0} tenants")
            return result
        except Exception as e:
            logger.error(f"Error getting tenants: {e}")
            return []

    def link_user_to_tenant(self, user_id, tenant_id):
        """Link a user to a tenant."""
        try:
            # Normalize tenant_id to use UUID format
            normalized_tenant_id = normalize_tenant_id(tenant_id)
            query = "INSERT INTO user_tenant_links (user_id, tenant_id) VALUES (%s, %s) ON CONFLICT (user_id, tenant_id) DO NOTHING"
            self.db.execute_query(query, (user_id, normalized_tenant_id), commit=True)
            logger.info(f"Linked user {user_id} to tenant {normalized_tenant_id}")
        except Exception as e:
            logger.error(f"Error linking user {user_id} to tenant {tenant_id}: {e}")
            raise

    def get_user_tenant_links(self):
        """Get all user-tenant links."""
        try:
            query = "SELECT user_id, tenant_id FROM user_tenant_links ORDER BY user_id, tenant_id"
            result = self.db.execute_query(query, fetch="all")
            logger.info(f"Found {len(result) if result else 0} user-tenant links")
            return result
        except Exception as e:
            logger.error(f"Error getting user-tenant links: {e}")
            return []

    def get_tenant_by_id(self, tenant_id):
        """Get specific tenant information."""
        try:
            query = "SELECT tenant_id, tenant_name FROM tenants WHERE tenant_id = %s"
            result = self.db.execute_query(query, (tenant_id,), fetch="one")
            return result
        except Exception as e:
            logger.error(f"Error getting tenant {tenant_id}: {e}")
            return None

    def get_users_for_tenant(self, tenant_id):
        """Get all users linked to a specific tenant."""
        try:
            query = "SELECT user_id FROM user_tenant_links WHERE tenant_id = %s ORDER BY user_id"
            result = self.db.execute_query(query, (tenant_id,), fetch="all")
            logger.info(f"Found {len(result) if result else 0} users for tenant {tenant_id}")
            return result
        except Exception as e:
            logger.error(f"Error getting users for tenant {tenant_id}: {e}")
            return [] 