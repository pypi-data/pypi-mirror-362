import time
import csv
import io
import random
import string
import nsv


def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    return ''.join(random.choices(string.ascii_letters, k=length))


def create_test_data(rows, cols):
    """Create test data with the specified number of rows and columns."""
    return [[generate_random_string() for _ in range(cols)] for _ in range(rows)]


def benchmark_csv_write(data, iterations=5):
    """Benchmark CSV writing performance."""
    total_time = 0
    for _ in range(iterations):
        output = io.StringIO()
        start_time = time.time()
        writer = csv.writer(output)
        writer.writerows(data)
        end_time = time.time()
        total_time += (end_time - start_time)
    return total_time / iterations


def benchmark_nsv_write(data, iterations=5):
    """Benchmark NSV writing performance."""
    total_time = 0
    for _ in range(iterations):
        output = io.StringIO()
        start_time = time.time()
        nsv.dump(data, output)
        end_time = time.time()
        total_time += (end_time - start_time)
    return total_time / iterations


def benchmark_csv_read(data, iterations=5):
    """Benchmark CSV reading performance."""
    # First, write the data to a string
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(data)
    csv_string = output.getvalue()

    total_time = 0
    for _ in range(iterations):
        input_file = io.StringIO(csv_string)
        start_time = time.time()
        reader = csv.reader(input_file)
        rows = list(reader)
        end_time = time.time()
        total_time += (end_time - start_time)
    return total_time / iterations


def benchmark_nsv_read(data, iterations=5):
    """Benchmark NSV reading performance."""
    # First, write the data to a string
    output = io.StringIO()
    nsv.dump(data, output)
    nsv_string = output.getvalue()

    total_time = 0
    for _ in range(iterations):
        input_file = io.StringIO(nsv_string)
        start_time = time.time()
        rows = nsv.load(input_file)
        end_time = time.time()
        total_time += (end_time - start_time)
    return total_time / iterations


def run_benchmarks():
    """Run all benchmarks and print results."""
    test_sizes = [
        (100, 5),  # Small dataset
        (1000, 10),  # Medium dataset
        (10000, 20),  # Large dataset
        (50000, 20),  # Very large dataset
        (100000, 20),  # Extremely large dataset
    ]

    results = []

    for rows, cols in test_sizes:
        print(f"Benchmarking {rows}x{cols} dataset...")
        data = create_test_data(rows, cols)

        # Writing benchmarks
        csv_write_time = benchmark_csv_write(data)
        nsv_write_time = benchmark_nsv_write(data)
        write_ratio = nsv_write_time / csv_write_time

        results.append((f"{rows}x{cols}", "Write", csv_write_time, nsv_write_time, write_ratio))

        # Reading benchmarks
        csv_read_time = benchmark_csv_read(data)
        nsv_read_time = benchmark_nsv_read(data)
        read_ratio = nsv_read_time / csv_read_time

        results.append((f"{rows}x{cols}", "Read", csv_read_time, nsv_read_time, read_ratio))

    # Print results in a nicely formatted table
    print("\nBenchmark Results:\n")
    print("┌──────────────┬───────────┬─────────────┬─────────────┬───────────────┐")
    print("│ Dataset Size │ Operation │ CSV Time(s) │ NSV Time(s) │ NSV/CSV Ratio │")
    print("├──────────────┼───────────┼─────────────┼─────────────┼───────────────┤")

    for size, op, csv_time, nsv_time, ratio in results:
        print(f"│ {size:<12} │ {op:<9} │ {csv_time:>11.6f} │ {nsv_time:>11.6f} │ {ratio:>13.2f} │")

    print("└──────────────┴───────────┴─────────────┴─────────────┴───────────────┘")


def generate_complex_data(rows, cols, multiline_prob=0.1, long_text_prob=0.1):
    """Generate test data with occasional multiline text and long values."""
    data = []
    for i in range(rows):
        row = []
        for j in range(cols):
            # Decide what type of data to generate
            if random.random() < multiline_prob:
                # Generate text with embedded newlines (which CSV would need to escape)
                lines = random.randint(2, 4)
                value = '\n'.join(generate_random_string(random.randint(5, 15))
                                  for _ in range(lines))
                # For CSV, we'd need to escape this; for NSV, we sanitize newlines
                value = value.replace('\n', '\\n')  # Sanitize for NSV
            elif random.random() < long_text_prob:
                # Generate long text
                value = generate_random_string(random.randint(100, 500))
            else:
                # Generate regular text
                value = generate_random_string(random.randint(5, 20))
            row.append(value)
        data.append(row)
    return data


