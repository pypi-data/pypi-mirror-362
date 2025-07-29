import logging
from typing import Generator

import grpc
from ommx.v1 import Instance, Solution

from jijzept_solver_proto import jijzept_solver_pb2_grpc
from jijzept_solver_proto.jijzept_solver_pb2 import SolveRequest, SolveRequestParams

from .channel import no_ssl_channel_manager, ssl_channel_manager
from .config import JijZeptSolverClientConfig

logger = logging.getLogger(__name__)


def solve(ommx_instance: Instance, *, time_limit_sec: float) -> Solution:
    """
    Options
    --------
    - `time_limit_sec`
      - The total calculation time (second).
        This solver tries to calculate within the specified time.

    Returns
    -------
    - Solution to the problem.

    Examples
    --------
    ```python
    import jijzept_solver
    import jijmodeling as jm

    # Define a problem

    v = jm.Placeholder("v", ndim=1)
    N = v.len_at(0, latex="N")
    w = jm.Placeholder("w", ndim=1)
    W = jm.Placeholder("W")
    x = jm.BinaryVar("x", shape=(N,))
    i = jm.Element("i", belong_to=(0, N))

    problem = jm.Problem("Knapsack", sense=jm.ProblemSense.MAXIMIZE)
    problem += jm.sum(i, v[i] * x[i])
    problem += jm.Constraint("weight", jm.sum(i, w[i] * x[i]) <= W)

    v = [
        9,28,26,5,26,29,13,20,24,10,23,15,5,27,21,8,7,8,21,13,24,5,5,6,20,
        16,25,12,28,20,20,6,6,10,29,29,17,12,26,20,22,20,22,23,6,23,28,5,18,17,
        22,13,24,17,18,11,8,9,23,21,17,7,10,15,7,20,17,29,22,29,15,5,24,7,5,
        12,11,28,13,6,9,8,8,13,6,15,27,7,15,29,9,26,25,27,6,26,29,26,9,10
    ]
    w = [
        21,37,35,19,39,36,32,32,22,20,29,21,12,39,24,8,9,19,22,12,38,21,7,9,24,
        23,35,27,29,21,18,10,20,21,30,35,36,10,45,36,38,22,34,23,4,29,28,12,37,23,
        39,32,32,18,28,26,6,10,23,29,20,18,14,26,23,20,36,37,31,27,18,23,30,22,8,
        26,16,37,26,10,24,12,11,21,4,14,34,12,15,34,24,27,36,31,23,37,45,44,7,20
    ]
    W = 100
    instance_data = {"v": v, "w": w, "W": W}

    interpreter = jm.Interpreter(instance_data)
    ommx_instance = interpreter.eval_problem(problem)

    # Solve the problem within 2 seconds
    ommx_solution = jijzept_solver.solve(ommx_instance, time_limit_sec=2.0)
    ```
    """
    # Preprocessing of request
    ommx_instance_bytes = ommx_instance.to_bytes()

    parameters = {}

    parameters["time_limit_sec"] = time_limit_sec

    request_params = SolveRequestParams(**parameters)

    # Execute request
    config = JijZeptSolverClientConfig()
    target = f"{config.get_host()}:{config.get_port()}"

    response_chunks = []
    request_iter = request_generator(
        ommx_instance=ommx_instance_bytes, request_params=request_params
    )

    if config.debug:
        channel_manager = no_ssl_channel_manager
    else:
        channel_manager = ssl_channel_manager

    try:
        jwt_token = config.JIJZEPT_SOLVER_AUTH_TOKEN
        metadata = [("authorization", f"Bearer {jwt_token}")]
        logger.info("Sending a request to the JijZept Solver API server...")
        with channel_manager(target) as channel:
            client = jijzept_solver_pb2_grpc.JijZeptSolverStub(channel)
            for res in client.Solve(request_iter, metadata=metadata):
                response_chunks.append(res.ommx_solution)  # noqa: PERF401
    except grpc.RpcError as e:
        raise RuntimeError(f"Request failed: {e.details()}") from None

    return Solution.from_bytes(b"".join(response_chunks))


def request_generator(
    ommx_instance: bytes, request_params: SolveRequestParams
) -> Generator[SolveRequest, None, None]:
    # First, send params without ommx_instance
    yield SolveRequest(request_params=request_params)

    # Send ommx_instance
    CHUNK_SIZE = 1024 * 1024  # 1MB
    for i in range(0, len(ommx_instance), CHUNK_SIZE):
        yield SolveRequest(ommx_instance=ommx_instance[i : i + CHUNK_SIZE])
