from concurrent.futures import ProcessPoolExecutor
from typing import List

from nornir.core.inventory import Host
from nornir.core.task import AggregatedResult, Task


class MultiProcessRunner:
    """
    MultiProcessRunner runs the task over each host using multiple processors

    Arguments:
        num_workers: number of processors to use
    """

    def __init__(self, num_workers: int = 10) -> None:
        self.num_workers = num_workers

    def run(self, task: Task, hosts: List[Host]) -> AggregatedResult:
        result = AggregatedResult(task.name)
        futures = []
        with ProcessPoolExecutor(self.num_workers) as pool:
            for host in hosts:
                future = pool.submit(task.copy().start, host)
                futures.append(future)

        for future in futures:
            worker_result = future.result()
            result[worker_result.host.name] = worker_result
        return result
