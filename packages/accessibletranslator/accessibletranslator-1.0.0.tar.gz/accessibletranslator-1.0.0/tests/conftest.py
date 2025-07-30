"""
Pytest configuration and fixtures for AccessibleTranslator SDK tests.
"""

import os
import pytest
from unittest.mock import AsyncMock, MagicMock

import accessibletranslator
from accessibletranslator.models.translation_request import TranslationRequest
from accessibletranslator.models.translation_response import TranslationResponse
from accessibletranslator.models.transformations_response import TransformationsResponse
from accessibletranslator.models.transformation_info import TransformationInfo
from accessibletranslator.models.function_info import FunctionInfo
from accessibletranslator.models.target_languages_response import TargetLanguagesResponse
from accessibletranslator.models.word_balance_response import WordBalanceResponse
from accessibletranslator.models.basic_health_check import BasicHealthCheck


@pytest.fixture
def mock_api_key():
    """Mock API key for testing."""
    return "sk_test_mock_key_12345"


@pytest.fixture
def mock_configuration(mock_api_key):
    """Mock configuration for testing."""
    return accessibletranslator.Configuration(
        api_key={'ApiKeyAuth': mock_api_key}
    )


@pytest.fixture
def real_api_key():
    """Real API key from environment variables."""
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
def real_configuration(real_api_key):
    """Real configuration for integration tests."""
    return accessibletranslator.Configuration(
        api_key={'ApiKeyAuth': real_api_key}
    )


@pytest.fixture
def sample_text():
    """Sample text for testing."""
    return "The implementation of this algorithm requires substantial computational resources and exhibits significant complexity in its operational parameters."


@pytest.fixture
def simple_text():
    """Simple text for testing."""
    return "Hello world"


@pytest.fixture
def complex_text():
    """Complex text for testing."""
    return "The pharmaceutical intervention demonstrated efficacy in ameliorating the patient's symptomatology through targeted molecular mechanisms that inhibit specific enzymatic pathways."


@pytest.fixture
def autism_transformations():
    """Common transformations for autism spectrum disorder."""
    return [
        "language_literal",        # Avoid metaphors and idioms
        "language_direct",         # Use direct language
        "clarity_pronouns",        # Replace pronouns with specific nouns
        "structure_headers",       # Add clear section headers
        "language_no_ambiguous"    # Remove ambiguous phrases
    ]


@pytest.fixture
def intellectual_disability_transformations():
    """Common transformations for intellectual disabilities."""
    return [
        "language_simple_sentences",     # Use simple sentence structure
        "language_common_words",         # Use everyday vocabulary
        "language_short_sentences",      # Keep sentences short
        "clarity_concrete_examples",     # Add concrete examples
        "structure_bullet_points"        # Use bullet points for clarity
    ]


@pytest.fixture
def limited_vocabulary_transformations():
    """Common transformations for limited vocabulary."""
    return [
        "language_child_words",          # Use very simple vocabulary
        "language_common_words",         # Use familiar words
        "language_add_synonyms",         # Add simple synonyms in brackets
        "clarity_explain_difficult_words" # Explain complex terms
    ]


@pytest.fixture
def sample_translation_request(sample_text):
    """Sample translation request."""
    return TranslationRequest(
        text=sample_text,
        transformations=["language_simple_sentences", "language_common_words"],
        target_language="Same as input"
    )


@pytest.fixture
def sample_translation_response():
    """Sample translation response."""
    return TranslationResponse(
        translated_text="The computer program needs a lot of computer power and is very hard to understand.",
        explanations=None,
        input_language="English",
        output_language="English",
        input_word_count=15,
        processing_time_ms=2500,
        word_balance=985,
        words_used=15
    )


@pytest.fixture
def sample_transformations_response():
    """Sample transformations response."""
    return TransformationsResponse(
        transformations=[
            TransformationInfo(
                name="language_simple_sentences",
                description="Use simple sentence structure with clear subject-verb-object patterns."
            ),
            TransformationInfo(
                name="language_common_words",
                description="Replace complex words with common, everyday alternatives."
            ),
            TransformationInfo(
                name="clarity_pronouns",
                description="Replace pronouns with specific nouns to avoid confusion."
            )
        ],
        total_transformations=3,
        functions=[
            FunctionInfo(
                name="explain_changes",
                description="Provide detailed explanations for changes made to the text."
            )
        ],
        total_functions=1,
        usage_note="Choose transformations based on your target audience's cognitive needs."
    )


