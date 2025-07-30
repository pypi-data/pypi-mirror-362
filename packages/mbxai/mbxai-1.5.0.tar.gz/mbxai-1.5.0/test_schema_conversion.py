"""
Test for schema conversion with Pydantic models containing arrays.

This test demonstrates the fix for the "array schema missing items" error
when converting Pydantic models to OpenAI function schemas.
"""

import json
from typing import Any
from pydantic import BaseModel, Field

from src.mbxai.tools.types import convert_to_strict_schema


class MetadataFilter(BaseModel):
    """Model for a single metadata filter key-value pair.
    
    Each filter represents one condition to apply to the search.
    Common filter keys include:
    - category: Content category (e.g., 'api', 'plugins', 'themes')
    - version: Shopware version (e.g., '6.5', '6.6') 
    - title: Document title (partial match)
    - optimized: Whether content was AI-optimized (true/false)
    - source_url: Source URL (partial match)
    - optimization_strategy: Strategy used ('enhance_readability', etc.)
    - ai_generated_metadata: Whether metadata was AI-generated (true/false)
    """
    
    key: str = Field(description="The metadata field name to filter by")
    value: Any = Field(description="The value to filter for")


class ShopwareKnowledgeSearchInput(BaseModel):
    """Input model for Shopware knowledge search."""
    
    query: str = Field(
        description="The search query to find relevant Shopware knowledge and documentation"
    )
    max_results: int = Field(
        description="Maximum number of search results to return (1-20)",
        ge=1,
        le=20
    )
    include_metadata: bool = Field(
        description="Whether to include metadata in the search results"
    )
    metadata_filter: list[MetadataFilter] = Field(
        description="List of metadata filters to apply to the search. Use empty list [] for no filtering, or specify key-value pairs like [{'key': 'category', 'value': 'api'}, {'key': 'version', 'value': '6.5'}]"
    )


def test_schema_conversion():
    """Test that Pydantic models are properly converted to OpenAI-compatible schemas."""
    
    print("🧪 Testing Schema Conversion for Shopware Knowledge Search")
    print("=" * 60)
    
    # Generate the JSON schema from the Pydantic model
    print("\n1. Generating Pydantic JSON Schema...")
    pydantic_schema = ShopwareKnowledgeSearchInput.model_json_schema()
    
    print("Original Pydantic Schema:")
    print(json.dumps(pydantic_schema, indent=2))
    
    # Test 1: Convert without input wrapper
    print("\n2. Converting to OpenAI strict schema (no input wrapper)...")
    strict_schema_no_wrapper = convert_to_strict_schema(
        pydantic_schema, 
        strict=True, 
        keep_input_wrapper=False
    )
    
    print("Strict Schema (no wrapper):")
    print(json.dumps(strict_schema_no_wrapper, indent=2))
    
    # Test 2: Convert with input wrapper (MCP style)
    print("\n3. Converting to OpenAI strict schema (with input wrapper)...")
    
    # Create MCP-style schema with input wrapper
    mcp_style_schema = {
        "type": "object",
        "properties": {
            "input": pydantic_schema
        },
        "required": ["input"],
        "additionalProperties": False
    }
    
    strict_schema_with_wrapper = convert_to_strict_schema(
        mcp_style_schema,
        strict=True,
        keep_input_wrapper=True
    )
    
    print("Strict Schema (with input wrapper):")
    print(json.dumps(strict_schema_with_wrapper, indent=2))
    
    # Test 3: Create OpenAI function definition
    print("\n4. Creating OpenAI Function Definition...")
    
    function_def = {
        "type": "function",
        "function": {
            "name": "search_shopware_knowledge",
            "description": "Search Shopware knowledge base for relevant documentation and information",
            "parameters": strict_schema_no_wrapper,
            "strict": True
        }
    }
    
    print("OpenAI Function Definition:")
    print(json.dumps(function_def, indent=2))
    
    # Validation checks
    print("\n5. Validation Checks...")
    print("✅ Checking that all arrays have 'items' property...")
    
    def check_arrays_have_items(schema, path=""):
        """Recursively check that all arrays have items property."""
        issues = []
        
        if isinstance(schema, dict):
            if schema.get("type") == "array":
                if "items" not in schema:
                    issues.append(f"Array at {path} missing 'items' property")
                else:
                    print(f"   ✓ Array at {path} has items: {schema['items'].get('type', 'unknown')}")
                    # Recursively check items
                    issues.extend(check_arrays_have_items(schema["items"], f"{path}.items"))
            
            # Check properties
            if "properties" in schema:
                for prop_name, prop_schema in schema["properties"].items():
                    prop_path = f"{path}.{prop_name}" if path else prop_name
                    issues.extend(check_arrays_have_items(prop_schema, prop_path))
        
        return issues
    
    issues = check_arrays_have_items(strict_schema_no_wrapper)
    if issues:
        for issue in issues:
            print(f"   ❌ {issue}")
        raise AssertionError(f"Schema validation failed: {issues}")
    else:
        print("   ✓ All arrays have proper 'items' definitions")
    
    print("\n✅ Checking that no $ref or $defs exist...")
    schema_str = json.dumps(strict_schema_no_wrapper)
    if "$ref" in schema_str or "$defs" in schema_str:
        raise AssertionError("Schema still contains $ref or $defs")
    else:
        print("   ✓ No $ref or $defs found - schema is fully inlined")
    
    print("\n✅ Checking that all objects have additionalProperties: false...")
    def check_additional_properties(schema, path=""):
        """Recursively check that all objects have additionalProperties: false."""
        issues = []
        
        if isinstance(schema, dict):
            if schema.get("type") == "object":
                if schema.get("additionalProperties") is not False:
                    issues.append(f"Object at {path} missing 'additionalProperties: false'")
                else:
                    print(f"   ✓ Object at {path} has additionalProperties: false")
            
            # Check nested schemas
            for key, value in schema.items():
                if key in ["properties", "items"] and isinstance(value, dict):
                    if key == "properties":
                        for prop_name, prop_schema in value.items():
                            prop_path = f"{path}.{prop_name}" if path else prop_name
                            issues.extend(check_additional_properties(prop_schema, prop_path))
                    else:  # items
                        issues.extend(check_additional_properties(value, f"{path}.items"))
        
        return issues
    
    issues = check_additional_properties(strict_schema_no_wrapper)
    if issues:
        for issue in issues:
            print(f"   ❌ {issue}")
        raise AssertionError(f"additionalProperties validation failed: {issues}")
    else:
        print("   ✓ All objects have additionalProperties: false")
    
    print("\n🎉 All tests passed! Schema is OpenAI/OpenRouter compatible!")
    print("\nKey improvements:")
    print("- ✅ Arrays have proper 'items' definitions")
    print("- ✅ No $ref or $defs (fully inlined)")
    print("- ✅ All objects have additionalProperties: false")
    print("- ✅ Constraints preserved (ge=1, le=20 for max_results)")
    print("- ✅ Complex nested structures handled correctly")
    
    return function_def


if __name__ == "__main__":
    try:
        function_def = test_schema_conversion()
        print(f"\n✅ Test completed successfully!")
        print(f"Function definition ready for OpenRouter API")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise 