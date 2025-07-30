"""
Core converter module for JavaScript/TypeScript code conversion.
"""

import os
from dotenv import load_dotenv
from anthropic import AnthropicBedrock
from .prompts import generate_conversion_prompt, generate_unit_test_prompt


class JSConverter:
    """
    JavaScript/TypeScript code converter using Claude AI.
    
    This class provides methods to convert code between JavaScript and TypeScript
    and to generate unit tests for TypeScript code.
    """
    
    def __init__(self, aws_access_key=None, aws_secret_key=None, aws_region=None):
        """
        Initialize the JavaScript/TypeScript converter.
        
        Args:
            aws_access_key (str, optional): AWS access key for Anthropic Bedrock.
                If not provided, will attempt to load from environment.
            aws_secret_key (str, optional): AWS secret key for Anthropic Bedrock.
                If not provided, will attempt to load from environment.
            aws_region (str, optional): AWS region for Anthropic Bedrock.
                If not provided, will attempt to load from environment.
        """
        # Load environment variables if credentials not explicitly provided
        load_dotenv()
        
        # Use provided credentials or fallback to environment variables
        aws_access_key = aws_access_key or os.getenv("AWS_ACCESS_KEY")
        aws_secret_key = aws_secret_key or os.getenv("AWS_SECRET_KEY")
        aws_region = aws_region or os.getenv("AWS_REGION")
        
        # Initialize Anthropic client
        self.client = AnthropicBedrock(
            aws_access_key=aws_access_key,
            aws_secret_key=aws_secret_key,
            aws_region=aws_region
        )
        
        # Default model
        self.model = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    
    def convert_code(self, source_code, source_language, target_language, case_format="camelCase"):
        """
        Convert code between JavaScript and TypeScript.
        
        Args:
            source_code (str): The source code to convert
            source_language (str): Source language ("JavaScript" or "TypeScript")
            target_language (str): Target language ("JavaScript" or "TypeScript")
            case_format (str, optional): Naming convention for code. Defaults to "camelCase".
        
        Returns:
            str: The converted code
        
        Raises:
            ValueError: If source_language or target_language are not "JavaScript" or "TypeScript"
        """
        # Validate languages
        valid_languages = ["JavaScript", "TypeScript"]
        if source_language not in valid_languages:
            raise ValueError(f"Source language must be one of {valid_languages}, got {source_language}")
        if target_language not in valid_languages:
            raise ValueError(f"Target language must be one of {valid_languages}, got {target_language}")
        
        # Generate prompt
        prompt = generate_JsTs_conversion_prompt(source_code, source_language, target_language, case_format)
        
        # Send to model
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": f"You are an AI specialized in translating code between programming languages.\n\n{prompt}"}
            ]
        )
        
        # Extract and return response
        return response.content[0].text if response and response.content else "Conversion failed."
    
    def generate_unit_test(self, source_code):
        """
        Generate unit tests for TypeScript code using Jasmine framework.
        
        Args:
            source_code (str): The TypeScript code to generate tests for
        
        Returns:
            str: Generated unit tests
        """
        # Generate prompt
        prompt = generate_unit_test_prompt(source_code)
        
        # Send to model
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": f"You are an AI specialized in generating unit tests.\n\n{prompt}"}
            ]
        )
        
        # Extract and return response
        return response.content[0].text if response and response.content else "Test generation failed."
    
    def set_model(self, model):
        """
        Set a different Claude model to use.
        
        Args:
            model (str): The model identifier to use
        """
        self.model = model
