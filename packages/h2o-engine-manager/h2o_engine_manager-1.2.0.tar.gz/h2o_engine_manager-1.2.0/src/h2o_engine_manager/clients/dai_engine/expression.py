from datetime import datetime
from enum import Enum

from h2o_engine_manager.clients.convert import quantity_convertor


class Op(Enum):
    """
    Op is an enum used for specifying logical operation to be performed with filter.
    """

    NIL = ""
    EQUAL = "="
    NOT_EQUAL = "!="
    GREATER = ">"
    GREATER_OR_EQUAL = ">="
    LESS = "<"
    LESS_OR_EQUAL = "<="


class Expression:
    """
    Expression is the base class used to compose filters.
    """

    _kind: str
    _op: Op
    _value: str

    def __str__(self):
        """Constructs a string representation of the expression.

        Returns:
            ExpressionString: the string.
        """
        if self._kind is None or self._op is None or self._value is None:
            return ""

        ret = self._kind
        ret += " " + self._op.value
        ret += " " + self._value
        return ret


class StringExpression(Expression):
    """Assigned values must be strings"""

    def GreaterThan(self, value: str):
        self._op = Op.GREATER
        self._value = value
        return self

    def LessThan(self, value: str):
        self._op = Op.LESS
        self._value = value
        return self

    def GreaterThanOrEqualTo(self, value: str):
        self._op = Op.GREATER_OR_EQUAL
        self._value = value
        return self

    def LessThanOrEqualTo(self, value: str):
        self._op = Op.LESS_OR_EQUAL
        self._value = value
        return self

    def EqualTo(self, value: str):
        self._op = Op.EQUAL
        self._value = value
        return self

    def NotEqualTo(self, value: str):
        self._op = Op.NOT_EQUAL
        self._value = value
        return self


class QuotedStringExpression(Expression):
    def GreaterThan(self, value: str):
        self._op = Op.GREATER
        self._value = '"' + value + '"'
        return self

    def LessThan(self, value: str):
        self._op = Op.LESS
        self._value = '"' + value + '"'
        return self

    def GreaterThanOrEqualTo(self, value: str):
        self._op = Op.GREATER_OR_EQUAL
        self._value = '"' + value + '"'
        return self

    def LessThanOrEqualTo(self, value: str):
        self._op = Op.LESS_OR_EQUAL
        self._value = '"' + value + '"'
        return self

    def EqualTo(self, value: str):
        self._op = Op.EQUAL
        self._value = '"' + value + '"'
        return self

    def NotEqualTo(self, value: str):
        self._op = Op.NOT_EQUAL
        self._value = '"' + value + '"'
        return self


class QuantityExpression(Expression):
    """Assigned value is a string representation of memory size"""

    @staticmethod
    def _parse(size: str):
        return quantity_convertor.quantity_to_number(size)

    def GreaterThan(self, value: str):
        self._op = Op.GREATER
        self._value = str(self._parse(value))
        return self

    def LessThan(self, value: str):
        self._op = Op.LESS
        self._value = str(self._parse(value))
        return self

    def GreaterThanOrEqualTo(self, value: str):
        self._op = Op.GREATER_OR_EQUAL
        self._value = str(self._parse(value))
        return self

    def LessThanOrEqualTo(self, value: str):
        self._op = Op.LESS_OR_EQUAL
        self._value = str(self._parse(value))
        return self

    def EqualTo(self, value: str):
        self._op = Op.EQUAL
        self._value = str(self._parse(value))
        return self

    def NotEqualTo(self, value: str):
        self._op = Op.NOT_EQUAL
        self._value = str(self._parse(value))
        return self


class NumberExpression(Expression):
    """Assigned value must be an integer"""

    def GreaterThan(self, value: int):
        self._op = Op.GREATER
        self._value = str(value)
        return self

    def LessThan(self, value: int):
        self._op = Op.LESS
        self._value = str(value)
        return self

    def GreaterThanOrEqualTo(self, value: int):
        self._op = Op.GREATER_OR_EQUAL
        self._value = str(value)
        return self

    def LessThanOrEqualTo(self, value: int):
        self._op = Op.LESS_OR_EQUAL
        self._value = str(value)
        return self

    def EqualTo(self, value: int):
        self._op = Op.EQUAL
        self._value = str(value)
        return self

    def NotEqualTo(self, value: int):
        self._op = Op.NOT_EQUAL
        self._value = str(value)
        return self


