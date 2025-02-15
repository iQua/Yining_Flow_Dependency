
# How to run the code

## Newly added files
- `new_setting.py`: The new flow setting that parse all the flow information into three dictionaries. Also, dfs was used to get the dependency orders within a flow group

- `optimized_flow_chunk.py`: The new idea implemented by the new setting

- `new_run_experiment.py`: A simplified version of run_experiment.py, which only contains the new idea

- `flow_chunk_competitor.py`: The new idea implemeted by the original setting

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
- -c "toy_example.json": the configuration file that contains the experiment configuration
- -p "toyExample": the name of the experiment
- -m "flowchunk": the new method

For example, if we run
```bash
$ python new_run_experiment.py -r ./new -c toy_example.json -p toyExample -m flowChunk
```
The results will be saved at `./new/toyExample/flowChunk/result.json