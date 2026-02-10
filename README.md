# Dragonfly Network Simulation for Path Congestion Detection and Disjoint Routing

This repository provides a cycle-accurate Python-based network simulator used to evaluate congestion-aware routing algorithms in **Dragonfly interconnection networks**, corresponding to **Section 7 (Evaluation)** of the paper:

**“Path Congestion Detection and Disjoint Path for Improving Communication Efficiency in Dragonfly Interconnection Networks”**  
Published in *The Journal of Supercomputing*  
https://link.springer.com/article/10.1007/s11227-025-08083-z

The codebase reproduces the experimental results on packet latency, packet distribution, and network behavior under varying traffic loads, as presented in the evaluation section of the paper.

---

## 1. Overview

The simulator models a regular Dragonfly topology with routers, buffers, links, and packet-level behavior. It is used to compare multiple routing and congestion-handling algorithms under identical configurations, including:

- Baseline Dragonfly routing
- Dropping Packets (DP)
- Queue Length–based control (QL)
- Path Congestion Detection (PCD)
- Path Congestion Detection with Disjoint Paths (PCDDJ)

All experiments are deterministic and repeatable, using fixed random seeds and averaged over multiple simulation runs.

---

## 2. Repository Structure

Each top-level directory corresponds directly to a subsection in **Section 7** of the paper:

```text
.
├── packet_latency/              # Section 7.1: Packet Latency
├── packet_distribution/         # Section 7.2: Packet Distribution
├── increased_traffic_load/      # Section 7.3 (Experiment 1): Increased Traffic Load
├── decreased_traffic_load/      # Section 7.3 (Experiment 2): Decreased Traffic Load
├── multi_groups/                # Section 7.3 (Experiment 3): Multiple Groups
.
```

## 3. Directory Description

### packet_latency/ (Section 7.1)

Evaluates average packet latency under different offered traffic loads λ.
This experiment focuses on how congestion-aware routing algorithms affect latency growth compared with baseline Dragonfly routing.

### packet_distribution/ (Section 7.2)

Analyzes packet distribution characteristics, showing how packets are spread across the network under different routing strategies.
This helps illustrate congestion concentration and load balancing behavior.

### increased_traffic_load/ (Section 7.3 – Experiment 1)

Simulates scenarios where the offered traffic load gradually increases, highlighting the robustness and scalability of each algorithm under rising congestion pressure.

### decreased_traffic_load/ (Section 7.3 – Experiment 2)

Evaluates system behavior when traffic load decreases after congestion, focusing on recovery speed and latency stabilization.

### multi_groups/ (Section 7.3 – Experiment 3)

Studies congestion behavior and routing performance in multi-group communication patterns, emphasizing the impact of global links and group-level congestion.


## 4. Common Code Components

Each directory contains:

- Five simulation scripts, each implementing a different routing or congestion-handling algorithm.

- Shared utility modules, reused across all experiments:

`ded_dict.py`
Prepares and initializes the simulation environment, including:

- Dragonfly topology construction

- Router and node ID generation

- Packet creation and injection parameters

`disjoint_path.py`
Implements the disjoint path routing logic, responsible for:

- Generating feasible node-disjoint paths for given source–destination pairs

- Supporting precomputation of disjoint path libraries


## 5. Simulation Environment

All experiments are conducted using:

- A cycle-accurate Python simulator

- Deterministic configurations with fixed random seeds

- Multiple repeated runs (≥100) with averaged results

The default configuration matches the paper:

- * **Topology**: dragonfly(4, 8, 5)

- * **Routers**: 328 

- * **Nodes**: 1312 

- * **Buffer capacity**: 12 packets

- * **Traffic pattern**: Uniform random

## 6. Purpose of This Repository

This repository is intended for:

- Reproducing the evaluation results in Section 7 of the paper

- Studying congestion-aware routing behavior in Dragonfly networks

- Serving as a reference implementation for PCD and PCDDJ algorithms

- Supporting further research on adaptive routing and disjoint paths in HPC interconnects

## 7. Citation
If you use this code in your research, please cite the corresponding paper:

Yaodong Wang, Yamin Li,

Path Congestion Detection and Disjoint Path for Improving Communication Efficiency in Dragonfly Interconnection Networks,

The Journal of Supercomputing, 2025.

## 8. Notes

- The traffic load introduced by the network controller is not modeled in this simulator.
Controller-generated traffic (binary congestion tags) is negligible compared to regular data packets, occurs infrequently, and is transmitted over dedicated router channels, ensuring no contention with normal packet traffic.

- The simulator prioritizes clarity and experimental fidelity over runtime performance.

- The code is structured to closely reflect the experimental design described in the paper.





