# Path Congestion Detection and Disjoint Path for Dragonfly Networks (Experiment 3)

This sub-repository contains the simulation source code for the paper:  
**"Path Congestion Detection and Disjoint Path for Improving Communication Efficiency in Dragonfly Interconnection Networks"** Published in *The Journal of Supercomputing* (2025).  
DOI: [10.1007/s11227-025-08083-z](https://link.springer.com/article/10.1007/s11227-025-08083-z)

This specific set of code corresponds to **Section 7.3 (Simulation 3)**, which analyzes the network's resilience against **Global Synchronization and Bursty Traffic Patterns** in large-scale HPC workloads.

## 1. Research Context

In Experiment 3, the simulation creates a challenging environment where a sudden surge of traffic (global synchronization) is injected into the network at a specific time (Cycle 220). This experiment measures the "Throughput vs. Time Cycle" to observe how different congestion control mechanisms prevent the network from falling into a state of permanent saturation or "congestion collapse."



## 2. Implemented Strategies

The following routing and control algorithms are evaluated:

* **Basic (`normal.py`)**: Standard routing. Vulnerable to synchronization, often resulting in a sharp and sustained drop in throughput.
* **DP (`dp.py`)**: Drop Packets. Uses a drop-on-congestion mechanism to clear buffer space, though at the cost of reliable delivery.
* **QL (`ql.py`)**: Queue Length-based routing. Decisions are made based on local buffer occupancy.
* **PCD (`pcd.py`)**: Path Congestion Detection. Proactively manages packet injection by sensing congestion along the entire routing path.
* **PCDDJ (`pcddj.py`)**: **The Proposed Optimal Strategy**. Combines PCD with **Vertex-Disjoint Paths**. It dynamically switches to alternative, non-overlapping paths when the primary route is blocked, ensuring the highest stability during bursts.

## 3. File Descriptions

* `ded_dict.py`: Core topology configuration, node/router mapping, and multi-group traffic generation.
* `disjoint_path.py`: The algorithmic implementation for calculating multiple vertex-disjoint paths in the Dragonfly topology.
* `pcddj.py`, `pcd.py`, `ql.py`, `dp.py`, `normal.py`: Specific simulation scripts that model the throughput response under synchronized burst conditions.

## 4. Simulation Setup

As detailed in Section 7.3 (Experiment 3):
* **Network Parameters**: Dragonfly(k=4, m=8, l=5), comprising 1,312 nodes and 328 routers.
* **Max Buffer Size**: Set to 16 packets per router (increased from Experiment 1 to handle higher bursts).
* **Synchronization Trigger**: At Cycle 220, the offered load ($\lambda$) transitions to a high-concurrency state (e.g., $\lambda=0.75$).
* **Metric**: Real-time throughput (packets received per cycle) from Cycle 200 to Cycle 300.

## 5. How to Run

### Prerequisites
* Python 3.x
* NumPy
* Matplotlib (optional, for plotting results)

### Execution
To run the simulation for the proposed PCDDJ algorithm:
```bash
python pcddj.py
```

The script performs multiple iterations (e.g., num=100) to provide statistically significant averages. The output data reflects the network's ability to maintain throughput above the saturation floor during the synchronization phase.

## 6. Key Findings

The results from Experiment 3 show that PCDDJ is the most robust algorithm. While Normal and QL routing experience a "throughput collapse" shortly after the burst at Cycle 220, PCDDJ leverages its precomputed disjoint paths to bypass congested routers, maintaining a steady packet flow and significantly reducing the recovery time of the network.