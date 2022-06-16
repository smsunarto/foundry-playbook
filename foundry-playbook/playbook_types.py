class Deployment:
    def __init__(self, address: str, deployer: str, tx_hash: str):
        self.address = address
        self.deployer = deployer
        self.tx_hash = tx_hash
