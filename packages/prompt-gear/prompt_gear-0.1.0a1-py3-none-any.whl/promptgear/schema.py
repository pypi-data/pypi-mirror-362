"""
Data schemas for Prompt Gear.
"""
from typing import Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict


class PromptTemplate(BaseModel):
    """
    Prompt template data model.
    """
    model_config = ConfigDict(
        json_encoders={
            # Custom encoders if needed
        },
        json_schema_extra={
            "example": {
                "name": "chatbot_greeting",
                "version": "v1",
                "system_prompt": "You are a helpful assistant that speaks politely.",
                "user_prompt": "{{user_input}}",
                "config": {
                    "temperature": 0.7,
                    "max_tokens": 512
                }
            }
        }
    )
    
    name: str = Field(..., description="Prompt name")
    version: str = Field(..., description="Prompt version")
    system_prompt: str = Field(..., description="System prompt content")
    user_prompt: str = Field(..., description="User prompt content")
    config: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Configuration parameters"
    )
    
    # Version management fields (internal use)
    sequence_number: Optional[int] = Field(None, description="Internal sequence number for version ordering")
    is_latest: bool = Field(False, description="Whether this is the latest version")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate prompt name format."""
        if not v or not v.strip():
            raise ValueError("Prompt name cannot be empty")
        # Allow alphanumeric, underscore, hyphen
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError("Prompt name can only contain letters, numbers, underscore, and hyphen")
        return v.strip()
    
    @field_validator('version')
    @classmethod
    def validate_version(cls, v):
        """Validate version format."""
        if not v or not v.strip():
            raise ValueError("Version cannot be empty")
        # More flexible version validation (allows v1, v1.0, 1.0.0, dev_v1, etc.)
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError("Version can only contain letters, numbers, underscore, and hyphen")
        return v.strip()
