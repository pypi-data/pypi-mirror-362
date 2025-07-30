# BasicHealthCheck

Model for basic public health check response

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** |  | 
**timestamp** | **str** |  | 

## Example

```python
from accessibletranslator.models.basic_health_check import BasicHealthCheck

# TODO update the JSON string below
json = "{}"
# create an instance of BasicHealthCheck from a JSON string
basic_health_check_instance = BasicHealthCheck.from_json(json)
# print the JSON string representation of the object
print(BasicHealthCheck.to_json())

# convert the object into a dict
basic_health_check_dict = basic_health_check_instance.to_dict()
# create an instance of BasicHealthCheck from a dict
basic_health_check_from_dict = BasicHealthCheck.from_dict(basic_health_check_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


