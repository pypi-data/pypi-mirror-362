from abc import ABC, abstractmethod
from ..helpers.env_helper import EnvHelper
from ..common.source_document import SourceDocument


class SearchHandlerBase(ABC):
    _VECTOR_FIELD = "content_vector"
    _IMAGE_VECTOR_FIELD = "image_vector"

    def __init__(self, env_helper: EnvHelper):
        self.env_helper = env_helper
        # Note: PostgreSQL implementation doesn't use search_client
        # self.search_client = self.create_search_client()

    def delete_from_index(self, blob_url, tenant_id: str = None) -> None:
        documents = self.search_by_blob_url(blob_url)
        if documents is None or len(documents) == 0:
            return
        files_to_delete = self.output_results(documents)
        self.delete_files(files_to_delete, tenant_id)

    @abstractmethod
    def perform_search(self, filename):
        pass

    @abstractmethod
    def process_results(self, results):
        pass

    @abstractmethod
    def get_files(self, tenant_id: str = None):
        """Get files from the search index.
        
        Args:
            tenant_id: Optional tenant ID for multi-tenant isolation.
        """
        pass

    @abstractmethod
    def output_results(self, results):
        pass

    @abstractmethod
    def delete_files(self, files, tenant_id: str = None):
        """Delete files from the search index.
        
        Args:
            files: List of files to delete.
            tenant_id: Optional tenant ID for multi-tenant isolation.
        """
        pass

    @abstractmethod
    def query_search(self, question, tenant_id: str = None) -> list[SourceDocument]:
        """Search for documents based on a question.
        
        Args:
            question: The search question.
            tenant_id: Optional tenant ID for multi-tenant isolation.
        """
        pass

    @abstractmethod
    def search_by_blob_url(self, blob_url):
        pass
