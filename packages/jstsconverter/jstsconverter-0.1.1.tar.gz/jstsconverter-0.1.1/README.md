# JavaScript/TypeScript Converter SDK

A powerful Python library for converting code between JavaScript and TypeScript using Claude AI through Anthropic Bedrock.

## Features

- **Code Conversion**: Convert JavaScript code to TypeScript with proper type annotations
- **Unit Test Generation**: Generate comprehensive unit tests for TypeScript code
- **AWS Bedrock Integration**: Uses Anthropic's Claude AI through AWS Bedrock for intelligent code conversion
- **Configurable Options**: Flexible configuration for different conversion scenarios

## Installation

```bash
pip install jstsconverter
```

## Quick Start

```python
from jstsconverter import JSConverter

# Initialize the converter
converter = JSConverter(
    aws_access_key="your-aws-access-key",
    aws_secret_key="your-aws-secret-key", 
    aws_region="us-east-1"
)

# Convert JavaScript to TypeScript
js_code = """
function greet(name) {
    return "Hello, " + name + "!";
}
"""

typescript_code = converter.convert_js_to_ts(js_code)
print(typescript_code)
```

## Configuration

The converter can be configured with AWS credentials in several ways:

1. **Direct initialization**:
```python
converter = JSConverter(
    aws_access_key="your-key",
    aws_secret_key="your-secret",
    aws_region="us-east-1"
)
```

2. **Environment variables**:
```bash
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
export AWS_DEFAULT_REGION=us-east-1
```

3. **`.env` file**:
```
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_DEFAULT_REGION=us-east-1
```

## Requirements

- Python 3.7+
- AWS account with Anthropic Bedrock access
- Valid AWS credentials

## Dependencies

- `anthropic`: For Claude AI integration
- `python-dotenv`: For environment variable management

## License

MIT License

## Author

Ramya Paranitharan (ramya.paranitharan@optisolbusiness.com)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 