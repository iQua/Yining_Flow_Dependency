# Design of experiments 

## Competitors

- Average allocation, meaning that the bandwidth is uniformly distributed across flow groups.
- Date-aware allocation, meaning that the bandwidth is distributed across flow groups based on the volum of the flows.

## Experiment1-Main

The major experiment is to verify that the proposed algorithm achieves the minimal average completion time of collectives under different number of collectives. And, thus the 
- x-axis: Various number of collectives.
- y-axis: Average completion time.


It would be great to show that our optimization algorithm can solve the problem in a polynomial time. Thus, the 
- x-axis: Various number of collectives.
- y-axis: Time required to solve the optimization

## Experiment2-Topology.
 
The effectiveness and robust of our proposed algorithm under different topologies. Thus,

- x-axis: Name of the topologies. (Please also create a table to explain these topologies)
- y-axis: Average completion time.

Still, it is better to present the problem solving time.



## Experiment2-Ablation.

The ablation study: as our algorithm is the combination of the (OP) and (OR), we can perform experiment to show that without using (OR), the performance is bad (as pointed by the theorem 2 of the paper).

Here are two parts:
- values: comparison of the completion times. Figure or Table: To be determined.
- Visualization: illustrate how (OR) can significantly reduce the completion time by showing the transmission time of flows in the figure.



