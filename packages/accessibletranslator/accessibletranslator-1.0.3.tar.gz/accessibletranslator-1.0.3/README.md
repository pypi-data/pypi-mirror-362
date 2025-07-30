# AccessibleTranslator Python SDK

Official Python SDK for AccessibleTranslator API - automated cognitive accessibility

Transform complex text into accessible content for users with autism, intellectual disabilities, limited vocabulary, and other cognitive accessibility needs.

## Features

- **Async/Sync Support**: Built with asyncio for optimal performance
- **Type Safety**: Full type hints with Pydantic models
- **Comprehensive Error Handling**: Detailed error messages and retry logic
- **API Key Authentication**: Secure API key-based authentication
- **Complete API Coverage**: All endpoints including text translation, transformations, and word balance

## Installation

```bash
pip install accessibletranslator
```

## Quick Start

```python
import asyncio
import accessibletranslator
from accessibletranslator.models.translation_request import TranslationRequest

async def main():
    # Configure the client with your API key
    configuration = accessibletranslator.Configuration(
        api_key={'ApiKeyAuth': 'sk_your_api_key_here'}
    )
    
    async with accessibletranslator.ApiClient(configuration) as api_client:
        # Create API instances
        translation_api = accessibletranslator.TranslationApi(api_client)
        
        # Transform text for better accessibility
        request = TranslationRequest(
            text="The implementation of this algorithm requires substantial computational resources and exhibits significant complexity in its operational parameters.",
            transformations=[
                "language_simple_sentences",
                "language_common_words",
                "clarity_concrete_examples"
            ]
        )
        
        # Get the accessible version
        result = await translation_api.text_api_translate_post(request)
        
        print(f"Original: {request.text}")
        print(f"Accessible: {result.translated_text}")
        print(f"Word balance: {result.word_balance}")
        print(f"Processing time: {result.processing_time_ms}ms")

# Run the example
asyncio.run(main())
```

## Authentication

