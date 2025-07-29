from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List
from langchain_core.messages import HumanMessage, SystemMessage

from langchain_core.output_parsers import JsonOutputParser
from json_repair import repair_json



from donut_ai_evaluate._agent._prompts.digitize_prompts import DigitizationMissingSectionsPrompts, \
                                                                DigitizeMissingSectionsCheckboxesPrompts, \
                                                                DigitizeMissingSectionTextPrompts

from donut_ai_evaluate._agent._schemas.digitize_schemas import PageMissingText, PageSectionChecboxes, PageSectionStatus

import json
import asyncio
import threading


# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

async def find_missing_sections(encoded_image, formatted_page_information):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    content = []

    content.append({
        "type": "text",
        "text": DigitizationMissingSectionsPrompts.HUMAN.format(digitized_document = json.dumps(formatted_page_information, indent=4)),
    })

    content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
            }
        )
    
    output_parser = JsonOutputParser(pydantic_object=PageSectionStatus)
    format_instructions = output_parser.get_format_instructions()

    content.append({
        "type": "text",
        "text": f"The format instructions for the output are given below:\n{format_instructions}",
    }, )

    system_content = [
        {
            "type": "text",
            "text": DigitizationMissingSectionsPrompts.SYSTEM,
        }
    ]

    sys_message = SystemMessage(
        content=system_content,
    )
    h_message = HumanMessage(
        content=content
    )

    result = await llm.ainvoke([sys_message, h_message])
    clean_content = repair_json(result.content)
    response = PageSectionStatus.model_validate_json(clean_content)

    return response




async def find_missing_checkboxes_sections(encoded_image, formatted_page_information):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    content = []

    content.append({
        "type": "text",
        "text": DigitizeMissingSectionsCheckboxesPrompts.HUMAN.format(digitized_document = json.dumps(formatted_page_information, indent=4)),
    })

    content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
            }
        )
    
    output_parser = JsonOutputParser(pydantic_object=PageSectionChecboxes)
    format_instructions = output_parser.get_format_instructions()
    
    content.append({
        "type": "text",
        "text": f"The format instructions for the output are given below:\n{format_instructions}",
    }, )

    system_content = [
        {
            "type": "text",
            "text": DigitizeMissingSectionsCheckboxesPrompts.SYSTEM,
        }
    ]

    sys_message = SystemMessage(
        content=system_content,
    )
    h_message = HumanMessage(
        content=content
    )

    result = await llm.ainvoke([sys_message, h_message])
    clean_content = repair_json(result.content)
    response = PageSectionChecboxes.model_validate_json(clean_content)

    return response


async def find_missing_section_text(encoded_image, formatted_page_information):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    content = []

    content.append({
        "type": "text",
        "text": DigitizeMissingSectionTextPrompts.HUMAN.format(digitized_document = json.dumps(formatted_page_information, indent=4)),
    })

    content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
            }
        )
    
    output_parser = JsonOutputParser(pydantic_object=PageMissingText)
    format_instructions = output_parser.get_format_instructions()
    
    content.append({
        "type": "text",
        "text": f"The format instructions for the output are given below:\n{format_instructions}",
    }, )

    system_content = [
        {
            "type": "text",
            "text": DigitizeMissingSectionTextPrompts.SYSTEM,
        }
    ]

    sys_message = SystemMessage(
        content=system_content,
    )
    h_message = HumanMessage(
        content=content
    )

    result = await llm.ainvoke([sys_message, h_message])    
    clean_content = repair_json(result.content)
    response = PageMissingText.model_validate_json(clean_content)


    return response