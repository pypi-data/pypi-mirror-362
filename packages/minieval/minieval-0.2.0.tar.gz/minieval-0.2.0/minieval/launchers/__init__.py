from enum import Enum
import json
import os
from dataclasses import asdict, dataclass

from rich import print

from rich.console import Console
console = Console()

from minieval.datatypes import LauncherConfig, Response


class WriterType(str, Enum):
    local = "local"
    datalake = "datalake"


@dataclass
class LocalConfig(LauncherConfig):
    save_path: str


class LocalWriter:
    def __init__(self, config: LocalConfig):
        self.config = config

    def save_responses(self, task_alias: str, responses: list[Response]):
        os.makedirs(self.config.save_path, exist_ok=True)

        save_path = f"{task_alias}_responses.jsonl"
        save_path = os.path.join(self.config.save_path, save_path)

        with open(save_path, "w") as f:
            for response in responses:
                f.write(json.dumps(asdict(response)) + "\n")

        print(f"Saved responses to [bold purple]{save_path}[/bold purple]")

    def save_metrics(self, task_alias: str, metrics: dict):
        os.makedirs(self.config.save_path, exist_ok=True)

        save_path = f"{task_alias}_metrics.json"
        save_path = os.path.join(self.config.save_path, save_path)

        with open(save_path, "w") as f:
            json.dump(metrics, f)

        print(f"Saved metrics to [bold purple]{save_path}[/bold purple]")

    def write_finalized_metrics(self, config):
        # metrics.json only implemented for Datalake Writer
        return


def init_writer(config, writer_type: WriterType):
    match writer_type:
        case WriterType.datalake:
            from minieval.writers.datalake import DatalakeWriter
            return DatalakeWriter(config=config)
        case WriterType.local:
            return LocalWriter(config=config)
        case _:
            raise ValueError(f"Unknown writer type: {writer_type}")
