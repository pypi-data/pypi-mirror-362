"""
Pretty assertions
"""

from datetime import datetime
from typing import Any, List, Optional, Union
import logging

from rich.console import Console
from rich.table import Table, Text
from zelos_sdk.core import ContextBase
from zelos_sdk.trace import TraceSourceCacheLastField
import pytest

from .items import CheckerItem, ForDurationCheckerItem, WithinDurationCheckerItem
from .ops import DescriptiveOp, get_op

log = logging.getLogger("zelos-checker")


class Checker(ContextBase):
    """
    A collection of checker assertions.
    """

    def __init__(self, title: Optional[str] = None, fail_fast: bool = True):
        """
        Initialize a Checklist with a name.

        :param title: Optional, adds additional title text to the checker board
        :param fail_fast: Optional, Flag to determine if a check should fail right away or delay
                          until the end of all checks. (Default: True)
        """
        super().__init__()
        self._fail_fast = fail_fast
        self._checks: List[CheckerItem] = []
        board_title = "Zelos Checkerboard"
        if title is not None:
            board_title += f"\n{title}"
        self._board = Table(title=board_title, show_header=True, title_style="bold bright_magenta")
        self._board.add_column("timestamp", justify="center")
        self._board.add_column("lhs", justify="center")
        self._board.add_column("operator", justify="center")
        self._board.add_column("rhs", justify="center")
        self._board.add_column("parameters", justify="center")
        self._board.add_column("result", justify="center")

    def that(
        self,
        lhs: Union[TraceSourceCacheLastField, Any],
        op: Union[str, DescriptiveOp] = "is true",
        rhs: Union[TraceSourceCacheLastField, Any] = None,
        for_duration_s: float = None,
        within_duration_s: float = None,
        interval_s: float = 0.1,
        blocking: bool = True,
        args: tuple = (),
        kwargs: dict = {},
    ) -> CheckerItem:
        """
        Add and evaluate a checker assertion.

        :param lhs: Left-hand side operand.
        :param op: Operator for the check.
        :param rhs: Right-hand side operand.
        :param within_duration_s: The condition should be true within this duration.
        :param for_duration_s: The condition should be true for this duration.
        :param interval_s: Interval between condition checks.
        :param blocking: Whether the polling should be blocking.
        :param args: Additional arguments for the operator.
        :param kwargs: Additional keyword arguments for the operator.
        """
        __tracebackhide__ = True
        op_func = get_op(op) if isinstance(op, str) else op

        # Determine which CheckerItem to build
        if for_duration_s is not None and within_duration_s is not None:
            raise ValueError("Cannot specify both 'for_duration_s' and 'within_duration_s'.")

        if for_duration_s is not None:
            item = ForDurationCheckerItem(
                lhs=lhs,
                op=op_func,
                rhs=rhs,
                args=args,
                kwargs=kwargs,
                duration_s=for_duration_s,
                interval_s=interval_s,
                blocking=blocking,
                callback=self._add_to_board,
            )
        elif within_duration_s is not None:
            item = WithinDurationCheckerItem(
                lhs=lhs,
                op=op_func,
                rhs=rhs,
                args=args,
                kwargs=kwargs,
                duration_s=within_duration_s,
                interval_s=interval_s,
                blocking=blocking,
                callback=self._add_to_board,
            )
        else:
            item = CheckerItem(lhs=lhs, op=op_func, rhs=rhs, args=args, kwargs=kwargs)
            self._add_to_board(item)

        return item

    def _add_to_board(self, item: CheckerItem) -> None:
        """
        Adds a checker item to the board.

        :param item: The checker item to add.
        """
        __tracebackhide__ = True

        self._checks.append(item)
        # Apply dim style for alternating rows, except for the last column
        dim_style = None if len(self._checks) % 2 != 0 else "dim"
        result_text, result_color = ("PASSED", "green") if item.result else ("FAILED", "red")

        self._board.add_row(
            Text(datetime.utcfromtimestamp(item.time_ns // 1e9).isoformat(), style=dim_style),
            Text(str(item.lhs), style=dim_style),
            Text(item.op.desc, style=dim_style),
            Text(str(item.rhs) if not item.op.is_unary else "", style=dim_style),
            Text(item.params, style=dim_style),
            Text(result_text, style=result_color),
        )

        if self._fail_fast and not item.result:
            pytest.fail(str(item))

    def _open(self) -> None:
        """Open the checker context."""
        pass

    def _close(self) -> None:
        """Close the checker context and print the results."""
        if self._checks:
            console = Console()
            with console.capture() as capture:
                console.print(self._board)
            log.info("\n%s", capture.get())

    def __len__(self) -> int:
        return len(self._checks)

    def __iter__(self) -> CheckerItem:
        yield from self._checks


def log_table(rich_table: Table) -> Text:
    """
    Generate rich table as ASCII without any column styling for logger.

    :param rich_table: The rich table to convert.
    :return: The ASCII representation of the rich table.
    """
    console = Console()
    with console.capture() as capture:
        console.print(rich_table)
    return Text.from_ansi(capture.get())