@pytest.fixture
def sample_languages_response():
    """Sample target languages response."""
    return TargetLanguagesResponse(
        languages=["Same as input", "English", "Spanish", "French", "German", "Italian", "Dutch", "Portuguese"],
        total_languages=8,
        usage_note="Use 'Same as input' to keep output in source language, or specify target language"
    )


@pytest.fixture
def sample_word_balance_response():
    """Sample word balance response."""
    return WordBalanceResponse(word_balance=1000)


@pytest.fixture
def sample_health_response():
    """Sample health check response."""
    return BasicHealthCheck(
        status="ok",
        timestamp="2024-01-15T10:30:00Z"
    )


@pytest.fixture
def mock_api_client():
    """Mock API client for testing."""
    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    return mock_client


@pytest.fixture
def mock_translation_api(mock_api_client):
    """Mock translation API for testing."""
    mock_api = MagicMock()
    mock_api.api_client = mock_api_client
    return mock_api


@pytest.fixture
def mock_user_api(mock_api_client):
    """Mock user management API for testing."""
    mock_api = MagicMock()
    mock_api.api_client = mock_api_client
    return mock_api


@pytest.fixture
def mock_system_api(mock_api_client):
    """Mock system API for testing."""
    mock_api = MagicMock()
    mock_api.api_client = mock_api_client
    return mock_api


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Add custom markers
    config.addinivalue_line(
        "markers", "real_api: marks tests as real API tests (requires API key and internet)"
    )
    config.addinivalue_line(
        "markers", "real_api_slow: marks tests as slow real API tests (may take minutes)"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "models: marks tests as model tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add unit marker to model tests
        if "test_models" in item.nodeid:
            item.add_marker(pytest.mark.unit)
            item.add_marker(pytest.mark.models)
        
        # Add integration marker to integration tests
        if "test_integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        
        # Add real_api marker to real API tests
        if "test_real_api" in item.nodeid:
            item.add_marker(pytest.mark.real_api)
            
            # Add slow marker to slow tests
            if "slow" in item.name or "large" in item.name or "concurrent" in item.name:
                item.add_marker(pytest.mark.real_api_slow)


def pytest_runtest_setup(item):
    """Setup function called before each test."""
    # Skip real API tests if no API key is provided
    if "real_api" in [mark.name for mark in item.iter_markers()]:
        import subprocess
        
        # Determine which branch we're on and check for appropriate API key
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                timeout=5
            )
            current_branch = result.stdout.strip() if result.returncode == 0 else ""
            
            # Check if we're on main branch (or master)
            if current_branch in ["main", "master"]:
                if not os.getenv("AT_API_TEST_KEY"):
                    pytest.skip(f"AT_API_TEST_KEY not set for main branch")
            else:
                if not os.getenv("AT_DEV_API_TEST_KEY"):
                    pytest.skip(f"AT_DEV_API_TEST_KEY not set for branch '{current_branch}'")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # Fallback: check for any API key
            if not (os.getenv("AT_API_TEST_KEY") or os.getenv("AT_DEV_API_TEST_KEY")):
                pytest.skip("AT_API_TEST_KEY or AT_DEV_API_TEST_KEY environment variable not set")


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Helper functions for tests
def assert_translation_response_valid(response):
    """Assert that a translation response is valid."""
    assert response.translated_text is not None
    assert len(response.translated_text) > 0
    assert response.input_language is not None
    assert response.output_language is not None
    assert response.input_word_count > 0
    assert response.processing_time_ms > 0
    assert response.word_balance >= 0
    assert response.words_used > 0


def assert_transformations_response_valid(response):
    """Assert that a transformations response is valid."""
    assert response.transformations is not None
    assert response.total_transformations >= 0
    assert response.total_transformations == len(response.transformations)
    assert response.functions is not None
    assert response.total_functions >= 0
    assert response.total_functions == len(response.functions)
    assert response.usage_note is not None


def assert_languages_response_valid(response):
    """Assert that a languages response is valid."""
    assert response.languages is not None
    assert response.total_languages >= 0
    assert response.total_languages == len(response.languages)
    assert response.usage_note is not None
    assert "Same as input" in response.languages


def assert_word_balance_response_valid(response):
    """Assert that a word balance response is valid."""
    assert response.word_balance is not None
    assert response.word_balance >= 0


def assert_health_response_valid(response):
    """Assert that a health response is valid."""
    assert response.status is not None
    assert response.timestamp is not None
    assert response.status in ["ok", "degraded", "unhealthy"]