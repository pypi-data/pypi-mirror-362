# TokenVerificationResponse

Response model for token verification

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**valid** | **bool** |  | 
**user_id** | **int** |  | 
**username** | **str** |  | 
**word_balance** | **int** |  | 

## Example

```python
from accessibletranslator.models.token_verification_response import TokenVerificationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TokenVerificationResponse from a JSON string
token_verification_response_instance = TokenVerificationResponse.from_json(json)
# print the JSON string representation of the object
print(TokenVerificationResponse.to_json())

# convert the object into a dict
token_verification_response_dict = token_verification_response_instance.to_dict()
# create an instance of TokenVerificationResponse from a dict
token_verification_response_from_dict = TokenVerificationResponse.from_dict(token_verification_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


