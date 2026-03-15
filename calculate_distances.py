"""
Coordinates Distance Pipeline
Calculates distances between a sample and reference points in N-dimensional space.
Supports any coordinate system regardless of the number of dimensions.
"""

import csv
import sys
import math
from pathlib import Path


def parse_sample(raw: str) -> tuple[str, list[float]]:
    """Parse a raw coordinate string into (label, coordinates)."""
    parts = raw.strip().split(",")
    label = parts[0]
    coords = [float(x) for x in parts[1:]]
    return label, coords


def load_references(filepath: str) -> list[tuple[str, list[float]]]:
    """Load reference points from a text file (one per line, same format as sample)."""
    refs = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            label, coords = parse_sample(line)
            refs.append((label, coords))
    return refs


def euclidean_distance(a: list[float], b: list[float]) -> float:
    """Calculate Euclidean distance between two coordinate vectors."""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def chebyshev_distance(a: list[float], b: list[float]) -> float:
    """Calculate Chebyshev distance (max absolute difference) between two vectors."""
    return max(abs(x - y) for x, y in zip(a, b))


DISTANCE_FUNCTIONS = {
    "euclidean": euclidean_distance,
    "chebyshev": chebyshev_distance,
}


def calculate_distances(
    sample_coords: list[float],
    references: list[tuple[str, list[float]]],
    metric: str = "euclidean",
) -> list[tuple[float, str]]:
    """Calculate distances from sample to all references. Returns sorted list of (distance, label)."""
    dist_fn = DISTANCE_FUNCTIONS.get(metric)
    if not dist_fn:
        raise ValueError(f"Unknown metric '{metric}'. Available: {list(DISTANCE_FUNCTIONS.keys())}")

    results = []
    for ref_label, ref_coords in references:
        if len(ref_coords) != len(sample_coords):
            print(f"Warning: skipping {ref_label} (expected {len(sample_coords)} dimensions, got {len(ref_coords)})")
            continue
        dist = dist_fn(sample_coords, ref_coords)
        results.append((dist, ref_label))

    results.sort(key=lambda x: x[0])
    return results


def write_csv(results: list[tuple[float, str]], output_path: str) -> None:
    """Write ranked distances to CSV."""
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["distance", "label"])
        for dist, label in results:
            writer.writerow([dist, label])


def main():
    if len(sys.argv) < 3:
        print("Usage: python calculate_distances.py <reference_file> <sample_string> [metric] [output_file]")
        print("  metric: euclidean (default), chebyshev")
        print()
        print("Example:")
        print('  python calculate_distances.py references/sample_data.txt "Point_A,0.5,1.2,0.8" euclidean output.csv')
        sys.exit(1)

    ref_file = sys.argv[1]
    sample_raw = sys.argv[2]
    metric = sys.argv[3] if len(sys.argv) > 3 else "euclidean"
    output_file = sys.argv[4] if len(sys.argv) > 4 else None

    # Parse sample
    sample_label, sample_coords = parse_sample(sample_raw)
    print(f"Sample: {sample_label} ({len(sample_coords)} dimensions)")
    print(f"Metric: {metric}")

    # Load references
    references = load_references(ref_file)
    print(f"Loaded {len(references)} reference points")

    # Calculate
    results = calculate_distances(sample_coords, references, metric)

    # Output
    if output_file:
        write_csv(results, output_file)
        print(f"Results written to {output_file}")
    else:
        print(f"\ndistance;label")
        for dist, label in results:
            print(f"{dist};{label}")


if __name__ == "__main__":
    main()