"""Unit tests for the validators module."""

import pytest
import warnings
from unittest.mock import Mock

from pyvenice.validators import validate_model_capabilities, filter_unsupported_params
from pyvenice.exceptions import InvalidRequestError
from pyvenice.models import ModelCapabilities


@pytest.mark.unit
class TestValidateModelCapabilitiesDecorator:
    """Test the validate_model_capabilities decorator."""

    def test_decorator_with_valid_params(self):
        """Test decorator allows valid parameters."""
        # Mock model capabilities
        mock_capabilities = ModelCapabilities(
            optimizedForCode=True,
            quantization="fp8",
            supportsFunctionCalling=True,
            supportsReasoning=True,
            supportsResponseSchema=True,
            supportsVision=False,
            supportsWebSearch=False,
            supportsLogProbs=True,
        )

        # Mock models instance
        mock_models = Mock()
        mock_models.get_capabilities.return_value = mock_capabilities

        # Mock self object
        mock_self = Mock()
        mock_self.models = mock_models

        @validate_model_capabilities()
        def test_function(self, model, messages, **kwargs):
            return {"model": model, "messages": messages, **kwargs}

        result = test_function(
            mock_self,
            model="qwen-2.5-qwq-32b",
            messages=[{"role": "user", "content": "test"}],
            parallel_tool_calls=True,
            tools=[{"type": "function"}],
        )

        # Should pass through all parameters for supported model
        assert result["parallel_tool_calls"] is True
        assert result["tools"] == [{"type": "function"}]

    def test_decorator_removes_unsupported_params(self):
        """Test decorator removes unsupported parameters."""
        # Mock model capabilities (no function calling support)
        mock_capabilities = ModelCapabilities(
            optimizedForCode=False,
            quantization="fp16",
            supportsFunctionCalling=False,
            supportsReasoning=True,
            supportsResponseSchema=False,
            supportsVision=False,
            supportsWebSearch=True,
            supportsLogProbs=False,
        )

        # Mock models instance
        mock_models = Mock()
        mock_models.get_capabilities.return_value = mock_capabilities

        # Mock self object
        mock_self = Mock()
        mock_self.models = mock_models

        @validate_model_capabilities(warn_on_removal=False)
        def test_function(self, model, messages, **kwargs):
            return {"model": model, "messages": messages, **kwargs}

        result = test_function(
            mock_self,
            model="venice-uncensored",
            messages=[{"role": "user", "content": "test"}],
            parallel_tool_calls=True,
            tools=[{"type": "function"}],
            logprobs=True,
        )

        # Unsupported parameters should be removed
        assert "parallel_tool_calls" not in result
        assert "tools" not in result
        assert "logprobs" not in result
        # Other params should remain
        assert result["model"] == "venice-uncensored"
        assert result["messages"] == [{"role": "user", "content": "test"}]

    def test_decorator_warns_on_removal(self):
        """Test decorator warns when removing parameters."""
        # Mock model capabilities (no function calling support)
        mock_capabilities = ModelCapabilities(
            optimizedForCode=False,
            quantization="fp16",
            supportsFunctionCalling=False,
            supportsReasoning=True,
            supportsResponseSchema=False,
            supportsVision=False,
            supportsWebSearch=True,
            supportsLogProbs=False,
        )

        # Mock models instance
        mock_models = Mock()
        mock_models.get_capabilities.return_value = mock_capabilities

        # Mock self object
        mock_self = Mock()
        mock_self.models = mock_models

        @validate_model_capabilities(warn_on_removal=True)
        def test_function(self, model, messages, **kwargs):
            return {"model": model, "messages": messages, **kwargs}

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            test_function(
                mock_self,
                model="venice-uncensored",
                messages=[{"role": "user", "content": "test"}],
                parallel_tool_calls=True,
            )

            # Should have warned about parameter removal
            assert len(w) > 0
            assert "parallel_tool_calls" in str(w[0].message)
            assert "not supported" in str(w[0].message)

    def test_decorator_raises_error_when_configured(self):
        """Test decorator raises error when auto_remove_unsupported=False."""
        # Mock model capabilities (no function calling support)
        mock_capabilities = ModelCapabilities(
            optimizedForCode=False,
            quantization="fp16",
            supportsFunctionCalling=False,
            supportsReasoning=True,
            supportsResponseSchema=False,
            supportsVision=False,
            supportsWebSearch=True,
            supportsLogProbs=False,
        )

        # Mock models instance
        mock_models = Mock()
        mock_models.get_capabilities.return_value = mock_capabilities

        # Mock self object
        mock_self = Mock()
        mock_self.models = mock_models

        @validate_model_capabilities(auto_remove_unsupported=False)
        def test_function(self, model, messages, **kwargs):
            return {"model": model, "messages": messages, **kwargs}

        with pytest.raises(InvalidRequestError) as exc_info:
            test_function(
                mock_self,
                model="venice-uncensored",
                messages=[{"role": "user", "content": "test"}],
                parallel_tool_calls=True,
            )

        assert "does not support" in str(exc_info.value)
        assert "parallel_tool_calls" in str(exc_info.value)

    def test_decorator_no_model_specified(self):
        """Test decorator handles case where no model is specified."""
        mock_self = Mock()

        @validate_model_capabilities()
        def test_function(self, messages, **kwargs):
            return {"messages": messages, **kwargs}

        # Should pass through without validation
        result = test_function(
            mock_self,
            messages=[{"role": "user", "content": "test"}],
            parallel_tool_calls=True,
        )

        assert result["parallel_tool_calls"] is True

    def test_decorator_no_capabilities_available(self):
        """Test decorator handles case where model capabilities can't be retrieved."""
        # Mock models instance that returns None for capabilities
        mock_models = Mock()
        mock_models.get_capabilities.return_value = None

        # Mock self object
        mock_self = Mock()
        mock_self.models = mock_models

        @validate_model_capabilities()
        def test_function(self, model, messages, **kwargs):
            return {"model": model, "messages": messages, **kwargs}

        # Should pass through without validation when capabilities unavailable
        result = test_function(
            mock_self,
            model="unknown-model",
            messages=[{"role": "user", "content": "test"}],
            parallel_tool_calls=True,
        )

        assert result["parallel_tool_calls"] is True

    def test_decorator_no_models_instance(self):
        """Test decorator handles case where models instance is not available."""
        # Mock self object without models
        mock_self = Mock()
        del mock_self.models  # No models attribute

        @validate_model_capabilities()
        def test_function(self, model, messages, **kwargs):
            return {"model": model, "messages": messages, **kwargs}

        # Should pass through without validation when models unavailable
        result = test_function(
            mock_self,
            model="test-model",
            messages=[{"role": "user", "content": "test"}],
            parallel_tool_calls=True,
        )

        assert result["parallel_tool_calls"] is True

    def test_decorator_with_client_models(self):
        """Test decorator works when models is accessed via client."""
        # Mock model capabilities
        mock_capabilities = ModelCapabilities(
            optimizedForCode=True,
            quantization="fp8",
            supportsFunctionCalling=True,
            supportsReasoning=True,
            supportsResponseSchema=True,
            supportsVision=False,
            supportsWebSearch=False,
            supportsLogProbs=True,
        )

        # Mock models instance
        mock_models = Mock()
        mock_models.get_capabilities.return_value = mock_capabilities

        # Mock client and self objects
        mock_client = Mock()
        mock_client.models = mock_models
        mock_self = Mock()
        mock_self.client = mock_client
        del mock_self.models  # No direct models attribute

        @validate_model_capabilities()
        def test_function(self, model, messages, **kwargs):
            return {"model": model, "messages": messages, **kwargs}

        result = test_function(
            mock_self,
            model="qwen-2.5-qwq-32b",
            messages=[{"role": "user", "content": "test"}],
            parallel_tool_calls=True,
        )

        assert result["parallel_tool_calls"] is True

    def test_decorator_custom_parameters_to_check(self):
        """Test decorator with custom parameters_to_check."""
        # Mock model capabilities
        mock_capabilities = ModelCapabilities(
            optimizedForCode=True,
            quantization="fp8",
            supportsFunctionCalling=False,  # No function calling
            supportsReasoning=True,
            supportsResponseSchema=False,
            supportsVision=False,
            supportsWebSearch=False,
            supportsLogProbs=True,  # Has logprobs
        )

        # Mock models instance
        mock_models = Mock()
        mock_models.get_capabilities.return_value = mock_capabilities

        # Mock self object
        mock_self = Mock()
        mock_self.models = mock_models

        # Only check specific parameters
        @validate_model_capabilities(
            parameters_to_check={"logprobs"}, warn_on_removal=False
        )
        def test_function(self, model, messages, **kwargs):
            return {"model": model, "messages": messages, **kwargs}

        result = test_function(
            mock_self,
            model="test-model",
            messages=[{"role": "user", "content": "test"}],
            parallel_tool_calls=True,  # Should NOT be checked/removed
            logprobs=True,  # Should be checked and kept
        )

        # parallel_tool_calls should remain (not checked)
        assert result["parallel_tool_calls"] is True
        # logprobs should remain (model supports it)
        assert result["logprobs"] is True


