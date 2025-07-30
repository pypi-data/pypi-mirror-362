# accessibletranslator.SystemApi

All URIs are relative to *https://api.accessibletranslator.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**health_check_health_get**](SystemApi.md#health_check_health_get) | **GET** /health | Public Health Check


# **health_check_health_get**
> BasicHealthCheck health_check_health_get()

Public Health Check

Public health check endpoint.

Returns basic service status without external dependencies.
Always returns 200 OK unless the service is completely down.

For detailed monitoring information, use the /health/detailed endpoint with proper authentication.

### Example


```python
import accessibletranslator
from accessibletranslator.models.basic_health_check import BasicHealthCheck
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
    api_instance = accessibletranslator.SystemApi(api_client)

    try:
        # Public Health Check
        api_response = await api_instance.health_check_health_get()
        print("The response of SystemApi->health_check_health_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->health_check_health_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**BasicHealthCheck**](BasicHealthCheck.md)

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

