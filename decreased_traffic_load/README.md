# Path Congestion Detection and Disjoint Path for Dragonfly Networks (Experiment 2)

This repository contains the simulation source code for the paper:  
**"Path Congestion Detection and Disjoint Path for Improving Communication Efficiency in Dragonfly Interconnection Networks"** Published in *The Journal of Supercomputing* (2025).  
DOI: [10.1007/s11227-025-08083-z](https://link.springer.com/article/10.1007/s11227-025-08083-z)

This specific set of code corresponds to **Section 7.3 (Simulation 2)**, which evaluates the network throughput and congestion stability under varying offered loads and global synchronization patterns.

## 1. Research Context

In Dragonfly networks, global synchronization and bursty traffic often lead to "congestion spreading." This experiment focuses on comparing how different routing and congestion control algorithms maintain throughput as the network load increases. 



## 2. Implemented Strategies

The following algorithms are evaluated in this simulation suite:

* **Basic (`normal.py`)**: Standard routing without advanced congestion awareness.
* **DP (`dp.py`)**: Packet-Loss/Drop Policy that regulates traffic by discarding packets during peak congestion.
* **QL (`ql.py`)**: Routing based on buffer Queue Length metrics.
* **PCD (`pcd.py`)**: Proposed Path Congestion Detection that stalls packet release at the source if the intended path is congested.
* **PCDDJ (`pccdj.py`)**: Our core contribution—combining PCD with **Disjoint Path** switching to bypass hotspots dynamically.

## 3. File Descriptions

* `ded_dict.py`: Topology dictionary generator and configuration handler.
* `disjoint_path.py`: Logic for calculating vertex-disjoint paths and neighbor discovery.
* `normal.py`, `dp.py`, `ql.py`, `pcd.py`, `pccdj.py`: Individual simulation scripts for each algorithm focusing on throughput metrics.

## 4. Simulation Parameters

As specified in Section 7.3 of the paper:
* **Topology**: Dragonfly(k=4, m=8, l=5).
* **Network Size**: 1,312 nodes.
* **Buffer Size**: 12 packets per router.
* **Simulation Duration**: Typically 150 to 300 cycles per run.
* **Offered Load ($\lambda$)**: Variable (e.g., 0.75 as shown in scripts) to measure the saturation point.

## 5. How to Run

### Prerequisites
* Python 3.x
* NumPy

### Execution
Run any of the main simulation files to generate throughput data:
```bash
python pccdj.py
```
The scripts are configured to repeat simulations (e.g., num = 100) to ensure statistical accuracy. The output provides the number of received packets per cycle, which is used to plot the throughput curves shown in the paper.

## 6. Key Results

Experiment 2 demonstrates that while standard algorithms (Basic, QL) suffer from a "throughput collapse" under high loads due to buffer saturation, the PCDDJ strategy maintains a stable and higher throughput by effectively utilizing alternative disjoint paths and preventing the injection of packets into already congested routes.

