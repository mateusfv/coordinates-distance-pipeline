# coordinates-distance-pipeline

Calculates distances between coordinate samples and reference points in N-dimensional space.

Supports any coordinate system regardless of the number of dimensions, as long as sample and reference have the same count.

## Distance metrics

- **Euclidean** (default) — straight-line distance in N-dimensional space
- **Chebyshev** — maximum absolute difference across all dimensions
- More to come

## Usage

```bash
python calculate_distances.py <reference_file> <sample_string> [metric] [output_file]
```

### Examples

Calculate Euclidean distances and print to terminal:
```bash
python calculate_distances.py references/sample_data.txt "Sample_A,0.092,0.101,-0.045,-0.030,-0.019,-0.012,0.001,-0.003,-0.004,0.006,0.0,-0.001,0.001,0.001,-0.007,0.005,0.006,0.007,0.001,-0.003,-0.003,-0.002,-0.004,-0.006,-0.002"
```

Calculate Chebyshev distances and save to file:
```bash
python calculate_distances.py references/sample_data.txt "Sample_A,0.092,0.101,..." chebyshev output.csv
```

### Output format

```
distance;label
0.021342;Cluster_A
0.022854;Cluster_B
0.030821;Cluster_C
```

## Reference files

Place reference files in the `references/` directory. Each line follows the format:

```
Label,coord1,coord2,coord3,...
```

The number of coordinates must match the sample input.
