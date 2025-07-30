import os
import io
import json
import tarfile
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from azure.core.exceptions import AzureError, ResourceExistsError, ResourceNotFoundError
from azure.storage.blob import BlobServiceClient, ContainerClient, generate_blob_sas, BlobSasPermissions, ContentSettings

class AzureStorage:
    """
    A class to interact with Azure Blob Storage.

    This class provides methods to initialize an Azure Blob Service client and fetch details of documents
    stored in a specific container. It uses the Azure Storage Blob library to interface with Azure services.

    Attributes:
        blob_service_client (BlobServiceClient): The Blob Service client instance for performing Blob operations.
    """
    def __init__(self, connection_string):
        """
        Initialize Azure Blob Service client for interacting with Azure storage.
        
        This method creates a BlobServiceClient instance using the provided connection string, which allows for various
        operations on Azure Blob containers and blobs.
        
        Parameters:
            connection_string (str): The connection string for the Azure Storage account.
        """
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.account_name = self.blob_service_client.account_name
        self.account_key = self.blob_service_client.credential.account_key
        # print(f"Initialized Azure Storage Service with connection string: {connection_string}")

    def get_document_details(self, container_name, prefix='', file_type=None):
        """
        Fetches details of documents from an Azure Blob container with a specific prefix and file type.

        This method retrieves the names, hashes, and sizes of documents in the specified
        Azure Blob container, filtering by optional prefix and file type.

        Parameters:
            container_name (str): The name of the Azure Blob container from which to retrieve documents.
            prefix (str, optional): The folder prefix within the container to filter results. 
                                    Defaults to '' (all blobs in the container).
            file_type (str, optional): The file extension (e.g., '.csv') to filter files. 
                                        Defaults to None (no filtering by file type).

        Returns:
            dict: A dictionary with document details including:
                  - key (str): Full path of the blob (equivalent to s3 object key)
                  - document_name (str): The name of the document without extension.
                  - document_hash (str): The MD5 hash of the document.
                  - document_size (int): The size of the document in bytes.
                  - file_type (str or None): The file type used for filtering (if provided).
                  - last_modified (datetime): The last modified timestamp of the blob.

        Raises:
            Exception: If the container does not exist or if the blob request fails.

        Examples:
            azure_service = AzureStorage('your_connection_string')
            documents = azure_service.get_document_details('my-container', prefix='data/', file_type='.csv')
            print(documents)

        Notes:
            - The method excludes files containing 'fhir_data' in their name.
            - To use this class, ensure you have the Azure Storage Blob library installed and configured.
        """
        if not container_name:
            raise ValueError("Container name must not be empty.")

        # print(f"Fetching document details from Azure Blob: container={container_name}, prefix={prefix}, file_type={file_type}")
        
        document_details = {}
        try:
            container_client = self.blob_service_client.get_container_client(container_name)

            # List blobs with specified prefix
            blob_list = container_client.list_blobs(name_starts_with=prefix)
            for blob in blob_list:
                full_document_name = blob.name
                
                # Filter by file type and exclude unwanted files
                if (file_type is None or full_document_name.endswith(file_type)) and 'fhir_data' not in full_document_name:
                    base_document_name = os.path.splitext(os.path.basename(full_document_name))[0]
                    document_size = blob.size
                    document_hash = blob.etag.strip('"')  # MD5 hash from blob metadata
                    last_modified = blob.last_modified

                    # Store document details
                    document_details[base_document_name] = {
                        'key': full_document_name,
                        'document_name': base_document_name,
                        'document_hash': document_hash,
                        'document_size': document_size,
                        'file_type': file_type,
                        'last_modified': last_modified
                    }

        except ResourceNotFoundError:
            print(f"Container '{container_name}' not found.")
            raise Exception(f"Failed to fetch documents from container '{container_name}': Container not found.")
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise Exception(f"An unexpected error occurred: {e}")

        return document_details

    def count_documents_in_storage(self, container_name, prefix='', file_extension=None):
        """
        Counts total and unique documents of a specific type in an Azure Blob container or within a specific prefix (folder).

        This method also returns a list of document names that match the specified criteria.

        Args:
            container_name (str): Name of the Azure Blob container.
            prefix (str, optional): Prefix to list blobs within a specific folder. 
                                    Defaults to '' (all blobs).
            file_extension (str, optional): File extension to filter by (e.g., 'xml' for XML files).

        Returns:
            tuple: A tuple containing:
                - total_count (int): The total number of documents found.
                - unique_count (int): The count of unique documents based on ETags.
                - document_names (list): A list of document names that match the criteria.

        Raises:
            Exception: If there is an error accessing Azure Blob Storage or if the container does not exist.

        Examples:
            total, unique, documents = azure_service.count_documents_in_blob_container('my-container', prefix='data/', file_extension='csv')
            print(total, unique, documents)
        """
        etags = set()
        total_count = 0
        document_names = []

        try:
            # Get the container client for the specified container
            container_client = self.blob_service_client.get_container_client(container_name)

            # List blobs with the specified prefix
            blob_list = container_client.list_blobs(name_starts_with=prefix)

            for blob in blob_list:
                # Filter blobs by file extension and exclude unwanted blobs
                if (file_extension is None or blob.name.endswith(file_extension)) and 'fhir_data' not in blob.name:
                    total_count += 1
                    etags.add(blob.etag.strip('"'))  # Collect unique ETags
                    document_names.append(blob.name)  # Collect document names

        except ResourceNotFoundError:
            raise Exception(f"Container '{container_name}' not found.")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {str(e)}")

        # Unique count is the size of the set of ETags
        unique_count = len(etags)
        return total_count, unique_count, document_names

    def key_exists_in_storage(self, container_name, blob_name, processing_info=None, key_to_set=None):
            """
            Check if a blob exists in an Azure Blob container.

            This method checks for the existence of a blob in the specified container by
            attempting to retrieve its properties. If the blob exists, it can optionally store
            the blob's ETag in a provided dictionary.

            Args:
                container_name (str): The name of the Azure Blob container to check.
                blob_name (str): The name of the blob to check for existence.
                processing_info (dict, optional): A dictionary to store additional processing
                                                information. If provided, the ETag of the
                                                blob will be stored under `key_to_set`.
                                                Defaults to None.
                key_to_set (str, optional): The key under which to store the ETag in
                                            `processing_info`. Defaults to None.

            Returns:
                bool: True if the blob exists, False otherwise.

            Raises:
                Exception: If an error occurs during the request to Azure Blob Storage.

            Examples:
                exists = azure_service.blob_exists('my-container', 'path/to/my/blob.txt')
                print(exists)  # True or False

                processing_info = {}
                exists = azure_service.blob_exists('my-container', 'path/to/my/blob.txt', processing_info, 'etag_key')
                if exists:
                    print(processing_info['etag_key'])  # Prints the ETag of the blob if it exists
            """
            try:
                blob_client = self.blob_service_client.get_blob_client(container_name, blob_name)
                blob_properties = blob_client.get_blob_properties()
                etag = blob_properties.etag

                if processing_info is not None and key_to_set is not None:
                    processing_info[key_to_set] = etag.strip('"')
                return True

            except ResourceNotFoundError:
                # print(f"Blob '{blob_name}' does not exist in container '{container_name}'.")
                return False
            except Exception as e:
                # print(f"Error checking for blob '{blob_name}' in container '{container_name}': {e}")
                return False

    def parquet_existence_check(self, container_name, patient_id, versions):
            """
            Check for the existence of a Parquet file in an Azure Blob container for a given patient ID across specified versions.

            This function checks if the Parquet file associated with the specified patient ID 
            exists for any of the provided version numbers. It returns the highest version number 
            where the file is found.

            Args:
                container_name (str): The name of the Azure Blob container where the Parquet files are stored.
                patient_id (str): The patient ID used to construct the blob name for the file.
                versions (list): A list of version numbers (integers) to check for the existence of the file.

            Returns:
                int or None: The version number where the Parquet file exists, or None if no file is found.

            Raises:
                ValueError: If `versions` is empty or contains non-integer values.
                Exception: For any other errors encountered during Azure Blob Storage access.

            Examples:
                container = 'my-container'
                patient = 'patient_123'
                available_versions = [1, 2, 3]
                version_found = azure_service.parquet_existence_check(container, patient, available_versions)
                if version_found is not None:
                    print(f'File found for version: {version_found}')
                else:
                    print('No file found for any version.')
            """
            # Validate input versions
            if not versions:
                raise ValueError("The 'versions' list must not be empty.")

            if not all(isinstance(v, int) for v in versions):
                raise ValueError("All elements in 'versions' must be integers.")

            # Sort the versions in descending order to check the latest versions first
            versions = sorted(versions, reverse=True)

            for version in versions:
                blob_name = f"{patient_id}/v{version}/addr.parquet"  # Generate the blob name for the file
                
                try:
                    if self.key_exists_in_storage(container_name, blob_name):
                        # print(f'Parquet exists for Version: {version}')
                        return version  # Return the first version where the file exists
                except Exception as e:
                    print(f"Error checking for file existence in container '{container_name}' for blob '{blob_name}': {e}")

            return None
    
    def load_parquet_file(self, container_name, blob_name, environment, project_root=None):
        """
        Load a Parquet file from Azure Blob Storage or a local path into a Pandas DataFrame.

        This function attempts to load a Parquet file from an Azure Blob container or from a local
        directory, depending on the specified environment. If the loading fails, it returns an empty
        DataFrame with default columns.

        Args:
            container_name (str): The name of the Azure Blob container.
            blob_name (str): The blob name (path) of the Parquet file to load.
            environment (str): The current environment ('local' or 'production').
            project_root (str): The root path of the project for local file access.

        Returns:
            pd.DataFrame: A DataFrame containing the data from the Parquet file, or an empty
                        DataFrame with default columns if loading fails.

        Raises:
            ValueError: If the blob_name is invalid.
            Exception: For any other errors encountered during file loading.

        Examples:
            df = load_parquet_file('my-container', 'path/to/file.parquet', 'production', '/path/to/project')
        """
        default_columns = ['section_name', 'document_id']
        
        # Validate the blob name
        if not blob_name:
            print("Error: The 'blob_name' must not be empty.")
            raise ValueError("The 'blob_name' must not be empty.")

        try:
            if environment == "local":
                file_path = (Path(project_root) / blob_name).resolve(strict=False)  # Adjust path as needed
                # print(f"Loading Parquet file from local path: {file_path}")
                df = pd.read_parquet(path=file_path)
            else:
                # print(f"Loading Parquet file from Azure Blob Storage: {blob_name}")
                blob_client = self.blob_service_client.get_blob_client(container_name, blob_name)
                blob_data = blob_client.download_blob().readall()
                df = pd.read_parquet(pd.io.common.BytesIO(blob_data))  # Load directly from bytes
            return df

        except ResourceNotFoundError:
            # print(f"Error: Blob not found: {blob_name}")
            return pd.DataFrame(columns=default_columns)

        except Exception as e:
            # print("Error: An unexpected error occurred while loading the Parquet file.")
            # print(e)
            return pd.DataFrame(columns=default_columns)

    def load_json_from_storage(self, container_name, blob_name):
            """
            Load a JSON file from Azure Blob Storage and return the parsed JSON object.

            This function retrieves a JSON file from the specified Azure Blob container and parses its
            content into a Python dictionary. If the file does not exist or an error occurs,
            an empty dictionary is returned.

            Args:
                container_name (str): The name of the Azure Blob container.
                blob_name (str): The name of the blob in Azure.

            Returns:
                dict: The parsed JSON object, or an empty dictionary if an error occurs.

            Raises:
                ValueError: If the blob_name is empty.

            Examples:
                json_data = load_json_from_azure('my-container', 'path/to/file.json')
            """
            # Validate the blob name
            if not blob_name:
                print("Error: The 'blob_name' must not be empty.")
                raise ValueError("The 'blob_name' must not be empty.")

            try:
                blob_client = self.blob_service_client.get_blob_client(container_name, blob_name)
                blob_data = blob_client.download_blob().readall()
                json_content = blob_data.decode('utf-8')  # Decode bytes to string
                json_data = json.loads(json_content)
                return json_data

            except ResourceNotFoundError:
                print(f"The specified blob '{blob_name}' does not exist in the container '{container_name}'.")
                return {}

            except Exception as e:
                print(f"An unexpected error occurred while loading the JSON file: {e}")
                return {}
            
    def download_folder_from_storage(self, container_name, folder_prefix, local_folder):
        """
        Download all files from a specified Azure Blob folder to a local directory.

        This function retrieves all blobs in the specified folder (prefix) and
        downloads them to the given local folder. If the local folder does not exist,
        it will be created.

        Args:
            container_name (str): The name of the Azure Blob container.
            folder_prefix (str): The prefix (folder path) in Azure from which to download files.
            local_folder (str): The local directory to which files will be downloaded.

        Raises:
            ValueError: If the container_name or folder_prefix is empty.
            Exception: If any unexpected error occurs during the download process.

        Examples:
            download_azure_folder('my-container', 'path/to/folder/', '/local/path/')
        """
        # Validate input parameters
        if not container_name:
            raise ValueError("Container name must not be empty.")
        if not folder_prefix:
            raise ValueError("Folder prefix must not be empty.")

        # print(f"Starting download from Azure Blob container '{container_name}' with prefix '{folder_prefix}' to local folder '{local_folder}'.")

        # Ensure the local folder exists
        os.makedirs(local_folder, exist_ok=True)

        try:
            # List blobs in the specified Azure folder
            blobs = self.blob_service_client.get_container_client(container_name).list_blobs(name_starts_with=folder_prefix)
            total_files = sum(1 for _ in blobs)  # Count total files
            
            if total_files > 0:
                # print(f"Found {total_files} files in Azure folder '{folder_prefix}'. Beginning download...")

                blobs = self.blob_service_client.get_container_client(container_name).list_blobs(name_starts_with=folder_prefix)
                for idx, blob in enumerate(blobs, start=1):
                    file_name = os.path.basename(blob.name)  # Get the file name from the blob name
                    local_file_path = os.path.join(local_folder, file_name)  # Create the local file path

                    # Download the file from Azure Blob Storage to the local folder
                    # print(f"Downloading file {idx}/{total_files}: '{file_name}' to '{local_file_path}'...")
                    blob_client = self.blob_service_client.get_blob_client(container_name, blob.name)
                    with open(local_file_path, 'wb') as file:
                        file.write(blob_client.download_blob().readall())

                print(f"Download completed. {total_files} files downloaded to '{local_folder}'.")
            else:
                print(f"No files found in the specified Azure folder '{folder_prefix}'.")

        except Exception as e:
            print(f"An error occurred during the download process: {e}")

    def generate_signed_url(self, container_name, blob_name, expiration_time=3600):
        """
        Generate a presigned URL or SAS token based on the environment.

        Parameters:
        - container_name (str): The name of the bucket/container.
        - object_key (str): The key (file path) of the object.
        - environment (str): The current environment ('s3' or 'azure').
        - expiration_time (int, optional): The time in seconds for the URL/token to remain valid.

        Returns:
        - str: A presigned URL for S3 or a SAS URL for Azure.
        """
        # Ensure container_name and blob_name are provided
        if not container_name:
            raise ValueError("Container name is required.")
        if not blob_name:
            raise ValueError("Blob name is required.")
        
        try:
            # Calculate the expiration time
            sas_expiry = datetime.utcnow() + timedelta(seconds=expiration_time)

            # Generate the SAS token with read permissions
            sas_token = generate_blob_sas(
                account_name=self.account_name,  # Azure Storage account name
                container_name=container_name,
                blob_name=blob_name,
                account_key=self.account_key,  # Azure Storage account key
                permission=BlobSasPermissions(read=True),
                expiry=sas_expiry
            )

            # Construct the full URL with the SAS token
            blob_url = f"https://{self.account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

            return blob_url

        except Exception as e:
            print(f"An error occurred while generating the SAS URL: {e}")
            return None

    def save_data_and_get_signed_url(self, container_name, file_name, result, environment, local_dir_path):
        """
        Save a JSON object either locally or to Azure Blob Storage, and generate a SAS URL for the Azure Blob.

        Parameters:
        - container_name (str): The name of the Azure Blob Storage container where the file will be stored.
        - blob_name (str): The name (key) of the file to save in Azure or locally.
        - result (dict): The JSON object to save.
        - environment (str): The current environment ('local' or 'azure').
        - local_dir_path (str): The local directory path to save the file if the environment is 'local'.

        Returns:
        - tuple:
            - If environment is 'local':
              ('local', None)
            - If environment is 'azure':
              - str: SAS URL for accessing the file in Azure.
              - str: The file's blob ETag (hash) from Azure.
              - int: The file's size in bytes.

        Raises:
        - ValueError: If required parameters are missing or invalid.
        - Exception: If an error occurs while uploading to or retrieving from Azure.

        Example:
            result_data = {"key": "value"}
            url, file_hash, file_size = save_data_and_get_signed_url(
                'my-container', 'data/result.json', result_data, environment='azure', local_dir_path='/tmp')
        """
        if environment == 'local':
            try:
                if isinstance(result, str):
                    result = json.loads(result)
                save_folder = "fhir" if "fhir" in str(local_dir_path).lower() else "output"
                local_path = Path(local_dir_path) / save_folder / Path(file_name).parent
                Path(local_path).mkdir(parents=True, exist_ok=True)
                with open(Path(local_dir_path) / save_folder / file_name, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False)
                return 'local', None, None
            except Exception as e:
                print(f"Error saving file locally: {e}")
                return None, None, None

        # Handle Azure Blob Storage environment
        try:
            if isinstance(result, str):
                result = json.loads(result)
            # Upload the JSON result to Azure Blob Storage
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=file_name)
            blob_client.upload_blob(json.dumps(result), overwrite=True)

            # Get the blob's ETag and size (content length)
            properties = blob_client.get_blob_properties()
            file_hash = properties['etag'].strip('"')
            file_size = properties['size']

            # Generate a SAS URL for the uploaded blob
            sas_expiry = datetime.utcnow() + timedelta(seconds=3600)
            sas_token = generate_blob_sas(
                account_name=self.account_name,
                container_name=container_name,
                blob_name=file_name,
                account_key=self.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=sas_expiry
            )
            sas_url = f"https://{self.account_name}.blob.core.windows.net/{container_name}/{file_name}?{sas_token}"

            # Return the SAS URL, file hash, and file size
            return sas_url, file_hash, file_size

        except ResourceExistsError:
            print(f"Error: The blob '{file_name}' already exists in the container '{container_name}'.")
            return None, None, None
        except ResourceNotFoundError:
            print(f"Error: The container '{container_name}' or blob '{file_name}' was not found.")
            return None, None, None
        except AzureError as e:
            print(f"Azure error: {e}")
            return None, None, None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None, None, None

    def download_ml_models(self, processing_info, container_name, azure_dir_path, local_dir_path):
            """
            Downloads all model files for a specific version from an Azure Blob Storage container.

            Args:
            - processing_info (dict): Dictionary containing processing metadata, including model version.
            - container_name (str): Name of the Azure Blob Storage container.
            - azure_dir_path (str): Path in the Azure container where models are stored (e.g., 'Summary_Models/').
            - local_dir_path (str): Local directory where the files will be downloaded.

            Returns:
            - bool: True if any model files were downloaded, False if no download was required.
            """
            model_download_required = False

            # Ensure the local directory exists
            try:
                os.makedirs(local_dir_path, exist_ok=True)
            except Exception as e:
                print(f"Error creating local directory '{local_dir_path}': {e}")
                return False

            # List blobs in the specified Azure directory
            container_client = self.blob_service_client.get_container_client(container_name)

            # Loop through the blobs in the specified directory
            blob_list = container_client.list_blobs(name_starts_with=azure_dir_path)

            for blob in blob_list:
                # Check if the blob name matches the specified version
                if f"/{processing_info['summary_version']}/" in blob.name:
                    filename = blob.name  # Extract filename from blob name
                    local_file_path = os.path.join(local_dir_path, filename)

                    # Ensure local directories exist
                    try:
                        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                    except Exception as e:
                        print(f"Error creating directories for '{local_file_path}': {e}")
                        continue

                    # Check if the file already exists locally
                    if not os.path.exists(local_file_path):
                        try:
                            # Download the blob to a local file
                            # print(f"Downloading {filename} from Azure Blob Storage...")
                            with open(local_file_path, 'wb') as file:
                                file.write(container_client.download_blob(blob.name).readall())
                            # print(f"Downloaded '{filename}' to '{local_file_path}'.")
                            model_download_required = True
                        except Exception as e:
                            print(f"Error downloading '{filename}': {e}")
                    else:
                        pass
                        # print(f"File '{filename}' already exists locally, skipping download.")

            return model_download_required
    
    def load_json_metadata(self, person_id, version, json_metadata_path):
        """
        Loads metadata for a person from three parquet files: trident changes, MR metadata, and HR metadata.

        Args:
            person_id (str): The ID of the person.
            version (str): The version of the metadata.
            json_metadata_path (str): The base Azure Blob Storage path where JSON metadata is stored.

        Returns:
            tuple: Three DataFrames (trident_changes_metadata_df, hr_metadata_df, mr_metadata_df)
        """
        # Define blob object keys
        trident_changes_metadata_blob_name = f"summary/{version}/{person_id}/{person_id}_trident_changes.parquet"
        mr_blob_name = f"summary/{version}/{person_id}/{person_id}_mr_metadata.parquet"
        hr_blob_name = f"summary/{version}/{person_id}/{person_id}_hr_metadata.parquet"
        
        # Define expected columns for each DataFrame
        trident_changes_columns = ['person_id', 'document_id', 'org_id', 'org_name', 'section_name', 'section_code', 
                                   'original_column', 'destination_column', 'changes_type', 'overlapping_count', 
                                   'predicted_scores', 'row_count', 'rows_below_95', 'top_5_predictions', 
                                   'merge_status', 'is_unknown', 'create_date']
        mr_metadata_columns = ['document_id', 'section_name', 'row_count', 'create_date']
        hr_metadata_columns = ['document_id', 'section_name', 'row_count', 'unknown_section', 'create_date']
        
        # Helper function to load a parquet file or return an empty DataFrame
        def load_parquet_or_empty(blob_name, columns):
            blob_client = self.blob_service_client.get_blob_client(container=json_metadata_path, blob=blob_name)
            try:
                # Check if the blob exists
                if blob_client.exists():
                    # Download the blob as bytes
                    blob_data = blob_client.download_blob().readall()
                    return pd.read_parquet(io.BytesIO(blob_data))
                else:
                    return pd.DataFrame(columns=columns)
            except Exception as e:
                print(f"Error loading parquet file '{blob_name}': {e}")
                return pd.DataFrame(columns=columns)

        # Load metadata
        trident_changes_metadata_df = load_parquet_or_empty(trident_changes_metadata_blob_name, trident_changes_columns)
        mr_metadata_df = load_parquet_or_empty(mr_blob_name, mr_metadata_columns)
        hr_metadata_df = load_parquet_or_empty(hr_blob_name, hr_metadata_columns)

        return trident_changes_metadata_df, hr_metadata_df, mr_metadata_df
    
    def save_json_metadata(self, processing_info, trident_changes_metadata_df, hr_metadata_df, mr_metadata_df, json_metadata_path):
        """
        Save metadata DataFrames to Azure Blob Storage as parquet files.

        Args:
            processing_info (dict): Information about the processing, including 'summary_version' and 'person_id'.
            trident_changes_metadata_df (pd.DataFrame): DataFrame containing trident changes metadata.
            hr_metadata_df (pd.DataFrame): DataFrame containing HR metadata.
            mr_metadata_df (pd.DataFrame): DataFrame containing MR metadata.
            json_metadata_path (str): The base Azure Blob Storage path (container name) where JSON metadata is stored.
        """
        summary_version = processing_info['summary_version']
        person_id = processing_info['person_id']

        try:
            # Save Trident Changes Metadata
            trident_changes_stream = io.BytesIO()
            trident_changes_metadata_df.to_parquet(trident_changes_stream, index=False)
            trident_changes_stream.seek(0)  # Reset stream position
            
            blob_client = self.blob_service_client.get_blob_client(container=json_metadata_path, 
                                                                    blob=f"summary/{summary_version}/{person_id}/{person_id}_trident_changes.parquet")
            blob_client.upload_blob(trident_changes_stream, overwrite=True)
            # print(f"Trident changes metadata saved for {person_id} in version {summary_version}.")

            # Save HR Metadata
            hr_stream = io.BytesIO()
            hr_metadata_df.to_parquet(hr_stream, index=False)
            hr_stream.seek(0)  # Reset stream position
            
            blob_client = self.blob_service_client.get_blob_client(container=json_metadata_path, 
                                                                    blob=f"summary/{summary_version}/{person_id}/{person_id}_hr_metadata.parquet")
            blob_client.upload_blob(hr_stream, overwrite=True)
            # print(f"HR metadata saved for {person_id} in version {summary_version}.")

            # Save MR Metadata
            mr_stream = io.BytesIO()
            mr_metadata_df.to_parquet(mr_stream, index=False)
            mr_stream.seek(0)  # Reset stream position
            
            blob_client = self.blob_service_client.get_blob_client(container=json_metadata_path, 
                                                                    blob=f"summary/{summary_version}/{person_id}/{person_id}_mr_metadata.parquet")
            blob_client.upload_blob(mr_stream, overwrite=True)
            # print(f"MR metadata saved for {person_id} in version {summary_version}.")

        except Exception as e:
            print(f"An error occurred while saving metadata for {person_id}: {e}")

    def add_unknown_sections(self, container_name, prefix, section_column_df):
        """
        Add unknown sections from Azure Blob Storage parquet files to the section_column_df DataFrame.

        Args:
            container_name (str): The name of the Azure Blob Storage container.
            prefix (str): The prefix to filter the blob names.
            section_column_df (pd.DataFrame): DataFrame containing existing section names.

        Returns:
            pd.DataFrame: Updated DataFrame including unknown sections.
        """
        try:
            # List blobs in the specified container with the given prefix
            container_client = self.blob_service_client.get_container_client(container_name)
            blobs = container_client.list_blobs(name_starts_with=prefix)

            for blob in blobs:
                if blob.name.endswith('_text.parquet'):
                    section_file = blob.name.split('/')[-1].replace('.parquet', '')

                    # Check if the section file is already in the DataFrame
                    if section_file not in section_column_df['hr_table_name'].values:
                        try:
                            section_name, codes = section_file.split('_(')
                            codes = codes.split(')_text')[0]
                        except ValueError:
                            section_name = section_file.replace('_text', '')
                            codes = ''

                        # Add the unknown section to the DataFrame
                        section_column_df.loc[len(section_column_df)] = {
                            'section_name': f"unknown {section_name}",
                            'hr_table_name': section_file,
                            'codes': json.dumps([codes])
                        }

            return section_column_df

        except Exception as e:
            print(f"An error occurred while adding unknown sections: {e}")
            return section_column_df

    def save_file_to_storage(self, df=None, container_name=None, key=None, file_type='parquet', compression=None,
                             data_dict=None, xml_content=None):
        """
        Saves a given DataFrame or JSON dictionary to an Azure Blob Storage container in the specified format.

        Parameters:
            df (pd.DataFrame, optional): The DataFrame to save (required for CSV, Parquet, Excel, and JSON if data_dict is not provided).
            container_name (str): The destination Azure container.
            key (str): The blob key (path including filename) where the file should be saved.
            file_type (str, optional): The type of file to save ('parquet', 'csv', 'excel', 'json', 'xml'). Defaults to 'parquet'.
            compression (str, optional): Compression type, applicable for formats like Parquet, CSV, and JSON.
            data_dict (dict, optional): Dictionary to save as a JSON file if file_type is 'json'. If not provided, the df will be converted to JSON.
            xml_content (str, optional): XML content to save if file_type is 'xml'.

        Raises:
            ValueError: If an unsupported file type is provided.
            Exception: If the upload fails.

        Example Usage:
            azure_service.save_file_to_storage(df=df, container_name='my-container', key='path/to/file.parquet', file_type='parquet')
        """
        supported_file_types = ['parquet', 'csv', 'excel', 'json', 'xml']
        if file_type not in supported_file_types:
            raise ValueError(f"Unsupported file type: {file_type}. Supported types: {supported_file_types}")

        if not container_name or not key:
            raise ValueError("Both container_name and key are required parameters.")

        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(key)

            if file_type == 'parquet':
                buffer = io.BytesIO()
                df.to_parquet(buffer, index=False, compression=compression)
                buffer.seek(0)
                blob_client.upload_blob(buffer.read(), overwrite=True)

            elif file_type == 'csv':
                buffer = io.StringIO()
                df.to_csv(buffer, index=False)
                blob_client.upload_blob(buffer.getvalue(), overwrite=True)

            elif file_type == 'excel':
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False)
                buffer.seek(0)
                blob_client.upload_blob(buffer.read(), overwrite=True)

            elif file_type == 'json':
                json_data_string = json.dumps(data_dict if data_dict is not None else df.to_dict(orient='records'))
                blob_client.upload_blob(json_data_string, overwrite=True)

            elif file_type == 'xml':
                if xml_content is None:
                    raise ValueError("xml_content must be provided for XML file type")
                blob_client.upload_blob(xml_content, overwrite=True, content_settings=ContentSettings(content_type="application/xml"))

            # print(f"File successfully saved to Azure Blob Storage: {key}")

        except Exception as e:
            raise Exception(f"Failed to save file to Azure Blob Storage: {e}")

    def download_ccda_files_from_storage(self, container_name, prefix=None, person_id=None, download_ccda_files=None,
                                         local_dir_path=None):
        """
        Downloads specific CCDA files from Azure Blob Storage based on provided document details.

        Args:
            container_name (str): The name of the Azure Blob container.
            prefix (str, optional): The path between the container name and the person_id, if applicable.
            person_id (str): The ID of the person whose files need to be downloaded.
            download_ccda_files (list): A list of dictionaries containing 'document_id' of files to download.
            local_dir_path (str): The local directory where files will be saved.

        Returns:
            list: Updated list of dictionaries with 'downloaded' status.

        Raises:
            ResourceNotFoundError: If the Azure blob does not exist.
            Exception: If there is an error during the file download process.

        Example Usage:
            azure_storage = AzureStorage('your_connection_string')
            files_to_download = [{'document_id': '12345'}, {'document_id': '67890'}]
            azure_storage.download_ccda_files_from_storage('my-container', 'data/v1', 'patient_001', files_to_download, '/local/path')
        """
        if not container_name or not person_id or not download_ccda_files or not local_dir_path:
            raise ValueError("All parameters except prefix are required.")

        local_dir = os.path.join(local_dir_path, person_id)
        os.makedirs(local_dir, exist_ok=True)

        try:
            container_client = self.blob_service_client.get_container_client(container_name)

            for obj in download_ccda_files:
                key = f"{prefix}/{person_id}/{obj['document_id']}.xml" if prefix else f"{person_id}/{obj['document_id']}.xml"
                local_file = os.path.join(local_dir, f"{obj['document_id']}.xml")

                # print(f"Downloading {key} to {local_file}...")

                blob_client = container_client.get_blob_client(key)
                with open(local_file, "wb") as file:
                    stream = blob_client.download_blob()
                    file.write(stream.readall())

                obj['downloaded'] = True
                # print(f"Downloaded: {key}")

        except ResourceNotFoundError:
            print(f"Blob not found: {key}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred while downloading files: {e}")
            return []

        return download_ccda_files

    def download_file_from_storage(self, container_name, key, local_path, unzip=False):
        """
        Downloads a specific file from Azure Blob Storage to a local path.

        Args:
            container_name (str): The name of the Azure Blob container.
            key (str): The blob key (full path) of the file to download.
            local_path (str): The local directory where the file will be saved.
            unzip (bool, optional): Whether to unzip `.tar.gz` files automatically. Defaults to True.

        Returns:
            str: The local file path, or extracted folder path if unzipping.

        Raises:
            Exception: If an error occurs during the file download process.

        Example Usage:
            azure_storage = AzureStorage('your_connection_string')
            azure_storage.download_file_from_storage('my-container', 'path/to/file.csv', '/local/path')
        """
        if not container_name or not key or not local_path:
            raise ValueError("All parameters are required.")

        local_file_path = os.path.join(local_path, os.path.basename(key))
        os.makedirs(local_path, exist_ok=True)

        try:
            # print(f"Downloading {key} to {local_file_path}...")

            blob_client = self.blob_service_client.get_container_client(container_name).get_blob_client(key)
            with open(local_file_path, "wb") as file:
                file.write(blob_client.download_blob().readall())

            # print(f"Downloaded: {local_file_path}")

            # Check if the file should be unzipped
            if unzip and local_file_path.endswith(".tar.gz"):
                extracted_folder = self.unzip_file(local_file_path, local_path)
                return extracted_folder  # Return the extracted folder path

            return local_file_path  # Return the normal file path if not unzipping

        except Exception as e:
            print(f"An unexpected error occurred while downloading file: {e}")
            return None

    def unzip_file(self, filename: str, dest: str):
        """
        Unzips a `.tar.gz` file into the specified destination folder.

        Args:
            filename (str): The path to the compressed file.
            dest (str): The destination folder to extract contents.

        Returns:
            str: The path to the extracted folder.

        Raises:
            Exception: If extraction fails.
        """
        try:
            # print(f'Unzipping {filename}...')
            with tarfile.open(filename, 'r:gz') as f:
                f.extractall(path=dest)

            extracted_folder = os.path.join(dest, os.path.basename(filename).replace(".tar.gz", ""))
            # print(f'Extracted to {extracted_folder}')
            return extracted_folder

        except Exception as e:
            print(f"Failed to unzip {filename}: {e}")
            raise
