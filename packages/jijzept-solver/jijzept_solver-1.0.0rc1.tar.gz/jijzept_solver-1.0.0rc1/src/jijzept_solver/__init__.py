import importlib.metadata

from .solve import solve

distributions = importlib.metadata.distributions()
installed_jijzept_solver = [
    dist.metadata["name"]
    for dist in distributions
    if dist.metadata["name"].startswith("jijzept_solver")
]
if len(installed_jijzept_solver) > 1:
    raise ImportError(
        f"Multiple jijzept_solver packages are installed: {installed_jijzept_solver}. "
        "Please uninstall all but one to avoid conflicts."
    )

__all__ = ["solve"]
