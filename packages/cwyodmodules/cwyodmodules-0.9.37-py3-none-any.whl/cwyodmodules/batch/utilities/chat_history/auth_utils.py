import base64
import json
import uuid

from ...utilities.helpers.env_helper import EnvHelper
from ...utilities.helpers.tenant_constants import GLOBAL_TENANT_ID, normalize_tenant_id
from ...utilities.helpers.tenant_helper import TenantHelper
from mgmt_config import logger

# Use default logging configuration for decorators
DEFAULT_LOG_EXECUTION = True
DEFAULT_LOG_ARGS = True
DEFAULT_LOG_RESULT = True

@logger.trace_function(log_execution=DEFAULT_LOG_EXECUTION, log_args=DEFAULT_LOG_ARGS, log_result=DEFAULT_LOG_RESULT)
def get_authenticated_user_details(request_headers):
    user_object = {}

    # check the headers for the Principal-Id (the guid of the signed in user)
    if "X-Ms-Client-Principal-Id" not in request_headers.keys():
        # if it's not, assume we're in development mode and return a default user
        try:
            from . import sample_user
            raw_user_object = sample_user.sample_user
        except (ImportError, AttributeError):
            # Fallback for test environments where relative imports fail
            raw_user_object = {
                "X-Ms-Client-Principal-Id": "00000000-0000-0000-0000-000000000000",
                "X-Ms-Client-Principal-Name": "testusername@constoso.com",
                "X-Ms-Client-Principal-Idp": "aad",
                "X-Ms-Token-Aad-Id-Token": "test_token",
                "X-Ms-Client-Principal": "test_principal"
            }
    else:
        # if it is, get the user details from the EasyAuth headers
        raw_user_object = {k: v for k, v in request_headers.items()}

    user_object["user_principal_id"] = raw_user_object.get("X-Ms-Client-Principal-Id")
    user_object["user_name"] = raw_user_object.get("X-Ms-Client-Principal-Name")
    user_object["auth_provider"] = raw_user_object.get("X-Ms-Client-Principal-Idp")
    user_object["auth_token"] = raw_user_object.get("X-Ms-Token-Aad-Id-Token")
    user_object["client_principal_b64"] = raw_user_object.get("X-Ms-Client-Principal")
    user_object["aad_id_token"] = raw_user_object.get("X-Ms-Token-Aad-Id-Token")

    return user_object

@logger.trace_function(log_execution=DEFAULT_LOG_EXECUTION, log_args=DEFAULT_LOG_ARGS, log_result=DEFAULT_LOG_RESULT)
def get_tenantid(client_principal_b64):
    tenant_id = ""
    if client_principal_b64:
        try:
            # Decode the base64 header to get the JSON string
            decoded_bytes = base64.b64decode(client_principal_b64)
            decoded_string = decoded_bytes.decode("utf-8")
            # Convert the JSON string into a Python dictionary
            user_info = json.loads(decoded_string)
            # Extract the tenant ID
            raw_tenant_id = user_info.get("tid")  # 'tid' typically holds the tenant ID
            
            # Validate and transform the tenant ID to ensure it's a valid UUID
            if raw_tenant_id:
                try:
                    # Try to parse as UUID first
                    tenant_uuid = uuid.UUID(raw_tenant_id)
                    tenant_id = str(tenant_uuid)
                except ValueError:
                    # If it's not a valid UUID, generate a deterministic UUID from the tenant ID
                    # This ensures we always have a valid UUID for PostgreSQL
                    logger.warning(f"Invalid UUID format for tenant_id: {raw_tenant_id}. Generating deterministic UUID.")
                    # Use SHA-1 hash of the tenant ID to generate a deterministic UUID
                    import hashlib
                    hash_object = hashlib.sha1(raw_tenant_id.encode())
                    hash_hex = hash_object.hexdigest()
                    # Create a UUID from the hash (version 5 UUID)
                    tenant_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, raw_tenant_id)
                    tenant_id = str(tenant_uuid)
                    
                    # Ensure the tenant exists in the database
                    try:
                        tenant_helper = TenantHelper()
                        tenant_helper.ensure_tenant_exists(tenant_id, f"tenant_{raw_tenant_id}")
                    except Exception as e:
                        logger.warning(f"Failed to ensure tenant exists in database: {e}. Continuing with tenant_id: {tenant_id}")
                    
        except Exception as ex:
            logger.exception(f"Error processing tenant_id: {ex}")
    
    # Normalize the tenant_id to use UUID format
    return normalize_tenant_id(tenant_id) if tenant_id else None
