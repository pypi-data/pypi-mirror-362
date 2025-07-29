# Donut AI Evaluate

```
```

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