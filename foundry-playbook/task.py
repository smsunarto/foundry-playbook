import logging
import uuid
import subprocess
import io
from playbook_types import Deployment


class Task:
    def __init__(
        self, task_obj: dict, deployments: dict, accounts: dict, variables: dict
    ):
        self.deployments = deployments
        self.accounts = accounts
        self.variables = variables
        self.completed = False

        task_type, task_params = task_obj.popitem()

        if "id" in task_params.keys():
            self.id = task_params["id"]
            del task_params["id"]
        else:
            self.id = uuid.uuid1()

        self.params = task_params
        self.tool, self.subcommand = task_type.split("_")

    # returns deployment object
    def run(self) -> Deployment:
        self.__parse_params()

        logging.info("Running task with ID: {}".format(self.id))
        cmd_params = ""
        for param, value in self.params.items():
            if type(value) == list:
                value = ['"{}"'.format(v) for v in value]
            else:
                value = '"{}"'.format(value)

            if param not in [
                "create-contract",
                "send-target",
                "send-signature",
                "send-arguments",
            ]:

                cmd_params += (
                    "--"
                    + param
                    + " "
                    + (" ".join(value) if type(value) == list else value)
                )
            else:
                cmd_params += " ".join(value) if type(value) == list else value

            cmd_params += " "

        cmd = "{} {} {}".format(self.tool, self.subcommand, cmd_params)
        logging.info(cmd)

        deployer = None
        address = None
        tx_hash = None
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
            if "Deployer: " in line:
                deployer = line.strip()[10:]
            elif "Deployed to: " in line:
                address = line.strip()[13:]
            elif "Transaction hash: " in line:
                tx_hash = line.strip()[18:]

        return self.id, Deployment(address, deployer, tx_hash)

    def __parse_params(self):
        for k, v in self.params.items():
            if type(v) == list:
                self.params[k] = [
                    i.format(
                        accounts=self.accounts,
                        variables=self.variables,
                        deployments=self.deployments,
                    )
                    for i in v
                ]
            else:
                self.params[k] = v.format(
                    accounts=self.accounts,
                    variables=self.variables,
                    deployments=self.deployments,
                )

        return self.params
