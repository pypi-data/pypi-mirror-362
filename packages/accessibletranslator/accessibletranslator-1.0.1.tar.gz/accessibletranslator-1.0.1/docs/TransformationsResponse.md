# TransformationsResponse

Response model for available transformations

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**transformations** | [**List[TransformationInfo]**](TransformationInfo.md) |  | 
**total_transformations** | **int** |  | 
**functions** | [**List[FunctionInfo]**](FunctionInfo.md) |  | 
**total_functions** | **int** |  | 
**usage_note** | **str** |  | 

## Example

```python
from accessibletranslator.models.transformations_response import TransformationsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TransformationsResponse from a JSON string
transformations_response_instance = TransformationsResponse.from_json(json)
# print the JSON string representation of the object
print(TransformationsResponse.to_json())

# convert the object into a dict
transformations_response_dict = transformations_response_instance.to_dict()
# create an instance of TransformationsResponse from a dict
transformations_response_from_dict = TransformationsResponse.from_dict(transformations_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


