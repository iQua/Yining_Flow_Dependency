
# How to run the code

## Adjustable hyper-parameters for the optimization

Please always create a new optimization configuration file for a new experiment. For example, the `toy_example_optimization.json` for the toy example. Then, place it under the `configs/`

Then, under this file, we can adjust:
- T: [15, 30] (You can adjust it based on the link capacity and flow size)
- segment_base: 1, (Do not change it)
- is_segment: "False", (Do not change it)
- small_lambda: 0.2, _[0.1, 0.5]_ (Reduce the value to search in small steps)
- jump_range: 20, _[10, 50]_ (Increase the value to have better results)

The actual optimization range is `small_lambda` * `jump_range`.


## Competitors

There will be three competitors to compare with our algorithm `steller`. They are:
- `averageAlloc`: Perform allocation equally across groups
- `dataAwareAlloc`: Perform allocation based on the groups' data competing the link
- `barrierAwareAlloc`: A SOTA competitor.


See the Command section to know how to run these competitors.

## Command

```bash
$ python examples/stellar/run_experiment.py -r ./results -c toy_example.json -o toy_example_optimization.json -p toyExample -m steller
$ python examples/stellar/run_experiment.py -r ./results -c toy_example.json -o toy_example_optimization.json -p toyExample -m barrierAwareAlloc
$ python examples/stellar/run_experiment.py -r ./results -c toy_example.json -o toy_example_optimization.json -p toyExample -m averageAlloc
$ python examples/stellar/run_experiment.py -r ./results -c toy_example.json -o toy_example_optimization.json -p toyExample -m dataAwareAlloc
```

The command structure is:

- examples/stellar/run_experiment.py: the script that runs the experiment (Do not change)
- -r "./results": the directory where the results will be saved (Do not change)
- -c "toy_example.json": the configuration file that contains the experiment configuration
- -o "optimization.json": the optimization file that contains the optimization configuration
- -p "toyExample": the name of the experiment
- -m "steller"/"averageAlloc"...: the model used to obtain the optimal flow rates 


## File structure

All files are placed under the `examples/stellar` directory.

The files are structured as follows:

- config/: contains the configuration files
- generic.py: contains the generic components used in the program
- priority.py: contains the priority optimization (Section 3-A)
- allocation.py: contains the allocation optimization (Section 3-B)
- stellar.py: contains the main algorithm (Section 3-C)
- run_experiment.py: the script that runs the experiment

## Result structure

Under the `results/` of the root directory, the detailed results are saved in the following structure:

- args.p: experiment name defined by the `-p` in the command line
    - `PriorityOptimization/`: Save all the results of the priority optimization
    - `AllocationOptimization/`: Save all the results of the allocation optimization
    - `Optimized-{}.json`: Configuration file with the optimized flow rates


## Run Experiments

__Always find the configuration file with the optimized flow rates under the `results/{Project Name}`__

#### Experiment for toy example

1. Create the optimization file under the `configs/` for the toy example. For example, the `toy_example_optimization.json` (See above about how to adjust the hyper-parameters).

2. Run the toy example
```bash
$ python examples/stellar/run_experiment.py -r ./results -c toy_example.json -o toy_example_optimization.json -p toyExample -m steller

$ python examples/stellar/run_experiment.py -r ./results -c toy_example.json -o toy_example_optimization.json -p toyExample -m averageAlloc

$ python examples/stellar/run_experiment.py -r ./results -c toy_example.json -o toy_example_optimization.json -p toyExample -m dataAwareAlloc
```

3. Find the configuration file with the optimized flow rates under the `results/toyExample`
4. Find the time cost of our optimization problem under the `results/toyExample/time_cost.json`

#### Experiment for Abilene_1-RAR

1. Create the optimization file under the `configs/` for the toy example. For example, the `Abilene_1-RAR_optimization` (See above about how to adjust the hyper-parameters).

2. Run the Abilene_1-RAR
```bash
$ python examples/stellar/run_experiment.py -r ./results -c Abilene_RAR/Abilene_1-RAR.json -o Abilene_RAR/Abilene_1-RAR_optimization.json -p Abilene_1-RAR
```

3. Find the configuration file with the optimized flow rates under the `results/Abilene_1-RAR`
4. Find the time cost of our optimization problem under the `results/Abilene_1-RAR/time_cost.json`

#### Experiment for Abilene_2-RAR

In `configs/`, you will see `Abilene_2-RAR_optimization.json`. 

```
$ python examples/stellar/run_experiment.py -r ./results -c Abilene_2-RAR.json -o Abilene_2-RAR_optimization.json -p Abilene_2-RAR
```

#### Experiment for Abilene_5-RAR

Experiments 1-4 were set up, `T` values can be seen in the appropriate configs. `5-RAR` seems to fail regardless of `T`.

```
$ python examples/stellar/run_experiment.py -r ./results -c Abilene_5-RAR.json -o Abilene_5-RAR_optimization.json -p Abilene_5-RAR
```

#### To run HiberniaIreland

```
python3 examples/stellar/run_experiment.py -r ./results -c topo_exp/HiberniaIreland_5-RAR.json -o topo_exp/HiberniaIreland_5-RAR_optimization.json -p HiberniaIreland_5-RAR -m dataAwareAlloc
```

#### To run Napnet

```
python3 examples/stellar/run_experiment.py -r ./results -c topo_exp/Napnet_5-RAR.json -o topo_exp/Napnet_5-RAR_optimization.json -p Napnet_5-RAR -m dataAwareAlloc
```