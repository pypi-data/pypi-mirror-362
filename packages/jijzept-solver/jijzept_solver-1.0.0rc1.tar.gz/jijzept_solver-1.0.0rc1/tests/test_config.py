from unittest import mock

from src.jijzept_solver.config import JijZeptSolverClientConfig


def test_default():
    with mock.patch.dict(
        "os.environ",
        {
            "JIJZEPT_SOLVER_ACCESS_TOKEN": "test_token",
            "JIJZEPT_SOLVER_SERVER_HOST": "test.example.com",
        },
    ):
        config = JijZeptSolverClientConfig()
        assert not config.debug
        assert config.get_host() == "test.example.com"
        assert config.get_port() == "443"


def test_set_host_and_port():
    with mock.patch.dict(
        "os.environ",
        {
            "JIJZEPT_SOLVER_ACCESS_TOKEN": "test_token",
            "JIJZEPT_SOLVER_SERVER_HOST": "aaa.com",
            "JIJZEPT_SOLVER_SERVER_PORT": "8888",
        },
    ):
        config = JijZeptSolverClientConfig()
        assert not config.debug
        assert config.get_host() == "aaa.com"
        assert config.get_port() == "8888"


def test_debug():
    with mock.patch.dict(
        "os.environ",
        {
            "JIJZEPT_SOLVER_CLIENT_DEBUG": "True",
            "JIJZEPT_SOLVER_ACCESS_TOKEN": "test_token",
        },
    ):
        config = JijZeptSolverClientConfig()
        assert config.debug
        assert config.get_host() == "localhost"
        assert config.get_port() == "443"


def test_debug_and_set_host_and_port():
    with mock.patch.dict(
        "os.environ",
        {
            "JIJZEPT_SOLVER_CLIENT_DEBUG": "True",
            "JIJZEPT_SOLVER_SERVER_HOST": "aaa.com",
            "JIJZEPT_SOLVER_SERVER_PORT": "8888",
            "JIJZEPT_SOLVER_ACCESS_TOKEN": "test_token",
        },
    ):
        config = JijZeptSolverClientConfig()
        assert config.debug
        assert config.get_host() == "aaa.com"
        assert config.get_port() == "8888"
