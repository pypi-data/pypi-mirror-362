"""
Integration tests for CLI functionality.
"""

import pytest
from typer.testing import CliRunner
from unittest.mock import patch, AsyncMock

from open_logistics.presentation.cli.main import app
from open_logistics.infrastructure.mlx_integration.mlx_optimizer import OptimizationResult

class TestCLIIntegration:
    """Integration tests for CLI commands."""

    def setup_method(self):
        """Setup test runner."""
        self.runner = CliRunner()

    def test_version_command(self):
        """Test version command works correctly."""
        result = self.runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "Open Logistics Platform" in result.stdout

    @patch('open_logistics.application.use_cases.optimize_supply_chain.OptimizeSupplyChainUseCase')
    def test_optimize_command(self, mock_use_case):
        """Test optimization command."""
        # Mock the use case
        mock_instance = mock_use_case.return_value
        
        # Mock the optimization result
        mock_result = OptimizationResult(
            optimized_plan={"test": "plan"},
            confidence_score=0.85,
            execution_time_ms=150.0,
            resource_utilization={"cpu": 0.7}
        )
        
        mock_instance.execute = AsyncMock(return_value=mock_result)

        result = self.runner.invoke(app, ["optimize", "--objectives", "minimize_cost"])
        
        assert result.exit_code == 0
        assert "Optimization" in result.stdout

    @patch('open_logistics.application.use_cases.predict_demand.PredictDemandUseCase')
    def test_predict_command(self, mock_use_case):
        """Test prediction command."""
        mock_instance = mock_use_case.return_value
        mock_instance.execute = AsyncMock(return_value={
            "predictions": {"day_1": 102.0},
            "confidence_scores": {"day_1": 0.85},
            "type": "demand",
            "time_horizon": 1
        })
        result = self.runner.invoke(app, ["predict", "--type", "demand"])
        assert result.exit_code == 0

    def test_agents_list_command(self):
        """Test agents list command."""
        result = self.runner.invoke(app, ["agents", "list"])
        assert result.exit_code == 0
        assert "AI Agents" in result.stdout

    def test_help_commands(self):
        """Test help is available for all commands."""
        # Test main help
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Open Logistics" in result.stdout

        # Test command-specific help
        commands = ["serve", "optimize", "predict", "agents", "setup"]
        for command in commands:
            result = self.runner.invoke(app, [command, "--help"])
            assert result.exit_code == 0
            assert command in result.stdout.lower()

    @patch('uvicorn.run')
    def test_serve_command(self, mock_uvicorn_run):
        """Test the serve command."""
        result = self.runner.invoke(app, ["serve", "--port", "8080"])
        assert result.exit_code == 0
        mock_uvicorn_run.assert_called_once_with(
            "open_logistics.presentation.api.main:app",
            host="127.0.0.1",
            port=8080,
            reload=False,
        )

    def test_setup_command(self):
        """Test setup command."""
        with patch('open_logistics.presentation.cli.main._setup_database') as mock_db:
            with patch('open_logistics.presentation.cli.main._setup_mlx') as mock_mlx:
                with patch('open_logistics.presentation.cli.main._setup_monitoring') as mock_mon:
                    mock_db.return_value = AsyncMock()
                    mock_mlx.return_value = AsyncMock()
                    mock_mon.return_value = AsyncMock()
                    
                    result = self.runner.invoke(app, ["setup", "--env", "development"])
                    assert result.exit_code == 0
                    assert "Setup" in result.stdout