class TimeExpression(Expression):
    """Assigned value must be datetime"""

    @staticmethod
    def _format(time: datetime):
        strval = time.isoformat(timespec="seconds")
        if time.tzinfo:
            srtval = strval.replace("+00:00", "Z")
        else:
            strval += "Z"
        return strval

    def GreaterThan(self, value: datetime):
        self._op = Op.GREATER
        self._value = self._format(value)
        return self

    def LessThan(self, value: datetime):
        self._op = Op.LESS
        self._value = self._format(value)
        return self

    def GreaterThanOrEqualTo(self, value: datetime):
        self._op = Op.GREATER_OR_EQUAL
        self._value = self._format(value)
        return self

    def LessThanOrEqualTo(self, value: datetime):
        self._op = Op.LESS_OR_EQUAL
        self._value = self._format(value)
        return self

    def EqualTo(self, value: datetime):
        self._op = Op.EQUAL
        self._value = self._format(value)
        return self

    def NotEqualTo(self, value: datetime):
        self._op = Op.NOT_EQUAL
        self._value = self._format(value)
        return self


class EnumExpression(Expression):
    """Assigned value must be enum, no greater or less than comparison possible"""

    def EqualTo(self, value: Enum):
        self._op = Op.EQUAL
        self._value = value.value
        return self

    def NotEqualTo(self, value: Enum):
        self._op = Op.NOT_EQUAL
        self._value = value.value
        return self


class BoolExpression(Expression):
    """Assigned value must be a bool, no greater or less than comparison possible"""

    def EqualTo(self, value: bool):
        self._op = Op.EQUAL
        self._value = str(value).lower()
        return self

    def NotEqualTo(self, value: Enum):
        self._op = Op.NOT_EQUAL
        self._value = str(value).lower()
        return self


class Version(StringExpression):
    def __init__(self):
        self._kind = "version"


class Name(QuotedStringExpression):
    def __init__(self):
        self._kind = "name"


class Creator(QuotedStringExpression):
    def __init__(self):
        self._kind = "creator"


class Uid(QuotedStringExpression):
    def __init__(self):
        self._kind = "uid"


class State(EnumExpression):
    def __init__(self):
        self._kind = "state"


class Cpu(NumberExpression):
    def __init__(self):
        self._kind = "cpu"


class Gpu(NumberExpression):
    def __init__(self):
        self._kind = "gpu"


class MemoryBytes(QuantityExpression):
    def __init__(self):
        self._kind = "memory_bytes"


class StorageBytes(QuantityExpression):
    def __init__(self):
        self._kind = "storage_bytes"


class CreateTime(TimeExpression):
    def __init__(self):
        self._kind = "create_time"


class UpdateTime(TimeExpression):
    def __init__(self):
        self._kind = "update_time"


class DeleteTime(TimeExpression):
    def __init__(self):
        self._kind = "delete_time"


class ResumeTime(TimeExpression):
    def __init__(self):
        self._kind = "resume_time"


class Reconciling(Expression):
    def __init__(self):
        self._kind = "reconciling"


class DisplayName(StringExpression):
    def __init__(self):
        self._kind = "display_name"


class MaxIdleDuration(StringExpression):
    def __init__(self):
        self._kind = "max_idle_duration"


class MaxRunningDuration(StringExpression):
    def __init__(self):
        self._kind = "max_running_duration"


class FilterBuilder:
    """
    FilterBuilder is used to construct filter strings for fetching DAI engines or versions

    Filter is composed by adding Expressions using WithFilter
    """

    def __init__(self):
        self._filters = []

    def WithFilter(self, expression: Expression):
        """
        Adds expression to the filter

        Arguments:
            Expression: Any kind of expression

        Returns:
            FilterBuilder
        """
        self._filters.append(expression)
        return self

    def Build(self):
        """
        Builds the filter string to be passed using the client API

        Returns:
            Filter: the composed filter string
        """
        ret = ""
        for fil in self._filters:
            strval = str(fil)
            if not strval:
                continue
            if not ret:
                ret = strval
                continue
            ret += " AND " + strval
        return ret
