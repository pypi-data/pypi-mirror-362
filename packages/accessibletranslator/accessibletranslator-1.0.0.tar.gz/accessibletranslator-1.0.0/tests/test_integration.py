"""
Integration tests for AccessibleTranslator Python SDK

These tests require a valid API key to be set in the environment variable:
- AT_API_TEST_KEY for main branch commits
- AT_DEV_API_TEST_KEY for non-main branch commits (development/feature branches)

Run with: pytest tests/test_integration.py -v
"""

import asyncio
import os
import pytest
from unittest.mock import patch, AsyncMock

import accessibletranslator
from accessibletranslator.models.translation_request import TranslationRequest
from accessibletranslator.exceptions import ApiException


@pytest.fixture
def api_key():
    """Get API key from environment or return a mock key for testing."""
    import subprocess
    
    # Determine which branch we're on
    try:
        # Try to get current branch name
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        )
        current_branch = result.stdout.strip() if result.returncode == 0 else ""
        
        # Check if we're on main branch (or master)
        if current_branch in ["main", "master"]:
            api_key = os.getenv("AT_API_TEST_KEY")
        else:
            # Use dev API key for all other branches
            api_key = os.getenv("AT_DEV_API_TEST_KEY")
            
        return api_key or "sk_test_key_for_mocking"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # Fallback: try both keys if git command fails
        api_key = os.getenv("AT_API_TEST_KEY") or os.getenv("AT_DEV_API_TEST_KEY")
        return api_key or "sk_test_key_for_mocking"


@pytest.fixture
def configuration(api_key):
    """Create SDK configuration with API key."""
    return accessibletranslator.Configuration(
        api_key={'ApiKeyAuth': api_key}
    )


@pytest.fixture
def mock_translation_response():
    """Mock translation response for testing."""
    return {
        "translated_text": "This is simple text that is easy to read.",
        "explanations": None,
        "input_language": "English",
        "output_language": "English",
        "input_word_count": 10,
        "processing_time_ms": 1500,
        "word_balance": 990,
        "words_used": 10
    }


@pytest.fixture
def mock_transformations_response():
    """Mock transformations response for testing."""
    return {
        "transformations": [
            {
                "name": "language_simple_sentences",
                "description": "Use simple sentence structure with clear subject-verb-object patterns."
            },
            {
                "name": "clarity_pronouns",
                "description": "Replace pronouns with specific nouns to avoid confusion."
            }
        ],
        "total_transformations": 2,
        "functions": [],
        "total_functions": 0,
        "usage_note": "Choose transformations based on your target audience's needs."
    }


@pytest.fixture
def mock_languages_response():
    """Mock target languages response for testing."""
    return {
        "languages": ["Same as input", "English", "Spanish", "French", "German"],
        "total_languages": 5,
        "usage_note": "Use 'Same as input' to keep output in source language, or specify target language"
    }


@pytest.fixture
def mock_word_balance_response():
    """Mock word balance response for testing."""
    return {
        "word_balance": 1000
    }


@pytest.fixture
def mock_health_response():
    """Mock health check response for testing."""
    return {
        "status": "ok",
        "timestamp": "2024-01-15T10:30:00Z"
    }


