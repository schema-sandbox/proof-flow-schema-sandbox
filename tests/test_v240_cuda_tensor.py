"""
Tests for ProofFlow v24.0 (High-Performance GPU/CUDA Parallel Matrix & Tensor Reduction Engine)

Covers:
    - CudaKernelDispatcher (GEMM kernel dispatch & GFLOPS estimation)
    - TensorDecompositionEngine (CP rank decomposition)
    - SparseMatrixSolver (Conjugate Gradient sparse solver)
    - GpuMemoryPoolManager (VRAM allocation and release)
"""

from __future__ import annotations

import pytest

from schemamath_api.cuda_tensor_engine import (
    CudaKernelDispatcher,
    GpuMemoryPoolManager,
    SparseMatrixSolver,
    TensorDecompositionEngine,
)


class TestCudaTensorEngine:
    def test_cuda_dispatcher_and_decomposition(self):
        dispatcher = CudaKernelDispatcher()
        lat = dispatcher.dispatch_gemm(1024, 1024, 1024)
        assert lat >= 0.0

        engine = TensorDecompositionEngine()
        res = engine.decompose_cp([100, 100, 100], rank=10)
        assert res.rank == 10
        assert res.reconstruction_error < 0.2

    def test_sparse_solver_and_vram_pool(self):
        solver = SparseMatrixSolver()
        res = solver.solve_cg(matrix_size=500)
        assert res.converged is True
        assert res.iterations > 0

        pool = GpuMemoryPoolManager(capacity_mb=1024)
        assert pool.allocate(500) is True
        assert pool.allocate(600) is False
        pool.free(500)
        assert pool.allocate(600) is True
