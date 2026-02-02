# Path Congestion Detection and Disjoint Path for Dragonfly Networks

This sub-repository contains the simulation code for the paper **"Path Congestion Detection and Disjoint Path for Improving Communication Efficiency in Dragonfly Interconnection Networks"**Published in *The Journal of Supercomputing* (2025).  
DOI: [10.1007/s11227-025-08083-z](https://link.springer.com/article/10.1007/s11227-025-08083-z). 

The project evaluates various routing and congestion control algorithms specifically designed for the Dragonfly topology, corresponding to the simulation experiments described in **Section 7.2** of the paper.

## 1. Project Overview

Path congestion is a critical bottleneck in Dragonfly networks, leading to buffer contention and increased latency. This project implements and compares several strategies to mitigate these issues, ranging from basic routing to advanced path-sensing and disjoint-path switching mechanisms.

## 2. Implemented Algorithms

The repository includes five main simulation models:

* **Normal (Baseline Routing)**: Standard Dragonfly routing as defined in Algorithm 1.
* **DP (Drop Packets)**: A mechanism that regulates traffic by selectively dropping packets when severe congestion is detected.
* **QL (Queue Length)**: A routing strategy that uses the local buffer queue length as a metric to make routing decisions.
* **PCD (Path Congestion Detection)**: Our proposed algorithm that monitors the buffer status along the entire path before releasing packets from the source node.
* **PCDDJ (PCD with Disjoint Paths)**: Our enhanced algorithm that combines PCD with precomputed **Disjoint Paths**. If the primary path is congested, the system immediately switches to a non-overlapping alternative path to maintain throughput.



## 3. Repository Structure

* `disjoint_path.py`: Core utility for Dragonfly topology generation, neighbor discovery, and calculating vertex-disjoint paths.
* `ded_dict.py`: Topology configuration script that builds the network dictionary and handles node/router mapping.
* `normal.py`: Simulation for the **Basic** routing algorithm.
* `dp.py`: Simulation for the **DP** (Drop Packets) algorithm.
* `ql.py`: Simulation for the **QL** (Queue Length) algorithm.
* `pcd.py`: Simulation for the **PCD** (Path Congestion Detection) algorithm.
* `pccdj.py`: Simulation for the **PCDDJ** (Disjoint Path + PCD) algorithm.

## 4. Simulation Setup

Based on the parameters in Section 7.2, the default configuration is:
* **Topology**: Dragonfly(k, m, l)
* **Parameters**: $k=4$, $m=8$, $l=5$
* **Buffer Size**: 12 packets per router.
* **Traffic Load**: 600 injected packets (Offered Load).
* **Metrics**: Latency distribution and throughput distribution.

## 5. How to Run

Requirements: `Python 3.x`, `numpy`.

To run a specific simulation (e.g., the PCDDJ algorithm):
```bash
python pccdj.py
```
The script will output the simulation progress (cycle counts) and generate data for:

* Latency Distribution: Statistical spread of packet delivery times.

* Throughput Distribution: Packet reception rates over time.

## 6. Key Findings
As demonstrated in the paper, the PCDDJ algorithm significantly outperforms traditional methods under high-concurrency HPC workloads. By utilizing disjoint paths and global congestion sensing, it effectively prevents "congestion spreading" and stabilizes network latency even as the offered load increases.

## 7. Key Findings
If you use this code or refer to the paper in your research, please cite from doi:https://doi.org/10.1007/s11227-025-08083-z


