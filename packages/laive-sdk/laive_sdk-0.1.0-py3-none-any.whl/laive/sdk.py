import requests
import os
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown


@dataclass
class QueryResponse:
    """Response from a RAG query"""
    answer: Optional[str]
    sources: List[Dict[str, Any]]
    timing: Dict[str, float]
    
    def prettyprint(self, format: str = 'table',print_metadata: bool = False):
        """
        Display the sources in a formatted output
        
        Args:
            format: Output format - 'table' (default) or 'json'
        """
        console = Console()
        
        if format.lower() == 'json':
            # JSON format - uses rich's built-in pretty printing
            console.print(self)
            return
            
        # Table format (default)
        console.print(f"Found [bold green]{len(self.sources)}[/] relevant documents")

        # Create a table for displaying sources
        table = Table(title="Retrieved Sources")
        table.add_column("Source", style="cyan")
        table.add_column("Content Preview", style="green", overflow="fold")
        if print_metadata:
            table.add_column("Metadata", style="magenta")

        # Add rows for each source
        for source in self.sources:
            source_name = source.get("source_name", "Unknown")
            page = source.get("metadata", {}).get("page", "")
            content = source.get("page_content", "")
            metadata = str(source.get("metadata", {}))
            # Truncate content and parse as markdown
            content_preview = content[:300] + "..." if len(content) > 150 else content
            markdown_content = Markdown(content_preview)
            source_with_page = f"{source_name}\nPage: {page}"
            if print_metadata:
                table.add_row(source_with_page, markdown_content, metadata)
            else:
                table.add_row(source_with_page, markdown_content)

        # Display the table
        console.print(table)

        # If there's an answer from the RAG system, display it
        if self.answer:
            console.print("\n[bold]Generated Answer:[/]")
            console.print(f"[yellow]{self.answer}[/]")


@dataclass
class BatchUploadResponse:
    """Response from a batch file upload"""
    message: str
    task_ids: List[str]
    status: str
    files_processed: int


