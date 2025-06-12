from dataclasses import dataclass

from problems import StripsProposition


@dataclass(frozen=True)
class Literal:
    """
    Literal represents a possibly negated STRIPS proposition.

    Attributes:
        proposition: StripsProposition
            A proposition forming the literal.
        true: bool
            Whether the proposition is true or negted.
    """
    proposition: StripsProposition
    true: bool

    def __str__(self):
        prefix = "" if self.true else "~"
        return f"{prefix}{self.proposition}"