def run_complex_benchmarks():
    """Run benchmarks with more complex data."""
    test_cases = [
        ("Regular", 5000, 10, 0, 0),  # Standard data
        ("Long Values", 5000, 10, 0, 0.2),  # 20% long values
        ("Multiline", 5000, 10, 0.2, 0),  # 20% multiline text
        ("Mixed", 5000, 10, 0.1, 0.1),  # Mixed complex data
        ("Complex Large", 10000, 20, 0.1, 0.1)  # Large complex dataset
    ]

    results = []

    for name, rows, cols, multiline_prob, long_text_prob in test_cases:
        print(f"Benchmarking {name} dataset ({rows}x{cols})...")
        data = generate_complex_data(rows, cols, multiline_prob, long_text_prob)

        # Writing benchmarks
        csv_write_time = benchmark_csv_write(data)
        nsv_write_time = benchmark_nsv_write(data)
        write_ratio = nsv_write_time / csv_write_time

        results.append((name, "Write", csv_write_time, nsv_write_time, write_ratio))

        # Reading benchmarks
        csv_read_time = benchmark_csv_read(data)
        nsv_read_time = benchmark_nsv_read(data)
        read_ratio = nsv_read_time / csv_read_time

        results.append((name, "Read", csv_read_time, nsv_read_time, read_ratio))

    # Print results in a nicely formatted table
    print("\nComplex Data Benchmark Results:\n")
    print("┌────────────────┬───────────┬─────────────┬─────────────┬──────────────┐")
    print("│ Data Type      │ Operation │ CSV Time(s) │ NSV Time(s) │ NSV/CSV Ratio│")
    print("├────────────────┼───────────┼─────────────┼─────────────┼──────────────┤")

    for type_, op, csv_time, nsv_time, ratio in results:
        print(f"│ {type_:<14} │ {op:<9} │ {csv_time:>11.6f} │ {nsv_time:>11.6f} │ {ratio:>12.2f} │")

    print("└────────────────┴───────────┴─────────────┴─────────────┴──────────────┘")

if __name__ == "__main__":
    run_benchmarks()
    run_complex_benchmarks()

# Benchmarking 100x5 dataset...
# Benchmarking 1000x10 dataset...
# Benchmarking 10000x20 dataset...
# Benchmarking 50000x20 dataset...
# Benchmarking 100000x20 dataset...
#
# Benchmark Results:
#
# ┌──────────────┬───────────┬─────────────┬─────────────┬───────────────┐
# │ Dataset Size │ Operation │ CSV Time(s) │ NSV Time(s) │ NSV/CSV Ratio │
# ├──────────────┼───────────┼─────────────┼─────────────┼───────────────┤
# │ 100x5        │ Write     │    0.000114 │    0.000089 │          0.78 │
# │ 100x5        │ Read      │    0.000078 │    0.000133 │          1.71 │
# │ 1000x10      │ Write     │    0.001670 │    0.001062 │          0.64 │
# │ 1000x10      │ Read      │    0.001295 │    0.002003 │          1.55 │
# │ 10000x20     │ Write     │    0.026352 │    0.014950 │          0.57 │
# │ 10000x20     │ Read      │    0.023674 │    0.036578 │          1.55 │
# │ 50000x20     │ Write     │    0.131118 │    0.078517 │          0.60 │
# │ 50000x20     │ Read      │    0.127514 │    0.191078 │          1.50 │
# │ 100000x20    │ Write     │    0.266915 │    0.155984 │          0.58 │
# │ 100000x20    │ Read      │    0.270458 │    0.392992 │          1.45 │
# └──────────────┴───────────┴─────────────┴─────────────┴───────────────┘
# Benchmarking Regular dataset (5000x10)...
# Benchmarking Long Values dataset (5000x10)...
# Benchmarking Multiline dataset (5000x10)...
# Benchmarking Mixed dataset (5000x10)...
# Benchmarking Complex Large dataset (10000x20)...
#
# Complex Data Benchmark Results:
#
# ┌────────────────┬───────────┬─────────────┬─────────────┬──────────────┐
# │ Data Type      │ Operation │ CSV Time(s) │ NSV Time(s) │ NSV/CSV Ratio│
# ├────────────────┼───────────┼─────────────┼─────────────┼──────────────┤
# │ Regular        │ Write     │    0.008221 │    0.005450 │         0.66 │
# │ Regular        │ Read      │    0.007457 │    0.011107 │         1.49 │
# │ Long Values    │ Write     │    0.036832 │    0.005852 │         0.16 │
# │ Long Values    │ Read      │    0.028319 │    0.013665 │         0.48 │
# │ Multiline      │ Write     │    0.010284 │    0.005504 │         0.54 │
# │ Multiline      │ Read      │    0.009078 │    0.010720 │         1.18 │
# │ Mixed          │ Write     │    0.022973 │    0.005561 │         0.24 │
# │ Mixed          │ Read      │    0.018129 │    0.011969 │         0.66 │
# │ Complex Large  │ Write     │    0.089767 │    0.019619 │         0.22 │
# │ Complex Large  │ Read      │    0.069776 │    0.049330 │         0.71 │
# └────────────────┴───────────┴─────────────┴─────────────┴──────────────┘
