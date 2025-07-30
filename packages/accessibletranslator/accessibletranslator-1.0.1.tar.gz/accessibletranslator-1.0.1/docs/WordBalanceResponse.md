# WordBalanceResponse

Response model for user word balance

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**word_balance** | **int** |  | 

## Example

```python
from accessibletranslator.models.word_balance_response import WordBalanceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of WordBalanceResponse from a JSON string
word_balance_response_instance = WordBalanceResponse.from_json(json)
# print the JSON string representation of the object
print(WordBalanceResponse.to_json())

# convert the object into a dict
word_balance_response_dict = word_balance_response_instance.to_dict()
# create an instance of WordBalanceResponse from a dict
word_balance_response_from_dict = WordBalanceResponse.from_dict(word_balance_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


