# TranslationResponse

Response model for text translation API

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**translated_text** | **str** |  | 
**explanations** | **str** |  | [optional] 
**input_language** | **str** |  | 
**output_language** | **str** |  | 
**input_word_count** | **int** |  | 
**processing_time_ms** | **int** |  | 
**word_balance** | **int** |  | 
**words_used** | **int** |  | 

## Example

```python
from accessibletranslator.models.translation_response import TranslationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TranslationResponse from a JSON string
translation_response_instance = TranslationResponse.from_json(json)
# print the JSON string representation of the object
print(TranslationResponse.to_json())

# convert the object into a dict
translation_response_dict = translation_response_instance.to_dict()
# create an instance of TranslationResponse from a dict
translation_response_from_dict = TranslationResponse.from_dict(translation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


