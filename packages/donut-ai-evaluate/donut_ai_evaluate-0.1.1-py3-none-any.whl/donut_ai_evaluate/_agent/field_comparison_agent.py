from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List
from langchain_core.messages import HumanMessage, SystemMessage

from langchain_core.output_parsers import JsonOutputParser
from json_repair import repair_json

class FieldCorrectness(BaseModel):
    field_name: str = Field(description="The name of the field whose values are being compared")
    correctess: str = Field(description="The level of correctess for the given field. Can bse set to `Correct`, `Partial`, or `Incorrect`")
    reasoning: str = Field(description="Provide the reasoning for choosing the correctness value for the given field")

class Correctness(BaseModel):
    all_field_correctness: List[FieldCorrectness] = Field(description = "A list of all the given fields and their correcteness values.")

def determine_correctness(field_text):
    SYSTEM_PROMPT = f"""You are an expert at analyzing outputs of AI systems. You are given AI predicted values as well as human-annotated values for field data extraction task. You have to check the AI predicted values for correctness.
    Rules defining correctness are delimited by @@@@.
    Field name, ai-predicted value and human-annotated value are delimited by ~~~~.
    
    @@@@
    Correctness rules:
    1. Correct: If the AI predicted value and human-annotated value is exactly the same.
    2. Partial: If the AI predicted value and human-annotated value is similar in meaning but not exactly the same e.g. Predicted value: FL, Annotated value: Florida.
    3. Incorrect: If the AI predicted value doesn't match the human-annotated value in any way.
    @@@@
    
    ~~~~
    Fields and Values
    {field_text}
    ~~~~

    """

    # Step 2. When given different formats for predicted and AI values for dates and numbers, parse the values into a common format and then compare them together and determine correctness.
    PROMPT_TEMPLATE = """
    Your task is to determine the correctness for each given field.
    Instructions for your task are delimited by ####. You must strictly follow the instructions.
    Guidelines for your task are delimited by ****. You must strictly follow the guidelines.
    
    

    ####
    Task Instructions:
    Step 1. For the given fields and their predicted and annotated values, determine the correctness of each field. Strictly adhere to the guidelines.
    ####
    
    ****
    Guidelines:
    1. Also take the field being compared into the account and determine the correctness of the field with the context of the field name.
    2. Ignore formatting differences as long as the information is the same.
    3. For dates and numbers ensure that the predicted and ground truth values have exactly the same information, ignore the formatting.
    4. Dates cannot match partially, they must match exactly, otherwise, they are incorrect. 
    ****
    
    
    Please follow all given task instructions and strictly adhere to all the given instructions.
    You must respond in JSON format only.
        """

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    output_parser = JsonOutputParser(pydantic_object=Correctness)
    format_instructions = output_parser.get_format_instructions()

    content = []
    
    content.append({
        "type": "text",
        "text": PROMPT_TEMPLATE,
    })
    content.append({
        "type": "text",
        "text": format_instructions,
    }, )

    system_content = [
        {
            "type": "text",
            "text": SYSTEM_PROMPT,
        }
    ]

    sys_message = SystemMessage(
        content=system_content,
    )
    h_message = HumanMessage(
        content=content
    )

    result = llm.invoke([sys_message, h_message])
    clean_content = repair_json(result.content)
    response = Correctness.model_validate_json(clean_content)
    # for field in response.all_field_correctness:
    #     print(field)
    return response


async def determine_correctness_async(field_text):
    SYSTEM_PROMPT = f"""You are an expert at analyzing outputs of AI systems. You are given AI predicted values as well as human-annotated values for field data extraction task. You have to check the AI predicted values for correctness.
    Rules defining correctness are delimited by @@@@.
    Field name, ai-predicted value and human-annotated value are delimited by ~~~~.
    
    @@@@
    Correctness rules:
    1. Correct: If the AI predicted value and human-annotated value is exactly the same.
    2. Partial: If the AI predicted value and human-annotated value is similar in meaning but not exactly the same e.g. Predicted value: FL, Annotated value: Florida.
    3. Incorrect: If the AI predicted value doesn't match the human-annotated value in any way.
    @@@@
    
    ~~~~
    Fields and Values
    {field_text}
    ~~~~

    """

    # Step 2. When given different formats for predicted and AI values for dates and numbers, parse the values into a common format and then compare them together and determine correctness.
    PROMPT_TEMPLATE = """
    Your task is to determine the correctness for each given field.
    Instructions for your task are delimited by ####. You must strictly follow the instructions.
    Guidelines for your task are delimited by ****. You must strictly follow the guidelines.
    
    

    ####
    Task Instructions:
    Step 1. For the given fields and their predicted and annotated values, determine the correctness of each field. Strictly adhere to the guidelines.
    ####
    
    ****
    Guidelines:
    1. Also take the field being compared into the account and determine the correctness of the field with the context of the field name.
    2. Ignore formatting differences as long as the information is the same.
    3. For dates and numbers ensure that the predicted and ground truth values have exactly the same information, ignore the formatting.
    4. Dates cannot match partially, they must match exactly, otherwise, they are incorrect. 
    ****
    
    
    Please follow all given task instructions and strictly adhere to all the given instructions.
    You must respond in JSON format only.
        """

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    output_parser = JsonOutputParser(pydantic_object=Correctness)
    format_instructions = output_parser.get_format_instructions()

    content = []
    
    content.append({
        "type": "text",
        "text": PROMPT_TEMPLATE,
    })
    content.append({
        "type": "text",
        "text": format_instructions,
    }, )

    system_content = [
        {
            "type": "text",
            "text": SYSTEM_PROMPT,
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
    response = Correctness.model_validate_json(clean_content)
    # for field in response.all_field_correctness:
    #     print(field)
    return response