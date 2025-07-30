"""
Prompt generation functions for JavaScript/TypeScript conversion.
"""

def generate_conversion_prompt(source_code, source_language, target_language, case_format):
    """
    Generate a prompt specifically for JavaScript to TypeScript (or reverse) code conversion.
    
    Args:
        source_code (str): The source code to convert
        source_language (str): Source language (JavaScript or TypeScript)
        target_language (str): Target language (JavaScript or TypeScript)
        case_format (str): Desired case format (camelCase, PascalCase, etc.)
        
    Returns:
        str: A formatted prompt for the AI model
    """
    return f"""
# Code Conversion Task: {source_language} to {target_language}

## Source Code ({source_language}):
```
{source_code}
```

## Conversion Instructions:
1. Convert the above {source_language} code to {target_language}.
2. Use {case_format} for variable and function naming.
3. Follow {target_language} best practices and idioms.
4. Preserve the functionality and logic of the original code.
5. Add appropriate type annotations if converting to TypeScript.
6. Include explanatory comments for any significant changes.
7. If appropriate, use modern features available in the target language.

## Output Format:
Provide ONLY the converted code in a code block with NO additional explanations.
```
// Your converted code here
```
"""


def generate_unit_test_prompt(ts_code):
    """
    Generates the prompt for creating a Jasmine unit test for the provided TypeScript code.
    
    Args:
        ts_code (str): TypeScript code to generate tests for
        
    Returns:
        str: Formatted unit test generation prompt
    """
    return f"""
# Unit Test Generation Request

## TypeScript Code to Test:
```typescript
{ts_code}
```

## Instructions:
1. Create comprehensive Jasmine unit tests for the TypeScript code above.
2. Include test cases for all functions, covering:
   - Normal input/output cases
   - Edge cases
   - Error handling scenarios
3. Use proper Jasmine syntax with describe(), it(), beforeEach() as appropriate.
4. Mock dependencies and external services as needed.
5. Include setup and teardown code if necessary.
6. Focus on full test coverage of the functionality.

## Output Format:
Provide ONLY the complete test code in a TypeScript format without explanations.
```typescript
// Your test code here
```
"""
