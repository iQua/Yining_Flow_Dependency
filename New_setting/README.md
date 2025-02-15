
# How to run the code

## Newly added files
- `new_setting.py`: The new flow setting that parse all the flow information into three dictionaries. Also, dfs was used to directly get the dependency orders within a flow group. This is a replacement of `generic.py` in the original code.

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
========= Var Values =========
('1', 1, 1, 1, 10, 1, 1)
Flow(k=1, n=1, order=1, part=1) Arriving time: 1.0
('1', 1, 1, 1, 10, 1, 2)
Flow(k=1, n=1, order=1, part=2) Arriving time: 2.0
('1', 1, 1, 1, 10, 1, 3)
Flow(k=1, n=1, order=1, part=3) Arriving time: 3.0
('1', 1, 1, 1, 10, 1, 4)
Flow(k=1, n=1, order=1, part=4) Arriving time: 4.0
('1', 1, 1, 1, 10, 1, 5)
Flow(k=1, n=1, order=1, part=5) Arriving time: 5.0
('1', 1, 1, 1, 10, 1, 6)
Flow(k=1, n=1, order=1, part=6) Arriving time: 6.0
('1', 1, 1, 1, 10, 1, 7)
Flow(k=1, n=1, order=1, part=7) Arriving time: 7.0
('1', 1, 1, 1, 10, 1, 8)
Flow(k=1, n=1, order=1, part=8) Arriving time: 8.0
('1', 1, 1, 1, 10, 1, 9)
Flow(k=1, n=1, order=1, part=9) Arriving time: 9.0
('1', 1, 1, 1, 10, 1, 10)
Flow(k=1, n=1, order=1, part=10) Arriving time: 10.0
('1', 1, 1, 1, 10, 1, 11)
Flow(k=1, n=1, order=1, part=11) Arriving time: 11.0
('1', 1, 1, 1, 10, 1, 12)
Flow(k=1, n=1, order=1, part=12) Arriving time: 12.0
('1', 1, 1, 1, 10, 1, 13)
Flow(k=1, n=1, order=1, part=13) Arriving time: 13.0
('1', 1, 1, 1, 10, 1, 14)
Flow(k=1, n=1, order=1, part=14) Arriving time: 14.0
('1', 1, 1, 1, 10, 1, 15)
Flow(k=1, n=1, order=1, part=15) Arriving time: 15.0
('2', 1, 2, 2, 11, 2, 1)
Flow(k=1, n=2, order=2, part=1) Arriving time: 16.0
('2', 1, 2, 2, 11, 2, 2)
Flow(k=1, n=2, order=2, part=2) Arriving time: 17.0
('2', 1, 2, 2, 11, 2, 3)
Flow(k=1, n=2, order=2, part=3) Arriving time: 18.0
('2', 1, 2, 2, 11, 2, 4)
Flow(k=1, n=2, order=2, part=4) Arriving time: 19.0
('2', 1, 2, 2, 11, 2, 5)
Flow(k=1, n=2, order=2, part=5) Arriving time: 20.0
('3', 1, 2, 2, 11, 1, 1)
Flow(k=1, n=2, order=1, part=1) Arriving time: 8.0
('3', 1, 2, 2, 11, 1, 2)
Flow(k=1, n=2, order=1, part=2) Arriving time: 9.0
('3', 1, 2, 2, 11, 1, 3)
Flow(k=1, n=2, order=1, part=3) Arriving time: 10.0
('3', 1, 2, 2, 11, 1, 4)
Flow(k=1, n=2, order=1, part=4) Arriving time: 11.0
('4', 2, 3, 3, 11, 1, 1)
Flow(k=2, n=3, order=1, part=1) Arriving time: 1.0
('4', 2, 3, 3, 11, 1, 2)
Flow(k=2, n=3, order=1, part=2) Arriving time: 2.0
('4', 2, 3, 3, 11, 1, 3)
Flow(k=2, n=3, order=1, part=3) Arriving time: 3.0
('4', 2, 3, 3, 11, 1, 4)
Flow(k=2, n=3, order=1, part=4) Arriving time: 4.0
('4', 2, 3, 3, 11, 1, 5)
Flow(k=2, n=3, order=1, part=5) Arriving time: 5.0
('4', 2, 3, 3, 11, 1, 6)
Flow(k=2, n=3, order=1, part=6) Arriving time: 6.0
('4', 2, 3, 3, 11, 1, 7)
Flow(k=2, n=3, order=1, part=7) Arriving time: 7.0
INFO - Solver status: optimal, objective value: 13.5, time cost: 0.04507017135620117
INFO - *************** toyExample Done.

We can also run the new idea on the original setting by
```bash
$ python run_experiment.py -r ./new -c toy_example.json -o toy_example_optimization.json -p toyExample -m flowChunk
```
The result (only time cost) will be saved at `./new/toyExample/flowChunk/time_cost.json`