Get your API key from [AccessibleTranslator](https://www.accessibletranslator.com/resources/api-docs):

```python
import accessibletranslator

configuration = accessibletranslator.Configuration(
    api_key={'ApiKeyAuth': 'sk_your_api_key_here'}
)
```

## API Reference

### Text Translation

Transform text for cognitive accessibility:

```python
import asyncio
import accessibletranslator
from accessibletranslator.models.translation_request import TranslationRequest

async def translate_text():
    configuration = accessibletranslator.Configuration(
        api_key={'ApiKeyAuth': 'sk_your_api_key_here'}
    )
    
    async with accessibletranslator.ApiClient(configuration) as api_client:
        translation_api = accessibletranslator.TranslationApi(api_client)
        
        request = TranslationRequest(
            text="Your complex text here",
            transformations=[
                "language_simple_sentences",
                "language_common_words",
                "clarity_pronouns"
            ],
            target_language="Same as input"  # or "English", "Spanish", etc.
        )
        
        result = await translation_api.text_api_translate_post(request)
        return result

asyncio.run(translate_text())
```

### Available Transformations

Get list of available transformations:

```python
async def get_transformations():
    configuration = accessibletranslator.Configuration(
        api_key={'ApiKeyAuth': 'sk_your_api_key_here'}
    )
    
    async with accessibletranslator.ApiClient(configuration) as api_client:
        translation_api = accessibletranslator.TranslationApi(api_client)
        
        transformations = await translation_api.available_transformations_api_transformations_get()
        
        print(f"Available transformations: {transformations.total_transformations}")
        for transform in transformations.transformations:
            print(f"- {transform.name}: {transform.description}")
        
        return transformations

asyncio.run(get_transformations())
```

### Target Languages

Get supported target languages:

```python
async def get_languages():
    configuration = accessibletranslator.Configuration(
        api_key={'ApiKeyAuth': 'sk_your_api_key_here'}
    )
    
    async with accessibletranslator.ApiClient(configuration) as api_client:
        translation_api = accessibletranslator.TranslationApi(api_client)
        
        languages = await translation_api.available_target_languages_api_target_languages_get()
        
        print(f"Supported languages: {languages.total_languages}")
        for lang in languages.languages:
            print(f"- {lang}")
        
        return languages

asyncio.run(get_languages())
```

### Word Balance

Check your remaining word balance:

```python
async def check_balance():
    configuration = accessibletranslator.Configuration(
        api_key={'ApiKeyAuth': 'sk_your_api_key_here'}
    )
    
    async with accessibletranslator.ApiClient(configuration) as api_client:
        user_api = accessibletranslator.UserManagementApi(api_client)
        
        balance = await user_api.word_balance_users_word_balance_get()
        print(f"Remaining words: {balance.word_balance}")
        
        return balance

asyncio.run(check_balance())
```


## Error Handling

```python
import asyncio
import accessibletranslator
from accessibletranslator.rest import ApiException

async def handle_errors():
    configuration = accessibletranslator.Configuration(
        api_key={'ApiKeyAuth': 'sk_your_api_key_here'}
    )
    
    async with accessibletranslator.ApiClient(configuration) as api_client:
        translation_api = accessibletranslator.TranslationApi(api_client)
        
        try:
            request = TranslationRequest(
                text="Text to transform",
                transformations=["language_simple_sentences"]
            )
            
            result = await translation_api.text_api_translate_post(request)
            return result
            
        except ApiException as e:
            if e.status == 401:
                print("Invalid API key")
            elif e.status == 402:
                print("Insufficient word balance")
            elif e.status == 422:
                print("Invalid request data")
            else:
                print(f"API error: {e.status} - {e.reason}")
        except Exception as e:
            print(f"Unexpected error: {e}")

asyncio.run(handle_errors())
```

## Rate Limiting

The API includes rate limiting. The SDK can automatically handle retries when properly configured:

```python
import asyncio
import accessibletranslator
from accessibletranslator.models.translation_request import TranslationRequest
from accessibletranslator.exceptions import ApiException

async def with_retry():
    # ⚠️ IMPORTANT: Retries must be explicitly enabled
    configuration = accessibletranslator.Configuration(
        api_key={'ApiKeyAuth': 'sk_your_api_key_here'},
        api_key_prefix={'ApiKeyAuth': 'Bearer'},  # Required for authentication
        retries=3  # Enable 3 retry attempts with exponential backoff
    )
    
    async with accessibletranslator.ApiClient(configuration) as api_client:
        translation_api = accessibletranslator.TranslationApi(api_client)
        
        # Define the request
        request = TranslationRequest(
            text="Text to translate",
            transformations=["language_simple_sentences"]
        )
        
        try:
            # The SDK will automatically retry on rate limits (429) and server errors (5xx)
            # Retry timing: 100ms → 200ms → 400ms → 800ms (exponential backoff)
            result = await translation_api.text_api_translate_post(request)
            return result
        except ApiException as e:
            if e.status == 429:
                print("Rate limit exceeded. All retries exhausted. Please wait and try again.")
            elif e.status >= 500:
                print("Server error. All retries exhausted.")
            else:
                print(f"API error: {e.status} - {e.reason}")
            raise

asyncio.run(with_retry())
```

**Note:** By default, retries are **disabled**. You must set `retries=N` to enable automatic retry handling for rate limits and server errors.

## Health Check

Check API health status:

```python
async def health_check():
    configuration = accessibletranslator.Configuration()
    
    async with accessibletranslator.ApiClient(configuration) as api_client:
        system_api = accessibletranslator.SystemApi(api_client)
        
        health = await system_api.health_check_health_get()
        print(f"API Status: {health.status}")
        print(f"Timestamp: {health.timestamp}")
        
        return health

asyncio.run(health_check())
```

## Requirements

- Python 3.9+
- aiohttp
- pydantic
- typing-extensions

## Support

- **Documentation**: [AccessibleTranslator API Docs](https://www.accessibletranslator.com/resources/api-docs)
- **Issues**: For SDK-related issues, please open an issue in the repository
- **API Support**: Visit [AccessibleTranslator.com](https://www.accessibletranslator.com) for general API support

## License

This SDK is licensed under the MIT License.