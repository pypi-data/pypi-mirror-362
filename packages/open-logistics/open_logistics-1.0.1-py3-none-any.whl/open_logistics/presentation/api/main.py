"""
Main FastAPI application for Open Logistics.

This module defines the main FastAPI application, including API routers,
middleware, and exception handlers.
"""

from fastapi import FastAPI
from open_logistics.application.use_cases.optimize_supply_chain import OptimizeSupplyChainUseCase
from open_logistics.infrastructure.mlx_integration.mlx_optimizer import OptimizationRequest, OptimizationResult

app = FastAPI(
    title="Open Logistics API",
    description="AI-Driven Air Defense Supply Chain Optimization Platform",
    version="1.0.0",
)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@app.post("/optimize", response_model=OptimizationResult)
async def optimize_supply_chain(request: OptimizationRequest):
    """
    Triggers a supply chain optimization task.
    """
    use_case = OptimizeSupplyChainUseCase()
    result = await use_case.execute(request)
    return result 