# accessibletranslator.UserManagementApi

All URIs are relative to *https://api.accessibletranslator.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**word_balance_users_word_balance_get**](UserManagementApi.md#word_balance_users_word_balance_get) | **GET** /users/word-balance | Get Word Balance


# **word_balance_users_word_balance_get**
> WordBalanceResponse word_balance_users_word_balance_get()

Get Word Balance

### Example


```python
import accessibletranslator
from accessibletranslator.models.word_balance_response import WordBalanceResponse
from accessibletranslator.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.accessibletranslator.com
# See configuration.py for a list of all supported configuration parameters.
configuration = accessibletranslator.Configuration(
    host = "https://api.accessibletranslator.com"
)


# Enter a context with an instance of the API client
async with accessibletranslator.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accessibletranslator.UserManagementApi(api_client)

    try:
        # Get Word Balance
        api_response = await api_instance.word_balance_users_word_balance_get()
        print("The response of UserManagementApi->word_balance_users_word_balance_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserManagementApi->word_balance_users_word_balance_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**WordBalanceResponse**](WordBalanceResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

