# Cloud Storage Service

A unified cloud storage package that provides seamless integration with major cloud providers: Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP). This library allows developers to easily access and manage cloud storage services with a consistent interface.

## Package Structure

```plaintext
- storage_manager.py   # Factory function to create DB connection based on the service type
- aws_storage.py       # AWS RDS MySQL connection class
- azure_storage.py     # Azure SQL Database connection class        
- gcp_storage.py       # Google Cloud MySQL connection class
```

## Features

- **Supports Multiple Cloud Providers**: Easily switch between AWS, Azure, and GCP.
- **Flexible Configuration**: Configure services with required parameters for each provider.
- **Intuitive API**: Simple methods for managing cloud storage operations.

## Installation
Ensure all necessary dependencies are installed:
```python
pip install cloud_storage_service
```

## Usage

```python
#! pip install cloud_storage_service

from cloud_storage_service import get_cloud_storage_service

def test_get_document_details():
    bucket_name = 'testbucket'
    prefix = '000740194c8c-adfe-2ab061872773d3/test_data/'  

    aws_service = get_cloud_storage_service('aws')

    try:
        documents = aws_service.get_document_details(bucket_name, prefix=prefix, file_type='.xml')
        
        if documents:
            print("Fetched document details:")
            for doc_name, doc_info in documents.items():
                print(f"Document Name: {doc_info['document_name']}")
                print(f"Document Hash: {doc_info['document_hash']}")
                print(f"Document Size: {doc_info['document_size']} bytes")
                print(f"File Type: {doc_info['file_type']}")
                print("-" * 40)
        else:
            print("No documents found.")
    
    except Exception as e:
        print(f"Error occurred: {e}")

test_get_document_details()
```

