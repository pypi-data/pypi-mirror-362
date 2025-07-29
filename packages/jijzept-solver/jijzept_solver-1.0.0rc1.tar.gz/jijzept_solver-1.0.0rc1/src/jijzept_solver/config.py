import os


class JijZeptSolverClientConfig:
    def __init__(self) -> None:
        # Get environment variables
        self.JIJZEPT_SOLVER_SERVER_HOST = os.getenv("JIJZEPT_SOLVER_SERVER_HOST")
        self.JIJZEPT_SOLVER_SERVER_PORT = os.getenv("JIJZEPT_SOLVER_SERVER_PORT")
        _JIJZEPT_SOLVER_CLIENT_DEBUG = os.getenv("JIJZEPT_SOLVER_CLIENT_DEBUG", "False")
        # Set debug mode
        try:
            self.JIJZEPT_SOLVER_CLIENT_DEBUG = {"true": True, "false": False}[
                _JIJZEPT_SOLVER_CLIENT_DEBUG.lower()
            ]
        except KeyError:
            raise ValueError("JIJZEPT_SOLVER_CLIENT_DEBUG must be True or False")
        # Get authentication token
        self.JIJZEPT_SOLVER_AUTH_TOKEN = os.getenv("JIJZEPT_SOLVER_ACCESS_TOKEN")
        if self.JIJZEPT_SOLVER_AUTH_TOKEN is None:
            raise ValueError(
                "Set your access token to the environment variable "
                "`JIJZEPT_SOLVER_ACCESS_TOKEN`."
            )

    @property
    def debug(self) -> bool:
        return self.JIJZEPT_SOLVER_CLIENT_DEBUG

    def get_host(self) -> str:
        if self.JIJZEPT_SOLVER_SERVER_HOST is not None:
            return self.JIJZEPT_SOLVER_SERVER_HOST
        if self.debug:
            # Local hostname
            return "localhost"
        else:
            raise ValueError(
                "Set API hostname to the environment variable "
                "`JIJZEPT_SOLVER_SERVER_HOST`."
            )

    def get_port(self) -> str:
        if self.JIJZEPT_SOLVER_SERVER_PORT is not None:
            return str(self.JIJZEPT_SOLVER_SERVER_PORT)
        else:
            return "443"
