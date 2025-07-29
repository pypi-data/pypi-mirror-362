# Donut AI Evaluate

Install the library using

```
pip install donut-ai-evaluate
```


Before running the evaluation, make sure that the google gemini API key is present in the environment variables.

## Data Entry Evaluation

The user can either compare a single field or multiple fields with one another. 

The following code snipped shows an example of how single field comparison works:

```
from donut_ai_evaluate.data_entry import compare_single_field

data = {
    "Name" : 
    {
        "predicted" : "John",
        "ground-truth" : "Jon"
    }
}

comparison_data = compare_single_field(data)

print(comparison_data)
```

The following code snipped shows an example of how multi field comparison works:

```
from donut_ai_evaluate.data_entry import compare_batch_fields

data = [
    {
        "Name" : 
        {
            "predicted" : "John",
            "ground-truth" : "Jon"
        }
    },
    {
        "State" : 
        {
            "predicted" : "Florida",
            "ground-truth" : "Fl"
        }
    },
    {
        "Phone Number" : 
        {
            "predicted" : "922000511",
            "ground-truth" : "92-2000-511"
        }
    }
]

comparison_data = compare_batch_fields(data)

print(comparison_data)
```

## Redact Evaluation

Field redactions can be evaluated using the following code:

```
from donut_ai_evaluate.redact import is_redacted_field_gt,is_gt_field_redacted
from donut_ai_evaluate._common.eval_logger import logger


# Example Ground Truth Bboxes as lists [x, y, w, h]
gt_boxes_raw = [
    [10, 10, 50, 20],   # GT 0
    [100, 100, 80, 30],  # GT 1
    [200, 50, 40, 40]   # GT 2
]

# Example AI Detected Bboxes as lists [x, y, w, h]
# Scenario 1: Perfect match
ai_boxes_perfect_raw = [
    [11, 11, 49, 19],   # AI 0 -> matches GT 0
    [100, 100, 80, 30], # AI 1 -> matches GT 1
    [201, 51, 39, 39],   # AI 2 -> matches GT 2
    [201, 51, 41, 123] , # AI 3 -> matches None
    [300, 41, 41, 123]  # AI 4 -> matches None
]


# Check if each GT is matched by an AI box
is_gt_field_redacted(gt_boxes_raw, ai_boxes_perfect_raw) # Should be [True, True, True]

# Check if each AI box matches a GT box
is_redacted_field_gt(ai_boxes_perfect_raw, gt_boxes_raw) # Should be [True, True, True]

```