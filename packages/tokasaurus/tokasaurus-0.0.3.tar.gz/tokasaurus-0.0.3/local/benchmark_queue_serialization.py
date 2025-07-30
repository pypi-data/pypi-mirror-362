#!/usr/bin/env python3

import multiprocessing as mp
import time
from typing import Tuple, Union

import numpy as np
import pydra
import torch


class BenchmarkConfig(pydra.Config):
    data_type: str = "list"  # list, numpy, torch
    dimensions: list[int] = [1000]  # e.g., [1000] for 1D, [100, 100] for 2D
    num_iterations: int = 100
    num_warmup_iterations: int = 10
    dtype: str = "float32"  # float32, float64, int32, int64


def create_data(config: BenchmarkConfig) -> Union[list, np.ndarray, torch.Tensor]:
    """Create data structure based on config."""
    shape = config.dimensions
    total_elements = 1
    for dim in shape:
        total_elements *= dim

    # Create base data
    if config.dtype in ["float32", "float64"]:
        base_data = np.random.randn(total_elements).astype(
            np.float32 if config.dtype == "float32" else np.float64
        )
    else:
        base_data = np.random.randint(0, 100, total_elements).astype(
            np.int32 if config.dtype == "int32" else np.int64
        )

    # Reshape and convert to desired type
    if config.data_type == "list":
        data = base_data.reshape(shape).tolist()
        return data
    elif config.data_type == "numpy":
        return base_data.reshape(shape)
    elif config.data_type == "torch":
        return torch.from_numpy(base_data.reshape(shape))
    else:
        raise ValueError(f"Unknown data type: {config.data_type}")


def main(config: BenchmarkConfig):
    print(f"Benchmarking {config.data_type} with dimensions {config.dimensions}")
    print(f"Data type: {config.dtype}, Iterations: {config.num_iterations}")

    # Create data
    data = create_data(config)

    # Calculate data size
    if config.data_type == "list":
        import sys

        data_size = sys.getsizeof(data)
    elif config.data_type == "numpy":
        data_size = data.nbytes
    elif config.data_type == "torch":
        data_size = data.element_size() * data.numel()

    total_elements = 1
    for dim in config.dimensions:
        total_elements *= dim

    print(f"Total elements: {total_elements:,}")
    print(f"Approximate data size: {data_size / 1024 / 1024:.2f} MB")

    # Create queue
    queue = mp.Queue()

    # Warm up
    for _ in range(config.num_warmup_iterations):
        queue.put(data)
        _ = queue.get()

    # Benchmark put operations
    put_times = []
    for _ in range(config.num_iterations):
        start = time.perf_counter()
        queue.put(data)
        end = time.perf_counter()
        put_times.append(end - start)

    # Benchmark get operations
    get_times = []
    for _ in range(config.num_iterations):
        start = time.perf_counter()
        _ = queue.get()
        end = time.perf_counter()
        get_times.append(end - start)

    # Calculate statistics
    avg_put_time = sum(put_times) / len(put_times)
    avg_get_time = sum(get_times) / len(get_times)
    total_roundtrip_time = avg_put_time + avg_get_time

    # Calculate throughput
    put_throughput_mb_per_sec = (data_size / 1024 / 1024) / avg_put_time
    get_throughput_mb_per_sec = (data_size / 1024 / 1024) / avg_get_time
    roundtrip_throughput_mb_per_sec = (data_size / 1024 / 1024) / total_roundtrip_time

    print(f"\nResults:")
    print(
        f"Average put time: {avg_put_time * 1000:.3f} ms ({put_throughput_mb_per_sec:.2f} MB/s)"
    )
    print(
        f"Average get time: {avg_get_time * 1000:.3f} ms ({get_throughput_mb_per_sec:.2f} MB/s)"
    )
    print(
        f"Total roundtrip time: {total_roundtrip_time * 1000:.3f} ms ({roundtrip_throughput_mb_per_sec:.2f} MB/s)"
    )

    # Show min/max for variance
    print(
        f"\nPut time range: {min(put_times) * 1000:.3f} - {max(put_times) * 1000:.3f} ms"
    )
    print(
        f"Get time range: {min(get_times) * 1000:.3f} - {max(get_times) * 1000:.3f} ms"
    )


if __name__ == "__main__":
    pydra.run(main)
