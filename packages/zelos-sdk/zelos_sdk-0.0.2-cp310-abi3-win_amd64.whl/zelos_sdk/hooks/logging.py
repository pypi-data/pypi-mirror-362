"""
Implements a TraceLoggingHandler which sends python logs to the Zelos SDK.
"""

import logging

import zelos_sdk


class TraceLoggingHandler(logging.Handler):
    """A logging handler that sends log records to the Zelos SDK."""

    def __init__(self, source_name: str = "logger", level: int = logging.DEBUG):
        super().__init__(level)

        self.trace_source = zelos_sdk.TraceSource(source_name)
        self.trace_event = self.trace_source.add_event(
            "log",
            [
                zelos_sdk.TraceEventFieldMetadata("level", zelos_sdk.DataType.String),
                zelos_sdk.TraceEventFieldMetadata("message", zelos_sdk.DataType.String),
                zelos_sdk.TraceEventFieldMetadata("name", zelos_sdk.DataType.String),
                zelos_sdk.TraceEventFieldMetadata("file", zelos_sdk.DataType.String),
                zelos_sdk.TraceEventFieldMetadata("line", zelos_sdk.DataType.UInt32),
            ],
        )

    def emit(self, record: logging.LogRecord) -> None:
        try:
            ts_ns = int(record.created * 1_000_000_000)
            self.trace_event.log_at(
                ts_ns,
                level=record.levelname,
                message=record.getMessage(),
                name=record.name,
                file=record.filename,
                line=record.lineno,
            )
        except Exception:
            pass
