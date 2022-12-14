from typing import TypeVar, Union, NoReturn, Callable, cast
import psutil
from rich.live import Live
from rich.table import Table


class CpuIterator():

    def __init__(self, interval:int = 1) -> None:
        self.interval = interval

    def get_curr_cpu(self, inter) -> float:
        return psutil.cpu_percent(interval=inter)

    def __iter__(self):
        return self

    def __next__(self):
        return self.get_curr_cpu(self.interval)

from rich.console import ConsoleRenderable, RichCast
ColumnName = TypeVar("ColumnName", bound=Union[ConsoleRenderable, RichCast, str])

class TableFabric(Table):
    
    def __init__(self, *args: ColumnName) -> None:
        super().__init__()
        for i in args:
            self.add_column(header=i)
            

def get_proc_percentage(cpu: float = 0) -> Table:
    """ cast в except для mypy
    """
    try:
        table = TableFabric("Metric", "Description", "Value")
        table.add_row('CPU', 'Current cpu usage', f"{str(cpu)}%")
        return table
    except Exception:
        cast(Callable[[], NoReturn], raise_exception)()


def raise_exception():
    raise Exception


if __name__ == "__main__":
    with Live(get_proc_percentage(), refresh_per_second=1) as live:
        cpu = CpuIterator()
        for i in cpu:
            live.update(get_proc_percentage(i))
