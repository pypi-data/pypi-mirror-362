from pydantic import BaseModel, Field
from typing import List


class SectionStatus(BaseModel):
    section_name: str = Field(description="The name of the section that is being evaluated")
    section_status: str = Field(description="The status that represents whether the given section is `present`, `not-digitized` or `falsely-digitized`")

class PageSectionStatus(BaseModel):
    sections: List[SectionStatus] = Field(description="A list of all the sections on the page and their section statuses", default_factory=list)





class SectionCheckboxs(BaseModel):
    section_name: str = Field(description="The name of the section that is being evaluated")
    falsely_checked: List[str] = Field(description="A list of all the checkboxes that have been falsely checked in the digitized version.")
    falsely_unchecked: List[str] = Field(description="A list of all the checkboxes that have been falsely unchecked in the digitized version.")
    reasoning: str = Field(description="Reason for making the decision.")

class PageSectionChecboxes(BaseModel):
    sections: List[SectionCheckboxs] = Field(description="A list of all the sections and their checkboxes", default_factory=list)


class SectionMissingText(BaseModel):
    section_name : str = Field(description="Name of the section the missing text belongs to")
    missing_text : List[str] = Field(description="List of missing words/phrases/sentences/paragraphs", default_factory=list)


class PageMissingText(BaseModel):
    sections: List[SectionMissingText] = Field(description="A list of all the sections and their missing text", default_factory=list)