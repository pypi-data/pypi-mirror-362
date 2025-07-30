"""Tests for ensemble execution."""

import asyncio
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from llm_orc.ensemble_config import EnsembleConfig
from llm_orc.ensemble_execution import EnsembleExecutor
from llm_orc.models import ClaudeCLIModel, ClaudeModel, ModelInterface, OAuthClaudeModel
from llm_orc.roles import RoleDefinition


class TestEnsembleExecutor:
    """Test ensemble execution."""

    @pytest.mark.asyncio
    async def test_execute_simple_ensemble(self) -> None:
        """Test executing a simple ensemble with mock agents."""
        # Create ensemble config
        config = EnsembleConfig(
            name="test_ensemble",
            description="Test ensemble",
            agents=[
                {"name": "agent1", "role": "tester", "model": "mock-model"},
                {"name": "agent2", "role": "reviewer", "model": "mock-model"},
            ],
            coordinator={
                "synthesis_prompt": "Combine the results from both agents",
                "output_format": "json",
            },
        )

        # Create mock model
        mock_model = AsyncMock(spec=ModelInterface)
        mock_model.generate_response.side_effect = [
            "Agent 1 response: This looks good",
            "Agent 2 response: I found some issues",
        ]
        mock_model.get_last_usage.return_value = {
            "total_tokens": 30,
            "input_tokens": 20,
            "output_tokens": 10,
            "cost_usd": 0.005,
            "duration_ms": 50,
        }

        # Create role definitions
        role1 = RoleDefinition(name="tester", prompt="You are a tester")
        role2 = RoleDefinition(name="reviewer", prompt="You are a reviewer")

        # Create executor with mock dependencies
        executor = EnsembleExecutor()

        # Create mock synthesis model
        mock_synthesis_model = AsyncMock(spec=ModelInterface)
        mock_synthesis_model.generate_response.return_value = (
            "Synthesis: Combined results from both agents"
        )
        mock_synthesis_model.get_last_usage.return_value = {
            "total_tokens": 50,
            "input_tokens": 30,
            "output_tokens": 20,
            "cost_usd": 0.01,
            "duration_ms": 100,
        }

        # Mock the role and model loading methods
        with (
            patch.object(
                executor, "_load_role", new_callable=AsyncMock
            ) as mock_load_role,
            patch.object(
                executor, "_load_model", new_callable=AsyncMock
            ) as mock_load_model,
            patch.object(
                executor, "_get_synthesis_model", new_callable=AsyncMock
            ) as mock_get_synthesis_model,
        ):
            mock_load_role.side_effect = [role1, role2]
            mock_load_model.return_value = mock_model
            mock_get_synthesis_model.return_value = mock_synthesis_model

            # Execute ensemble
            result = await executor.execute(config, input_data="Test this code")

        # Verify result structure
        assert result["ensemble"] == "test_ensemble"
        assert result["status"] == "completed"
        assert "input" in result
        assert "results" in result
        assert "synthesis" in result
        assert "metadata" in result

        # Verify agent results
        agent_results = result["results"]
        assert len(agent_results) == 2
        assert "agent1" in agent_results
        assert "agent2" in agent_results

        # Verify metadata
        metadata = result["metadata"]
        assert "duration" in metadata
        assert metadata["agents_used"] == 2

    @pytest.mark.asyncio
    async def test_execute_ensemble_with_different_models(self) -> None:
        """Test executing ensemble with different models per agent."""
        config = EnsembleConfig(
            name="multi_model_ensemble",
            description="Ensemble with different models",
            agents=[
                {"name": "claude_agent", "role": "analyst", "model": "claude-3-sonnet"},
                {"name": "local_agent", "role": "checker", "model": "llama3"},
            ],
            coordinator={
                "synthesis_prompt": "Compare the analysis and check",
                "output_format": "structured",
            },
        )

        # Mock different models
        claude_model = AsyncMock(spec=ModelInterface)
        claude_model.generate_response.return_value = "Claude analysis result"
        claude_model.get_last_usage.return_value = {
            "total_tokens": 40,
            "input_tokens": 25,
            "output_tokens": 15,
            "cost_usd": 0.008,
            "duration_ms": 80,
        }

        llama_model = AsyncMock(spec=ModelInterface)
        llama_model.generate_response.return_value = "Llama check result"
        llama_model.get_last_usage.return_value = {
            "total_tokens": 25,
            "input_tokens": 15,
            "output_tokens": 10,
            "cost_usd": 0.003,
            "duration_ms": 60,
        }

        # Mock role
        analyst_role = RoleDefinition(name="analyst", prompt="Analyze this")
        checker_role = RoleDefinition(name="checker", prompt="Check this")

        executor = EnsembleExecutor()

        # Create mock synthesis model
        mock_synthesis_model = AsyncMock(spec=ModelInterface)
        mock_synthesis_model.generate_response.return_value = (
            "Synthesis: The analysis and check both confirm the feature is solid"
        )
        mock_synthesis_model.get_last_usage.return_value = {
            "total_tokens": 35,
            "input_tokens": 20,
            "output_tokens": 15,
            "cost_usd": 0.006,
            "duration_ms": 70,
        }

        # Mock the role and model loading methods
        with (
            patch.object(
                executor, "_load_role", new_callable=AsyncMock
            ) as mock_load_role,
            patch.object(
                executor, "_load_model", new_callable=AsyncMock
            ) as mock_load_model,
            patch.object(
                executor, "_get_synthesis_model", new_callable=AsyncMock
            ) as mock_get_synthesis_model,
        ):
            mock_load_role.side_effect = [analyst_role, checker_role]
            mock_load_model.side_effect = [claude_model, llama_model]
            mock_get_synthesis_model.return_value = mock_synthesis_model

            result = await executor.execute(config, input_data="Analyze this feature")

        assert result["status"] == "completed"
        assert len(result["results"]) == 2
        assert "claude_agent" in result["results"]
        assert "local_agent" in result["results"]

    @pytest.mark.asyncio
    async def test_execute_ensemble_handles_agent_failure(self) -> None:
        """Test that ensemble execution handles individual agent failures."""
        config = EnsembleConfig(
            name="test_ensemble_with_failure",
            description="Test ensemble with one failing agent",
            agents=[
                {"name": "working_agent", "role": "tester", "model": "mock-model"},
                {"name": "failing_agent", "role": "reviewer", "model": "mock-model"},
            ],
            coordinator={
                "synthesis_prompt": "Combine available results",
                "output_format": "json",
            },
        )

        # Create mock models - one works, one fails
        working_model = AsyncMock(spec=ModelInterface)
        working_model.generate_response.return_value = "Working agent response"

        failing_model = AsyncMock(spec=ModelInterface)
        failing_model.generate_response.side_effect = Exception("Model failed")

        # Mock roles
        role = RoleDefinition(name="tester", prompt="You are a tester")

        executor = EnsembleExecutor()

        # Mock synthesis model
        mock_synthesis_model = AsyncMock(spec=ModelInterface)
        mock_synthesis_model.generate_response.return_value = (
            "Synthesis of available results"
        )
        mock_synthesis_model.get_last_usage.return_value = {
            "total_tokens": 30,
            "input_tokens": 20,
            "output_tokens": 10,
            "cost_usd": 0.005,
            "duration_ms": 50,
        }

        # Mock the role and model loading methods
        with (
            patch.object(
                executor, "_load_role", new_callable=AsyncMock
            ) as mock_load_role,
            patch.object(
                executor, "_load_model", new_callable=AsyncMock
            ) as mock_load_model,
            patch.object(
                executor, "_get_synthesis_model", new_callable=AsyncMock
            ) as mock_get_synthesis_model,
        ):
            mock_load_role.return_value = role
            mock_load_model.side_effect = [working_model, failing_model]
            mock_get_synthesis_model.return_value = mock_synthesis_model

            result = await executor.execute(config, input_data="Test input")

        # Should still complete but mark failures
        assert result["status"] == "completed_with_errors"
        assert len(result["results"]) == 2
        assert "working_agent" in result["results"]
        assert "failing_agent" in result["results"]

        # Working agent should have response
        assert "response" in result["results"]["working_agent"]

        # Failing agent should have error
        assert "error" in result["results"]["failing_agent"]

    @pytest.mark.asyncio
    async def test_execute_ensemble_synthesis(self) -> None:
        """Test that ensemble execution includes synthesis of results."""
        config = EnsembleConfig(
            name="synthesis_test",
            description="Test synthesis functionality",
            agents=[
                {"name": "agent1", "role": "analyst", "model": "mock-model"},
            ],
            coordinator={
                "synthesis_prompt": "Summarize the analysis results",
                "output_format": "json",
            },
        )

        # Mock agent response
        agent_model = AsyncMock(spec=ModelInterface)
        agent_model.generate_response.return_value = "Detailed analysis result"

        # Mock synthesis model
        synthesis_model = AsyncMock(spec=ModelInterface)
        synthesis_model.generate_response.return_value = "Synthesized summary"

        role = RoleDefinition(name="analyst", prompt="Analyze")

        executor = EnsembleExecutor()

        # Mock the role and model loading methods
        with (
            patch.object(
                executor, "_load_role", new_callable=AsyncMock
            ) as mock_load_role,
            patch.object(
                executor, "_load_model", new_callable=AsyncMock
            ) as mock_load_model,
            patch.object(
                executor, "_get_synthesis_model", new_callable=AsyncMock
            ) as mock_get_synthesis_model,
        ):
            mock_load_role.return_value = role
            mock_load_model.return_value = agent_model
            mock_get_synthesis_model.return_value = synthesis_model

            result = await executor.execute(config, input_data="Test analysis")

        assert result["synthesis"] == "Synthesized summary"

        # Verify synthesis model was called with agent results
        synthesis_model.generate_response.assert_called_once()
        synthesis_call_args = synthesis_model.generate_response.call_args[1]
        assert "Summarize the analysis results" in synthesis_call_args["role_prompt"]

    @pytest.mark.asyncio
    async def test_execute_ensemble_tracks_usage_metrics(self) -> None:
        """Test that ensemble execution tracks LLM usage metrics."""
        config = EnsembleConfig(
            name="usage_tracking_test",
            description="Test usage tracking",
            agents=[
                {"name": "agent1", "role": "analyst", "model": "claude-3-sonnet"},
                {"name": "agent2", "role": "reviewer", "model": "llama3"},
            ],
            coordinator={
                "synthesis_prompt": "Combine results",
                "output_format": "json",
            },
        )

        # Mock models with usage tracking
        claude_model = AsyncMock(spec=ModelInterface)
        claude_model.generate_response.return_value = "Claude response"
        claude_model.get_last_usage.return_value = {
            "input_tokens": 50,
            "output_tokens": 100,
            "total_tokens": 150,
            "cost_usd": 0.0045,
            "duration_ms": 1200,
            "model": "claude-3-sonnet",
        }

        llama_model = AsyncMock(spec=ModelInterface)
        llama_model.generate_response.return_value = "Llama response"
        llama_model.get_last_usage.return_value = {
            "input_tokens": 45,
            "output_tokens": 80,
            "total_tokens": 125,
            "cost_usd": 0.0,  # Local model, no cost
            "duration_ms": 800,
            "model": "llama3",
        }

        synthesis_model = AsyncMock(spec=ModelInterface)
        synthesis_model.generate_response.return_value = "Synthesized result"
        synthesis_model.get_last_usage.return_value = {
            "input_tokens": 200,
            "output_tokens": 50,
            "total_tokens": 250,
            "cost_usd": 0.0075,
            "duration_ms": 1500,
            "model": "llama3",
        }

        role = RoleDefinition(name="test", prompt="Test role")

        executor = EnsembleExecutor()

        # Mock the role and model loading methods
        with (
            patch.object(
                executor, "_load_role", new_callable=AsyncMock
            ) as mock_load_role,
            patch.object(
                executor, "_load_model", new_callable=AsyncMock
            ) as mock_load_model,
            patch.object(
                executor, "_get_synthesis_model", new_callable=AsyncMock
            ) as mock_get_synthesis_model,
        ):
            mock_load_role.return_value = role
            mock_load_model.side_effect = [claude_model, llama_model]
            mock_get_synthesis_model.return_value = synthesis_model

            result = await executor.execute(config, input_data="Test usage tracking")

        # Verify usage tracking is included in results
        assert "usage" in result["metadata"]
        usage = result["metadata"]["usage"]

        # Check individual agent usage
        assert "agents" in usage
        agent_usage = usage["agents"]

        assert "agent1" in agent_usage
        assert agent_usage["agent1"]["model"] == "claude-3-sonnet"
        assert agent_usage["agent1"]["input_tokens"] == 50
        assert agent_usage["agent1"]["output_tokens"] == 100
        assert agent_usage["agent1"]["total_tokens"] == 150
        assert agent_usage["agent1"]["cost_usd"] == 0.0045
        assert agent_usage["agent1"]["duration_ms"] == 1200

        assert "agent2" in agent_usage
        assert agent_usage["agent2"]["model"] == "llama3"
        assert agent_usage["agent2"]["total_tokens"] == 125
        assert agent_usage["agent2"]["cost_usd"] == 0.0

        # Check synthesis usage
        assert "synthesis" in usage
        synthesis_usage = usage["synthesis"]
        assert synthesis_usage["total_tokens"] == 250
        assert synthesis_usage["cost_usd"] == 0.0075

        # Check totals
        assert "totals" in usage
        totals = usage["totals"]
        assert totals["total_tokens"] == 525  # 150 + 125 + 250
        assert totals["total_cost_usd"] == 0.012  # 0.0045 + 0.0 + 0.0075
        assert totals["total_duration_ms"] == 3500  # 1200 + 800 + 1500
        assert totals["agents_count"] == 2

    @pytest.mark.asyncio
    async def test_execute_ensemble_with_timeout(self) -> None:
        """Test that ensemble execution respects timeout settings."""
        config = EnsembleConfig(
            name="timeout_test",
            description="Test timeout functionality",
            agents=[
                {"name": "slow_agent", "role": "analyst", "model": "slow-model"},
            ],
            coordinator={
                "synthesis_prompt": "Summarize results",
                "output_format": "json",
                "timeout_seconds": 0.1,  # 100ms timeout
            },
        )

        # Mock model that takes too long
        slow_model = AsyncMock(spec=ModelInterface)

        async def slow_response(*args: Any, **kwargs: Any) -> str:
            await asyncio.sleep(0.2)  # Takes 200ms, longer than 100ms timeout
            return "This should timeout"

        slow_model.generate_response = slow_response
        slow_model.get_last_usage.return_value = {
            "input_tokens": 50,
            "output_tokens": 100,
            "total_tokens": 150,
            "cost_usd": 0.001,
            "duration_ms": 200,
            "model": "slow-model",
        }

        role = RoleDefinition(name="analyst", prompt="Analyze")

        executor = EnsembleExecutor()

        # Mock the role and model loading methods
        with (
            patch.object(
                executor, "_load_role", new_callable=AsyncMock
            ) as mock_load_role,
            patch.object(
                executor, "_load_model", new_callable=AsyncMock
            ) as mock_load_model,
        ):
            mock_load_role.return_value = role
            mock_load_model.return_value = slow_model

            result = await executor.execute(config, input_data="Test timeout")

        # Should complete with errors due to timeout
        assert result["status"] == "completed_with_errors"
        assert "slow_agent" in result["results"]
        agent_result = result["results"]["slow_agent"]
        assert agent_result["status"] == "failed"
        assert "timed out" in agent_result["error"].lower()

    @pytest.mark.asyncio
    async def test_execute_ensemble_with_per_agent_timeout(self) -> None:
        """Test that individual agents can have their own timeout settings."""
        config = EnsembleConfig(
            name="per_agent_timeout_test",
            description="Test per-agent timeout functionality",
            agents=[
                {
                    "name": "fast_agent",
                    "role": "analyst",
                    "model": "fast-model",
                    "timeout_seconds": 1.0,
                },
                {
                    "name": "slow_agent",
                    "role": "reviewer",
                    "model": "slow-model",
                    "timeout_seconds": 0.05,  # 50ms timeout
                },
            ],
            coordinator={
                "synthesis_prompt": "Combine results",
                "output_format": "json",
            },
        )

        # Fast model
        fast_model = AsyncMock(spec=ModelInterface)
        fast_model.generate_response.return_value = "Fast response"
        fast_model.get_last_usage.return_value = {
            "input_tokens": 20,
            "output_tokens": 30,
            "total_tokens": 50,
            "cost_usd": 0.001,
            "duration_ms": 500,
            "model": "fast-model",
        }

        # Slow model that exceeds its timeout
        slow_model = AsyncMock(spec=ModelInterface)

        async def slow_response(*args: Any, **kwargs: Any) -> str:
            await asyncio.sleep(0.1)  # Takes 100ms, longer than 50ms timeout
            return "This should timeout"

        slow_model.generate_response = slow_response
        slow_model.get_last_usage.return_value = {
            "input_tokens": 30,
            "output_tokens": 40,
            "total_tokens": 70,
            "cost_usd": 0.002,
            "duration_ms": 100,
            "model": "slow-model",
        }

        role = RoleDefinition(name="test", prompt="Test")

        executor = EnsembleExecutor()

        # Mock the role and model loading methods
        with (
            patch.object(
                executor, "_load_role", new_callable=AsyncMock
            ) as mock_load_role,
            patch.object(
                executor, "_load_model", new_callable=AsyncMock
            ) as mock_load_model,
        ):
            mock_load_role.return_value = role
            mock_load_model.side_effect = [fast_model, slow_model]

            result = await executor.execute(config, input_data="Test per-agent timeout")

        # Should complete with errors due to one agent timing out
        assert result["status"] == "completed_with_errors"

        # Fast agent should succeed
        assert result["results"]["fast_agent"]["status"] == "success"
        assert result["results"]["fast_agent"]["response"] == "Fast response"

        # Slow agent should fail with timeout
        assert result["results"]["slow_agent"]["status"] == "failed"
        assert "timed out" in result["results"]["slow_agent"]["error"].lower()

    @pytest.mark.asyncio
    async def test_execute_ensemble_with_synthesis_timeout(self) -> None:
        """Test that synthesis step respects timeout settings."""
        config = EnsembleConfig(
            name="synthesis_timeout_test",
            description="Test synthesis timeout",
            agents=[
                {"name": "agent1", "role": "analyst", "model": "fast-model"},
            ],
            coordinator={
                "synthesis_prompt": "Synthesize results",
                "output_format": "json",
                "synthesis_timeout_seconds": 0.05,  # 50ms timeout
            },
        )

        # Fast agent
        fast_model = AsyncMock(spec=ModelInterface)
        fast_model.generate_response.return_value = "Agent response"
        fast_model.get_last_usage.return_value = {
            "input_tokens": 20,
            "output_tokens": 30,
            "total_tokens": 50,
            "cost_usd": 0.001,
            "duration_ms": 500,
            "model": "fast-model",
        }

        # Slow synthesis model
        slow_synthesis_model = AsyncMock(spec=ModelInterface)

        async def slow_synthesis(*args: Any, **kwargs: Any) -> str:
            await asyncio.sleep(0.1)  # Takes 100ms, longer than 50ms timeout
            return "This should timeout"

        slow_synthesis_model.generate_response = slow_synthesis
        slow_synthesis_model.get_last_usage.return_value = {
            "input_tokens": 100,
            "output_tokens": 50,
            "total_tokens": 150,
            "cost_usd": 0.003,
            "duration_ms": 100,
            "model": "synthesis-model",
        }

        role = RoleDefinition(name="analyst", prompt="Analyze")

        executor = EnsembleExecutor()

        # Mock the role and model loading methods
        with (
            patch.object(
                executor, "_load_role", new_callable=AsyncMock
            ) as mock_load_role,
            patch.object(
                executor, "_load_model", new_callable=AsyncMock
            ) as mock_load_model,
            patch.object(
                executor, "_get_synthesis_model", new_callable=AsyncMock
            ) as mock_get_synthesis_model,
        ):
            mock_load_role.return_value = role
            mock_load_model.return_value = fast_model
            mock_get_synthesis_model.return_value = slow_synthesis_model

            result = await executor.execute(config, input_data="Test synthesis timeout")

        # Should complete with errors due to synthesis timeout
        assert result["status"] == "completed_with_errors"
        assert result["results"]["agent1"]["status"] == "success"
        assert (
            "synthesis failed" in result["synthesis"].lower()
            or "timeout" in result["synthesis"].lower()
        )

    @pytest.mark.asyncio
    async def test_load_model_with_authentication_configurations(self) -> None:
        """Test _load_model resolves auth configurations to model instances."""
        executor = EnsembleExecutor()

        # Mock authentication system
        with (
            patch("llm_orc.ensemble_execution.ConfigurationManager"),
            patch(
                "llm_orc.ensemble_execution.CredentialStorage"
            ) as mock_credential_storage,
        ):
            mock_storage_instance = mock_credential_storage.return_value

            # Test 1: Load model for "anthropic-api" auth configuration
            mock_storage_instance.get_auth_method.return_value = "api_key"
            mock_storage_instance.get_api_key.return_value = "sk-ant-test123"

            model = await executor._load_model("anthropic-api")

            # Should create ClaudeModel with API key
            assert isinstance(model, ClaudeModel)
            assert model.api_key == "sk-ant-test123"

            # Test 2: Load model for "anthropic-claude-pro-max" OAuth configuration
            mock_storage_instance.get_auth_method.return_value = "oauth"
            mock_storage_instance.get_oauth_token.return_value = {
                "access_token": "oauth_access_token",
                "refresh_token": "oauth_refresh_token",
                "client_id": "oauth_client_id",
            }

            model = await executor._load_model("anthropic-claude-pro-max")

            # Should create OAuthClaudeModel
            assert isinstance(model, OAuthClaudeModel)
            assert model.access_token == "oauth_access_token"
            assert model.refresh_token == "oauth_refresh_token"
            assert model.client_id == "oauth_client_id"

            # Test 3: Load model for "claude-cli" configuration
            # claude-cli stores path as "api_key"
            mock_storage_instance.get_auth_method.return_value = "api_key"
            mock_storage_instance.get_api_key.return_value = "/usr/local/bin/claude"

            model = await executor._load_model("claude-cli")

            # Should create ClaudeCLIModel
            assert isinstance(model, ClaudeCLIModel)
            assert model.claude_path == "/usr/local/bin/claude"

    @pytest.mark.asyncio
    async def test_load_model_prompts_for_auth_setup_when_not_configured(self) -> None:
        """Test that _load_model prompts user to set up auth when not configured."""
        executor = EnsembleExecutor()

        # Mock authentication system - no auth method configured
        with (
            patch("llm_orc.ensemble_execution.ConfigurationManager"),
            patch(
                "llm_orc.ensemble_execution.CredentialStorage"
            ) as mock_credential_storage,
            patch(
                "llm_orc.ensemble_execution._should_prompt_for_auth", return_value=True
            ),
            patch("llm_orc.ensemble_execution._prompt_auth_setup") as mock_prompt_setup,
        ):
            mock_storage_instance = mock_credential_storage.return_value

            # Simulate no auth method configured
            mock_storage_instance.get_auth_method.return_value = None

            # Mock successful auth setup
            mock_prompt_setup.return_value = True

            # After setup, mock the configured auth method
            # First call: None, second call: oauth
            mock_storage_instance.get_auth_method.side_effect = [None, "oauth"]
            mock_storage_instance.get_oauth_token.return_value = {
                "access_token": "new_oauth_token",
                "refresh_token": "new_refresh_token",
                "client_id": "new_client_id",
            }

            model = await executor._load_model("anthropic-claude-pro-max")

            # Should prompt for auth setup
            mock_prompt_setup.assert_called_once_with(
                "anthropic-claude-pro-max", mock_storage_instance
            )

            # Should create OAuthClaudeModel after setup
            assert isinstance(model, OAuthClaudeModel)

    @pytest.mark.asyncio
    async def test_load_model_fallback_when_user_declines_auth_setup(self) -> None:
        """Test that _load_model falls back to Ollama when user declines auth setup."""
        executor = EnsembleExecutor()

        # Mock authentication system - no auth method configured
        with (
            patch("llm_orc.ensemble_execution.ConfigurationManager"),
            patch(
                "llm_orc.ensemble_execution.CredentialStorage"
            ) as mock_credential_storage,
            patch(
                "llm_orc.ensemble_execution._should_prompt_for_auth", return_value=True
            ),
            patch("llm_orc.ensemble_execution._prompt_auth_setup") as mock_prompt_setup,
        ):
            mock_storage_instance = mock_credential_storage.return_value

            # Simulate no auth method configured
            mock_storage_instance.get_auth_method.return_value = None

            # User declines to set up authentication
            mock_prompt_setup.return_value = False

            model = await executor._load_model("anthropic-claude-pro-max")

            # Should prompt user for auth setup
            mock_prompt_setup.assert_called_once_with(
                "anthropic-claude-pro-max", mock_storage_instance
            )

            # Should fall back to Ollama
            from llm_orc.models import OllamaModel

            assert isinstance(model, OllamaModel)

    def test_should_prompt_for_auth_returns_true_for_known_configs(self) -> None:
        """Test that _should_prompt_for_auth returns True for known auth configs."""
        from llm_orc.ensemble_execution import _should_prompt_for_auth

        # Should return True for known auth configurations
        assert _should_prompt_for_auth("anthropic-api") is True
        assert _should_prompt_for_auth("anthropic-claude-pro-max") is True
        assert _should_prompt_for_auth("claude-cli") is True
        assert _should_prompt_for_auth("openai-api") is True
        assert _should_prompt_for_auth("google-api") is True

    def test_should_prompt_for_auth_returns_false_for_mock_models(self) -> None:
        """Test that _should_prompt_for_auth returns False for mock/local models."""
        from llm_orc.ensemble_execution import _should_prompt_for_auth

        # Should return False for mock models and local models
        assert _should_prompt_for_auth("mock-model") is False
        assert _should_prompt_for_auth("mock-claude") is False
        assert _should_prompt_for_auth("llama3") is False
        assert _should_prompt_for_auth("llama2") is False
        assert _should_prompt_for_auth("unknown-model") is False

    @pytest.mark.asyncio
    async def test_ensemble_execution_with_model_profile(self) -> None:
        """Test ensemble execution using model_profile.

        Uses model_profile instead of explicit model+provider.
        """
        from pathlib import Path
        from tempfile import TemporaryDirectory

        import yaml

        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create config with model profiles
            global_dir = temp_path / "global"
            global_dir.mkdir()
            config_data = {
                "model_profiles": {
                    "test-profile": {
                        "model": "claude-3-5-sonnet-20241022",
                        "provider": "anthropic-claude-pro-max",
                    }
                }
            }
            config_file = global_dir / "config.yaml"
            with open(config_file, "w") as f:
                yaml.dump(config_data, f)

            executor = EnsembleExecutor()

            # Test the _load_model_from_agent_config method directly
            with patch(
                "llm_orc.ensemble_execution.ConfigurationManager"
            ) as mock_config_manager_class:
                mock_config_manager = mock_config_manager_class.return_value
                mock_config_manager.resolve_model_profile.return_value = (
                    "claude-3-5-sonnet-20241022",
                    "anthropic-claude-pro-max",
                )

                with patch(
                    "llm_orc.ensemble_execution.CredentialStorage"
                ) as mock_credential_storage:
                    mock_storage_instance = mock_credential_storage.return_value
                    mock_storage_instance.get_auth_method.return_value = None

                    # This should call resolve_model_profile and use the resolved
                    # model+provider
                    # Note: The method may not raise an error due to fallback logic,
                    # but should call resolve_model_profile
                    await executor._load_model_from_agent_config(
                        {"name": "agent1", "model_profile": "test-profile"}
                    )

                    # Verify that resolve_model_profile was called
                    mock_config_manager.resolve_model_profile.assert_called_once_with(
                        "test-profile"
                    )

    @pytest.mark.asyncio
    async def test_ensemble_execution_fallback_to_explicit_model_provider(
        self,
    ) -> None:
        """Test fallback to explicit model+provider when no model_profile."""
        executor = EnsembleExecutor()

        with patch(
            "llm_orc.ensemble_execution.ConfigurationManager"
        ) as mock_config_manager_class:
            mock_config_manager = mock_config_manager_class.return_value

            with patch(
                "llm_orc.ensemble_execution.CredentialStorage"
            ) as mock_credential_storage:
                mock_storage_instance = mock_credential_storage.return_value
                mock_storage_instance.get_auth_method.return_value = None

                # This should use explicit model+provider, not call
                # resolve_model_profile
                await executor._load_model_from_agent_config(
                    {
                        "name": "agent1",
                        "model": "claude-3-5-sonnet-20241022",
                        "provider": "anthropic-claude-pro-max",
                    }
                )

                # Verify that resolve_model_profile was NOT called
                mock_config_manager.resolve_model_profile.assert_not_called()
