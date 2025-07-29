import os
import argparse
from tensorpool.helpers import (
    login,
    get_tensorpool_key,
    get_version,
    health_check,
    job_run,
    ssh_key_prechecks,
    get_empty_tp_config,
    listen_to_job,
    dump_file,
    fetch_dashboard,
    download_files,
    cluster_create,
    cluster_destroy,
    cluster_list,
    ssh_to_instance,
    fetch_user_info,
)
from tensorpool.spinner import Spinner
from typing import Optional, List


def gen_tp_config() -> None:
    """
    Command to generate a tp.[config].toml file
    """
    # Get empty config from the server
    with Spinner(text="Fetching empty config..."):
        success, empty_config, message = get_empty_tp_config()

    if not success:
        print(f"Failed to fetch empty config: {message}")
        exit(1)

    if message:
        print(message)

    # Find a unique filename
    tp_config_path = "tp.config.toml"
    if os.path.exists(tp_config_path):
        count = 1
        while True:
            tp_config_path = f"tp.config{count}.toml"
            if not os.path.exists(tp_config_path):
                break
            count += 1

    # Ask the user if they want this name, or if they want to specify a different name
    print(f"Enter a name for the tp config, or press ENTER to use {tp_config_path}")
    new_name = input()
    new_name = f"tp.{new_name}.toml" if new_name else None
    if new_name:
        tp_config_path = new_name

    save_success = dump_file(empty_config, tp_config_path)

    if not save_success:
        print("Failed to create new tp config")
        exit(1)

    print(f"{tp_config_path} created")
    print(f"Configure it to do `tp job run {tp_config_path}`")

    return


def job_listen(
    job_id: str, pull_on_complete: bool = False, overwrite_on_pull: bool = False
):
    if not job_id:
        print("Error: Job ID required")
        print("Usage: tp listen <job_id>")
        exit(1)

    completed = listen_to_job(job_id)

    if completed and pull_on_complete:
        job_pull(job_id, files=None, overwrite=overwrite_on_pull)

    return


def job_pull(
    job_id: str,
    files: Optional[List[str]] = None,
    overwrite: bool = False,
    preview: bool = False,
):
    # if not job_id:
    #     print("Error: Job ID required")
    #     print("Usage: tp pull <job_id>")
    #     return
    raise NotImplementedError("nah buh")
    if files and len(files) > 100:
        print(f"{len(files)} files requested, this may take a while")

    from tensorpool.helpers import job_pull as job_pull_helper

    with Spinner(text="Pulling job..."):
        download_map, msg = job_pull_helper(job_id, files, preview)

    if not download_map:
        if msg:
            print(msg)
        return

    num_files = len(download_map)
    if num_files == 0:
        print("No changed files to pull")
        return

    download_success = download_files(download_map, overwrite)

    if not download_success:
        print(
            "Failed to download job files\nPlease try again or visit https://dashboard.tensorpool.dev/dashboard\nContact team@tensorpool.dev if this persists"
        )
        exit(1)

    print("Job files pulled successfully")

    return


def job_cancel(job_id: str):
    from tensorpool.helpers import job_cancel as job_cancel_helper

    cancel_success, message = job_cancel_helper(job_id)
    print(message)
    if not cancel_success:
        exit(1)


def job_dashboard():
    dash = fetch_dashboard()

    if dash:
        print(dash)
    else:
        print("Failed fetch dashboard, visit https://tensorpool.dev")
        exit(1)

    return


