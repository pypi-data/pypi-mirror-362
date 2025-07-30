from typing import Optional, Dict, Any, cast
from google.cloud import secretmanager
from google.oauth2 import service_account

class Client(secretmanager.SecretManagerServiceClient):
    """Secret Manager client with service account authentication"""
    
    def __init__(self, service_account_key_path=None):
        """
        Initialize the Secret Manager client
        
        Args:
            service_account_key_path (str, optional): Path to service account key file.
                                                    If None, uses default credentials.
        """
        credentials = service_account.Credentials.from_service_account_file(
            service_account_key_path
        )
        super().__init__(credentials=credentials)
        
    
    def get_secret_value(self, project_id: str, secret_id: str, version_id: str = "latest") -> str:
        """
        Get the value of a secret
        
        Args:
            project_id (str): GCP project ID
            secret_id (str): Secret ID
            version_id (str): Secret version (default: "latest")
            
        Returns:
            str: Secret value
        """
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.access_secret_version(request={"name": name})
        return response.payload.data.decode("utf-8")
    
    def create_new_secret(self, project_id: str, secret_id: str, labels: Optional[Dict[str, str]] = None) -> str:
        """
        Create a new secret
        
        Args:
            project_id (str): GCP project ID
            secret_id (str): Secret ID to create
            labels (dict, optional): Labels to associate with the secret
            
        Returns:
            str: Full name of the created secret
        """
        parent = f"projects/{project_id}"
        secret: Dict[str, Any] = {"replication": {"automatic": {}}}
        if labels:
            secret["labels"] = cast(Any, labels)
            
        response = super().create_secret(
            request={
                "parent": parent,
                "secret_id": secret_id,
                "secret": secret
            }
        )
        return response.name
    
    def add_new_secret_version(self, project_id: str, secret_id: str, payload: str) -> str:
        """
        Add a new version to an existing secret
        
        Args:
            project_id (str): GCP project ID
            secret_id (str): Secret ID
            payload (str): Secret value
            
        Returns:
            str: Full name of the created version
        """
        parent = f"projects/{project_id}/secrets/{secret_id}"
        response = super().add_secret_version(
            request={
                "parent": parent,
                "payload": {"data": payload.encode("utf-8")}
            }
        )
        return response.name
    
    def remove_secret(self, project_id: str, secret_id: str) -> None:
        """
        Delete a secret
        
        Args:
            project_id (str): GCP project ID
            secret_id (str): Secret ID to delete
        """
        name = f"projects/{project_id}/secrets/{secret_id}"
        super().delete_secret(request={"name": name})
    
    def get_all_secrets(self, project_id: str) -> list:
        """
        List all secrets in a project
        
        Args:
            project_id (str): GCP project ID
            
        Returns:
            list: List of secrets
        """
        parent = f"projects/{project_id}"
        secrets = []
        for secret in super().list_secrets(request={"parent": parent}):
            secrets.append({
                "name": secret.name,
                "labels": dict(secret.labels) if secret.labels else {},
                "create_time": secret.create_time,
            })
        return secrets
    
    def update_secret_labels(self, project_id: str, secret_id: str, labels: Dict[str, str]) -> str:
        """
        Update secret labels
        
        Args:
            project_id (str): GCP project ID
            secret_id (str): Secret ID
            labels (dict): New labels
            
        Returns:
            str: Full name of the updated secret
        """
        name = f"projects/{project_id}/secrets/{secret_id}"
        secret = {"name": name, "labels": labels}
        update_mask = {"paths": ["labels"]}
        
        response = super().update_secret(
            request={
                "secret": secret,
                "update_mask": update_mask
            }
        )
        return response.name
