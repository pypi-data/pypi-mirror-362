import argparse
import os
import pprint
import sys
from weskit_client.oidc import login, logout
from weskit_client.runs import exec_run, get_runs, get_run
from weskit_client.service_info import get_service_info
from weskit_client.workflows import init_workflow, get_workflows

pp = pprint.PrettyPrinter(indent=4)


def get_args_parser():
    # parse arguments
    parser = argparse.ArgumentParser(prog="weskit")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for "service-info"
    subparsers.add_parser("service-info", help="Show service-info")

    # Subparser for "workflows"
    subparsers.add_parser("workflows", help="List workflows")

    # Subparser for "init"
    init_parser = subparsers.add_parser("init", help="Initialize workflow run")
    init_parser.add_argument("--name", required=True, help="Name of the workflow")

    # Subparser for "exec" command
    execute_parser = subparsers.add_parser("exec", help="Execute a workflow via WESkit")
    execute_parser.add_argument("--name", required=True, help="Name of the workflow")
    execute_parser.add_argument("--config", required=True, help="Path to config file")

    # Subparser for "runs"
    status_parser = subparsers.add_parser("runs", help="List runs")
    status_parser.add_argument("--rid", default=False, help="Specify single run")
    status_parser.add_argument("--all", action="store_true",
                               help="List all runs (default shows only current workdir runs)")

    # login/logout
    subparsers.add_parser("login", help="Set OIDC access token")
    subparsers.add_parser("logout", help="Remove OIDC access token")

    return parser


def main():
    try:
        weskit_api_url = os.environ["WESKIT_API_URL"]
    except KeyError:
        print("Please set environmental variable `WESKIT_API_URL`")
        sys.exit(1)

    parser = get_args_parser()
    args = parser.parse_args()

    if args.command == "service-info":
        get_service_info(weskit_api_url=weskit_api_url)
    elif args.command == "workflows":
        get_workflows(weskit_api_url=weskit_api_url)
    elif args.command == "init":
        init_workflow(weskit_api_url, args.name)
    elif args.command == "exec":
        exec_run(
            weskit_api_url=weskit_api_url,
            workflow_name=args.name,
            workflow_config_file=args.config)
    elif args.command == "runs":
        if args.rid:
            get_run(
                weskit_api_url=weskit_api_url,
                run_id=args.rid)
        else:
            get_runs(
                weskit_api_url=weskit_api_url,
                list_all=args.all)
    elif args.command == "login":
        login()
    elif args.command == "logout":
        logout()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
