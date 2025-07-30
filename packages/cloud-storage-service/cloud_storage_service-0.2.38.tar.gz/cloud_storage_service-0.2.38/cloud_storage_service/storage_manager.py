from .aws_storage import AWSStorage
from .azure_storage import AzureStorage
from .gcp_storage import GCPStorage

def get_cloud_storage_service(provider, connection_string=None):
    """
    Initializes and returns a cloud storage service instance based on the specified provider.

    This function supports three cloud providers: AWS, Azure, and GCP. It instantiates the
    appropriate storage service class based on the input and returns the instance.

    Parameters:
        provider (str): The cloud provider to use. Acceptable values are:
                        - 'aws': Amazon Web Services
                        - 'azure': Microsoft Azure
                        - 'gcp': Google Cloud Platform
        connection_string (str, optional): Required for Azure. The connection string 
                                           for accessing Azure Blob Storage. 
                                           If using AWS or GCP, this parameter should not be provided.
                                           Defaults to None.

    Returns:
        CloudStorage: An instance of the appropriate cloud storage service 
                       (AWS, Azure, or GCP) based on the provided provider.

    Raises:
        ValueError: If the specified provider is unsupported or if the connection string is not provided 
                    for Azure.

    Examples:
        >>> aws_service = get_cloud_storage_service('aws')
        >>> azure_service = get_cloud_storage_service('azure', connection_string='your_connection_string')
        >>> gcp_service = get_cloud_storage_service('gcp')

    Notes:
        - Ensure that the required dependencies for the selected cloud provider are installed.
        - For Azure, the connection string must have the correct permissions for the desired operations.

    See Also:
        - AWSStorage
        - AzureStorage
        - GCPStorage
    """
    if provider not in ['aws', 'azure', 'gcp']:
        raise ValueError(f"Unsupported cloud provider: '{provider}'. Supported providers: aws, azure, gcp")
    
    if provider == 'aws':
        return AWSStorage()
    elif provider == 'azure':
        if not connection_string:
            raise ValueError("Azure requires a connection string")
        return AzureStorage(connection_string)
    elif provider == 'gcp':
        return GCPStorage()
    else:
        raise ValueError(f"Unsupported cloud provider: {provider}")
