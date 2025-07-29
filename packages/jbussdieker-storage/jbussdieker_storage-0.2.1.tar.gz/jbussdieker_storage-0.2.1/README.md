# jbussdieker-storage

A modern Python development toolkit plugin for persistent storage operations using cloud storage services. This plugin integrates with the jbussdieker CLI framework to provide seamless storage management capabilities.

## 🚀 Features

- **Cloud Storage Integration**: Seamlessly connect to AWS S3 storage buckets
- **Directory Listing**: List and explore storage prefixes and directories
- **Configurable Storage URLs**: Support for S3 storage URLs with bucket and prefix configuration
- **CLI Integration**: Fully integrated with the jbussdieker CLI framework
- **Extensible Architecture**: Easy to extend for additional storage backends

## 📦 Installation

```bash
pip install jbussdieker-storage --upgrade
```

## 🔧 Prerequisites

- Python 3.9 or higher
- AWS credentials configured (via AWS CLI, environment variables, or IAM roles)
- jbussdieker CLI framework
- Valid S3 bucket access permissions

## 🎯 Usage

### Basic Usage

List directories in your configured storage:

```bash
jbussdieker storage
```

### Configuration

The plugin requires a storage URL to be configured in your jbussdieker configuration. The storage URL should follow the S3 format:

```
s3://bucket-name/prefix/
```

### Example Configuration

Add the following to your jbussdieker configuration:

```yaml
storage_url: "s3://my-project-bucket/data/"
```

## 🔍 How It Works

1. **Configuration Validation**: Checks for a valid storage URL in your jbussdieker configuration
2. **URL Parsing**: Extracts bucket name and prefix from the S3 URL
3. **Storage Connection**: Establishes connection to AWS S3 using boto3
4. **Directory Listing**: Lists all subdirectories under the configured prefix
5. **Output Display**: Prints the directory structure to stdout

## 🛠️ Supported Storage Backends

### AWS S3

Currently supports AWS S3 storage with the following features:

- **Bucket Access**: Connect to any S3 bucket you have access to
- **Prefix Support**: Work within specific prefixes in your bucket
- **Directory Listing**: List all subdirectories under a given prefix
- **Pagination**: Handles large directory structures efficiently

### Future Backends

The plugin architecture is designed to support additional storage backends:

- Google Cloud Storage
- Azure Blob Storage
- Local file system
- Other S3-compatible services

## 📋 Storage URL Format

The plugin supports the following URL format for S3:

```
s3://<bucket-name>/<prefix>/
```

### Examples

- `s3://my-project-bucket/` - Root of bucket
- `s3://my-project-bucket/data/` - Data directory
- `s3://my-project-bucket/users/john/` - User-specific directory

## 🔍 Error Handling

The plugin provides clear error messages for common issues:

- **Missing Configuration**: When no storage URL is configured
- **Invalid URL Format**: When the storage URL doesn't match expected format
- **Unsupported Backend**: When trying to use an unsupported storage service
- **Access Denied**: When AWS credentials are invalid or insufficient

## 🛠️ Development

This plugin is part of the jbussdieker ecosystem. It integrates seamlessly with the jbussdieker CLI framework.

### Project Structure

```
src/jbussdieker/storage/
├── __init__.py
├── cli.py          # CLI interface and argument parsing
└── store.py        # Storage backend implementations
```

### Adding New Storage Backends

To add support for a new storage backend:

1. Create a new store class in `store.py`
2. Implement the required interface methods
3. Update the CLI logic in `cli.py` to handle the new URL scheme
4. Add appropriate tests

## 📝 License

This project is licensed under **MIT**.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📚 Related

- [jbussdieker](https://pypi.org/project/jbussdieker/) - The main CLI framework
- [boto3](https://boto3.amazonaws.com/) - AWS SDK for Python
- [AWS S3](https://aws.amazon.com/s3/) - Amazon Simple Storage Service
