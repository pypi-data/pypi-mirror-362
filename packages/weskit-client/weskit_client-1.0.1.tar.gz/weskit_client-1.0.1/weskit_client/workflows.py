import yaml
from datetime import datetime
from weskit_client.com import requests_to_json
from tabulate import tabulate


def create_dict_from_schema(schema):
    def generate_defaults(schema):
        if "default" in schema:
            return schema["default"]
        if "properties" in schema:
            return {k: generate_defaults(v) for k, v in schema["properties"].items()}
        if "items" in schema:
            return [generate_defaults(schema["items"])]
        if "type" in schema:
            if schema["type"] == "object":
                return {}
            if schema["type"] == "array":
                return []
            if schema["type"] == "string":
                return ""
            if schema["type"] == "number":
                return 0
            if schema["type"] == "boolean":
                return False
        return None
    return generate_defaults(schema)


def get_workflows_info(weskit_api_url):
    workflows_info = requests_to_json(url="{}weskit/v1/wf-info".format(weskit_api_url), method="GET")
    return workflows_info["content"]["workflows"]


def get_workflows(weskit_api_url):
    workflows_info = get_workflows_info(weskit_api_url)
    data = [["Name", "Type", "Version", "URI", "Description"]]
    for workflow_name in workflows_info.keys():
        data.append([
            workflow_name,
            workflows_info[workflow_name]["type"],
            workflows_info[workflow_name]["version"],
            workflows_info[workflow_name]["uri"],
            workflows_info[workflow_name]["config"]["description"]])
    print(tabulate(data, headers="firstrow", tablefmt="grid"))


def init_workflow(weskit_api_url, workflow_name):
    workflow_default_config = create_dict_from_schema(
        get_workflows_info(weskit_api_url)[workflow_name]["config"])
    timestamp = datetime.now().strftime("%Y%m%d")
    config_filename = f"{timestamp}_config_{workflow_name}.yaml"
    with open(config_filename, "w") as file:
        yaml.dump(workflow_default_config, file)
    print(f"Workflow '{workflow_name}' initialized and '{config_filename}' created.")