def main():
    parser = argparse.ArgumentParser(description="TensorPool https://tensorpool.dev")

    subparsers = parser.add_subparsers(dest="command")

    # Create job subparser for job-related commands
    # job_parser = subparsers.add_parser("job", help="Manage jobs on TensorPool")
    # job_subparsers = job_parser.add_subparsers(dest="job_command")

    # job_subparsers.add_parser(
    #     "init",
    #     help="Create a new tp.config.toml file.",
    # )

    # run_parser = job_subparsers.add_parser("run", help="Run a job on TensorPool")
    # run_parser.add_argument("tp_config_path", help="Path to a tp.[config].toml file")
    # run_parser.add_argument(
    #     "--skip-cache",
    #     action="store_true",
    #     help="Don't check your job cache for previously uploaded files",
    # )
    # run_parser.add_argument(
    #     "--detach", action="store_true", help="Run the job in the background"
    # )

    # listen_parser = job_subparsers.add_parser("listen", help="Listen to a job")
    # listen_parser.add_argument("job_id", help="ID of the job to listen to")
    # listen_parser.add_argument(
    #     "--pull", action="store_true", help="Pull the job files after listening"
    # )
    # listen_parser.add_argument(
    #     "--overwrite", action="store_true", help="Overwrite existing files if pulling"
    # )
    # pull_parser = job_subparsers.add_parser("pull", help="Pull a job")
    # pull_parser.add_argument("job_id", nargs="?", help="ID of the job to pull")
    # pull_parser.add_argument("files", nargs="*", help="List of filenames to pull")
    # pull_parser.add_argument(
    #     "--overwrite", action="store_true", help="Overwrite existing files"
    # )
    # pull_parser.add_argument(
    #     "--preview", action="store_true", help="Preview the files to be pulled"
    # )

    # cancel_parser = job_subparsers.add_parser("cancel", help="Cancel a job")
    # cancel_parser.add_argument("job_ids", nargs="+", help="IDs of the job(s) to cancel")

    # job_subparsers.add_parser(
    #     "dashboard",
    #     aliases=[
    #         "dash",
    #         "jobs",
    #     ],
    #     help="Open the TensorPool dashboard",
    # )

    cluster_parser = subparsers.add_parser(
        "cluster",
        help="Manage clusters",
    )

    cluster_subparsers = cluster_parser.add_subparsers(dest="cluster_command")

    cluster_create_parser = cluster_subparsers.add_parser(
        "create", help="Create a new cluster"
    )
    cluster_create_parser.add_argument(
        "-i",  # uh this is kinda weird but -i is standard for ssh,
        "--public-key",
        help="Path to your public SSH key (e.g. ~/.ssh/id_rsa.pub)",
        required=True,
    )
    cluster_create_parser.add_argument(
        "-t",
        "--instance-type",
        help="Instance type (e.g. 1xH100, 2xH100, 4xH100, 8xH100)",
        required=True,
    )
    cluster_create_parser.add_argument("--name", help="Cluster name (optional)")
    cluster_create_parser.add_argument(
        "-n",
        "--num-nodes",
        type=int,
        help="Number of nodes (optional, required if instance type is 8xH100)",
    )
    cluster_destroy_parser = cluster_subparsers.add_parser(
        "destroy", help="Destroy a cluster"
    )
    cluster_destroy_parser.add_argument("cluster_id", help="Cluster ID to destroy")
    list_parser = cluster_subparsers.add_parser("list", help="List available clusters")
    list_parser.add_argument(
        "--org",
        "--organization",
        action="store_true",
        help="List all clusters in organization",
        dest="org",
    )

    # on_parser = cluster_subparsers.add_parser("on", help="Activate a cluster")
    # on_parser.add_argument("cluster_id", help="ID of the instance/cluster to turn on")

    # off_parser = cluster_subparsers.add_parser("off", help="Deactivate a cluster")
    # off_parser.add_argument("cluster_id", help="ID of the instance/cluster to turn off")

    # ssh_parser = subparsers.add_parser("ssh", help="SSH into an instance")
    # ssh_parser.add_argument("instance_id", help="Instance ID to SSH into")
    # ssh_parser.add_argument(
    #     "ssh_args",
    #     nargs=argparse.REMAINDER,
    #     help="Additional SSH arguments to pass through (e.g. -i)",
    # )

    subparsers.add_parser("me", help="Show current user information")

    parser.add_argument("-v", "--version", action="version", version=f"{get_version()}")

    args = parser.parse_args()

    key = get_tensorpool_key()
    if not key:
        print("TENSORPOOL_KEY environment variable not found.")
        inp = input("Would you like to add it to .env? [Y/n] ")
        if inp.lower() not in ["n", "no"]:
            if not login():
                print("Failed to set API key")
                exit(1)
        else:
            print("Please set TENSORPOOL_KEY environment variable before proceeding.")
            exit(1)
    else:
        os.environ["TENSORPOOL_KEY"] = key

    # Health check
    with Spinner(text="Authenticating..."):
        health_accepted, health_message = health_check()
    if not health_accepted:
        print(health_message)
        exit(1)
    else:
        if health_message:
            print(health_message)

    # if args.command == "job":
    #     if args.job_command == "init":
    #         return gen_tp_config()
    #     elif args.job_command == "run":
    #         if not args.tp_config_path:
    #             print("Error: tp config path required")
    #             run_parser.print_help()
    #             return

    #         # Check SSH keys before running job
    #         prechecks_success, pub_key_path, priv_key_path = ssh_key_prechecks()
    #         if not prechecks_success:
    #             print("SSH key setup failed. Cannot proceed with job.")
    #             exit(1)

    #         success = job_run(
    #             args.tp_config_path,
    #             pub_key_path,
    #             priv_key_path
    #         )
    #         if not success:
    #             exit(1)
    #         return
    #     elif args.job_command == "listen":
    #         return job_listen(args.job_id, args.pull, args.overwrite)
    #     elif args.job_command == "pull":
    #         return job_pull(args.job_id, args.files, args.overwrite, args.preview)
    #     elif args.job_command == "cancel":
    #         for job_id in args.job_ids:
    #             job_cancel(job_id)
    #         return
    #     elif (
    #         args.job_command == "dashboard"
    #         or args.job_command == "dash"
    #         or args.job_command == "jobs"
    #     ):
    #         return job_dashboard()
    #     else:
    #         job_parser.print_help()
    #         return
    if args.command == "cluster":
        if args.cluster_command == "create":
            # Force user to provide identity file - no default SSH key prechecks
            if args.public_key:
                identity_file_path = args.public_key
            else:
                # # Check SSH keys before creating cluster
                # prechecks_success, pub_key_path, priv_key_path = ssh_key_prechecks()
                # if not prechecks_success:
                #     print(
                #         "SSH key setup failed. Provide a public key with -i, or create a key pair at ~/.ssh/tensorpool{,.pub}"
                #     )
                #     exit(1)
                # identity_file_path = pub_key_path
                print("Error: Public SSH key is required")
                print(
                    "Usage: tp cluster create -i <public_key_path> -t <instance_type>"
                )
                exit(1)

            # This will stream some things to stdout, but also a final message is returned
            success, final_message = cluster_create(
                identity_file_path, args.instance_type, args.name, args.num_nodes
            )
            if final_message:
                print(final_message)
            if not success:
                exit(1)
            return
        elif args.cluster_command == "destroy":
            success, message = cluster_destroy(args.cluster_id)
            if message:
                print(message)
            if not success:
                exit(1)
            return
        elif args.cluster_command == "list":
            success, message = cluster_list(org=args.org)
            if message:
                print(message)
            if not success:
                exit(1)
            return
        else:
            cluster_parser.print_help()
            return
    elif args.command == "ssh":
        ssh_args = args.ssh_args if hasattr(args, "ssh_args") and args.ssh_args else []
        success, message = ssh_to_instance(args.instance_id, ssh_args)
        if message:
            print(message)
        if not success:
            exit(1)
        return
    elif args.command == "me":
        success, message = fetch_user_info()
        print(message)
        if not success:
            exit(1)
        return

    parser.print_help()
    return

    # text = " ".join(args.query)
    # print(f"You said: {text}")


if __name__ == "__main__":
    main()
