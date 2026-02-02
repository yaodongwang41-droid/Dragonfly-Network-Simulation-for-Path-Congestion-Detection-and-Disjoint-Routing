# Path Congestion Detection and Disjoint Path for Dragonfly Networks (Experiment 1)

This repository contains the simulation source code for the paper:  
**"Path Congestion Detection and Disjoint Path for Improving Communication Efficiency in Dragonfly Interconnection Networks"** Published in *The Journal of Supercomputing* (2025).  
DOI: [10.1007/s11227-025-08083-z](https://link.springer.com/article/10.1007/s11227-025-08083-z)

This specific set of code corresponds to **Section 7.3 (Experiment 1)**, which investigates the impact of **global synchronization and bursty traffic** on network throughput over a continuous time series.

## 1. Research Context

In high-performance computing (HPC) environments, collective communication often leads to synchronized traffic patterns. This experiment simulates a scenario where the network transitions from a steady state to a high-load synchronized state. It measures how quickly different algorithms can recover from or mitigate the resulting congestion.



## 2. Implemented Strategies

The simulation compares five distinct approaches:

* **Basic (`normal.py`)**: Baseline routing. Shows how standard Dragonfly routing handles sudden traffic bursts.
* **DP (`dp.py`)**: Packet-Loss/Drop Policy. Evaluates if dropping packets can prevent catastrophic network saturation during synchronization.
* **QL (`ql.py`)**: Queue Length-based routing. Uses buffer occupancy to adjust routing but often suffers from "congestion lag."
* **PCD (`pcd.py`)**: Path Congestion Detection. Proactively stalls packet injection at the source based on end-to-end path status.
* **PCDDJ (`pccdj.py`)**: PCD with **Disjoint Paths**. The proposed optimal solution that utilizes non-overlapping paths to bypass synchronized congestion hotspots.

## 3. File Descriptions

* `ded_dict.py`: Generates the network topology dictionary and handles the `config` for source-destination pairs.
* `disjoint_path.py`: Contains the mathematical logic for Dragonfly routing and precomputing vertex-disjoint paths.
* `pccdj.py`, `pcd.py`, `ql.py`, `dp.py`, `normal.py`: Simulation engines that calculate throughput per cycle under the synchronization model.

## 4. Simulation Setup

As detailed in Section 7.3 (Simulation 1):
* **Topology**: Dragonfly(k=4, m=8, l=5) with 1,312 nodes.
* **Synchronization Trigger**: At a specific cycle (e.g., cycle 220 in scripts), the traffic pattern changes or the load increases significantly to simulate global synchronization.
* **Buffer Size**: 12 packets per router.
* **Load ($\lambda$)**: 0.75 (representing heavy traffic).
* **Metric**: Throughput (number of received packets) recorded at each cycle.

## 5. How to Run

### Prerequisites
* Python 3.x
* NumPy

### Execution
To generate the throughput time-series data for the proposed PCDDJ algorithm:
```bash
python pccdj.py
```

The script will simulate the network over a period (e.g., 300+ cycles) and output the throughput values. These values correspond to the "Throughput vs. Time Cycle" graphs in Figure 11/12 of the paper.

## 6. Key Findings

Experiment 1 highlights the superiority of PCDDJ in maintaining stable throughput. While other algorithms like normal.py and ql.py experience a sharp decline in throughput (throughput collapse) once synchronization begins, PCDDJ maintains a high and steady packet delivery rate by effectively distributing traffic across disjoint paths.


