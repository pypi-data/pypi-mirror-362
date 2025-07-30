"""
Performance benchmarks for Open Logistics platform.
"""

import pytest
import asyncio
import time
from statistics import mean, stdev

from open_logistics.infrastructure.mlx_integration.mlx_optimizer import (
    MLXOptimizer, OptimizationRequest
)


class TestPerformanceBenchmarks:
    """Performance benchmark tests."""
    
    @pytest.fixture
    def optimizer(self):
        """Create MLX optimizer instance."""
        return MLXOptimizer()
    
    @pytest.fixture
    def large_dataset(self):
        """Create large dataset for benchmarking."""
        return {
            "inventory": {f"item_{i}": 100 + i * 10 for i in range(100)},
            "demand_history": [100 + i % 50 for i in range(365)],  # 1 year
            "constraints": {
                "budget": 50000000,
                "time_limit": 168,  # 1 week
                "capacity_limit": 10000
            },
            "locations": [
                {
                    "id": f"location_{i}",
                    "capacity": 1000 + i * 100,
                    "distance": i * 25
                }
                for i in range(20)
            ]
        }
    
    @pytest.mark.asyncio
    async def test_optimization_performance(self, optimizer, large_dataset):
        """Benchmark optimization performance."""
        request = OptimizationRequest(
            supply_chain_data=large_dataset,
            constraints={"budget": 50000000, "time_limit": 168},
            objectives=["minimize_cost", "maximize_efficiency"],
            time_horizon=60,
            priority_level="high"
        )

        # Benchmark the optimization
        result = await optimizer.optimize_supply_chain(request)
        
        assert result.confidence_score > 0.5
        assert result.execution_time_ms > 0
    
    @pytest.mark.asyncio
    async def test_throughput_benchmark(self, optimizer):
        """Test optimization throughput."""
        small_dataset = {
            "inventory": {"item_1": 500, "item_2": 300},
            "demand_history": [100, 120, 90, 110, 95] * 6,
            "constraints": {"budget": 1000000, "time_limit": 24}
        }
        
        request = OptimizationRequest(
            supply_chain_data=small_dataset,
            constraints={"budget": 1000000, "time_limit": 24},
            objectives=["minimize_cost"],
            time_horizon=7,
            priority_level="medium"
        )
        
        # Run multiple optimizations
        iterations = 10
        execution_times = []
        
        for _ in range(iterations):
            start_time = time.time()
            result = await optimizer.optimize_supply_chain(request)
            execution_time = time.time() - start_time
            execution_times.append(execution_time)
            
            assert result.confidence_score > 0.0
        
        # Calculate statistics
        avg_time = mean(execution_times)
        std_time = stdev(execution_times) if len(execution_times) > 1 else 0
        throughput = 1 / avg_time
        
        print(f"Average execution time: {avg_time:.3f}s")
        print(f"Standard deviation: {std_time:.3f}s")
        print(f"Throughput: {throughput:.2f} ops/sec")
        
        # Performance assertions
        assert avg_time < 5.0  # Should complete within 5 seconds
        assert throughput > 0.2  # At least 0.2 operations per second
    
    @pytest.mark.asyncio
    async def test_memory_usage(self, optimizer, large_dataset):
        """Test memory usage during optimization."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        request = OptimizationRequest(
            supply_chain_data=large_dataset,
            constraints={"budget": 50000000, "time_limit": 168},
            objectives=["minimize_cost", "maximize_efficiency", "minimize_risk"],
            time_horizon=90,
            priority_level="critical"
        )
        
        result = await optimizer.optimize_supply_chain(request)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"Initial memory: {initial_memory:.2f} MB")
        print(f"Final memory: {final_memory:.2f} MB")
        print(f"Memory increase: {memory_increase:.2f} MB")
        
        # Memory usage should be reasonable
        assert memory_increase < 500  # Less than 500MB increase
        assert result.confidence_score > 0.0
    
    @pytest.mark.asyncio
    async def test_concurrent_optimizations(self, optimizer):
        """Test concurrent optimization performance."""
        dataset = {
            "inventory": {"item_1": 500, "item_2": 300, "item_3": 800},
            "demand_history": [100, 120, 90, 110, 95] * 12,
            "constraints": {"budget": 2000000, "time_limit": 48}
        }
        
        request = OptimizationRequest(
            supply_chain_data=dataset,
            constraints={"budget": 2000000, "time_limit": 48},
            objectives=["minimize_cost", "maximize_efficiency"],
            time_horizon=30,
            priority_level="high"
        )
        
        # Run concurrent optimizations
        concurrent_tasks = 5
        start_time = time.time()
        
        tasks = [
            optimizer.optimize_supply_chain(request)
            for _ in range(concurrent_tasks)
        ]
        
        results = await asyncio.gather(*tasks)
        
        total_time = time.time() - start_time
        
        print(f"Concurrent tasks: {concurrent_tasks}")
        print(f"Total time: {total_time:.3f}s")
        print(f"Average time per task: {total_time/concurrent_tasks:.3f}s")
        
        # All tasks should complete successfully
        assert len(results) == concurrent_tasks
        for result in results:
            assert result.confidence_score > 0.0
            assert result.execution_time_ms > 0
        
        # Concurrent execution should be efficient
        assert total_time < concurrent_tasks * 3.0  # Better than sequential
