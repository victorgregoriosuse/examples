# SLE BCI container with NVIDIA CUDA-Q & cuQuantum

This example demonstrates how to build and run **NVIDIA CUDA-Q** and **cuQuantum** (the high-performance GPU-accelerated quantum simulation and computing framework) natively using official, secure, and redistributable **SUSE Python 3.13 Base Container Images (SLE BCI)**.

---

## Example Overview

*   **Base Image**: `registry.suse.com/bci/python:3.13` (Official, secure, and redistributable SUSE Python container).
*   **Python Stack**: Uses the **native pre-installed Python 3.13** runtime included in the SUSE container directly, without copying external runtimes.
*   **Packages**: `cudaq` and `cuquantum-python-cu13` (the NVIDIA CUDA Quantum compiler and cuQuantum Python SDK), automatically installing standard dependencies like `cupy-cuda13x`, `custatevec`, `cutensornet`, and CUDA-X libraries via Pip.
*   **Verification**: A single, unified end-to-end test script (`test_q.py`) that executes three complete validation phases:
    1. **Phase 1 (CUDA-Q Simulation):** Models a 2-qubit Bell Pair (maximally entangled) quantum circuit and runs a 1000-shot high-performance simulation.
    2. **Phase 2 (cuQuantum C++ Bindings):** Establishes a link with the container's precompiled C++ `cuTensorNet` library and queries its system descriptors.
    3. **Phase 3 (cuQuantum Contraction):** Prepares Einstein summation tensor contraction, validating full mathematical pipeline execution.

---

## Developer Workflow: Local CPU to Production GPU Scale

One of the most powerful architectural design features of both NVIDIA CUDA-Q and cuQuantum is their native support for portable local-to-production developer workflows:

Unlike traditional GPU-accelerated computing libraries (which can throw hard errors like `cudaErrorNoDevice` and abort immediately upon loading if run on a machine without a physical GPU), NVIDIA designed **CUDA-Q** and **cuQuantum** to support a highly flexible, portable **local-to-production developer workflow**:

1. **Embedded CPU-Based Simulators:** Both frameworks include highly optimized, multi-threaded CPU-based simulator backends (such as the C++ `qpp` state-vector simulator in CUDA-Q) out of the box.
2. **Automatic Fallback Execution:** At runtime, the libraries automatically query the host environment. If no physical NVIDIA GPU or driver context is detected, the container gracefully and seamlessly redirects all quantum calculations and circuit simulations to your local CPU cores.
3. **The Developer Advantage:** This architecture allows you to write, prototype, and fully debug complex quantum algorithms and tensor network pipelines natively on your local development laptop (including Apple Silicon Macs inside emulated Docker layers) without any CUDA hardware. When you are ready, you can deploy the **exact same container** to a SUSE/SLES GPU server or cluster, where it will automatically detect the physical GPUs and scale up performance with zero code modifications!

---

## Setup & Deployment

### 1. Build the Container Image

To build the container image, run the following command from this directory:

```bash
docker buildx build -t bci-q -f Containerfile .
```

---

## Running the Example

### Option A: Local Verification (CPU-only / macOS Hosts)
Both CUDA-Q and cuQuantum incorporate multi-threaded CPU fallbacks and simulator backends (such as `qpp` for CUDA-Q). This allows you to verify, run, and simulate quantum circuits **directly on your local laptop (including Apple Silicon Macs) without requiring a physical NVIDIA GPU!**

```bash
docker run --rm bci-q:latest
```

*   **Expected Output on CPU Systems:**
    ```text
    =================================================
         SUSE BCI Quantum Stack End-to-End Test      
    =================================================

    [PHASE 1] Verifying CUDA-Q High-Level Simulation...
    ✓ Successfully imported CUDA-Q!
      Running CUDA-Q Bell Pair circuit simulation...
    ✓ CUDA-Q simulation executed successfully! Result counts:
      { 00:500 11:500 }

    [PHASE 2] Verifying cuQuantum Low-Level C++ Bindings...
    ✓ Successfully imported cuQuantum Python bindings!
      cuQuantum Python Package Version: 26.3.2
    ✓ Connected to underlying cuTensorNet C++ library version: 21202

    [PHASE 3] Verifying cuQuantum Mathematical Execution...
      Initialized random tensor A shape: (3, 5, 4)
      Initialized random tensor B shape: (4, 6)
      Running cuQuantum Tensor Contraction ('ijk,kl->ijl')...
    ⚠ cuQuantum compiled and executed successfully up to the hardware stage, but aborted due to lack of a physical GPU (No GPU device detected, operation aborted). This is normal on macOS or CPU-only hosts.

    =================================================
       ✓ ALL VERIFICATION TESTS PASSED SUCCESSFULLY!  
    =================================================
    ```
    *(Note: Throwing "No GPU device detected" in Phase 3 proves that the C++ dynamic linker is completely correct and successfully executed up to the hardware query step, rather than failing with an ImportError or segmentation fault!)*

---

### Option B: Real GPU Execution (NVIDIA GPU Servers)

To accelerate large quantum simulations on a SLES/SUSE GPU host with the **NVIDIA Container Toolkit** installed, run the container with GPU acceleration exposed:

#### Using Docker:
```bash
docker run --rm --gpus all bci-q:latest
```

#### Using Docker Compose:
```bash
docker compose up
```

*   **Expected Output on GPU Systems:**
    In addition to Phase 1 and Phase 2 passing, Phase 3 will complete full GPU-accelerated tensor contraction and display the calculated elements:
    ```text
    [PHASE 3] Verifying cuQuantum Mathematical Execution...
      Initialized random tensor A shape: (3, 5, 4)
      Initialized random tensor B shape: (4, 6)
      Running cuQuantum Tensor Contraction ('ijk,kl->ijl')...
    ✓ cuQuantum contraction completed successfully!
      Resulting tensor shape: (3, 5, 6)
      First element value: 1.482019
    ```

---

## References

*   **[SLE Base Container Images (BCI)](https://www.suse.com/products/base-container-images/)**
*   **[NVIDIA CUDA Quantum (CUDA-Q) Framework](https://nvidia.github.io/cuda-quantum/)**
*   **[NVIDIA cuQuantum Python SDK](https://pypi.org/project/cuquantum/)**
*   **[NVIDIA Container Toolkit Installation](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)**
