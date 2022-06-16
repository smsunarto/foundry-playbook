import logging
import typer
import yaml
import glob
from task import Task


class TaskRunner:
    def __init__(self, playbook):
        self.deployments = dict()
        self.accounts = playbook["accounts"]
        self.variables = playbook["variables"]
        self.tasks = [
            Task(task_obj, self.deployments, self.accounts, self.variables)
            for task_obj in playbook["tasks"]
        ]

    def run_all(self):
        for task in self.tasks:
            task_id, task_deployment_obj = task.run()
            self.deployments[task_id] = task_deployment_obj


def main(playbook_folder: str = "./playbook"):
    playbook_paths = glob.glob(f"{playbook_folder}/*.yaml")

    for playbook_path in playbook_paths:
        playbook = None

        with open(playbook_path, "r") as playbook_yaml:
            playbook = yaml.safe_load(playbook_yaml)

        if playbook:
            tr = TaskRunner(playbook)
            tr.run_all()


if __name__ == "__main__":
    logging.basicConfig(
        format="[foundry-playbook:%(levelname)s] %(message)s", level=logging.INFO
    )
    typer.run(main)
