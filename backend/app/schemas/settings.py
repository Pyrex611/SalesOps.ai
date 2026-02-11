from pydantic import BaseModel, Field


class TemplatesOut(BaseModel):
    crm_field_mapping: dict[str, str] = Field(default_factory=dict)
    call_analysis_template: dict = Field(default_factory=dict)


class TemplatesUpdate(BaseModel):
    crm_field_mapping: dict[str, str] = Field(default_factory=dict)
    call_analysis_template: dict = Field(default_factory=dict)
