from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class DatabaseClientBase(ABC):
    @abstractmethod
    async def connect(self):
        """Establish a connection to the database."""
        pass

    @abstractmethod
    async def close(self):
        """Close the connection to the database."""
        pass

    @abstractmethod
    async def ensure(self):
        """Verify that the database and required tables/collections exist."""
        pass

    @abstractmethod
    async def create_conversation(
        self, user_id: str, conversation_id: str, title: str = "", tenant_id: Optional[str] = None
    ) -> bool:
        """Create a new conversation entry.
        
        Args:
            user_id: The ID of the user.
            conversation_id: The ID of the conversation.
            title: The title of the conversation.
            tenant_id: Optional tenant ID for multi-tenant isolation.
        """
        pass

    @abstractmethod
    async def upsert_conversation(self, conversation: Dict[str, Any], tenant_id: Optional[str] = None) -> bool:
        """Update or insert a conversation entry.
        
        Args:
            conversation: The conversation data to upsert.
            tenant_id: Optional tenant ID for multi-tenant isolation.
        """
        pass

    @abstractmethod
    async def delete_conversation(self, user_id: str, conversation_id: str, tenant_id: Optional[str] = None) -> bool:
        """Delete a specific conversation.
        
        Args:
            user_id: The ID of the user.
            conversation_id: The ID of the conversation.
            tenant_id: Optional tenant ID for multi-tenant isolation.
        """
        pass

    @abstractmethod
    async def delete_messages(
        self, conversation_id: str, user_id: str, tenant_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Delete all messages associated with a conversation.
        
        Args:
            conversation_id: The ID of the conversation.
            user_id: The ID of the user.
            tenant_id: Optional tenant ID for multi-tenant isolation.
        """
        pass

    @abstractmethod
    async def get_conversations(
        self, user_id: str, limit: int, sort_order: str = "DESC", offset: int = 0, tenant_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of conversations for a user.
        
        Args:
            user_id: The ID of the user.
            limit: Maximum number of conversations to retrieve.
            sort_order: Sort order for conversations.
            offset: Offset for pagination.
            tenant_id: Optional tenant ID for multi-tenant isolation.
        """
        pass

    @abstractmethod
    async def get_conversation(
        self, user_id: str, conversation_id: str, tenant_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Retrieve a specific conversation by ID.
        
        Args:
            user_id: The ID of the user.
            conversation_id: The ID of the conversation.
            tenant_id: Optional tenant ID for multi-tenant isolation.
        """
        pass

    @abstractmethod
    async def create_message(
        self,
        uuid: str,
        conversation_id: str,
        user_id: str,
        input_message: Dict[str, Any],
        tenant_id: Optional[str] = None,
    ) -> bool:
        """Create a new message within a conversation.
        
        Args:
            uuid: The unique identifier for the message.
            conversation_id: The ID of the conversation.
            user_id: The ID of the user.
            input_message: The message data.
            tenant_id: Optional tenant ID for multi-tenant isolation.
        """
        pass

    @abstractmethod
    async def update_message_feedback(
        self, user_id: str, message_id: str, feedback: str, tenant_id: Optional[str] = None
    ) -> bool:
        """Update feedback for a specific message.
        
        Args:
            user_id: The ID of the user.
            message_id: The ID of the message.
            feedback: The feedback content.
            tenant_id: Optional tenant ID for multi-tenant isolation.
        """
        pass

    @abstractmethod
    async def get_messages(
        self, user_id: str, conversation_id: str, tenant_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve all messages within a conversation.
        
        Args:
            user_id: The ID of the user.
            conversation_id: The ID of the conversation.
            tenant_id: Optional tenant ID for multi-tenant isolation.
        """
        pass