class LaiveClient:
    """Client for the Laive RAG API"""
    
    def __init__(self, api_key: Optional[str] = None, domain: str = "https://api.laive.ai", base_url_path: str = "api/v1"):
        """
        Initialize the Laive API client
        
        Args:
            api_key: Your API key for authentication. If not provided, will use LAIVE_API_KEY from environment.
            domain: The API domain (defaults to https://api.laive.ai)
            base_url_path: The base URL path for the API (defaults to api/v1)
        """
        if api_key is None:
            api_key = os.environ.get("LAIVE_API_KEY")
            if not api_key:
                raise ValueError("API key must be provided either as an argument or via the LAIVE_API_KEY environment variable.")
        self.api_key = api_key
        self.domain = domain.rstrip('/')
        self.base_url_path = base_url_path.strip('/')
        self.base_url = f"{self.domain}/{self.base_url_path}"
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
        # Health check on initialization (no versioning)
        health_url = f"{self.domain}/health"
        try:
            response = requests.get(health_url, headers=self.headers, timeout=5)
            response.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Laive API health check failed: {e}")
    
    def _get_retriever_url(self, endpoint: str) -> str:
        """Get the full URL for a retriever endpoint"""
        return f"{self.base_url}/retriever/{endpoint}"
    
    def _get_vaults_url(self, endpoint: str = "") -> str:
        """Get the full URL for a vaults endpoint"""
        if endpoint:
            return f"{self.base_url}/vaults/{endpoint}"
        return f"{self.base_url}/vaults"
        
    def create_vault(self, name: str, description: str = "") -> Dict[str, Any]:
        """
        Create a new vault
        
        Args:
            name: Name of the vault
            description: Optional description of the vault
            
        Returns:
            Dictionary containing the created vault information
        """
        url = self._get_vaults_url() + "/"
        
        payload = {
            "name": name,
            "description": description
        }
        
        response = requests.post(
            url,
            headers=self.headers,
            json=payload
        )
        
        response.raise_for_status()
        return response.json()
    
    def get_vaults(self) -> List[Dict[str, Any]]:
        """
        Get all vaults for the authenticated user
        
        Returns:
            List of vaults
        """
        url = self._get_vaults_url()
        
        response = requests.get(
            url,
            headers=self.headers
        )
        
        response.raise_for_status()
        return response.json()
    
    def get_vault(self, vault_id: int) -> Dict[str, Any]:
        """
        Get a specific vault by ID
        
        Args:
            vault_id: ID of the vault to retrieve
            
        Returns:
            Dictionary containing the vault information
        """
        url = self._get_vaults_url(str(vault_id))
        
        response = requests.get(
            url,
            headers=self.headers
        )
        
        response.raise_for_status()
        return response.json()
    
    def delete_vault(self, vault_id: int) -> Dict[str, Any]:
        """
        Delete a vault by ID
        
        Args:
            vault_id: ID of the vault to delete
            
        Returns:
            Dictionary containing the deletion confirmation
        """
        url = self._get_vaults_url(str(vault_id))
        
        response = requests.delete(
            url,
            headers=self.headers
        )
        
        response.raise_for_status()
        return response.json()
    
    def query(self, query: str, vault_id: Optional[int] = None, top_k: int = 4) -> QueryResponse:
        """
        Perform a RAG query against a vault
        
        Args:
            query: The search query
            vault_id: Optional ID of the vault to search in
            top_k: Number of results to return (default: 4)
            
        Returns:
            QueryResponse object with results
        """
        url = self._get_retriever_url("query")
        
        payload = {
            "query": query,
            "top_k": top_k
        }
        
        if vault_id is not None:
            payload["vault_id"] = vault_id
            
        response = requests.post(
            url,
            headers=self.headers,
            json=payload
        )
        
        response.raise_for_status()
        data = response.json()
        
        return QueryResponse(
            answer=data.get("answer"),
            sources=data.get("sources", []),
            timing=data.get("timing", {"total_time": 0.0, "search_time": 0.0, "processing_time": 0.0})
        )
    
    def upload_files(self, 
                   files: List[Union[str, bytes, os.PathLike]], 
                   source_names: List[str],
                   vault_id: int, 
                   source_urls: Optional[List[str]] = None) -> BatchUploadResponse:
        """
        Upload multiple files to a vault
        
        Args:
            files: List of file paths or file-like objects
            source_names: List of names for the sources (must match length of files)
            vault_id: ID of the vault to upload to
            source_urls: Optional list of source URLs
            
        Returns:
            BatchUploadResponse with task IDs and status
        """
        url = self._get_retriever_url("upload")
        
        headers = self.headers.copy()
        headers.pop("Content-Type", None)
        
        form_data = {"vault_id": str(vault_id)}
        
        files_data = []
        
        # Add files to the payload
        for i, file in enumerate(files):
            if isinstance(file, (str, os.PathLike)):
                file_name = os.path.basename(file)
                files_data.append(
                    ("files", (file_name, open(file, "rb")))
                )
            else:
                files_data.append(
                    ("files", (f"file_{i}", file if isinstance(file, bytes) else file.read()))
                )
        
        # Add source names (one field per name)
        for name in source_names:
            files_data.append(("source_names", (None, name)))
            
        # Add source URLs if provided (one field per URL)
        if source_urls:
            for url in source_urls:
                files_data.append(("source_urls", (None, url)))
                
        response = requests.post(
            url,
            headers=headers,
            data=form_data,
            files=files_data
        )
        
        response.raise_for_status()
        data = response.json()
        
        return BatchUploadResponse(
            message=data.get("message", ""),
            task_ids=data.get("task_ids", []),
            status=data.get("status", ""),
            files_processed=data.get("files_processed", 0)
        )
        
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of a task
        
        Args:
            task_id: ID of the task to check
            
        Returns:
            Dictionary with task status information
        """
        url = self._get_retriever_url(f"task/{task_id}")
        
        response = requests.get(
            url,
            headers=self.headers
        )
        
        response.raise_for_status()
        return response.json()