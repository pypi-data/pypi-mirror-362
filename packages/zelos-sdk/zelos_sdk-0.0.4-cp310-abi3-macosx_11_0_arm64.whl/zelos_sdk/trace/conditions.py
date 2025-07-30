from abc import ABC, abstractmethod
from typing import Any, List
import sys

DEFAULT_LOGGING_TIME_PERIOD = 1.0
DEFAULT_LOGGING_EPSILON = 0.1  # sys.float_info.epsilon is a bit too fine grained for general use


class LogCondition(ABC):
    """Base class for logging conditions that determine when a field should be logged."""

    def __init__(self):
        self.last_log_time_ns: int = 0
        self.last_logged_value: Any = None

    @abstractmethod
    def should_log(self, current_value: Any, current_time_ns: int) -> bool:
        """
        Determine if the field should be logged based on current and last logged values.

        Args:
            current_value: The current value to potentially log
            last_logged_value: The last value that was actually logged (not just cached)
            current_time_ns: Current time in nanoseconds

        Returns:
            True if the field should be logged, False otherwise
        """
        pass

    def on_logged(self, current_value: Any, current_time_ns: int) -> None:
        """Called when the field is actually logged to update internal state."""
        self.last_logged_value = current_value
        self.last_log_time_ns = current_time_ns

    @staticmethod
    def time_elapsed(current_time_ns: int, last_time_ns: int, threshold_s: float) -> bool:
        """Check if enough time has elapsed based on threshold."""
        if last_time_ns == 0:
            return True  # First log
        elapsed_s = (current_time_ns - last_time_ns) / 1e9
        return elapsed_s >= threshold_s


class TimeLogCondition(LogCondition):
    """Log based purely on time intervals."""

    def __init__(self, time_threshold_s: float = DEFAULT_LOGGING_TIME_PERIOD):
        super().__init__()
        self.time_threshold_s = time_threshold_s

    def should_log(self, current_value: Any, current_time_ns: int) -> bool:
        return self.time_elapsed(current_time_ns, self.last_log_time_ns, self.time_threshold_s)


class ValueLogCondition(LogCondition):
    """Log when the value changes from the last logged value."""

    def should_log(self, current_value: Any, current_time_ns: int) -> bool:
        return current_value != self.last_logged_value


class DeltaLogCondition(LogCondition):
    """Log when the numeric value changes by more than the specified delta from the last logged value."""

    def __init__(self, delta: Any):
        super().__init__()
        self.delta = delta

    def should_log(self, current_value: Any, current_time_ns: int) -> bool:
        if self.last_logged_value is None:
            return True

        try:
            diff = abs(current_value - self.last_logged_value)
            return diff >= self.delta
        except (TypeError, ValueError):
            # Fallback to simple inequality for non-numeric types
            return current_value != self.last_logged_value


class EpsilonLogCondition(DeltaLogCondition):
    """Log when the float value changes by more than machine epsilon."""

    def __init__(self, epsilon: float = sys.float_info.epsilon):
        super().__init__(epsilon)


class CompositeLogCondition(LogCondition):
    """Combine multiple conditions with OR logic."""

    def __init__(self, conditions: List[LogCondition]):
        super().__init__()
        self.conditions = conditions

    def should_log(self, current_value: Any, current_time_ns: int) -> bool:
        return any(condition.should_log(current_value, current_time_ns) for condition in self.conditions)

    def on_logged(self, current_value: Any, current_time_ns: int) -> None:
        super().on_logged(current_value, current_time_ns)
        for condition in self.conditions:
            condition.on_logged(current_value, current_time_ns)


class DefaultLogCondition(LogCondition):
    """Default logging condition: time-based at 1Hz + (value change for non-floats OR epsilon for floats)."""

    def __init__(self, time_threshold_s: float = DEFAULT_LOGGING_TIME_PERIOD, epsilon: float = DEFAULT_LOGGING_EPSILON):
        super().__init__()
        self.time_threshold_s = time_threshold_s
        self.epsilon = epsilon

    def should_log(self, current_value: Any, current_time_ns: int) -> bool:
        # Time-based logging
        if self.time_elapsed(current_time_ns, self.last_log_time_ns, self.time_threshold_s):
            return True

        # Value-based logging
        if self.last_logged_value is None:
            return True

        # For float types, use epsilon comparison
        # TODO(tkeairns): Consider that we want to have type coercion for floats that are set to ints and vice versa
        if isinstance(current_value, float) and isinstance(self.last_logged_value, float):
            diff = abs(current_value - self.last_logged_value)
            return diff >= self.epsilon

        # For non-float types, use value change
        return current_value != self.last_logged_value


class ValueOrTimeLogCondition(CompositeLogCondition):
    """Log when value changes OR when time threshold is exceeded."""

    def __init__(self, time_threshold_s: float = DEFAULT_LOGGING_TIME_PERIOD):
        conditions = [TimeLogCondition(time_threshold_s), ValueLogCondition()]
        super().__init__(conditions)


class EpsilonOrTimeLogCondition(CompositeLogCondition):
    """Log when value changes by epsilon OR when time threshold is exceeded."""

    def __init__(self, epsilon: float, time_threshold_s: float = DEFAULT_LOGGING_TIME_PERIOD):
        conditions = [TimeLogCondition(time_threshold_s), EpsilonLogCondition(epsilon)]
        super().__init__(conditions)


class DeltaOrTimeLogCondition(CompositeLogCondition):
    """Log when value changes by delta OR when time threshold is exceeded."""

    def __init__(self, delta: float, time_threshold_s: float = DEFAULT_LOGGING_TIME_PERIOD):
        conditions = [TimeLogCondition(time_threshold_s), DeltaLogCondition(delta)]
        super().__init__(conditions)
