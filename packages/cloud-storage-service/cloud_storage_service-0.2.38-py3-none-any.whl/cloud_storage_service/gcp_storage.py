import os
import io
import tempfile
import json
import tarfile
import pandas as pd
from pathlib import Path
from datetime import timedelta
from google.cloud import storage
from google.api_core.exceptions import NotFound

class GCPStorage:
    """
    A class to interact with Google Cloud Storage.

    This class provides methods to initialize a GCP client and fetch details of documents
    stored in a GCP bucket.

    Attributes:
        gcp_client (google.cloud.storage.Client): The GCP client instance for performing GCP operations.
    """
    def __init__(self):
        """
        Initialize GCP client for interacting with Google Cloud Storage.
        
        This method creates a GCP client instance using the Google Cloud Storage library,
        which allows for various operations on GCP buckets and objects.
        """
        self.gcp_client = storage.Client()
        # print("Initialized Google Cloud Storage client for interacting with GCP.")

    def get_document_details(self, bucket_name, prefix='', file_type=None):
        """
        Fetches details of documents from a Google Cloud Storage bucket with a specific prefix and file type.

        This method retrieves the names, hashes, and sizes of documents in the specified
        GCP bucket, filtering by optional prefix and file type.

        Parameters:
            bucket_name (str): The name of the GCP bucket from which to retrieve documents.
            prefix (str, optional): The folder prefix within the GCP bucket to filter results. 
                                    Defaults to '' (all objects in the bucket).
            file_type (str, optional): The file extension (e.g., '.csv') to filter files. 
                                        Defaults to None (no filtering by file type).

        Returns:
            dict: A dictionary with document details including:
                  - key (str): Full path of the blob (equivalent to s3 object key)
                  - document_name (str): The name of the document without extension.
                  - document_hash (str): The MD5 hash of the document (not directly available from GCP).
                  - document_size (int): The size of the document in bytes.
                  - file_type (str or None): The file type used for filtering (if provided).
                  - last_modified (datetime): The last modified timestamp of the blob.

        Raises:
            Exception: If the GCP request fails or if the bucket does not exist.

        Examples:
            gcp_service = GCPStorage()
            documents = gcp_service.get_document_details('my-bucket', prefix='data/', file_type='.csv')
            print(documents)

        Notes:
            - The method excludes files containing 'fhir_data' in their name.
            - To use this class, ensure you have the google-cloud-storage library installed and configured.
        """
        if not bucket_name:
            raise ValueError("Bucket name must not be empty.")

        # print(f"Fetching document details from Google Cloud Storage: bucket={bucket_name}, prefix={prefix}, file_type={file_type}")

        document_details = {}
        try:
            # Get the bucket
            bucket = self.gcp_client.get_bucket(bucket_name)

            # List blobs in the specified prefix
            blobs = bucket.list_blobs(prefix=prefix)

            for blob in blobs:
                full_document_name = blob.name
                
                # Filter by file type and exclude unwanted files
                if (file_type is None or full_document_name.endswith(file_type)) and 'fhir_data' not in full_document_name:
                    base_document_name = os.path.splitext(os.path.basename(full_document_name))[0]
                    document_size = blob.size
                    document_hash = blob.md5_hash  # MD5 hash from GCP metadata
                    last_modified = blob.updated

                    # Store document details
                    document_details[base_document_name] = {
                        'key': full_document_name,
                        'document_name': base_document_name,
                        'document_hash': document_hash,
                        'document_size': document_size,
                        'file_type': file_type,
                        'last_modified': last_modified
                    }

        except NotFound:
            print(f"Bucket '{bucket_name}' not found.")
            raise Exception(f"Bucket '{bucket_name}' does not exist.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise Exception(f"An unexpected error occurred: {e}")

        return document_details

    def count_documents_in_storage(self, bucket_name, prefix='', file_extension=None):
        """
        Counts total and unique documents of a specific type in a GCP bucket or within a specific prefix (folder).

        This method also returns a list of document names that match the specified criteria.

        Args:
            bucket_name (str): Name of the GCP bucket.
            prefix (str, optional): Prefix to list objects within a specific folder. 
                                    Defaults to '' (all objects).
            file_extension (str, optional): File extension to filter by (e.g., 'xml' for XML files).

        Returns:
            tuple: A tuple containing:
                - total_count (int): The total number of documents found.
                - unique_count (int): The count of unique documents based on MD5 hashes.
                - document_names (list): A list of document names that match the criteria.

        Raises:
            Exception: If there is an error accessing GCP or if the bucket does not exist.

        Examples:
            total, unique, documents = gcp_service.count_documents_in_storage('my-bucket', prefix='data/', file_extension='csv')
            print(total, unique, documents)
        """
        md5_hashes = set()
        total_count = 0
        document_names = []

        try:
            # Get the bucket
            bucket = self.gcp_client.get_bucket(bucket_name)

            # List blobs in the specified prefix
            blobs = bucket.list_blobs(prefix=prefix)

            # Ensure the file extension starts with a dot
            if file_extension and not file_extension.startswith('.'):
                file_extension = '.' + file_extension

            for blob in blobs:
                # Filter objects by file extension and exclude unwanted files
                if (file_extension is None or blob.name.endswith(file_extension)) and 'fhir_data' not in blob.name:
                    total_count += 1
                    md5_hashes.add(blob.md5_hash)  # Use MD5 hash for uniqueness
                    document_names.append(blob.name)  # Collect document names

        except NotFound:
            raise Exception(f"Bucket '{bucket_name}' does not exist.")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {str(e)}")

        # Unique count is the size of the set of MD5 hashes
        unique_count = len(md5_hashes)
        return total_count, unique_count, document_names
    
    def key_exists_in_storage(self, bucket_name, object_key, processing_info=None, key_to_set=None):
        """
        Check if an object exists in a GCP bucket.

        This method checks for the existence of an object in the specified GCP bucket by
        attempting to retrieve its metadata. If the object exists, it can optionally store
        the object's MD5 hash in a provided dictionary.

        Args:
            bucket_name (str): The name of the GCP bucket to check.
            object_key (str): The key (name) of the object to check for existence.
            processing_info (dict, optional): A dictionary to store additional processing
                                                information. If provided, the MD5 hash of the
                                                object will be stored under `key_to_set`.
                                                Defaults to None.
            key_to_set (str, optional): The key under which to store the MD5 hash in
                                            `processing_info`. Defaults to None.

        Returns:
            bool: True if the object exists, False otherwise.

        Raises:
            Exception: If an error occurs during the request to GCP.

        Examples:
            exists = gcp_service.key_exists_in_storage('my-bucket', 'path/to/my/object.txt')
            print(exists)  # True or False

            processing_info = {}
            exists = gcp_service.key_exists_in_storage('my-bucket', 'path/to/my/object.txt', processing_info, 'md5_key')
            if exists:
                print(processing_info['md5_key'])  # Prints the MD5 hash of the object if it exists
        """
        try:
            # Get the bucket and blob
            bucket = self.gcp_client.get_bucket(bucket_name)
            blob = bucket.get_blob(object_key)

            if blob is not None:
                md5_hash = blob.md5_hash
                if processing_info and key_to_set:
                    processing_info[key_to_set] = md5_hash  # Store MD5 hash in processing_info
                return True
            else:
                print(f"Object with key '{object_key}' does not exist in bucket '{bucket_name}'.")
                return False
                
        except NotFound:
            # print(f"Bucket '{bucket_name}' does not exist.")
            return False
        except Exception as e:
            # print(f"Error checking for object '{object_key}' in bucket '{bucket_name}': {e}")
            return False

    def parquet_existence_check(self, bucket_name, patient_id, versions):
        """
        Check for the existence of a Parquet file in a GCP bucket for a given patient ID across specified versions.

        This function checks if the Parquet file associated with the specified patient ID 
        exists for any of the provided version numbers. It returns the highest version number 
        where the file is found.

        Args:
            bucket_name (str): The name of the GCP bucket where the Parquet files are stored.
            patient_id (str): The patient ID used to construct the GCP key for the file.
            versions (list): A list of version numbers (integers) to check for the existence of the file.

        Returns:
            int or None: The version number where the Parquet file exists, or None if no file is found.

        Raises:
            ValueError: If `versions` is empty or contains non-integer values.
            Exception: For any other errors encountered during GCP access.

        Examples:
            bucket = 'my-bucket'
            patient = 'patient_123'
            available_versions = [1, 2, 3]
            version_found = parquet_existence_check(bucket, patient, available_versions)
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
            object_key = f"{patient_id}/v{version}/addr.parquet"  # Generate the GCP key for the file
            
            try:
                # Check if the blob exists in GCP
                if self.key_exists_in_storage(bucket_name, object_key):
                    # print(f'Parquet exists for Version: {version}')
                    return version  # Return the first version where the file exists
            except Exception as e:
                print(f"Error checking for file existence in bucket '{bucket_name}' for key '{object_key}': {e}")

        return None

    def load_parquet_file(self, bucket_name, object_key, environment, project_root=None):
        """
        Load a Parquet file from GCP or a local path into a Pandas DataFrame.

        This function attempts to load a Parquet file from a GCP bucket or from a local
        directory, depending on the specified environment. If the loading fails, it returns an empty
        DataFrame with default columns.

        Args:
            bucket_name (str): The name of the GCP bucket.
            object_key (str): The GCP key (path) of the Parquet file to load.
            environment (str): The current environment ('local' or 'production').
            project_root (str): The root path of the project for local file access.

        Returns:
            pd.DataFrame: A DataFrame containing the data from the Parquet file, or an empty
                        DataFrame with default columns if loading fails.

        Raises:
            ValueError: If the object_key is invalid.
            Exception: For any other errors encountered during file loading.

        Examples:
            df = load_parquet_file('my-bucket', 'path/to/file.parquet', 'production', '/path/to/project')
        """
        default_columns = ['section_name', 'document_id']
        gcp_path = f'gs://{bucket_name}/{object_key}'

        # Validate the object key
        if not object_key:
            print("Error: The 'object_key' must not be empty.")
            raise ValueError("The 'object_key' must not be empty.")

        try:
            if environment == "local":
                file_path = (Path(project_root) / object_key).resolve(strict=False)
                # print(f"Loading Parquet file from local path: {file_path}")
                df = pd.read_parquet(path=file_path)
            else:
                # print(f"Loading Parquet file from GCP: {gcp_path}")
                df = pd.read_parquet(path=gcp_path)  # Use pandas to read from GCP directly
                
            return df

        except FileNotFoundError as e:
            # print(f"Error: File not found: {e}")
            return pd.DataFrame(columns=default_columns)
        
        except Exception as e:
            print("Error: An unexpected error occurred while loading the Parquet file.")
            print(e)
            return pd.DataFrame(columns=default_columns)

    def load_json_from_storage(self, bucket_name, file_key):
            """
            Load a JSON file from GCP and return the parsed JSON object.

            This function retrieves a JSON file from the specified GCP bucket and parses its
            content into a Python dictionary. If the file does not exist or an error occurs,
            an empty dictionary is returned.

            Args:
                bucket_name (str): The name of the GCP bucket.
                file_key (str): The key (path) to the JSON file in GCP.

            Returns:
                dict: The parsed JSON object, or an empty dictionary if an error occurs.

            Raises:
                ValueError: If the file_key is empty.

            Examples:
                json_data = load_json_from_gcp('my-bucket', 'path/to/file.json')
            """
            # Validate the file key
            if not file_key:
                print("Error: The 'file_key' must not be empty.")
                raise ValueError("The 'file_key' must not be empty.")

            try:
                # Retrieve the bucket and the blob (file) from GCP
                bucket = self.gcp_client.get_bucket(bucket_name)
                blob = bucket.blob(file_key)

                # Check if the blob exists
                if not blob.exists():
                    print(f"The specified key '{file_key}' does not exist in the bucket '{bucket_name}'.")
                    return {}

                # Read the content of the file and parse it as JSON
                json_content = blob.download_as_text()
                json_data = json.loads(json_content)
                return json_data

            except Exception as e:
                print(f"An unexpected error occurred while loading the JSON file: {e}")
                return {}
            
    def download_folder_from_storage(self, bucket_name, folder_prefix, local_folder):
        """
        Download all files from a specified GCP folder to a local directory.

        This function retrieves all objects in the specified GCP folder (prefix) and
        downloads them to the given local folder. If the local folder does not exist,
        it will be created.

        Args:
            bucket_name (str): The name of the GCP bucket.
            folder_prefix (str): The prefix (folder path) in GCP from which to download files.
            local_folder (str): The local directory to which files will be downloaded.

        Raises:
            ValueError: If the bucket_name or folder_prefix is empty.
            Exception: If any unexpected error occurs during the download process.

        Examples:
            download_gcp_folder('my-bucket', 'path/to/folder/', '/local/path/')
        """
        # Validate input parameters
        if not bucket_name:
            raise ValueError("Bucket name must not be empty.")
        if not folder_prefix:
            raise ValueError("Folder prefix must not be empty.")

        # print(f"Starting download from GCP bucket '{bucket_name}' with prefix '{folder_prefix}' to local folder '{local_folder}'.")

        # Ensure the local folder exists
        os.makedirs(local_folder, exist_ok=True)

        try:
            # List objects in the specified GCP folder
            bucket = self.gcp_client.get_bucket(bucket_name)
            blobs = bucket.list_blobs(prefix=folder_prefix)

            total_files = 0
            for blob in blobs:
                total_files += 1
            
            if total_files > 0:
                # print(f"Found {total_files} files in GCP folder '{folder_prefix}'. Beginning download...")

                # Reset the blobs generator to iterate over the blobs again
                blobs = bucket.list_blobs(prefix=folder_prefix)

                # Loop through all objects in the GCP folder
                for idx, blob in enumerate(blobs, start=1):
                    file_name = os.path.basename(blob.name)  # Get the file name from the GCP blob name
                    if not file_name or blob.name.endswith('/'):
                        print(f"Skipping directory or empty file name: '{blob.name}'")
                        continue
                    local_file_path = os.path.join(local_folder, file_name)  # Create the local file path

                    # Download the file from GCP to the local folder
                    # print(f"Downloading file {idx}/{total_files}: '{file_name}' to '{local_file_path}'...")
                    blob.download_to_filename(local_file_path)

                print(f"Download completed. {total_files} files downloaded to '{local_folder}'.")

            else:
                print(f"No files found in the specified GCP folder '{folder_prefix}'.")

        except Exception as e:
            print(f"An error occurred during the download process: {e}")       

    def generate_signed_url(self, bucket_name, object_key, expiration_time=3600):
        """
        Generate a signed URL to retrieve an object from a GCP bucket.

        This function creates a signed URL that allows users to retrieve a specific 
        object from a GCP bucket without requiring direct access to the Google Cloud credentials.
        
        Parameters:
        - bucket_name (str): The name of the GCP bucket.
        - object_key (str): The key (file path) of the object in the GCP bucket.
        - expiration_time (int, optional): The time in seconds for the signed URL 
        to remain valid (default is 3600 seconds = 1 hour).

        Returns:
        - str: A signed URL for accessing the specified GCP object.

        Raises:
        - ValueError: If either bucket_name or object_key is not provided.
        - Exception: If an error occurs when generating the signed URL.

        Example:
            url = generate_signed_url('my-bucket', 'folder/myfile.txt', expiration_time=1800)
            print(url)

        Notes:
        - Ensure that the Google Cloud credentials used have sufficient permissions to generate
        signed URLs for GCP objects.
        """
        
        # Ensure bucket_name and object_key are provided
        if not bucket_name:
            raise ValueError("Bucket name is required.")
        if not object_key:
            raise ValueError("Object key is required.")

        try:
            # Get the bucket and blob
            bucket = self.gcp_client.get_bucket(bucket_name)
            blob = bucket.blob(object_key)

            # Generate the signed URL
            pre_signed_url = blob.generate_signed_url(
                version='v4',
                expiration=timedelta(seconds=expiration_time),
                method='GET'  # The method can be 'GET' or 'PUT'
            )
            return pre_signed_url

        except Exception as e:
            print(f"An error occurred while generating the signed URL: {e}")
            return None

    def save_data_and_get_signed_url(self, bucket_name, file_name, result, environment, local_dir_path):
        """
        Save a JSON object either locally or to GCP, and generate a signed URL for the GCP object.

        Parameters:
        - bucket_name (str): The name of the GCP bucket where the file will be stored.
        - file_name (str): The name (key) of the file to save in GCP or locally.
        - result (dict): The JSON object to save.
        - environment (str): The current environment ('local' or 'gcp').
        - local_dir_path (str): The local directory path to save the file if the environment is 'local'.

        Returns:
        - tuple:
            - If environment is 'local':
              ('local', None)
            - If environment is 'gcp':
              - str: Signed URL for accessing the file in GCP.
              - str: The file's ETag (hash) from GCP.
              - int: The file's size in bytes.
        
        Raises:
        - ValueError: If required parameters are missing or invalid.
        - Exception: If an error occurs while uploading to or retrieving from GCP.

        Example:
            result_data = {"key": "value"}
            url, file_hash, file_size = save_data_and_get_signed_url(
                'my-bucket', 'data/result.json', result_data, environment='gcp', local_dir_path='/tmp')
        """
        
        # Handle local environment
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
        
        # Handle GCP environment
        try:
            if isinstance(result, str):
                result = json.loads(result)
            bucket = self.gcp_client.get_bucket(bucket_name)
            blob = bucket.blob(file_name)

            # Upload the JSON object to GCP
            blob.upload_from_string(json.dumps(result), content_type='application/json')

            # Get the file's ETag (hash)
            file_hash = blob.etag.strip('"')

            # Get the file size from the blob
            file_size = blob.size

            # Generate the signed URL
            signed_url = blob.generate_signed_url(version='v4', expiration=timedelta(hours=1), method='GET')

            # Return the signed URL, file hash, and file size
            return signed_url, file_hash, file_size

        except Exception as e:
            print(f"An error occurred while saving to GCP: {e}")
            return None, None, None

    def download_ml_models(self, processing_info, bucket_name, gcp_dir_path, local_dir_path):
        """
        Downloads all model files for a specific version from a GCP bucket.

        Args:
        - processing_info (dict): Dictionary containing processing metadata, including model version.
        - bucket_name (str): Name of the GCP bucket.
        - gcp_dir_path (str): Path in the GCp bucket where models are stored (e.g., 'Summary_Models/').
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

        # Get the GCP bucket
        bucket = self.gcp_client.get_bucket(bucket_name)

        # List objects in the specified GCP directory
        blobs = bucket.list_blobs(prefix=gcp_dir_path)

        # Loop through the GCP objects and download relevant files
        for blob in blobs:
            key = blob.name
            
            # Check if the key matches the specified version
            if f"/{processing_info['summary_version']}/" in key:
                filename = key  # Extract filename from key
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
                        # Download the file from GCP
                        # print(f"Downloading {filename} from GCP...")
                        blob.download_to_filename(local_file_path)
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
                json_metadata_path (str): The base GCP path where JSON metadata is stored.

            Returns:
                tuple: Three DataFrames (trident_changes_metadata_df, hr_metadata_df, mr_metadata_df)
            """
            # Define GCP object keys
            trident_changes_metadata_object_key = f"summary/{version}/{person_id}/{person_id}_trident_changes.parquet"
            mr_object_key = f"summary/{version}/{person_id}/{person_id}_mr_metadata.parquet"
            hr_object_key = f"summary/{version}/{person_id}/{person_id}_hr_metadata.parquet"
            
            # Define expected columns for each DataFrame
            trident_changes_columns = ['person_id', 'document_id', 'org_id', 'org_name', 'section_name', 'section_code', 
                                    'original_column', 'destination_column', 'changes_type', 'overlapping_count', 
                                    'predicted_scores', 'row_count', 'rows_below_95', 'top_5_predictions', 
                                    'merge_status', 'is_unknown', 'create_date']
            mr_metadata_columns = ['document_id', 'section_name', 'row_count', 'create_date']
            hr_metadata_columns = ['document_id', 'section_name', 'row_count', 'unknown_section', 'create_date']
            
            # Helper function to load a parquet file or return an empty DataFrame
            def load_parquet_or_empty(gcp_path, columns):
                try:
                    # Check if the file exists in GCP
                    blob = self.gcp_client.get_bucket(json_metadata_path).blob(gcp_path)
                    if blob.exists():
                        return pd.read_parquet(blob.open("rb"))  # Load parquet file from GCP
                    else:
                        print(f"File '{gcp_path}' does not exist in GCP.")
                        return pd.DataFrame(columns=columns)
                except Exception as e:
                    print(f"Error loading parquet file '{gcp_path}': {e}")
                    return pd.DataFrame(columns=columns)

            # Load metadata
            trident_changes_metadata_df = load_parquet_or_empty(trident_changes_metadata_object_key, trident_changes_columns)
            mr_metadata_df = load_parquet_or_empty(mr_object_key, mr_metadata_columns)
            hr_metadata_df = load_parquet_or_empty(hr_object_key, hr_metadata_columns)

            return trident_changes_metadata_df, hr_metadata_df, mr_metadata_df

    def _save_dataframe_to_gcp(self, dataframe, bucket_name, gcp_path):
        """
        Save a DataFrame to a specified path in Google Cloud Storage as a parquet file.

        Args:
            dataframe (pd.DataFrame): The DataFrame to save.
            bucket_name (str): The name of the GCP bucket.
            gcp_path (str): The GCP path where the file will be stored.
        """
        bucket = self.gcp_client.get_bucket(bucket_name)
        blob = bucket.blob(gcp_path)
        
        # Save DataFrame to a temporary file before uploading to GCP
        with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
            dataframe.to_parquet(tmp_file.name)
            tmp_file.seek(0)  # Move to the beginning of the file
            
            # Upload the temporary file to GCP
            blob.upload_from_file(tmp_file, content_type='application/octet-stream')
            print(f"Saved '{gcp_path}' to GCP.")
    
    def save_json_metadata(self, processing_info, trident_changes_metadata_df, hr_metadata_df, mr_metadata_df, json_metadata_path):
        """
        Save metadata DataFrames to GCP as parquet files.

        Args:
            processing_info (dict): Information about the processing, including 'summary_version' and 'person_id'.
            trident_changes_metadata_df (pd.DataFrame): DataFrame containing trident changes metadata.
            hr_metadata_df (pd.DataFrame): DataFrame containing HR metadata.
            mr_metadata_df (pd.DataFrame): DataFrame containing MR metadata.
            json_metadata_path (str): The base GCP path where JSON metadata is stored.
        """
        summary_version = processing_info['summary_version']
        person_id = processing_info['person_id']
        
        # Define GCP paths for saving the parquet files
        trident_changes_gcp_path = f"summary/{summary_version}/{person_id}/{person_id}_trident_changes.parquet"
        hr_gcp_path = f"summary/{summary_version}/{person_id}/{person_id}_hr_metadata.parquet"
        mr_gcp_path = f"summary/{summary_version}/{person_id}/{person_id}_mr_metadata.parquet"

        try:
            # Save DataFrames to GCP as parquet files
            self._save_dataframe_to_gcp(trident_changes_metadata_df, json_metadata_path, trident_changes_gcp_path)
            self._save_dataframe_to_gcp(hr_metadata_df, json_metadata_path, hr_gcp_path)
            self._save_dataframe_to_gcp(mr_metadata_df, json_metadata_path, mr_gcp_path)

            # print(f"Metadata saved for {person_id} in version {summary_version}.")
            
        except Exception as e:
            print(f"An error occurred while saving metadata for {person_id}: {e}")

    def add_unknown_sections(self, bucket_name, prefix, section_column_df):
        """
        Add unknown sections from GCP parquet files to the section_column_df DataFrame.

        Args:
            bucket_name (str): The name of the GCP bucket.
            prefix (str): The GCP prefix to filter the objects.
            section_column_df (pd.DataFrame): DataFrame containing existing section names.

        Returns:
            pd.DataFrame: Updated DataFrame including unknown sections.
        """
        try:
            # Initialize GCP client
            client = storage.Client()
            bucket = client.get_bucket(bucket_name)
            blobs = bucket.list_blobs(prefix=prefix)

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

    def save_file_to_storage(self, df=None, bucket_name=None, key=None, file_type='parquet', compression=None,
                             data_dict=None, xml_content=None):
        """
        Saves a given DataFrame or JSON dictionary to a Google Cloud Storage (GCS) bucket in the specified format.

        Parameters:
            df (pd.DataFrame, optional): The DataFrame to save (required for CSV, Parquet, Excel, and JSON if data_dict is not provided).
            bucket_name (str): The destination GCS bucket.
            key (str): The blob key (path including filename) where the file should be saved.
            file_type (str, optional): The type of file to save ('parquet', 'csv', 'excel', 'json', 'xml'). Defaults to 'parquet'.
            compression (str, optional): Compression type, applicable for formats like Parquet, CSV, and JSON.
            data_dict (dict, optional): Dictionary to save as a JSON file if file_type is 'json'. If not provided, the df will be converted to JSON.
            xml_content (str, optional): XML content to save if file_type is 'xml'.

        Raises:
            ValueError: If an unsupported file type is provided.
            Exception: If the upload fails.
        """
        supported_file_types = ['parquet', 'csv', 'excel', 'json', 'xml']
        if file_type not in supported_file_types:
            raise ValueError(f"Unsupported file type: {file_type}. Supported types: {supported_file_types}")

        if not bucket_name or not key:
            raise ValueError("Both bucket_name and key are required parameters.")

        try:
            bucket = self.gcp_client.bucket(bucket_name)
            blob = bucket.blob(key)

            if file_type == 'parquet':
                buffer = io.BytesIO()
                df.to_parquet(buffer, index=False, compression=compression)
                buffer.seek(0)
                blob.upload_from_file(buffer, content_type='application/octet-stream')

            elif file_type == 'csv':
                buffer = io.StringIO()
                df.to_csv(buffer, index=False)
                blob.upload_from_string(buffer.getvalue(), content_type='text/csv')

            elif file_type == 'excel':
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False)
                buffer.seek(0)
                blob.upload_from_file(buffer,
                                      content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            elif file_type == 'json':
                json_data_string = json.dumps(data_dict if data_dict is not None else df.to_dict(orient='records'))
                blob.upload_from_string(json_data_string, content_type="application/json")

            elif file_type == 'xml':
                if xml_content is None:
                    raise ValueError("xml_content must be provided for XML file type")
                blob.upload_from_string(xml_content, content_type="application/xml")

        except Exception as e:
            raise Exception(f"Failed to save file to Google Cloud Storage: {e}")

    def download_ccda_files_from_storage(self, bucket_name, prefix=None, person_id=None, download_ccda_files=None,
                                         local_dir_path=None):
        """
        Downloads specific CCDA files from Google Cloud Storage based on provided document details.

        Args:
            bucket_name (str): The name of the GCP bucket.
            prefix (str, optional): The path between the bucket name and the person_id, if applicable.
            person_id (str): The ID of the person whose files need to be downloaded.
            download_ccda_files (list): A list of dictionaries containing 'document_id' of files to download.
            local_dir_path (str): The local directory where files will be saved.

        Returns:
            list: Updated list of dictionaries with 'downloaded' status.

        Raises:
            Exception: If there is an error during the file download process.

        Example Usage:
            gcp_storage = GCPStorage()
            files_to_download = [{'document_id': '12345'}, {'document_id': '67890'}]
            gcp_storage.download_ccda_files_from_storage('my-bucket', 'data/v1', 'patient_001', files_to_download, '/local/path')
        """
        if not bucket_name or not person_id or not download_ccda_files or not local_dir_path:
            raise ValueError("All parameters except prefix are required.")

        local_dir = os.path.join(local_dir_path, person_id)
        os.makedirs(local_dir, exist_ok=True)

        try:
            bucket = self.gcp_client.bucket(bucket_name)

            for obj in download_ccda_files:
                key = f"{prefix}/{person_id}/{obj['document_id']}.xml" if prefix else f"{person_id}/{obj['document_id']}.xml"
                local_file = os.path.join(local_dir, f"{obj['document_id']}.xml")

                # print(f"Downloading {key} to {local_file}...")

                blob = bucket.blob(key)
                blob.download_to_filename(local_file)

                obj['downloaded'] = True
                # print(f"Downloaded: {key}")

        except Exception as e:
            print(f"An unexpected error occurred while downloading files: {e}")
            return []

        return download_ccda_files

    def download_file_from_storage(self, bucket_name, key, local_path, unzip=False):
        """
        Downloads a specific file from Google Cloud Storage (GCS) to a local path.

        Args:
            bucket_name (str): The name of the GCP bucket.
            key (str): The object key (full path) of the file to download.
            local_path (str): The local directory where the file will be saved.
            unzip (bool, optional): Whether to unzip `.tar.gz` files automatically. Defaults to True.

        Returns:
            str: The local file path, or extracted folder path if unzipping.

        Raises:
            Exception: If an error occurs during the file download process.

        Example Usage:
            gcp_storage = GCPStorage()
            gcp_storage.download_file_from_storage('my-bucket', 'path/to/file.csv', '/local/path')
        """
        if not bucket_name or not key or not local_path:
            raise ValueError("All parameters are required.")

        local_file_path = os.path.join(local_path, os.path.basename(key))
        os.makedirs(local_path, exist_ok=True)

        try:
            # print(f"Downloading {key} to {local_file_path}...")

            bucket = self.gcp_client.bucket(bucket_name)
            blob = bucket.blob(key)
            blob.download_to_filename(local_file_path)

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
            print(f'Unzipping {filename}...')
            with tarfile.open(filename, 'r:gz') as f:
                f.extractall(path=dest)

            extracted_folder = os.path.join(dest, os.path.basename(filename).replace(".tar.gz", ""))
            print(f'Extracted to {extracted_folder}')
            return extracted_folder

        except Exception as e:
            print(f"Failed to unzip {filename}: {e}")
            raise
