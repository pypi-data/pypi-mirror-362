# TargetLanguagesResponse

Response model for available target languages

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**languages** | **List[str]** |  | 
**total_languages** | **int** |  | 
**usage_note** | **str** |  | 

## Example

```python
from accessibletranslator.models.target_languages_response import TargetLanguagesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TargetLanguagesResponse from a JSON string
target_languages_response_instance = TargetLanguagesResponse.from_json(json)
# print the JSON string representation of the object
print(TargetLanguagesResponse.to_json())

# convert the object into a dict
target_languages_response_dict = target_languages_response_instance.to_dict()
# create an instance of TargetLanguagesResponse from a dict
target_languages_response_from_dict = TargetLanguagesResponse.from_dict(target_languages_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


