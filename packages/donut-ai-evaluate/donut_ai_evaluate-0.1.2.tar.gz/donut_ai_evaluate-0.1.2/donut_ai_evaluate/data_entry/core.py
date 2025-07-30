from typing import Dict, List
from donut_ai_evaluate._agent.field_comparison_agent import determine_correctness, determine_correctness_async

def __get_field_string(fields_data: List[Dict]) -> str:
    field_string = ""
    
    field_num = 1
    for field in fields_data:
        if len(field) == 0:
            raise Exception("An empty field dictionary has been provided in the input.")
        
        for field_name in field:
            if "predicted" in field[field_name]:
                predicted_value = field[field_name]["predicted"].lower()
            else:
                raise Exception(f"Predicted value not provided for {field_name}")

            if "ground-truth" in field[field_name]:
                ground_truth_value = field[field_name]["ground-truth"].lower()
            else:
                raise Exception(f"Ground Truth value not provided for {field_name}")

            field_string += f"{field_num}. Field Name: {field_name} - AI Value: {predicted_value} | Ground Truth Value: {ground_truth_value}\n"
            field_num += 1

    return field_string

def __compare_fields(fields_data: List[Dict]):
    field_string = __get_field_string(fields_data=fields_data)
    fields_correctness = determine_correctness(field_text=field_string)
    field_correctness_dict = {}
    field_correctness_list = []

    for field_input in fields_data:
        field_name = list(field_input.keys())[0]
        found = False
        for field_with_correctness in fields_correctness.all_field_correctness:
            if field_with_correctness.field_name == field_name:
                if field_with_correctness.correctess.lower() == "correct":
                    field_correctness_dict[field_with_correctness.field_name] = 1.0
                    field_correctness_list.append(1.0)
                elif field_with_correctness.correctess.lower() == "partial":
                    field_correctness_dict[field_with_correctness.field_name] = 0.4
                    field_correctness_list.append(0.4)
                else:
                    field_correctness_dict[field_with_correctness.field_name] = 0.0
                    field_correctness_list.append(0.0)
                
                found = True
                break

        if not found:
            field_correctness_dict[field_input.field_name] = 0.0
            field_correctness_list.append(0.0)

    return field_correctness_list

def compare_single_field(fields_data: Dict):
    """
    This function compares the ground truth and predicted value of a single field and determines whether or not the two vlues are the same.
    Parameters:
    fields_data:         Contains the predicted and ground truth data for a field that must be compared with one another. Must follow the following format:
                        {
                            <Field Name> : {
                                                "ground-truth" : <ground-truth-value>,
                                                "predicted" : <predicted-value>,
                                            }
                        }
    Returns:
    A dictionary that indicates whether the predicted value for the given field is the same as the ground truth value. 
    """
    if type(fields_data) != dict:
        raise TypeError(f"The function expects input to be of type dict, but type {type(fields_data)} was provided.")

    field_correctness_list = __compare_fields([fields_data])
    
    return field_correctness_list

def compare_batch_fields(fields_data: List[Dict]):
    """
    This function compares the ground truth and predicted value multiple fields and determines whether or not the values for all the fields are the same or not.
    Parameters:
    fields_data:         Contains the predicted and ground truth data for a field that must be compared with one another. Must follow the following format:
                        [
                            {
                                <Field Name> : {
                                                    "ground-truth" : <ground-truth-value>,
                                                    "predicted" : <predicted-value>,
                                                }
                            },
                            ...,
                            ...
                        ]
    Returns:
    A dictionary that indicates whether the predicted value for the given field is the same as the ground truth value. 
    """

    if type(fields_data) != list:
        raise TypeError(f"The function expects input to be of type list, but type {type(fields_data)} was provided.")
    

    field_correctness_list = __compare_fields(fields_data)
    
    return field_correctness_list

async def __compare_fields_async(fields_data: List[Dict]):
    field_string = __get_field_string(fields_data=fields_data)
    fields_correctness = await determine_correctness_async(field_text=field_string)
    field_correctness_dict = {}
    field_correctness_list = []

    for field_input in fields_data:
        field_name = list(field_input.keys())[0]
        found = False
        for field_with_correctness in fields_correctness.all_field_correctness:
            if field_with_correctness.field_name == field_name:
                if field_with_correctness.correctess.lower() == "correct":
                    field_correctness_dict[field_with_correctness.field_name] = 1.0
                    field_correctness_list.append(1.0)
                elif field_with_correctness.correctess.lower() == "partial":
                    field_correctness_dict[field_with_correctness.field_name] = 0.4
                    field_correctness_list.append(0.4)
                else:
                    field_correctness_dict[field_with_correctness.field_name] = 0.0
                    field_correctness_list.append(0.0)
                
                found = True
                break

        if not found:
            field_correctness_dict[field_input.field_name] = 0.0
            field_correctness_list.append(0.0)

    return field_correctness_list

async def compare_batch_fields_async(fields_data: List[Dict]):
    """
    This function compares the ground truth and predicted value multiple fields and determines whether or not the values for all the fields are the same or not.
    Parameters:
    fields_data:         Contains the predicted and ground truth data for a field that must be compared with one another. Must follow the following format:
                        [
                            {
                                <Field Name> : {
                                                    "ground-truth" : <ground-truth-value>,
                                                    "predicted" : <predicted-value>,
                                                }
                            },
                            ...,
                            ...
                        ]
    Returns:
    A dictionary that indicates whether the predicted value for the given field is the same as the ground truth value. 
    """

    if type(fields_data) != list:
        raise TypeError(f"The function expects input to be of type list, but type {type(fields_data)} was provided.")
    

    field_correctness_list = await __compare_fields_async(fields_data)
    
    return field_correctness_list