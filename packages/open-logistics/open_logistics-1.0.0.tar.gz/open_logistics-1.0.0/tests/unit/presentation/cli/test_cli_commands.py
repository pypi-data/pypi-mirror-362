"""
Unit tests for CLI commands to improve coverage.
"""
import json
from typer.testing import CliRunner
from unittest.mock import patch, AsyncMock

from open_logistics.presentation.cli.main import app
from open_logistics.infrastructure.mlx_integration.mlx_optimizer import OptimizationResult

class TestCLICommandsCoverage:
    """Tests for CLI commands to improve coverage."""

    def setup_method(self):
        """Setup test runner."""
        self.runner = CliRunner()

    @patch('open_logistics.application.use_cases.predict_demand.PredictDemandUseCase')
    def test_predict_non_demand(self, mock_use_case):
        """Test predict command for a non-demand type."""
        result = self.runner.invoke(app, ["predict", "--type", "failures"])
        assert result.exit_code == 0
        assert "Failures Predictions" in result.stdout
        # The use case should not have been called for this invalid type
        mock_use_case.assert_not_called() 