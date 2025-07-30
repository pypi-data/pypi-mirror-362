"""
Unit tests for MLX optimizer.
"""
import pytest
from unittest.mock import patch
from open_logistics.infrastructure.mlx_integration.mlx_optimizer import MLXOptimizer, OptimizationRequest

@pytest.mark.asyncio
async def test_optimizer_with_mlx_enabled():
    """Test optimizer with MLX enabled."""
    with patch('open_logistics.infrastructure.mlx_integration.mlx_optimizer.MLX_AVAILABLE', True):
        with patch('open_logistics.infrastructure.mlx_integration.mlx_optimizer.get_settings') as mock_get_settings:
            mock_get_settings.return_value.mlx.MLX_ENABLED = True
            optimizer = MLXOptimizer()
            assert optimizer.use_mlx is True
            request = OptimizationRequest(
                supply_chain_data={"inventory": {"item_1": 10}},
                objectives=["minimize_cost"],
                time_horizon=7
            )
            result = await optimizer.optimize_supply_chain(request)
            assert "mlx_output_vector" in result.optimized_plan

@pytest.mark.asyncio
async def test_optimizer_with_mlx_disabled():
    """Test optimizer with MLX disabled."""
    with patch('open_logistics.infrastructure.mlx_integration.mlx_optimizer.MLX_AVAILABLE', False):
        with patch('open_logistics.infrastructure.mlx_integration.mlx_optimizer.get_settings') as mock_get_settings:
            mock_get_settings.return_value.mlx.MLX_ENABLED = False
            optimizer = MLXOptimizer()
            assert optimizer.use_mlx is False
            request = OptimizationRequest(
                supply_chain_data={"inventory": {"item_1": 10}},
                objectives=["minimize_cost"],
                time_horizon=7
            )
            result = await optimizer.optimize_supply_chain(request)
            assert "predicted_stock_level" in result.optimized_plan

@pytest.mark.asyncio
async def test_predict_demand():
    """Test demand prediction."""
    optimizer = MLXOptimizer()
    historical_data = {"demand_history": [10, 20, 30]}
    time_horizon = 5
    result = await optimizer.predict_demand(historical_data, time_horizon)
    assert len(result) == time_horizon 