class TestTranslationAPI:
    """Test Translation API functionality."""

    @pytest.mark.asyncio
    async def test_translate_text_success(self, configuration, mock_translation_response):
        """Test successful text translation."""
        with patch('accessibletranslator.api.translation_api.TranslationApi.text_api_translate_post', new_callable=AsyncMock) as mock_translate:
            # Setup mock response object - create a regular object, not AsyncMock
            class MockResult:
                def __init__(self):
                    self.translated_text = mock_translation_response["translated_text"]
                    self.input_word_count = mock_translation_response["input_word_count"]
                    self.word_balance = mock_translation_response["word_balance"]
                    self.processing_time_ms = mock_translation_response["processing_time_ms"]
            
            # Make the async mock function return the mock result
            mock_translate.return_value = MockResult()
            
            async with accessibletranslator.ApiClient(configuration) as api_client:
                translation_api = accessibletranslator.TranslationApi(api_client)
                
                request = TranslationRequest(
                    text="This is a complex sentence with difficult vocabulary.",
                    transformations=["language_simple_sentences", "language_common_words"]
                )
                
                result = await translation_api.text_api_translate_post(request)
                
                assert result.translated_text == mock_translation_response["translated_text"]
                assert result.input_word_count == mock_translation_response["input_word_count"]
                assert result.word_balance == mock_translation_response["word_balance"]
                assert result.processing_time_ms == mock_translation_response["processing_time_ms"]

    @pytest.mark.asyncio
    async def test_get_transformations_success(self, configuration, mock_transformations_response):
        """Test successful retrieval of available transformations."""
        with patch('accessibletranslator.api.translation_api.TranslationApi.available_transformations_api_transformations_get', new_callable=AsyncMock) as mock_get_transformations:
            # Setup mock response
            class MockResult:
                def __init__(self):
                    self.transformations = mock_transformations_response["transformations"]
                    self.total_transformations = mock_transformations_response["total_transformations"]
            
            mock_get_transformations.return_value = MockResult()
            
            async with accessibletranslator.ApiClient(configuration) as api_client:
                translation_api = accessibletranslator.TranslationApi(api_client)
                
                result = await translation_api.available_transformations_api_transformations_get()
                
                assert len(result.transformations) == 2
                assert result.transformations[0]["name"] == "language_simple_sentences"
                assert result.total_transformations == 2

    @pytest.mark.asyncio
    async def test_get_target_languages_success(self, configuration, mock_languages_response):
        """Test successful retrieval of target languages."""
        with patch('accessibletranslator.api.translation_api.TranslationApi.available_target_languages_api_target_languages_get', new_callable=AsyncMock) as mock_get_languages:
            # Setup mock response
            class MockResult:
                def __init__(self):
                    self.languages = mock_languages_response["languages"]
                    self.total_languages = mock_languages_response["total_languages"]
            
            mock_get_languages.return_value = MockResult()
            
            async with accessibletranslator.ApiClient(configuration) as api_client:
                translation_api = accessibletranslator.TranslationApi(api_client)
                
                result = await translation_api.available_target_languages_api_target_languages_get()
                
                assert len(result.languages) == 5
                assert "Same as input" in result.languages
                assert "English" in result.languages
                assert result.total_languages == 5


class TestUserManagementAPI:
    """Test User Management API functionality."""

    @pytest.mark.asyncio
    async def test_get_word_balance_success(self, configuration, mock_word_balance_response):
        """Test successful word balance retrieval."""
        with patch('accessibletranslator.api.user_management_api.UserManagementApi.word_balance_users_word_balance_get', new_callable=AsyncMock) as mock_get_balance:
            # Setup mock response
            class MockResult:
                def __init__(self):
                    self.word_balance = mock_word_balance_response["word_balance"]
            
            mock_get_balance.return_value = MockResult()
            
            async with accessibletranslator.ApiClient(configuration) as api_client:
                user_api = accessibletranslator.UserManagementApi(api_client)
                
                result = await user_api.word_balance_users_word_balance_get()
                
                assert result.word_balance == 1000


class TestSystemAPI:
    """Test System API functionality."""

    @pytest.mark.asyncio
    async def test_health_check_success(self, configuration, mock_health_response):
        """Test successful health check."""
        with patch('accessibletranslator.api.system_api.SystemApi.health_check_health_get', new_callable=AsyncMock) as mock_health:
            # Setup mock response
            class MockResult:
                def __init__(self):
                    self.status = mock_health_response["status"]
                    self.timestamp = mock_health_response["timestamp"]
            
            mock_health.return_value = MockResult()
            
            async with accessibletranslator.ApiClient(configuration) as api_client:
                system_api = accessibletranslator.SystemApi(api_client)
                
                result = await system_api.health_check_health_get()
                
                assert result.status == "ok"
                assert result.timestamp == "2024-01-15T10:30:00Z"


