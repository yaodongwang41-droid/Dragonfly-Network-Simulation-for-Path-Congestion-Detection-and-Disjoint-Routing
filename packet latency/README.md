# Path Congestion Detection and Disjoint Path (PCDDJ) Simulation for Dragonfly Networks

This sub-repository contains the simulation framework and source code for the paper: **"Path Congestion Detection and Disjoint Path for Improving Communication Efficiency in Dragonfly Interconnection Networks"**.
DOI: [10.1007/s11227-025-08083-z](https://link.springer.com/article/10.1007/s11227-025-08083-z). 

The project evaluates several routing and congestion control strategies designed to mitigate path congestion in high-performance computing (HPC) systems using Dragonfly topologies.

##1. Project Overview

The Dragonfly network is a high-radix, low-diameter topology widely used in supercomputers. However, it is susceptible to path congestion, which leads to buffer contention. This project provides a Python-based simulation environment to test the following algorithms:

- **Basic**: Baseline Dragonfly routing (Algorithm 1 in the paper).
- **QL (Queue Length)**: Congestion management based on router queue lengths.
- **PCD (Path Congestion Detection)**: Detects buffer availability along the intended path before packet release.
- **DP (Drop Packets)**: Discarding packets when congestion occurs.
- **PCDDJ (Path Congestion Detection with Disjoint Paths)**: The proposed framework that combines real-time path monitoring with rapid rerouting via precomputed disjoint paths.

## 2. File Structure

### Core Modules
- `ded_dict.py`: Contains the Dragonfly topology generator, k-ary conversion utilities, and traffic configuration functions (`config`).
- `disjoint_path.py`: Implements the logic for pre-calculating edge-disjoint paths between any two nodes in a Dragonfly group.

### Simulation Scripts (Section 7.1)
Each script corresponds to a specific algorithm discussed in the experimental evaluation:
- `normal.py`: Baseline performance simulation.
- `ql.py`: Performance under Queue-Length-based congestion control.
- `pcd.py`: Performance under the path congestion detection algorithm.
- `dp.py`: Performance using the drop packets routing strategy.
- `pccdj.py`: The full implementation of the proposed PCDDJ algorithm.

## 3. Experimental Setup

The simulations are configured according to the parameters in **Section 7.1** of the paper:
- **Topology**: Dragonfly($k, m, l$) where $k=3, m=4, l=2$.
- **Traffic Load ($\lambda$)**: Iterates from 0.05 to 0.9 (18 data points).
- **Iterations**: Each data point is averaged over 100 simulation runs for statistical accuracy.
- **Metrics Evaluated**:
    - Average Packet Latency (Cycles)
    - Throughput
    - Received Ratio
    - Link Utilization Rate
    - Congested Path Percentage

## 4. Getting Started

### Prerequisites
- Python 3.x
- NumPy

```bash
pip install numpy
```

### Running the Simulations
To run a specific simulation (e.g., the PCDDJ algorithm), execute the corresponding script:

```bash
python latency_pccdj.py
```

The script will output real-time metrics for each traffic load $\lambda$ and save the final averaged results into .txt files (e.g., cycles_pccdj.txt, Throughput_pccdj.txt).

## 5. Results

The generated output files can be used to reproduce the performance curves shown in the paper, illustrating how PCDDJ maintains lower latency and higher throughput under heavy traffic loads compared to standard routing.