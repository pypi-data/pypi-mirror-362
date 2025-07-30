import ast
from typing import Any

from classiq.interface.exceptions import (
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.functions.classical_type import Integer, Real
from classiq.interface.generator.functions.type_name import TypeName

from classiq.evaluators.qmod_annotated_expression import QmodAnnotatedExpression
from classiq.evaluators.qmod_node_evaluators.bool_op_evaluation import is_bool_type
from classiq.evaluators.qmod_node_evaluators.utils import QmodType, is_numeric_type


def unary_op_allowed(op: ast.AST, operand_type: QmodType) -> bool:
    if isinstance(op, ast.Not):
        return is_bool_type(operand_type)
    return is_numeric_type(operand_type)


def eval_unary_op(expr_val: QmodAnnotatedExpression, node: ast.UnaryOp) -> None:
    operand = node.operand
    op = node.op

    operand_type = expr_val.get_type(operand)
    if not unary_op_allowed(op, operand_type):
        expected_val_type = "Boolean" if isinstance(op, ast.Not) else "scalar"
        raise ClassiqExpansionError(
            f"The operand of the unary operator {type(op).__name__!r} must be "
            f"a {expected_val_type} value"
        )
    if isinstance(op, ast.Invert) and isinstance(operand_type, Real):
        raise ClassiqExpansionError(
            f"Operation {type(op).__name__!r} on a real value is not supported"
        )
    op_type: QmodType
    if isinstance(operand_type, TypeName):
        op_type = Integer()
    else:
        op_type = operand_type
    expr_val.set_type(node, op_type)

    if not expr_val.has_value(operand):
        return
    operand_value = expr_val.get_value(operand)
    constant_value: Any
    if isinstance(op, ast.Not):
        constant_value = not operand_value
    elif isinstance(op, ast.Invert):
        constant_value = ~operand_value
    elif isinstance(op, ast.UAdd):
        constant_value = +operand_value
    elif isinstance(op, ast.USub):
        constant_value = -operand_value
    else:
        raise ClassiqInternalExpansionError
    expr_val.set_value(node, constant_value)
