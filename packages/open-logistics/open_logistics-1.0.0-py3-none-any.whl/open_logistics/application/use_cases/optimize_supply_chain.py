"""
Use case for optimizing the supply chain.

This module defines the application-level use case for triggering
and managing the supply chain optimization process.
"""
from typing import Optional

from open_logistics.infrastructure.mlx_integration.mlx_optimizer import (
    MLXOptimizer, OptimizationRequest, OptimizationResult
)


class OptimizeSupplyChainUseCase:
    """
    Orchestrates the supply chain optimization process by using the MLXOptimizer.
    """
    def __init__(self, optimizer: Optional[MLXOptimizer] = None):
        self.optimizer = optimizer or MLXOptimizer()

    async def execute(self, request: OptimizationRequest) -> OptimizationResult:
        """
        Executes the optimization use case.

        Args:
            request: The optimization request containing all necessary data.

        Returns:
            The result of the optimization.
        """
        # Here you could add more application-specific logic, such as:
        # - Logging the request
        # - Storing the request and result in a database
        # - Publishing events
        # - Performing extra validation

        result = await self.optimizer.optimize_supply_chain(request)

        return result 