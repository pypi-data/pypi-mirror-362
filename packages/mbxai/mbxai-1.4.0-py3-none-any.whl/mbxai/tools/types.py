"""
Type definitions for the tools package.
"""

from typing import Any, Callable
from pydantic import BaseModel, Field
import logging
import json

logger = logging.getLogger(__name__)

def convert_to_strict_schema(schema: dict[str, Any], strict: bool = True, keep_input_wrapper: bool = False) -> dict[str, Any]:
    """Convert a schema to strict format required by OpenAI.
    
    Args:
        schema: The input schema to validate and convert
        strict: Whether to enforce strict validation with additionalProperties: false
        keep_input_wrapper: Whether to keep the input wrapper (for MCP tools)
        
    Returns:
        A schema in strict format
    """
    if not schema:
        return {"type": "object", "properties": {}, "required": [], "additionalProperties": False}

    # Create a new schema object to ensure we have all required fields
    strict_schema = {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False  # Always enforce additionalProperties: false for OpenRouter
    }

    # Handle input wrapper
    if "properties" in schema and "input" in schema["properties"]:
        inputSchema = schema["properties"]["input"]
        
        # If input has a $ref, resolve it
        if "$ref" in inputSchema:
            ref = inputSchema["$ref"].split("/")[-1]
            inputSchema = schema.get("$defs", {}).get(ref, {})
        
        if keep_input_wrapper:
            # Create the input property schema
            input_prop_schema = {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False  # Always enforce additionalProperties: false for OpenRouter
            }
            
            # Copy over input properties
            if "properties" in inputSchema:
                for prop_name, prop in inputSchema["properties"].items():
                    # Create a new property object with only allowed fields
                    new_prop = {
                        "type": prop.get("type", "string"),
                        "description": prop.get("description", f"The {prop_name} parameter")
                    }
                    
                    # If the property is an object, ensure it has additionalProperties: false
                    if new_prop["type"] == "object":
                        new_prop["additionalProperties"] = False
                    
                    input_prop_schema["properties"][prop_name] = new_prop
            
            # Copy over required fields for input schema
            if "required" in inputSchema:
                input_prop_schema["required"] = inputSchema["required"]
            
            # Add the input property to the main schema
            strict_schema["properties"]["input"] = input_prop_schema
            
            # Copy over required fields for main schema
            if "required" in schema:
                strict_schema["required"] = schema["required"]
        else:
            # If not keeping input wrapper, use input schema directly
            if "properties" in inputSchema:
                for prop_name, prop in inputSchema["properties"].items():
                    # Create a new property object with only allowed fields
                    new_prop = {
                        "type": prop.get("type", "string"),
                        "description": prop.get("description", f"The {prop_name} parameter")
                    }
                    
                    # If the property is an object, ensure it has additionalProperties: false
                    if new_prop["type"] == "object":
                        new_prop["additionalProperties"] = False
                    
                    strict_schema["properties"][prop_name] = new_prop
            
            # Copy over required fields
            if "required" in inputSchema:
                strict_schema["required"] = inputSchema["required"]
    else:
        # If no input wrapper, use the schema as is
        if "properties" in schema:
            for prop_name, prop in schema["properties"].items():
                # Create a new property object with only allowed fields
                new_prop = {
                    "type": prop.get("type", "string"),
                    "description": prop.get("description", f"The {prop_name} parameter")
                }
                
                # If the property is an object, ensure it has additionalProperties: false
                if new_prop["type"] == "object":
                    new_prop["additionalProperties"] = False
                
                strict_schema["properties"][prop_name] = new_prop
        
        # Copy over required fields
        if "required" in schema:
            strict_schema["required"] = schema["required"]

    return strict_schema

class ToolCall(BaseModel):
    """A tool call from the model."""
    id: str
    name: str
    arguments: dict[str, Any]

class Tool(BaseModel):
    """A tool that can be used by the model."""
    name: str
    description: str
    function: Callable[..., Any] | None = None  # Make function optional
    schema: dict[str, Any]

    def to_openai_function(self) -> dict[str, Any]:
        """Convert the tool to an OpenAI function definition."""
        # Ensure schema is in strict format
        strict_schema = convert_to_strict_schema(self.schema)
        
        function_def = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": strict_schema,
                "strict": True
            }
        }
        
        logger.debug(f"(types) Created function definition for {self.name}: {json.dumps(function_def, indent=2)}")
        return function_def 