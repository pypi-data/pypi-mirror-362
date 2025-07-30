import ast
from typing import Any

from classiq.interface.exceptions import (
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.expressions.proxies.classical.qmod_struct_instance import (
    QmodStructInstance,
)
from classiq.interface.generator.functions.classical_type import (
    Bool,
    ClassicalTuple,
    ClassicalType,
    Integer,
    Real,
)
from classiq.interface.generator.functions.type_name import Struct
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.quantum_type import QuantumType

from classiq.evaluators.qmod_annotated_expression import QmodAnnotatedExpression


def _infer_classical_type(value: Any) -> ClassicalType:
    if isinstance(value, bool):
        return Bool()
    if isinstance(value, int):
        return Integer()
    if isinstance(value, (float, complex)):
        return Real()
    if isinstance(value, list):
        return ClassicalTuple(
            element_types=[_infer_classical_type(item) for item in value]
        )
    if isinstance(value, QmodStructInstance):
        classical_type = Struct(name=value.struct_declaration.name)
        classical_type.set_classical_struct_decl(value.struct_declaration)
        return classical_type
    raise ClassiqInternalExpansionError


def eval_name(expr_val: QmodAnnotatedExpression, node: ast.Name, value: Any) -> None:
    if isinstance(value, (bool, int, float, complex, list, QmodStructInstance)):
        expr_val.set_type(node, _infer_classical_type(value))
        expr_val.set_value(node, value)
    elif isinstance(value, (ClassicalType, QuantumType)):
        expr_val.set_type(node, value)
        expr_val.set_var(node, HandleBinding(name=node.id))
    else:
        raise ClassiqInternalExpansionError
