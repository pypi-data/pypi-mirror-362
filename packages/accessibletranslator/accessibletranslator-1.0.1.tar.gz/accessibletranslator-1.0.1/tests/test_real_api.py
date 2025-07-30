"""
Real API tests for AccessibleTranslator Python SDK

These tests connect to the actual API and require:
1. A valid API key set in environment variable:
   - AT_API_TEST_KEY for main branch commits
   - AT_DEV_API_TEST_KEY for non-main branch commits (development/feature branches)
2. Internet connection
3. Valid word balance in the account

These tests are marked as "real_api" and can be run with:
pytest tests/test_real_api.py -v -m real_api

Or skipped with:
pytest tests/ -v -m "not real_api"
"""

import asyncio
import os
import pytest

import accessibletranslator
from accessibletranslator.models.translation_request import TranslationRequest
from accessibletranslator.exceptions import ApiException


@pytest.fixture
def api_key():
    """Get API key from environment."""
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
            key = os.getenv("AT_API_TEST_KEY")
        else:
            # Use dev API key for all other branches
            key = os.getenv("AT_DEV_API_TEST_KEY")
            
        if not key:
            pytest.skip(f"API key not set for branch '{current_branch}' (AT_API_TEST_KEY or AT_DEV_API_TEST_KEY)")
        return key
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # Fallback: try both keys if git command fails
        key = os.getenv("AT_API_TEST_KEY") or os.getenv("AT_DEV_API_TEST_KEY")
        if not key:
            pytest.skip("AT_API_TEST_KEY or AT_DEV_API_TEST_KEY environment variable not set")
        return key


@pytest.fixture
def configuration(api_key):
    """Create SDK configuration with API key."""
    return accessibletranslator.Configuration(
        api_key={'ApiKeyAuth': api_key}
    )


