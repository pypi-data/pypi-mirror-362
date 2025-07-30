# TranslationRequest

Request model for text translation API  This model defines the structure for text translation requests sent to the /api/translate endpoint.  Attributes:     text: The original text to be translated (required)     transformations: List of transformation names to apply (required)         Available transformations include language, clarity, structure, tone, and content modifications.  Example:     {         \"text\": \"Complex text to translate\",         \"transformations\": [\"language_literal\", \"clarity_pronouns\", \"structure_headers\"],         \"target_language\": \"Spanish\"     }

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** |  | 
**transformations** | **List[str]** |  | 
**input_type** | **str** |  | [optional] 
**target_language** | **str** |  | [optional] 

## Example

```python
from accessibletranslator.models.translation_request import TranslationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TranslationRequest from a JSON string
translation_request_instance = TranslationRequest.from_json(json)
# print the JSON string representation of the object
print(TranslationRequest.to_json())

# convert the object into a dict
translation_request_dict = translation_request_instance.to_dict()
# create an instance of TranslationRequest from a dict
translation_request_from_dict = TranslationRequest.from_dict(translation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


