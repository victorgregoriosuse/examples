# SLE BCI container with NVIDIA CUDA-Q

This example demonstrates how to build and run **NVIDIA CUDA-Q** (the GPU-accelerated quantum-classical computing framework) natively using official, redistributable **SUSE Python 3.13 Base Container Images (SLE BCI)**.

---

## Example Overview

*   **Base Image**: `registry.suse.com/bci/python:3.13` (Official, secure, and redistributable SUSE Python container).
*   **Python Stack**: Uses the **native pre-installed Python 3.13** runtime included in the SUSE container directly, without copying external runtimes.
*   **Packages**: `cudaq` (NVIDIA CUDA Quantum framework), automatically installing standard dependencies like `cupy-cuda13x`, `custatevec`, and CUDA-X libraries via Pip.
*   **Verification**: Models a **Bell Pair (maximally entangled 2-qubit state)** quantum circuit, running a 1000-shot high-performance simulation.

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
Unlike core GPU packages like RAPIDS cuOpt, **CUDA Quantum includes a highly optimized, multi-threaded CPU-based simulator backend** (`qpp`) by default. This means you can run, simulate, and fully solve quantum circuits **directly on your local laptop (including Apple Silicon Macs) without requiring a physical NVIDIA GPU!**

```bash
docker run --rm bci-q:latest
```

*   **Expected Output on CPU Systems:**
    ```text
    ✓ Successfully imported CUDA-Q!
    Defining a 2-qubit Bell Pair quantum circuit...
    Running quantum simulation (sampling 1000 shots on default CPU backend)...

    ✓ Quantum Simulation Completed Successfully!
    Measurement Results (Counts):
    { 00:508 11:492 }
    Successfully verified quantum superposition and entanglement!
    ```

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

---

## References

*   **[SLE Base Container Images (BCI)](https://www.suse.com/products/base-container-images/)**
*   **[NVIDIA CUDA Quantum (CUDA-Q) Framework](https://nvidia.github.io/cuda-quantum/)**
*   **[NVIDIA Container Toolkit Installation](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)**
