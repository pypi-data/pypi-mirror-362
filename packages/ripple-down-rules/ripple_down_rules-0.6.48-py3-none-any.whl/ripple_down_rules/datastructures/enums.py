from __future__ import annotations

from enum import auto, Enum

from typing_extensions import List, Dict, Any, Type

from ripple_down_rules.utils import SubclassJSONSerializer


class ExitStatus(Enum):
    """
    Describes the status at exit of the user interface.
    """
    CLOSE = auto()
    """
    The user wants to stop the program.
    """
    SUCCESS = auto()
    """
    The user completed the task successfully.
    """

class InteractionMode(Enum):
    """
    The interaction mode of the RDR.
    """
    IPythonOnly = auto()
    """
    IPythonOnly mode, the mode where the user uses only an Ipython shell to interact with the RDR.
    """
    GUI = auto()
    """
    GUI mode, the mode where the user uses a GUI to interact with the RDR.
    """


class Editor(str, Enum):
    """
    The editor that is used to edit the rules.
    """
    Pycharm = "pycharm"
    """
    PyCharm editor.
    """
    Code = "code"
    """
    Visual Studio Code editor.
    """
    CodeServer = "code-server"
    """
    Visual Studio Code server editor.
    """
    @classmethod
    def from_str(cls, editor: str) -> Editor:
        """
        Convert a string value to an Editor enum.

        :param editor: The string that represents the editor name.
        :return: The Editor enum.
        """
        if editor not in cls._value2member_map_:
            raise ValueError(f"Editor {editor} is not supported.")
        return cls._value2member_map_[editor]


class Category(str, SubclassJSONSerializer, Enum):

    @classmethod
    def from_str(cls, value: str) -> Category:
        return getattr(cls, value)

    @classmethod
    def from_strs(cls, values: List[str]) -> List[Category]:
        return [cls.from_str(value) for value in values]

    @property
    def as_dict(self):
        return {self.__class__.__name__.lower(): self.value}

    def _to_json(self) -> Dict[str, Any]:
        return self.as_dict

    @classmethod
    def _from_json(cls, data: Dict[str, Any]) -> Category:
        return cls.from_str(data[cls.__name__.lower()])


class Stop(Category):
    """
    A stop category is a special category that represents the stopping of the classification to prevent a wrong
    conclusion from being made.
    """
    stop = "stop"


class ExpressionParser(Enum):
    """
    Parsers for expressions to evaluate and encapsulate the expression into a callable function.
    """
    ASTVisitor: int = auto()
    """
    Generic python Abstract Syntax Tree that detects variables, attributes, binary/boolean expressions , ...etc.
    """
    SQLAlchemy: int = auto()
    """
    Specific for SQLAlchemy expressions on ORM Tables.
    """


class PromptFor(Enum):
    """
    The reason of the prompt. (e.g. get conditions, conclusions, or affirmation).
    """
    Conditions: str = "conditions"
    """
    Prompt for rule conditions about a case.
    """
    Conclusion: str = "value"
    """
    Prompt for rule conclusion about a case.
    """
    Affirmation: str = "affirmation"
    """
    Prompt for rule conclusion affirmation about a case.
    """

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class CategoricalValue(Enum):
    """
    A categorical value is a value that is a category.
    """

    def __eq__(self, other):
        if isinstance(other, CategoricalValue):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        return self.name == other

    def __hash__(self):
        return hash(self.name)

    @classmethod
    def to_list(cls):
        return list(cls._value2member_map_.keys())

    @classmethod
    def from_str(cls, category: str):
        return cls[category.lower()]

    @classmethod
    def from_strs(cls, categories: List[str]):
        return [cls.from_str(c) for c in categories]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class RDRMode(Enum):
    Propositional = auto()
    """
    Propositional mode, the mode where the rules are propositional.
    """
    Relational = auto()
    """
    Relational mode, the mode where the rules are relational.
    """


class MCRDRMode(Enum):
    """
    The modes of the MultiClassRDR.
    """
    StopOnly = auto()
    """
    StopOnly mode, stop wrong conclusion from being made and does not add a new rule to make the correct conclusion.
    """
    StopPlusRule = auto()
    """
    StopPlusRule mode, stop wrong conclusion from being made and adds a new rule with same conditions as stopping rule
     to make the correct conclusion.
    """
    StopPlusRuleCombined = auto()
    """
    StopPlusRuleCombined mode, stop wrong conclusion from being made and adds a new rule with combined conditions of
    stopping rule and the rule that should have fired.
    """


class RDREdge(Enum):
    Refinement = "except if"
    """
    Refinement edge, the edge that represents the refinement of an incorrectly fired rule.
    """
    Alternative = "else if"
    """
    Alternative edge, the edge that represents the alternative to the rule that has not fired.
    """
    Next = "next"
    """
    Next edge, the edge that represents the next rule to be evaluated.
    """
    Filter = "filter if"
    """
    Filter edge, the edge that represents the filter condition.
    """

class ValueType(Enum):
    Unary = auto()
    """
    Unary value type (eg. null).
    """
    Binary = auto()
    """
    Binary value type (eg. True, False).
    """
    Discrete = auto()
    """
    Discrete value type (eg. 1, 2, 3).
    """
    Continuous = auto()
    """
    Continuous value type (eg. 1.0, 2.5, 3.4).
    """
    Nominal = auto()
    """
    Nominal value type (eg. red, blue, green), categories where the values have no natural order.
    """
    Ordinal = auto()
    """
    Ordinal value type (eg. low, medium, high), categories where the values have a natural order.
    """
    Iterable = auto()
    """
    Iterable value type (eg. [1, 2, 3]).
    """