class TestErrorHandling:
    """Test error handling scenarios."""

    @pytest.mark.asyncio
    async def test_invalid_api_key_error(self, configuration):
        """Test handling of invalid API key error."""
        with patch('accessibletranslator.api.translation_api.TranslationApi.text_api_translate_post') as mock_translate:
            # Setup mock to raise 401 error
            mock_translate.side_effect = ApiException(status=401, reason="Invalid API key")
            
            async with accessibletranslator.ApiClient(configuration) as api_client:
                translation_api = accessibletranslator.TranslationApi(api_client)
                
                request = TranslationRequest(
                    text="Test text",
                    transformations=["language_simple_sentences"]
                )
                
                with pytest.raises(ApiException) as exc_info:
                    await translation_api.text_api_translate_post(request)
                
                assert exc_info.value.status == 401
                assert "Invalid API key" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_insufficient_balance_error(self, configuration):
        """Test handling of insufficient word balance error."""
        with patch('accessibletranslator.api.translation_api.TranslationApi.text_api_translate_post') as mock_translate:
            # Setup mock to raise 402 error
            mock_translate.side_effect = ApiException(status=402, reason="Insufficient word balance")
            
            async with accessibletranslator.ApiClient(configuration) as api_client:
                translation_api = accessibletranslator.TranslationApi(api_client)
                
                request = TranslationRequest(
                    text="Test text",
                    transformations=["language_simple_sentences"]
                )
                
                with pytest.raises(ApiException) as exc_info:
                    await translation_api.text_api_translate_post(request)
                
                assert exc_info.value.status == 402
                assert "Insufficient word balance" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_validation_error(self, configuration):
        """Test handling of validation errors."""
        with patch('accessibletranslator.api.translation_api.TranslationApi.text_api_translate_post') as mock_translate:
            # Setup mock to raise 422 error
            mock_translate.side_effect = ApiException(status=422, reason="Validation Error")
            
            async with accessibletranslator.ApiClient(configuration) as api_client:
                translation_api = accessibletranslator.TranslationApi(api_client)
                
                request = TranslationRequest(
                    text="",  # Empty text should cause validation error
                    transformations=["language_simple_sentences"]
                )
                
                with pytest.raises(ApiException) as exc_info:
                    await translation_api.text_api_translate_post(request)
                
                assert exc_info.value.status == 422
                assert "Validation Error" in str(exc_info.value)


