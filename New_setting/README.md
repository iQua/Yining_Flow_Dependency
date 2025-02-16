
# How to run the code

## Newly added files
- `new_setting.py`: The new flow setting that parse all the flow information into three dictionaries. This is a replacement of `generic.py` in the original code.

- `new_run_experiment.py`: A simplified version of run_experiment.py, which only contains the new idea.

- `optimized_flow_chunk.py`: The new idea implemented by the new setting.

- `flow_chunk_competitor.py`: The new idea implemeted by the original setting.

## Command
```bash
$ python new_run_experiment.py -r ./new -c toy_example.json -p toyExample -m flowChunk
$ python new_run_experiment.py -r ./new -c simple_example_1.json -p simpleExample -m flowChunk
$ python new_run_experiment.py -r ./new -c simple_example_2.json -p simpleExample -m flowChunk
$ python new_run_experiment.py -r ./new -c simple_example_3.json -p simpleExample -m flowChunk
```

The command structure is:

- new_run_experiment.py: the new script that runs the experiment
- -r "./new": the directory where the results will be saved
- -c "toy_example.json": the configuration file that contains the experiment configuration; "simple_example_{x}.json": the configuration files that contain three simpler setting than toyexample for testing the groud truths.
- -p "toyExample": the name of the experiment
- -m "flowchunk": the new method

For example, if we run
```bash
$ python new_run_experiment.py -r ./new -c toy_example.json -p toyExample -m flowChunk
```
The results (optimal solution and time cost) will be saved at `./new/toyExample/flowChunk/result.json`. The detailed variable values will also be displayed at terminal, like follows:
| Flow id | Collective | Group | Source | Destination | Order | Part | Arriving Time |
|:-----:|:-:|:-:|:-----:|:-----:|:-----:|:----:|:-------------:|
| 1     | 1 | 1 | 1     | 10    | 1     | 1    | 1.0           |
| 1     | 1 | 1 | 1     | 10    | 1     | 2    | 2.0           |
| 1     | 1 | 1 | 1     | 10    | 1     | 3    | 3.0           |
| 1     | 1 | 1 | 1     | 10    | 1     | 4    | 4.0           |
| 1     | 1 | 1 | 1     | 10    | 1     | 5    | 5.0           |
| 1     | 1 | 1 | 1     | 10    | 1     | 6    | 6.0           |
| 1     | 1 | 1 | 1     | 10    | 1     | 7    | 7.0           |
| 1     | 1 | 1 | 1     | 10    | 1     | 8    | 8.0           |
| 1     | 1 | 1 | 1     | 10    | 1     | 9    | 9.0           |
| 1     | 1 | 1 | 1     | 10    | 1     | 10   | 10.0          |
| 1     | 1 | 1 | 1     | 10    | 1     | 11   | 11.0          |
| 1     | 1 | 1 | 1     | 10    | 1     | 12   | 12.0          |
| 1     | 1 | 1 | 1     | 10    | 1     | 13   | 13.0          |
| 1     | 1 | 1 | 1     | 10    | 1     | 14   | 14.0          |
| 1     | 1 | 1 | 1     | 10    | 1     | 15   | 15.0          |
| 2     | 1 | 2 | 2     | 11    | 2     | 1    | 16.0          |
| 2     | 1 | 2 | 2     | 11    | 2     | 2    | 17.0          |
| 2     | 1 | 2 | 2     | 11    | 2     | 3    | 18.0          |
| 2     | 1 | 2 | 2     | 11    | 2     | 4    | 19.0          |
| 2     | 1 | 2 | 2     | 11    | 2     | 5    | 20.0          |
| 3     | 1 | 2 | 2     | 11    | 1     | 1    | 8.0           |
| 3     | 1 | 2 | 2     | 11    | 1     | 2    | 9.0           |
| 3     | 1 | 2 | 2     | 11    | 1     | 3    | 10.0          |
| 3     | 1 | 2 | 2     | 11    | 1     | 4    | 11.0          |
| 4     | 2 | 3 | 3     | 11    | 1     | 1    | 1.0           |
| 4     | 2 | 3 | 3     | 11    | 1     | 2    | 2.0           |
| 4     | 2 | 3 | 3     | 11    | 1     | 3    | 3.0           |
| 4     | 2 | 3 | 3     | 11    | 1     | 4    | 4.0           |
| 4     | 2 | 3 | 3     | 11    | 1     | 5    | 5.0           |
| 4     | 2 | 3 | 3     | 11    | 1     | 6    | 6.0           |
| 4     | 2 | 3 | 3     | 11    | 1     | 7    | 7.0           |

| Solver Status | Objective Value | Time Cost (s)  |
|---------------|-----------------|----------------|
| optimal       | 13.5            | 0.04475903511047363 |

We can also run the new idea on the original setting by
```bash
$ python run_experiment.py -r ./new -c toy_example.json -o toy_example_optimization.json -p toyExample -m flowChunk
```
The result (only time cost) will be saved at `./new/toyExample/flowChunk/time_cost.json`