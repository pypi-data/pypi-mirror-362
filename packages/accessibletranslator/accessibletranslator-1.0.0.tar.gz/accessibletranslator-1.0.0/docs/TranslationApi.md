# accessibletranslator.TranslationApi

All URIs are relative to *https://api.accessibletranslator.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**available_target_languages_api_target_languages_get**](TranslationApi.md#available_target_languages_api_target_languages_get) | **GET** /api/target-languages | Get Available Target Languages
[**available_transformations_api_transformations_get**](TranslationApi.md#available_transformations_api_transformations_get) | **GET** /api/transformations | Get Available Transformations
[**text_api_translate_post**](TranslationApi.md#text_api_translate_post) | **POST** /api/translate | Translate Text


# **available_target_languages_api_target_languages_get**
> TargetLanguagesResponse available_target_languages_api_target_languages_get()

Get Available Target Languages

Get a list of all supported target languages for translation

Returns a comprehensive list of all supported target languages that can be used
with the /api/translate endpoint for translating simplified output to different languages.

Returns:
    Dictionary with languages list and metadata
    
Example response:
    {
        "languages": ["Same as input", "English", "French", "German", "Spanish", ...],
        "total_languages": 10,
        "usage_note": "Use 'Same as input' to keep output in source language, or specify target language"
    }

### Example


```python
import accessibletranslator
from accessibletranslator.models.target_languages_response import TargetLanguagesResponse
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
    api_instance = accessibletranslator.TranslationApi(api_client)

    try:
        # Get Available Target Languages
        api_response = await api_instance.available_target_languages_api_target_languages_get()
        print("The response of TranslationApi->available_target_languages_api_target_languages_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TranslationApi->available_target_languages_api_target_languages_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**TargetLanguagesResponse**](TargetLanguagesResponse.md)

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

# **available_transformations_api_transformations_get**
> TransformationsResponse available_transformations_api_transformations_get()

Get Available Transformations

Get a list of all available text transformations

Returns a comprehensive list of all transformation options that can be used
with the /api/translate endpoint, including their documentation strings.

Returns:
    Dictionary with transformations list and metadata
    
Example response:
    {
        "transformations": [
            {
                "name": "language_literal",
                "description": "Use literal language. Avoid metaphors, idioms, sarcasm, and figurative speech."
            },
            ...
        ],
        "total_count": 51,
        "special_transformations": ["explain_changes"]
    }

### Example


```python
import accessibletranslator
from accessibletranslator.models.transformations_response import TransformationsResponse
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
    api_instance = accessibletranslator.TranslationApi(api_client)

    try:
        # Get Available Transformations
        api_response = await api_instance.available_transformations_api_transformations_get()
        print("The response of TranslationApi->available_transformations_api_transformations_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TranslationApi->available_transformations_api_transformations_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**TransformationsResponse**](TransformationsResponse.md)

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

# **text_api_translate_post**
> TranslationResponse text_api_translate_post(translation_request)

Translate Text

Translate text according to user-selected accessibility transformations

Main API endpoint for text translation. Takes input text and transformation options,
checks the user's word balance, processes the text using AI, and records
usage statistics. The word balance is charged based on input text word count.

Authentication:
    Supports both JWT tokens (web UI) and API keys (programmatic access).
    
    API Key Usage:
    - Authorization header: "Authorization: Bearer sk_your_api_key_here"
    - X-API-Key header: "X-API-Key: sk_your_api_key_here"

Args:
    request: TranslationRequest with text and transformations
    current_user: Authenticated user from flexible authentication (JWT or API key)
    db: Database session dependency
    
Returns:
    Dictionary with comprehensive translation results:
    {
        "translated_text": "The processed text with transformations applied",
        "explanations": "Detailed explanations if requested, or null",
        "input_language": "Detected language of the input text",
        "output_language": "Target language ('Same as input' uses detected language)",
        "input_word_count": 123,
        "processing_time_ms": 15234,
        "word_balance": 877,
        "words_used": 123
    }

Example API Key Usage:
    curl -H "Authorization: Bearer sk_your_api_key_here" \
         -H "Content-Type: application/json" \
         -d '{"text": "Complex text", "transformations": ["language_simple_sentences"]}' \
         https://api.yourdomain.com/api/translate
    
Raises:
    HTTPException(402): If user has insufficient word balance
    HTTPException(500): For any other processing errors

### Example


```python
import accessibletranslator
from accessibletranslator.models.translation_request import TranslationRequest
from accessibletranslator.models.translation_response import TranslationResponse
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
    api_instance = accessibletranslator.TranslationApi(api_client)
    translation_request = accessibletranslator.TranslationRequest() # TranslationRequest | 

    try:
        # Translate Text
        api_response = await api_instance.text_api_translate_post(translation_request)
        print("The response of TranslationApi->text_api_translate_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TranslationApi->text_api_translate_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **translation_request** | [**TranslationRequest**](TranslationRequest.md)|  | 

### Return type

[**TranslationResponse**](TranslationResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

