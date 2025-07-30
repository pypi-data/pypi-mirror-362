import ast
from typing import TYPE_CHECKING

from classiq.interface.exceptions import (
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.functions.classical_type import Integer, Real
from classiq.interface.model.quantum_type import QuantumNumeric

from classiq.evaluators.qmod_annotated_expression import QmodAnnotatedExpression
from classiq.evaluators.qmod_node_evaluators.utils import (
    IntegerValueType,
    NumberValueType,
    QmodType,
    is_classical_integer,
    is_classical_type,
    is_numeric_type,
)


def _binary_op_allowed(left: QmodType, right: QmodType) -> bool:
    return is_numeric_type(left) and is_numeric_type(right)


def _validate_binary_op(op: ast.AST, left_type: QmodType, right_type: QmodType) -> None:
    if not _binary_op_allowed(left_type, right_type):
        raise ClassiqExpansionError(
            f"Both sides of the binary operator {type(op).__name__!r} must be "
            f"scalar values"
        )
    if isinstance(op, (ast.LShift, ast.RShift)) and (
        isinstance(left_type, Real) or isinstance(right_type, Real)
    ):
        raise ClassiqExpansionError(
            f"Bitshift operation {type(op).__name__!r} on real values is not "
            f"supported"
        )
    if isinstance(op, (ast.BitOr, ast.BitXor, ast.BitAnd)) and (
        isinstance(left_type, Real) or isinstance(right_type, Real)
    ):
        raise ClassiqExpansionError(
            f"Bitwise operation {type(op).__name__!r} on real values is not supported"
        )

    if isinstance(op, ast.MatMult):
        raise ClassiqExpansionError(
            f"Binary operation {type(op).__name__!r} is not supported"
        )

    if not is_classical_type(right_type) and (
        isinstance(
            op, (ast.Div, ast.FloorDiv, ast.Mod, ast.Pow, ast.LShift, ast.RShift)
        )
    ):
        raise ClassiqExpansionError(
            f"Right-hand side of binary operation {type(op).__name__!r} must be classical numeric value"
        )


def _eval_binary_op_constant(
    op: ast.AST, left_value: NumberValueType, right_value: NumberValueType
) -> NumberValueType:
    if isinstance(op, ast.Add):
        return left_value + right_value
    if isinstance(op, ast.Sub):
        return left_value - right_value
    if isinstance(op, ast.Mult):
        return left_value * right_value
    if isinstance(op, ast.Div):
        if right_value == 0:
            raise ClassiqExpansionError("Division by zero")
        return left_value / right_value
    if isinstance(op, ast.FloorDiv):
        if right_value == 0:
            raise ClassiqExpansionError("Integer division by zero")
        if isinstance(left_value, complex) or isinstance(right_value, complex):
            raise ClassiqExpansionError("Integer division with a complex number")
        return left_value // right_value
    if isinstance(op, ast.Mod):
        if right_value == 0:
            raise ClassiqExpansionError("Integer modulu by zero")
        if isinstance(left_value, complex) or isinstance(right_value, complex):
            raise ClassiqExpansionError("Integer modulu with a complex number")
        return left_value % right_value
    if isinstance(op, ast.Pow):
        return left_value**right_value

    if TYPE_CHECKING:
        assert isinstance(left_value, IntegerValueType)
        assert isinstance(right_value, IntegerValueType)

    if isinstance(op, ast.LShift):
        return left_value << right_value
    if isinstance(op, ast.RShift):
        return left_value >> right_value
    if isinstance(op, ast.BitAnd):
        return left_value & right_value
    if isinstance(op, ast.BitOr):
        return left_value | right_value
    if isinstance(op, ast.BitXor):
        return left_value ^ right_value

    raise ClassiqInternalExpansionError


def eval_binary_op(expr_val: QmodAnnotatedExpression, node: ast.BinOp) -> None:
    left = node.left
    right = node.right
    op = node.op

    left_type = expr_val.get_type(left)
    right_type = expr_val.get_type(right)
    _validate_binary_op(op, left_type, right_type)

    node_type: QmodType
    if not is_classical_type(left_type) or not is_classical_type(left_type):
        node_type = QuantumNumeric()
    elif (
        not isinstance(op, ast.Div)
        and is_classical_integer(left_type)
        and is_classical_integer(right_type)
    ):
        node_type = Integer()
    else:
        node_type = Real()
    expr_val.set_type(node, node_type)

    if expr_val.has_value(left) and expr_val.has_value(right):
        left_value = expr_val.get_value(left)
        right_value = expr_val.get_value(right)
        expr_val.set_value(node, _eval_binary_op_constant(op, left_value, right_value))
