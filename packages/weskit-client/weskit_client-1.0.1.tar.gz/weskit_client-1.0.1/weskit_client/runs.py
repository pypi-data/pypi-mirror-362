
import json
import os
import pprint
import yaml
from weskit_client.com import requests_to_json
from weskit_client.workflows import get_workflows_info
from tabulate import tabulate

pp = pprint.PrettyPrinter(indent=1)


def exec_run(weskit_api_url, workflow_name, workflow_config_file):
    workflow_info = get_workflows_info(weskit_api_url)[workflow_name]
    with open(workflow_config_file) as file:
        workflow_params = json.dumps(yaml.load(file, Loader=yaml.FullLoader))
    data = {
        "workflow_params": workflow_params,
        "workflow_type": workflow_info["type"],
        "workflow_type_version": workflow_info["version"],
        "workflow_url": workflow_info["uri"]}
    run_info = requests_to_json(url=f"{weskit_api_url}ga4gh/wes/v1/runs", method="POST", data=data)
    with open(".{}".format(run_info["run_id"]), "w") as file:
        pass
    print(f"Executed workflow '{workflow_name}' with config '{workflow_config_file}'. Run-id: {run_info["run_id"]}")


def get_run(weskit_api_url, run_id):
    run_info = requests_to_json(url=f"{weskit_api_url}/ga4gh/wes/v1/runs/{run_id}", method="GET")
    pp.pprint(run_info)


def get_runs(weskit_api_url, list_all):
    runs = requests_to_json(url=f"{weskit_api_url}/ga4gh/wes/v1/runs", method="GET")
    data = [["ID", "State", "workflow", "start_time"]]
    for run in runs["runs"]:
        if list_all or os.path.isfile(f".{run["run_id"]}"):
            run_info = requests_to_json(url=f"{weskit_api_url}/ga4gh/wes/v1/runs/{run["run_id"]}", method="GET")
            data.append([
                run["run_id"],
                run["state"],
                run_info["run_log"]["name"],
                run_info["run_log"]["start_time"]])
    else:
        print(tabulate(data, headers="firstrow", tablefmt="grid"))
