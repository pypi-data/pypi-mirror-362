# TransformationInfo

Model for individual transformation information

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | 

## Example

```python
from accessibletranslator.models.transformation_info import TransformationInfo

# TODO update the JSON string below
json = "{}"
# create an instance of TransformationInfo from a JSON string
transformation_info_instance = TransformationInfo.from_json(json)
# print the JSON string representation of the object
print(TransformationInfo.to_json())

# convert the object into a dict
transformation_info_dict = transformation_info_instance.to_dict()
# create an instance of TransformationInfo from a dict
transformation_info_from_dict = TransformationInfo.from_dict(transformation_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


