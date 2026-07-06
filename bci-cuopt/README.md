# SLE BCI container with NVIDIA cuOpt

This example demonstrates how to build and run **NVIDIA cuOpt** (the GPU-accelerated decision optimization engine) natively using official, redistributable **SUSE Python Base Container Images (SLE BCI)**.

---

## Example Overview

*   **Base Image**: `registry.suse.com/bci/python:3.11` (Official, secure, and redistributable SUSE Python container).
*   **Packages**: `cuopt-cu12` (GPU combinatorial routing engine and dynamic solvers), automatically installing standard dependencies like `cudf` and CUDA-X libraries via Pip.
*   **Verification**: Models a small **Vehicle Routing Problem (VRP)** consisting of 4 physical locations (including Depot), 2 vehicles, and 3 customer delivery orders.

---

## Setup & Deployment

### 1. Build the Container Image

To build the container image, run the following command from this directory:

```bash
docker buildx build -t bci-cuopt -f Containerfile .
```

---

## Running the Example

### Option A: Local Verification (Non-GPU / macOS Hosts)
Since local laptops or Apple Silicon Macs lack CUDA-capable physical NVIDIA GPUs, running the image locally validates that the image correctly boots up, loads Python 3.11, resolves, and loads all underlying compiled C/C++ core files (like `libcuopt.so` and `libcublas.so`) from their site-package folders successfully:

```bash
docker run --rm bci-cuopt:latest
```

*   **Expected Output on Non-GPU Systems:**
    ```text
    ✗ Failed to import libraries. Error: cudaErrorNoDevice: no CUDA-capable device is detected
    ```
    *(This is the correct result on a Mac; it proves Python and all deep C/C++ dependencies of cuOpt successfully bind together!)*

---

### Option B: Real GPU Execution (NVIDIA GPU Servers)

On a SLES/SUSE GPU host with the **NVIDIA Container Toolkit** installed, run the container with GPU acceleration exposed:

#### Using Docker:
```bash
docker run --rm --gpus all bci-cuopt:latest
```

#### Using Docker Compose:
```bash
docker compose up
```

*   **Expected Output on GPU Systems:**
    ```text
    ✓ Successfully imported cuDF and cuOpt!
    ✓ Successfully created GPU-backed cost matrix dataframe!
    ✓ Successfully configured the cuOpt Routing DataModel!
    Attempting to run cuOpt Solver...

    ✓ Routing solved successfully!
    Total Optimal Cost: 7.0
    Vehicle 0 Route:
      Depot (0) -> Location 1 -> Location 2 -> Depot (0)
    Vehicle 1 Route:
      Depot (0) -> Location 3 -> Depot (0)
    ```

---

## References

*   **[SLE Base Container Images (BCI)](https://www.suse.com/products/base-container-images/)**
*   **[NVIDIA cuOpt Python SDK](https://pypi.org/project/cuopt/)**
*   **[NVIDIA Container Toolkit Installation](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)**