@pytest.mark.real_api
@pytest.mark.asyncio
class TestRealAPI:
    """Test against the real AccessibleTranslator API."""

    async def test_health_check(self, configuration):
        """Test that the API is accessible and healthy."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            system_api = accessibletranslator.SystemApi(api_client)
            
            health = await system_api.health_check_health_get()
            
            assert health.status == "ok"
            assert health.timestamp is not None
            print(f"API Health: {health.status} at {health.timestamp}")

    async def test_get_transformations(self, configuration):
        """Test retrieving available transformations."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            translation_api = accessibletranslator.TranslationApi(api_client)
            
            transformations = await translation_api.available_transformations_api_transformations_get()
            
            assert transformations.total_transformations > 0
            assert len(transformations.transformations) > 0
            
            # Check that we have expected transformations
            transformation_names = [t.name for t in transformations.transformations]
            assert "language_simple_sentences" in transformation_names
            assert "clarity_pronouns" in transformation_names
            
            print(f"Available transformations: {transformations.total_transformations}")
            for t in transformations.transformations[:5]:  # Show first 5
                print(f"  - {t.name}: {t.description}")

    async def test_get_target_languages(self, configuration):
        """Test retrieving target languages."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            translation_api = accessibletranslator.TranslationApi(api_client)
            
            languages = await translation_api.available_target_languages_api_target_languages_get()
            
            assert languages.total_languages > 0
            assert len(languages.languages) > 0
            assert "Same as input" in languages.languages
            assert "English" in languages.languages
            
            print(f"Available languages: {languages.total_languages}")
            print(f"Languages: {languages.languages}")

    async def test_get_word_balance(self, configuration):
        """Test retrieving word balance."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            user_api = accessibletranslator.UserManagementApi(api_client)
            
            balance = await user_api.word_balance_users_word_balance_get()
            
            assert balance.word_balance >= 0
            print(f"Word balance: {balance.word_balance}")

    async def test_translate_simple_text(self, configuration):
        """Test translating simple text."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            translation_api = accessibletranslator.TranslationApi(api_client)
            
            request = TranslationRequest(
                text="The implementation of this algorithm requires substantial computational resources and exhibits significant complexity in its operational parameters.",
                transformations=["language_simple_sentences", "language_common_words"]
            )
            
            result = await translation_api.text_api_translate_post(request)
            
            assert result.translated_text is not None
            assert result.translated_text != request.text  # Should be different
            assert result.input_word_count > 0
            assert result.processing_time_ms > 0
            assert result.word_balance >= 0
            assert result.words_used > 0
            assert result.input_language is not None
            assert result.output_language is not None
            
            print(f"Original: {request.text}")
            print(f"Translated: {result.translated_text}")
            print(f"Words used: {result.words_used}")
            print(f"Processing time: {result.processing_time_ms}ms")
            print(f"Remaining balance: {result.word_balance}")

    async def test_translate_with_target_language(self, configuration):
        """Test translating with target language."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            translation_api = accessibletranslator.TranslationApi(api_client)
            
            request = TranslationRequest(
                text="Complex medical terminology requires careful explanation.",
                transformations=["language_simple_sentences"],
                target_language="Spanish"
            )
            
            result = await translation_api.text_api_translate_post(request)
            
            assert result.translated_text is not None
            assert result.output_language == "Spanish"
            assert result.input_word_count > 0
            assert result.words_used > 0
            
            print(f"Original (English): {request.text}")
            print(f"Translated (Spanish): {result.translated_text}")
            print(f"Output language: {result.output_language}")

    async def test_translate_autism_friendly(self, configuration):
        """Test autism-friendly transformations."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            translation_api = accessibletranslator.TranslationApi(api_client)
            
            request = TranslationRequest(
                text="It's raining cats and dogs outside, so we should probably stay indoors and wait for it to pass.",
                transformations=[
                    "language_literal",        # Avoid metaphors and idioms
                    "language_direct",         # Use direct language
                    "clarity_pronouns",        # Replace pronouns with specific nouns
                ]
            )
            
            result = await translation_api.text_api_translate_post(request)
            
            assert result.translated_text is not None
            assert "cats and dogs" not in result.translated_text  # Should remove idiom
            
            print(f"Original: {request.text}")
            print(f"Autism-friendly: {result.translated_text}")

    async def test_translate_intellectual_disability_friendly(self, configuration):
        """Test intellectual disability-friendly transformations."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            translation_api = accessibletranslator.TranslationApi(api_client)
            
            request = TranslationRequest(
                text="The pharmaceutical intervention demonstrated efficacy in ameliorating the patient's symptomatology through targeted molecular mechanisms.",
                transformations=[
                    "language_simple_sentences",     # Use simple sentence structure
                    "language_common_words",         # Use everyday vocabulary
                    "clarity_concrete_examples",     # Add concrete examples
                ]
            )
            
            result = await translation_api.text_api_translate_post(request)
            
            assert result.translated_text is not None
            assert len(result.translated_text) > 0
            
            print(f"Original: {request.text}")
            print(f"ID-friendly: {result.translated_text}")

    async def test_translate_with_explanations(self, configuration):
        """Test translation with explanations."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            translation_api = accessibletranslator.TranslationApi(api_client)
            
            request = TranslationRequest(
                text="The algorithm's computational complexity exhibits exponential growth patterns.",
                transformations=["language_simple_sentences", "explain_changes"]
            )
            
            result = await translation_api.text_api_translate_post(request)
            
            assert result.translated_text is not None
            assert result.explanations is not None  # Should have explanations
            assert len(result.explanations) > 0
            
            print(f"Original: {request.text}")
            print(f"Translated: {result.translated_text}")
            print(f"Explanations: {result.explanations}")

    async def test_multiple_transformations(self, configuration):
        """Test translation with multiple transformations."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            translation_api = accessibletranslator.TranslationApi(api_client)
            
            request = TranslationRequest(
                text="The CEO's strategic initiative to leverage synergistic opportunities will revolutionize our paradigm.",
                transformations=[
                    "language_simple_sentences",
                    "language_common_words",
                    "language_direct",
                    "clarity_pronouns",
                    "clarity_concrete_examples"
                ]
            )
            
            result = await translation_api.text_api_translate_post(request)
            
            assert result.translated_text is not None
            assert result.words_used > 0
            
            print(f"Original: {request.text}")
            print(f"Multi-transform: {result.translated_text}")
            print(f"Transformations applied: {len(request.transformations)}")

    async def test_error_handling_invalid_transformation(self, configuration):
        """Test error handling for invalid transformations."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            translation_api = accessibletranslator.TranslationApi(api_client)
            
            request = TranslationRequest(
                text="Test text",
                transformations=["invalid_transformation_name"]
            )
            
            with pytest.raises(ApiException) as exc_info:
                await translation_api.text_api_translate_post(request)
            
            assert exc_info.value.status in [400, 422]  # Bad request or validation error
            print(f"Expected error caught: {exc_info.value.status} - {exc_info.value.reason}")

    async def test_error_handling_empty_text(self, configuration):
        """Test error handling for empty text."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            translation_api = accessibletranslator.TranslationApi(api_client)
            
            request = TranslationRequest(
                text="",
                transformations=["language_simple_sentences"]
            )
            
            with pytest.raises(ApiException) as exc_info:
                await translation_api.text_api_translate_post(request)
            
            assert exc_info.value.status == 422  # Validation error
            print(f"Expected validation error caught: {exc_info.value.status}")

    async def test_error_handling_empty_transformations(self, configuration):
        """Test error handling for empty transformations."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            translation_api = accessibletranslator.TranslationApi(api_client)
            
            request = TranslationRequest(
                text="Test text",
                transformations=[]
            )
            
            with pytest.raises(ApiException) as exc_info:
                await translation_api.text_api_translate_post(request)
            
            assert exc_info.value.status == 422  # Validation error
            print(f"Expected validation error caught: {exc_info.value.status}")

    async def test_performance_small_text(self, configuration):
        """Test performance with small text."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            translation_api = accessibletranslator.TranslationApi(api_client)
            
            request = TranslationRequest(
                text="Hello world",
                transformations=["language_simple_sentences"]
            )
            
            result = await translation_api.text_api_translate_post(request)
            
            assert result.processing_time_ms < 30000  # Should be under 30 seconds
            assert result.input_word_count == 2
            assert result.words_used == 2
            
            print(f"Small text processing time: {result.processing_time_ms}ms")

    async def test_performance_medium_text(self, configuration):
        """Test performance with medium text."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            translation_api = accessibletranslator.TranslationApi(api_client)
            
            # Create a medium-length text
            medium_text = " ".join([
                "The implementation of machine learning algorithms requires careful consideration of various factors.",
                "Data preprocessing steps include normalization, feature selection, and dimensionality reduction.",
                "Model training involves iterative optimization using gradient descent or similar techniques.",
                "Evaluation metrics such as accuracy, precision, and recall help assess model performance.",
                "Deployment strategies must account for scalability, maintainability, and real-time requirements."
            ])
            
            request = TranslationRequest(
                text=medium_text,
                transformations=["language_simple_sentences", "language_common_words"]
            )
            
            result = await translation_api.text_api_translate_post(request)
            
            assert result.processing_time_ms < 60000  # Should be under 60 seconds
            assert result.input_word_count > 20
            
            print(f"Medium text ({result.input_word_count} words) processing time: {result.processing_time_ms}ms")

    async def test_concurrent_requests(self, configuration):
        """Test handling of concurrent requests."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            translation_api = accessibletranslator.TranslationApi(api_client)
            
            # Create multiple concurrent requests
            requests = [
                TranslationRequest(
                    text=f"Test text number {i} with different content to translate.",
                    transformations=["language_simple_sentences"]
                )
                for i in range(3)  # Start with 3 concurrent requests
            ]
            
            # Send all requests concurrently
            tasks = [
                translation_api.text_api_translate_post(req)
                for req in requests
            ]
            
            results = await asyncio.gather(*tasks)
            
            # Verify all requests completed successfully
            assert len(results) == 3
            for i, result in enumerate(results):
                assert result.translated_text is not None
                assert result.words_used > 0
                print(f"Concurrent request {i+1}: {result.processing_time_ms}ms")