@pytest.mark.unit
class TestFilterUnsupportedParams:
    """Test the filter_unsupported_params function."""

    def test_filter_with_supported_params(self):
        """Test filtering when all parameters are supported."""
        # Mock model capabilities with all features
        mock_capabilities = ModelCapabilities(
            optimizedForCode=True,
            quantization="fp8",
            supportsFunctionCalling=True,
            supportsReasoning=True,
            supportsResponseSchema=True,
            supportsVision=False,
            supportsWebSearch=False,
            supportsLogProbs=True,
        )

        # Mock models instance
        mock_models = Mock()
        mock_models.get_capabilities.return_value = mock_capabilities

        params = {
            "model": "qwen-2.5-qwq-32b",
            "messages": [{"role": "user", "content": "test"}],
            "parallel_tool_calls": True,
            "tools": [{"type": "function"}],
            "logprobs": True,
            "temperature": 0.7,
        }

        filtered = filter_unsupported_params(
            model="qwen-2.5-qwq-32b",
            params=params,
            models_instance=mock_models,
            warn=False,
        )

        # All parameters should be preserved
        assert filtered == params

    def test_filter_removes_unsupported_params(self):
        """Test filtering removes unsupported parameters."""
        # Mock model capabilities with no function calling
        mock_capabilities = ModelCapabilities(
            optimizedForCode=False,
            quantization="fp16",
            supportsFunctionCalling=False,
            supportsReasoning=True,
            supportsResponseSchema=False,
            supportsVision=False,
            supportsWebSearch=True,
            supportsLogProbs=False,
        )

        # Mock models instance
        mock_models = Mock()
        mock_models.get_capabilities.return_value = mock_capabilities

        params = {
            "model": "venice-uncensored",
            "messages": [{"role": "user", "content": "test"}],
            "parallel_tool_calls": True,
            "tools": [{"type": "function"}],
            "logprobs": True,
            "temperature": 0.7,
        }

        filtered = filter_unsupported_params(
            model="venice-uncensored",
            params=params,
            models_instance=mock_models,
            warn=False,
        )

        # Unsupported parameters should be removed
        expected = {
            "model": "venice-uncensored",
            "messages": [{"role": "user", "content": "test"}],
            "temperature": 0.7,
        }
        assert filtered == expected

    def test_filter_warns_on_removal(self):
        """Test that filtering warns when removing parameters."""
        # Mock model capabilities with no function calling
        mock_capabilities = ModelCapabilities(
            optimizedForCode=False,
            quantization="fp16",
            supportsFunctionCalling=False,
            supportsReasoning=True,
            supportsResponseSchema=False,
            supportsVision=False,
            supportsWebSearch=True,
            supportsLogProbs=False,
        )

        # Mock models instance
        mock_models = Mock()
        mock_models.get_capabilities.return_value = mock_capabilities

        params = {
            "model": "venice-uncensored",
            "parallel_tool_calls": True,
            "temperature": 0.7,
        }

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            filtered = filter_unsupported_params(
                model="venice-uncensored",
                params=params,
                models_instance=mock_models,
                warn=True,
            )

            # Should have warned about parameter removal
            assert len(w) > 0
            assert "parallel_tool_calls" in str(w[0].message)
            assert "not supported" in str(w[0].message)

        # Parameter should still be removed
        assert "parallel_tool_calls" not in filtered

    def test_filter_no_capabilities(self):
        """Test filtering when capabilities are not available."""
        # Mock models instance that returns None
        mock_models = Mock()
        mock_models.get_capabilities.return_value = None

        params = {
            "model": "unknown-model",
            "parallel_tool_calls": True,
            "temperature": 0.7,
        }

        filtered = filter_unsupported_params(
            model="unknown-model",
            params=params,
            models_instance=mock_models,
            warn=False,
        )

        # Should return params unchanged when capabilities unavailable
        assert filtered == params

    def test_filter_none_values(self):
        """Test that None values are properly handled."""
        # Mock model capabilities
        mock_capabilities = ModelCapabilities(
            optimizedForCode=False,
            quantization="fp16",
            supportsFunctionCalling=False,
            supportsReasoning=True,
            supportsResponseSchema=False,
            supportsVision=False,
            supportsWebSearch=True,
            supportsLogProbs=False,
        )

        # Mock models instance
        mock_models = Mock()
        mock_models.get_capabilities.return_value = mock_capabilities

        params = {
            "model": "venice-uncensored",
            "parallel_tool_calls": None,  # None value
            "tools": None,  # None value
            "temperature": 0.7,
        }

        filtered = filter_unsupported_params(
            model="venice-uncensored",
            params=params,
            models_instance=mock_models,
            warn=False,
        )

        # None values should not be filtered (only non-None unsupported params)
        expected = {
            "model": "venice-uncensored",
            "parallel_tool_calls": None,
            "tools": None,
            "temperature": 0.7,
        }
        assert filtered == expected

    def test_parameter_mapping_coverage(self):
        """Test that all parameter mappings are covered."""
        # Mock model capabilities with no support for anything
        mock_capabilities = ModelCapabilities(
            optimizedForCode=False,
            quantization="fp16",
            supportsFunctionCalling=False,
            supportsReasoning=False,
            supportsResponseSchema=False,
            supportsVision=False,
            supportsWebSearch=False,
            supportsLogProbs=False,
        )

        # Mock models instance
        mock_models = Mock()
        mock_models.get_capabilities.return_value = mock_capabilities

        # Test all mapped parameters
        params = {
            "parallel_tool_calls": True,
            "tools": [{"type": "function"}],
            "tool_choice": "auto",
            "functions": [{"name": "test"}],
            "function_call": "auto",
            "response_format": {"type": "json_object"},
            "response_schema": {"type": "object"},
            "logprobs": True,
            "top_logprobs": 5,
            "reasoning_effort": "high",
            "temperature": 0.7,  # Should remain
        }

        filtered = filter_unsupported_params(
            model="test-model", params=params, models_instance=mock_models, warn=False
        )

        # Only temperature should remain
        assert filtered == {"temperature": 0.7}
