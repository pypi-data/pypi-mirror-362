from typing import TYPE_CHECKING, Literal

from classiq.interface.ast_node import ASTNodeType, reset_lists
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.model.quantum_statement import QuantumOperation

if TYPE_CHECKING:
    from classiq.interface.model.statement_block import StatementBlock


class ClassicalIf(QuantumOperation):
    kind: Literal["ClassicalIf"]

    condition: Expression
    then: "StatementBlock"
    else_: "StatementBlock"

    def _as_back_ref(self: ASTNodeType) -> ASTNodeType:
        return reset_lists(self, ["then", "else_"])

    @property
    def expressions(self) -> list[Expression]:
        return [self.condition]
