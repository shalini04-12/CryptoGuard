import csv
import json
import time
from pathlib import Path

from qiskit import QuantumCircuit, transpile


# CryptoGuard preliminary architecture benchmark
# Illustrative configurations only.
# Replace them with the official challenge definitions before
# claiming official Processor A/B benchmark results.

ROOT = Path(__file__).resolve().parent.parent
PROCESSOR_DIR = ROOT / "processors"
RESULTS_DIR = ROOT / "results" / "tables"

BASIS_GATES = ["rz", "sx", "x", "cx"]

DEMO_CONFIGS = {
    "Processor A": {
        "num_qubits": 5,
        "coupling_map": [[0, 1], [1, 2], [2, 3], [3, 4]],
        "basis_gates": BASIS_GATES,
    },
    "Processor B": {
        "num_qubits": 7,
        "coupling_map": [
            [0, 1], [1, 2], [2, 3],
            [3, 4], [2, 5], [5, 6]
        ],
        "basis_gates": BASIS_GATES,
    },
}


def load_processor(name):
    path = PROCESSOR_DIR / f"{name}.json"

    with path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    demo = DEMO_CONFIGS[
        "Processor A" if name == "processor_A" else "Processor B"
    ]

    # Use demonstration settings only when official values are missing.
    missing = (
        not config.get("coupling_map")
        or not config.get("basis_gates")
    )

    if missing:
        config["coupling_map"] = demo["coupling_map"]
        config["basis_gates"] = demo["basis_gates"]
        config["benchmark_status"] = "PRELIMINARY_ILLUSTRATIVE"
    else:
        config["benchmark_status"] = "CONFIGURATION_LOADED"

    if config.get("num_qubits") is None:
        config["num_qubits"] = demo["num_qubits"]

    return config


def create_test_circuit():
    """Same five-qubit architecture test for both processors."""

    circuit = QuantumCircuit(5)

    circuit.h(0)
    circuit.h(2)

    # Interactions that help reveal connectivity and routing effects.
    circuit.cx(0, 4)
    circuit.cx(1, 3)
    circuit.cx(2, 4)
    circuit.rz(0.785398, 4)
    circuit.cx(0, 2)

    return circuit


def run_benchmark(processor_name):
    config = load_processor(processor_name)
    circuit = create_test_circuit()

    start = time.perf_counter()

    compiled = transpile(
        circuit,
        basis_gates=config["basis_gates"],
        coupling_map=config["coupling_map"],
        optimization_level=1,
        seed_transpiler=42,
    )

    compile_time = time.perf_counter() - start

    operations = compiled.count_ops()

    two_qubit_gates = sum(
        count
        for gate, count in operations.items()
        if gate in {"cx", "cz", "ecr"}
    )

    return {
        "processor": config["processor_name"],
        "qubits_available": config["num_qubits"],
        "logical_qubits": circuit.num_qubits,
        "circuit_depth": compiled.depth(),
        "two_qubit_gates": two_qubit_gates,
        "swap_count": operations.get("swap", 0),
        "transpilation_time_seconds": round(compile_time, 6),
        "benchmark_status": config["benchmark_status"],
    }


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    results = []

    for name in ("processor_A", "processor_B"):
        try:
            result = run_benchmark(name)
            results.append(result)

            print(f"\n{result['processor']}")
            for key, value in result.items():
                print(f"  {key}: {value}")

        except Exception as error:
            print(f"\nError benchmarking {name}: {error}")
            print("Check the processor configuration and Qiskit installation.")
            return

    output_file = RESULTS_DIR / "processor_comparison.csv"

    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print("\nBenchmark completed.")
    print(f"Results saved to: {output_file}")

    if any(
        result["benchmark_status"] == "PRELIMINARY_ILLUSTRATIVE"
        for result in results
    ):
        print(
            "\nIMPORTANT: These are preliminary software measurements "
            "using illustrative connectivity. They are NOT official "
            "challenge benchmark results."
        )


if __name__ == "__main__":
    main()