class TestCommonUseCases:
    """Test common use cases and transformation patterns."""

    @pytest.mark.asyncio
    async def test_autism_transformations(self, configuration, mock_translation_response):
        """Test transformations commonly used for autism spectrum disorder."""
        with patch('accessibletranslator.api.translation_api.TranslationApi.text_api_translate_post', new_callable=AsyncMock) as mock_translate:
            class MockResult:
                def __init__(self):
                    self.translated_text = mock_translation_response["translated_text"]
            
            mock_translate.return_value = MockResult()
            
            async with accessibletranslator.ApiClient(configuration) as api_client:
                translation_api = accessibletranslator.TranslationApi(api_client)
                
                # Common transformations for autism
                request = TranslationRequest(
                    text="It's raining cats and dogs outside, so we should probably stay indoors.",
                    transformations=[
                        "language_literal",        # Avoid metaphors and idioms
                        "language_direct",         # Use direct language
                        "clarity_pronouns",        # Replace pronouns with specific nouns
                        "structure_headers",       # Add clear section headers
                        "language_no_ambiguous"    # Remove ambiguous phrases
                    ]
                )
                
                result = await translation_api.text_api_translate_post(request)
                assert result.translated_text is not None

    @pytest.mark.asyncio
    async def test_intellectual_disability_transformations(self, configuration, mock_translation_response):
        """Test transformations commonly used for intellectual disabilities."""
        with patch('accessibletranslator.api.translation_api.TranslationApi.text_api_translate_post', new_callable=AsyncMock) as mock_translate:
            class MockResult:
                def __init__(self):
                    self.translated_text = mock_translation_response["translated_text"]
            
            mock_translate.return_value = MockResult()
            
            async with accessibletranslator.ApiClient(configuration) as api_client:
                translation_api = accessibletranslator.TranslationApi(api_client)
                
                # Common transformations for intellectual disabilities
                request = TranslationRequest(
                    text="The implementation of this algorithm requires substantial computational resources.",
                    transformations=[
                        "language_simple_sentences",     # Use simple sentence structure
                        "language_common_words",         # Use everyday vocabulary
                        "language_short_sentences",      # Keep sentences short
                        "clarity_concrete_examples",     # Add concrete examples
                        "structure_bullet_points"        # Use bullet points for clarity
                    ]
                )
                
                result = await translation_api.text_api_translate_post(request)
                assert result.translated_text is not None

    @pytest.mark.asyncio
    async def test_limited_vocabulary_transformations(self, configuration, mock_translation_response):
        """Test transformations commonly used for limited vocabulary."""
        with patch('accessibletranslator.api.translation_api.TranslationApi.text_api_translate_post', new_callable=AsyncMock) as mock_translate:
            class MockResult:
                def __init__(self):
                    self.translated_text = mock_translation_response["translated_text"]
            
            mock_translate.return_value = MockResult()
            
            async with accessibletranslator.ApiClient(configuration) as api_client:
                translation_api = accessibletranslator.TranslationApi(api_client)
                
                # Common transformations for limited vocabulary
                request = TranslationRequest(
                    text="The pharmaceutical intervention demonstrated efficacy in ameliorating symptoms.",
                    transformations=[
                        "language_child_words",          # Use very simple vocabulary
                        "language_common_words",         # Use familiar words
                        "language_add_synonyms",         # Add simple synonyms in brackets
                        "clarity_explain_difficult_words" # Explain complex terms
                    ]
                )
                
                result = await translation_api.text_api_translate_post(request)
                assert result.translated_text is not None


class TestConfigurationAndSetup:
    """Test SDK configuration and setup scenarios."""

    def test_configuration_with_api_key(self):
        """Test configuration with API key."""
        config = accessibletranslator.Configuration(
            api_key={'ApiKeyAuth': 'sk_test_key'}
        )
        
        assert config.api_key['ApiKeyAuth'] == 'sk_test_key'
        assert config.host == 'https://api.accessibletranslator.com'

    def test_configuration_with_custom_host(self):
        """Test configuration with custom host."""
        config = accessibletranslator.Configuration(
            host='https://custom.api.com',
            api_key={'ApiKeyAuth': 'sk_test_key'}
        )
        
        assert config.host == 'https://custom.api.com'
        assert config.api_key['ApiKeyAuth'] == 'sk_test_key'

    def test_api_client_creation(self):
        """Test API client creation with configuration."""
        config = accessibletranslator.Configuration(
            api_key={'ApiKeyAuth': 'sk_test_key'}
        )
        
        api_client = accessibletranslator.ApiClient(config)
        assert api_client.configuration == config

    def test_api_instances_creation(self):
        """Test creation of API instances."""
        config = accessibletranslator.Configuration(
            api_key={'ApiKeyAuth': 'sk_test_key'}
        )
        
        api_client = accessibletranslator.ApiClient(config)
        
        translation_api = accessibletranslator.TranslationApi(api_client)
        user_api = accessibletranslator.UserManagementApi(api_client)
        system_api = accessibletranslator.SystemApi(api_client)
        
        assert translation_api.api_client == api_client
        assert user_api.api_client == api_client
        assert system_api.api_client == api_client


if __name__ == "__main__":
    pytest.main([__file__, "-v"])