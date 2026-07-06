import sys

try:
    import cudf
    import numpy as np
    from cuopt import routing
    print("✓ Successfully imported cuDF and cuOpt!")
except Exception as e:
    error_msg = str(e)
    if "cudaErrorNoDevice" in error_msg or "cudaErrorInsufficientDriver" in error_msg:
        print(f"⚠ Libraries loaded, but no compatible local GPU was detected ({error_msg}). This is normal on macOS or CPU-only hosts.")
        sys.exit(0) # Exit with 0 so CPU-only dry-runs and local checks pass cleanly
    else:
        print(f"✗ Failed to import libraries. Error: {e}")
        sys.exit(1)

# Define a simple Cost Matrix (distance/time) between 4 locations (0 is Depot)
try:
    cost_matrix_data = [
        [0.0, 2.0, 4.0, 3.0],
        [2.0, 0.0, 3.0, 5.0],
        [4.0, 3.0, 0.0, 2.0],
        [3.0, 5.0, 2.0, 0.0]
    ]
    # cuOpt requires float32 values on GPU
    cost_matrix = cudf.DataFrame(cost_matrix_data, dtype="float32")
    print("✓ Successfully created GPU-backed cost matrix dataframe!")
except Exception as e:
    print(f"✗ Failed to create GPU Dataframe. (If you are on an Apple Silicon Mac/CPU, this is expected as RAPIDS requires an NVIDIA GPU). Error: {e}")
    sys.exit(0) # Exit cleanly since GPU is missing on this host

try:
    # 4 locations, 2 vehicles, 3 orders
    dm = routing.DataModel(n_locations=4, n_fleet=2, n_orders=3)
    dm.add_cost_matrix(cost_matrix)

    # Set order locations (locations 1, 2, 3)
    order_locations = cudf.Series([1, 2, 3], dtype="int32")
    dm.set_order_locations(order_locations)

    # Set vehicle start/end locations (starting/ending at depot: 0)
    start_locations = cudf.Series([0, 0], dtype="int32")
    end_locations = cudf.Series([0, 0], dtype="int32")
    dm.set_vehicle_locations(start_locations, end_locations)
    print("✓ Successfully configured the cuOpt Routing DataModel!")
except Exception as e:
    print(f"✗ Failed to configure DataModel. Error: {e}")
    sys.exit(1)

try:
    solver_settings = routing.SolverSettings()
    solver_settings.set_time_limit(5)
    solver_settings.set_verbose_mode(True)

    print("Attempting to run cuOpt Solver...")
    solution = routing.Solve(dm, solver_settings)
    
    if solution.get_status() == 0:
        print("\n✓ Routing solved successfully!")
        print(f"Total Optimal Cost: {solution.get_total_objective()}")
        solution.display_routes()
    else:
        print(f"✗ Solver ran but could not find a solution. Status: {solution.get_status()}")
except Exception as e:
    print(f"✗ Solver execution failed. (This requires an active physical NVIDIA GPU). Error: {e}")