@pytest.mark.real_api_slow
@pytest.mark.asyncio
class TestRealAPISlowTests:
    """Slow real API tests that take more time."""

    async def test_performance_large_text(self, configuration):
        """Test performance with large text."""
        async with accessibletranslator.ApiClient(configuration) as api_client:
            translation_api = accessibletranslator.TranslationApi(api_client)
            
            # Create a large text (but not too large to avoid hitting limits)
            large_text = " ".join([
                "The comprehensive implementation of advanced machine learning algorithms in contemporary software development environments requires meticulous consideration of numerous interdependent factors and variables.",
                "Data preprocessing methodologies encompass sophisticated normalization techniques, strategic feature selection processes, and complex dimensionality reduction algorithms that collectively optimize model performance.",
                "Training procedures involve iterative optimization mechanisms utilizing gradient descent algorithms or analogous mathematical techniques that systematically minimize loss functions.",
                "Evaluation frameworks incorporate multiple metrics including accuracy measurements, precision calculations, recall assessments, and F1-score determinations to comprehensively evaluate model effectiveness.",
                "Deployment architectures must accommodate scalability requirements, maintainability considerations, performance optimization needs, and real-time processing constraints in production environments."
            ] * 2)  # Double the text
            
            request = TranslationRequest(
                text=large_text,
                transformations=["language_simple_sentences", "language_common_words", "clarity_concrete_examples"]
            )
            
            result = await translation_api.text_api_translate_post(request)
            
            assert result.processing_time_ms < 120000  # Should be under 2 minutes
            assert result.input_word_count > 50
            
            print(f"Large text ({result.input_word_count} words) processing time: {result.processing_time_ms}ms")
            print(f"Words per second: {result.input_word_count / (result.processing_time_ms / 1000):.2f}")


if __name__ == "__main__":
    # Run only the real API tests
    pytest.main([__file__, "-v", "-m", "real_api"])