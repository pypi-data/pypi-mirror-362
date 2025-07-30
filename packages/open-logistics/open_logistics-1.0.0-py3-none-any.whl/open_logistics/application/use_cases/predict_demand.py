"""
Use case for predicting demand.
"""
from typing import Dict, Optional
from open_logistics.infrastructure.mlx_integration.mlx_optimizer import (
    MLXOptimizer
)

class PredictDemandUseCase:
    """
    Orchestrates the demand prediction process.
    """
    def __init__(self, optimizer: Optional[MLXOptimizer] = None):
        self.optimizer = optimizer or MLXOptimizer()

    async def execute(self, historical_data: dict, time_horizon: int) -> dict:
        """
        Executes the prediction use case.
        """
        predictions = await self.optimizer.predict_demand(historical_data, time_horizon)
        return {
            "predictions": predictions,
            "confidence_scores": {k: 0.85 for k in predictions.keys()},
            "type": "demand",
            "time_horizon": time_horizon
        } 