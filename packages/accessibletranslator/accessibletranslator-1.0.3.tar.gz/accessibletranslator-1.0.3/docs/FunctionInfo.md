# FunctionInfo

Model for individual function information

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | 

## Example

```python
from accessibletranslator.models.function_info import FunctionInfo

# TODO update the JSON string below
json = "{}"
# create an instance of FunctionInfo from a JSON string
function_info_instance = FunctionInfo.from_json(json)
# print the JSON string representation of the object
print(FunctionInfo.to_json())

# convert the object into a dict
function_info_dict = function_info_instance.to_dict()
# create an instance of FunctionInfo from a dict
function_info_from_dict = FunctionInfo.from_dict(function_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


