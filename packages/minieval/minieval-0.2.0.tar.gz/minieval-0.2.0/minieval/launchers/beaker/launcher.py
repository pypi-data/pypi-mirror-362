import os
import re
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional

try:
    import beaker as bk
    from gantry.exceptions import DirtyRepoError
    from gantry.api import launch_experiment
except ImportError:
    raise ImportError("Beaker is required for the Beaker launcher. Install with: pip install minieval[beaker]")

from minieval.datatypes import LauncherConfig
from minieval.launchers.beaker.constants import WEKA_CLUSTERS, WEKA_MOUNTS
from minieval.launchers.beaker.defaults import get_env_vars


@dataclass
class BeakerConfig(LauncherConfig):
    workspace: str = "ai2/olmo-3-evals"
    cluster: List[str] = field(default_factory=lambda: WEKA_CLUSTERS)
    budget: str = "ai2/oe-eval"
    save_path: str = "/results"
    entrypoint: str = "python minieval/cli.py"
    hostname: Optional[List[str]] = None  # specific nodes to run a job
    max_retries: int = 0
    gpus: int = 0
    num_nodes: int = 1
    image: str = "ai2/cuda12.8-dev-ubuntu22.04-torch2.7.0"
    description: str = "my minieval job"
    task_name: str = "minieval"
    priority: str = "normal"
    preemptible: bool = True
    pure_docker_mode: bool = True  # If false, will cd into os.getcwd()
    beaker_datasets: List[Dict[str, str]] = field(
        default_factory=list
    )  # TODO: Add parser from mason.py
    env: List[Dict[str, str]] = field(default_factory=list)  # TODO: Add parser from mason.py
    secret: List[Dict[str, str]] = field(default_factory=list)  # TODO: Add parser from mason.py
    no_host_networking: bool = False
    dry_run: bool = False
    allow_dirty: bool = False
    follow: bool = False


def make_command(cmd: List[str], config: BeakerConfig) -> str:
    # escape the command (e.g., --stop_strings "</answer>")
    for i in range(len(cmd)):
        if "</" in cmd[i]:
            cmd[i] = f"'{cmd[i]}'"

    # special logic to deal with escape like
    # python mason.py ... -- python x.py --dataset_mixer '{"trl-internal-testing/sentiment-trl-style": 1.0}'
    # we need to wrap the json string with single quote
    for idx in range(len(cmd)):
        if "{" in cmd[idx]:
            cmd[idx] = "'" + cmd[idx] + "'"

    setup_cmd = ""
    if not config.pure_docker_mode:
        setup_cmd = f"cd {os.getcwd()} && "

    # override accelerate call
    join_cmd = " ".join(cmd)
    if config.num_nodes > 1:
        if "--num_processes" not in join_cmd and "accelerate" in join_cmd:
            raise ValueError(
                "num_processes must be specified in the command for accelerate-based multi-node jobs."
            )
        join_cmd = re.sub(
            r"--num_processes (\d+)",
            lambda m: (
                f"--num_processes {int(m.group(1)) * config.num_nodes} "
                f"--num_machines {config.num_nodes} "
                "--machine_rank $BEAKER_REPLICA_RANK "
                "--main_process_ip $BEAKER_LEADER_REPLICA_HOSTNAME "
                "--main_process_port 29400 "
            ),
            join_cmd,
        )

    cmd = setup_cmd + join_cmd

    return cmd


def parse_commands(entrypoint) -> List[List[str]]:
    """ Get arguments used to run script """

    # use cli.py as the entrypoint in-case this was run in some other way
    args = [entrypoint] + sys.argv[1:]

    # gantry requires our argv to start with "--"
    args = ["--"] + args
    
    # use the list of lists for multiple commands
    return [args]


def launch_gantry(config: BeakerConfig):
    beaker_client = bk.Beaker.from_env(default_workspace=config.workspace)

    beaker_secrets = [
        secret.name for secret in beaker_client.secret.list(workspace=config.workspace)
    ]
    whoami = beaker_client.user_name

    commands = parse_commands(entrypoint=config.entrypoint)

    full_commands = []
    for command in commands:
        full_commands += [make_command(command, config)]

    assert len(full_commands) == 1, "only one command supported for now"
    full_commands = full_commands[0]

    # Gantry requires the sys.argv to be set to our constructed gantry command
    sys.argv = full_commands

    env_vars, env_secrets = get_env_vars(
        config.cluster,
        beaker_secrets,
        whoami,
        config.pure_docker_mode,
        config.num_nodes,
        config.env,
        config.secret,
        config.preemptible,
    )
    env_vars = [f"{var.name}={var.value}" for var in env_vars]
    env_secrets = [f"{var.name}={var.secret}" for var in env_secrets]

    # Workaournd as Gantry doesn't support uv
    UV_INIT = "deactivate && pip install uv && uv venv && source .venv/bin/activate && "
    ### this deps pre-install is required for B200s
    # UV_DEPS = "uv pip install torch && sudo apt install -y libmpich-dev && "
    UV_DEPS = ""
    INSTALL_CMD = UV_INIT + UV_DEPS + "uv pip install -e '.[all]'"

    # Launch the experiment
    try:
        launch_experiment(
            args=full_commands.split(" "),
            workspace=config.workspace,
            clusters=config.cluster,
            budget=config.budget,
            name=config.task_name,
            description=config.description,
            hostnames=config.hostname,
            beaker_image=config.image,
            gpus=config.gpus,
            preemptible=config.preemptible,
            retries=config.max_retries,
            replicas=config.num_nodes,
            host_networking=not config.no_host_networking,
            env_vars=env_vars,
            env_secrets=env_secrets,
            yes=True,
            allow_dirty=config.allow_dirty,
            priority=config.priority,
            dry_run=config.dry_run,
            weka=WEKA_MOUNTS,
            timeout=(
                99999999 if config.follow else 0
            ),  # only way to follow the experiment without canceling
            install=INSTALL_CMD,  
        )
    except DirtyRepoError:
        raise DirtyRepoError("You have uncommitted changes! Use --launch.allow_dirty True to force")

