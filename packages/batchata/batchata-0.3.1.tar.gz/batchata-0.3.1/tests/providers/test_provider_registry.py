"""Tests for provider registry.

Testing:
1. Provider lookup by model name
2. Registration and discovery
3. Error handling for unknown models
"""

import pytest
from unittest.mock import patch, MagicMock

from batchata.providers import get_provider
from batchata.providers.provider_registry import providers
from batchata.exceptions import ProviderNotFoundError
from tests.mocks.mock_provider import MockProvider


class TestProviderRegistry:
    """Test provider registry functionality."""
    
    def test_provider_lookup_by_model(self):
        """Test looking up providers by model name."""
        # Create a mock provider and register it
        mock_provider = MockProvider()
        
        # Temporarily modify the registry
        original_providers = providers.copy()
        try:
            # Clear and add our mock
            providers.clear()
            providers["mock-model-basic"] = mock_provider
            providers["mock-model-advanced"] = mock_provider
            
            # Test successful lookup
            provider = get_provider("mock-model-basic")
            assert provider is mock_provider
            
            provider2 = get_provider("mock-model-advanced")
            assert provider2 is mock_provider
            
            # Same provider instance for both models
            assert provider is provider2
            
        finally:
            # Restore original registry
            providers.clear()
            providers.update(original_providers)
    
    def test_provider_not_found_error(self):
        """Test error handling for unknown models."""
        # Save original state
        original_providers = providers.copy()
        
        try:
            # Set up limited registry
            providers.clear()
            providers["known-model"] = MockProvider()
            
            # Test unknown model
            with pytest.raises(ProviderNotFoundError) as exc_info:
                get_provider("unknown-model")
            
            error_msg = str(exc_info.value)
            assert "No provider for model: unknown-model" in error_msg
            assert "Available: known-model" in error_msg
            
        finally:
            # Restore
            providers.clear()
            providers.update(original_providers)
    
    def test_registry_auto_population(self):
        """Test that providers are auto-registered on import."""
        # The registry should already contain Anthropic models
        # Check for some expected Anthropic models
        expected_models = [
            "claude-3-5-haiku-20241022",
            "claude-3-5-sonnet-20241022",
            "claude-3-opus-20240229"
        ]
        
        for model in expected_models:
            assert model in providers
            provider = providers[model]
            # Should be the same provider instance for all Anthropic models
            assert provider.__class__.__name__ == "AnthropicProvider"
        
        # Verify all registered models have the same provider instance
        anthropic_providers = [p for p in providers.values() 
                             if p.__class__.__name__ == "AnthropicProvider"]
        if anthropic_providers:
            # All should be the same instance
            first = anthropic_providers[0]
            assert all(p is first for p in anthropic_providers)