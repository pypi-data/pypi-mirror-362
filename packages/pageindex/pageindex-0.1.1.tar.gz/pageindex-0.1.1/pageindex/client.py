import requests
from typing import Optional, Dict, Any

from .exceptions import PageIndexAPIError

class PageIndexClient:
    """
    Python SDK client for the PageIndex API.
    """

    BASE_URL = "https://api.pageindex.ai"

    def __init__(self, api_key: str):
        """
        Initialize the client with your API key.
        """
        self.api_key = api_key

    def _headers(self) -> Dict[str, str]:
        return {"api_key": self.api_key}

    # ---------- TREE GENERATION ----------

    def submit_document(
        self,
        file_path: str,
        if_add_node_summary: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload a PDF to generate a PageIndex tree.

        Args:
            file_path (str): Path to the PDF file.
            if_add_node_summary (str, optional): 'yes' or 'no'.

        Returns:
            dict: {'doc_id': ...}
        """
        files = {'file': open(file_path, "rb")}
        data = {}
        if if_add_node_summary is not None:
            data['if_add_node_summary'] = if_add_node_summary

        response = requests.post(
            f"{self.BASE_URL}/tree/",
            headers=self._headers(),
            files=files,
            data=data
        )
        files['file'].close()
        if response.status_code != 200:
            raise PageIndexAPIError(f"Failed to submit document: {response.text}")
        return response.json()

    def get_tree_result(self, doc_id: str) -> Dict[str, Any]:
        """
        Get status and (if completed) the PageIndex tree structure.

        Args:
            doc_id (str): Document ID.

        Returns:
            dict: API response with status and, if ready, tree/result.
        """
        response = requests.get(
            f"{self.BASE_URL}/tree/{doc_id}/",
            headers=self._headers()
        )
        if response.status_code != 200:
            raise PageIndexAPIError(f"Failed to get tree result: {response.text}")
        return response.json()

    def delete_document(self, doc_id: str) -> Dict[str, Any]:
        """
        Delete a PageIndex document and its tree.

        Args:
            doc_id (str): Document ID.

        Returns:
            dict: API response.
        """
        response = requests.delete(
            f"{self.BASE_URL}/tree/{doc_id}/",
            headers=self._headers()
        )
        if response.status_code != 200:
            raise PageIndexAPIError(f"Failed to delete document: {response.text}")
        return response.json()

    def get_document_text(
        self,
        doc_id: str,
        start: Optional[int] = None,
        end: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get document text for a single page or a page range.

        Args:
            doc_id (str): Document ID.
            start (int, optional): Start page (1-indexed).
            end (int, optional): End page (inclusive, 1-indexed).

        Returns:
            dict: {'doc_id': ..., 'pages': [...], 'text': [...]}
        """
        params = {}
        if start is not None:
            params['start'] = start
        if end is not None:
            params['end'] = end

        response = requests.get(
            f"{self.BASE_URL}/tree/{doc_id}/text",
            headers=self._headers(),
            params=params
        )
        if response.status_code != 200:
            raise PageIndexAPIError(f"Failed to get document text: {response.text}")
        return response.json()

    # ---------- RETRIEVAL ----------

    def submit_retrieval_query(
        self,
        doc_id: str,
        query: str,
        thinking: bool = False
    ) -> Dict[str, Any]:
        """
        Submit a retrieval query.

        Args:
            doc_id (str): Document ID.
            query (str): User query.
            thinking (bool, optional): If true, enables "thinking" reasoning mode.

        Returns:
            dict: {'retrieval_id': ...}
        """
        payload = {
            "doc_id": doc_id,
            "query": query,
            "thinking": thinking
        }
        response = requests.post(
            f"{self.BASE_URL}/retrieval/",
            headers=self._headers(),
            json=payload
        )
        if response.status_code != 200:
            raise PageIndexAPIError(f"Failed to submit retrieval: {response.text}")
        return response.json()

    def get_retrieval_result(self, retrieval_id: str) -> Dict[str, Any]:
        """
        Get retrieval result by retrieval ID.

        Args:
            retrieval_id (str): Retrieval ID.

        Returns:
            dict: Retrieval status and results.
        """
        response = requests.get(
            f"{self.BASE_URL}/retrieval/{retrieval_id}/",
            headers=self._headers()
        )
        if response.status_code != 200:
            raise PageIndexAPIError(f"Failed to get retrieval result: {response.text}")
        return response.json()