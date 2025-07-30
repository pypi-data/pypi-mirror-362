import ast
from typing import Optional, cast

from classiq.interface.exceptions import (
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.arith.arithmetic import (
    aggregate_numeric_types,
    compute_arithmetic_result_type,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.classical_type import (
    ClassicalArray,
    ClassicalTuple,
    Integer,
    Real,
)
from classiq.interface.model.handle_binding import (
    SlicedHandleBinding,
    SubscriptHandleBinding,
)
from classiq.interface.model.quantum_type import (
    QuantumBitvector,
    QuantumNumeric,
    QuantumType,
    register_info_to_quantum_type,
)

from classiq.evaluators.qmod_annotated_expression import QmodAnnotatedExpression
from classiq.evaluators.qmod_node_evaluators.utils import (
    QmodType,
    element_types,
    get_qmod_type_name,
    qnum_is_qint,
)


def _eval_slice(expr_val: QmodAnnotatedExpression, node: ast.Subscript) -> None:
    subject = node.value
    slice_ = cast(ast.Slice, node.slice)
    start = cast(ast.AST, slice_.lower)
    stop = cast(ast.AST, slice_.upper)
    if slice_.step is not None:
        raise ClassiqExpansionError("Slice step is not supported")

    start_type = expr_val.get_type(start)
    stop_type = expr_val.get_type(stop)
    for index_type in (start_type, stop_type):
        if not isinstance(index_type, Integer):
            raise ClassiqExpansionError(
                f"Slice indices must be integers, not {get_qmod_type_name(index_type)!r}"
            )

    start_val: Optional[int] = None
    if expr_val.has_value(start):
        start_val = cast(int, expr_val.get_value(start))
        if start_val < 0:
            raise ClassiqExpansionError("Slice indices must be positive integers")
    stop_val: Optional[int] = None
    if expr_val.has_value(stop):
        stop_val = cast(int, expr_val.get_value(stop))
        if start_val is not None and stop_val < start_val:
            raise ClassiqExpansionError(
                "Slice upper bound must be greater or equal to the lower bound"
            )

    subject_type = expr_val.get_type(subject)
    slice_type: QmodType
    if isinstance(subject_type, ClassicalArray):
        if subject_type.has_length and (
            (start_val is not None and start_val >= subject_type.length_value)
            or (stop_val is not None and stop_val > subject_type.length_value)
        ):
            raise ClassiqExpansionError("Array index out of range")
        length_expr: Optional[Expression] = None
        if start_val is not None and stop_val is not None:
            length_expr = Expression(expr=str(stop_val - start_val))
        slice_type = ClassicalArray(
            element_type=subject_type.element_type, length=length_expr
        )
    elif isinstance(subject_type, ClassicalTuple):
        if start_val is not None and stop_val is not None:
            if start_val >= len(subject_type.element_types) or stop_val > len(
                subject_type.element_types
            ):
                raise ClassiqExpansionError("Array index out of range")
            slice_type = ClassicalTuple(
                element_types=subject_type.element_types[start_val:stop_val]
            )
        else:
            slice_type = subject_type.get_raw_type()
    elif isinstance(subject_type, QuantumBitvector):
        if start_val is not None and stop_val is not None:
            if subject_type.has_length and (
                start_val >= subject_type.length_value
                or stop_val > subject_type.length_value
            ):
                raise ClassiqExpansionError("Array index out of range")
            slice_length = Expression(expr=str(stop_val - start_val))
        else:
            slice_length = None
        slice_type = QuantumBitvector(
            element_type=subject_type.element_type, length=slice_length
        )
    else:
        raise ClassiqExpansionError(
            f"{get_qmod_type_name(subject_type)} is not subscriptable"
        )
    expr_val.set_type(node, slice_type)

    if start_val is None or stop_val is None:
        return
    if expr_val.has_value(subject):
        subject_val = expr_val.get_value(subject)
        expr_val.set_value(node, subject_val[start_val:stop_val])
    elif expr_val.has_var(subject):
        subject_var = expr_val.get_var(subject)
        expr_val.set_var(
            node,
            SlicedHandleBinding(
                base_handle=subject_var,
                start=Expression(expr=str(start_val)),
                end=Expression(expr=str(stop_val)),
            ),
        )
        expr_val.remove_var(subject)


def _eval_subscript(expr_val: QmodAnnotatedExpression, node: ast.Subscript) -> None:
    subject = node.value
    subscript = node.slice

    index_type = expr_val.get_type(subscript)
    if not isinstance(index_type, Integer):
        raise ClassiqExpansionError(
            f"Array indices must be integers or slices, not {get_qmod_type_name(index_type)}"
        )

    sub_val: Optional[int] = None
    if expr_val.has_value(subscript):
        sub_val = cast(int, expr_val.get_value(subscript))
        if sub_val < 0:
            raise ClassiqExpansionError("Array indices must be positive integers")

    subject_type = expr_val.get_type(subject)
    sub_type: QmodType
    if isinstance(subject_type, (ClassicalArray, QuantumBitvector)):
        if (
            sub_val is not None
            and subject_type.has_length
            and sub_val >= subject_type.length_value
        ):
            raise ClassiqExpansionError("Array index out of range")
        sub_type = subject_type.element_type
    elif isinstance(subject_type, ClassicalTuple):
        if sub_val is not None:
            if sub_val >= len(subject_type.element_types):
                raise ClassiqExpansionError("Array index out of range")
            sub_type = subject_type.element_types[sub_val]
        else:
            raw_subject_type = subject_type.get_raw_type()
            if not isinstance(raw_subject_type, ClassicalArray):
                raise ClassiqInternalExpansionError
            sub_type = raw_subject_type.element_type
    else:
        raise ClassiqExpansionError(
            f"{get_qmod_type_name(subject_type)} is not subscriptable"
        )
    expr_val.set_type(node, sub_type)

    if sub_val is None:
        return
    if expr_val.has_value(subject):
        subject_val = expr_val.get_value(subject)
        expr_val.set_value(node, subject_val[sub_val])
    elif expr_val.has_var(subject):
        subject_var = expr_val.get_var(subject)
        expr_val.set_var(
            node,
            SubscriptHandleBinding(
                base_handle=subject_var, index=Expression(expr=str(sub_val))
            ),
        )
        expr_val.remove_var(subject)


def eval_subscript(expr_val: QmodAnnotatedExpression, node: ast.Subscript) -> None:
    if isinstance(node.slice, ast.Slice):
        _eval_slice(expr_val, node)
    else:
        _eval_subscript(expr_val, node)


def eval_quantum_subscript(
    expr_val: QmodAnnotatedExpression, node: ast.Subscript, machine_precision: int
) -> None:
    subject = node.value
    subscript = node.slice

    index_type = cast(QuantumType, expr_val.get_type(subscript))
    if not qnum_is_qint(index_type):
        raise ClassiqExpansionError("Quantum indices must be unsigned quantum numerics")
    subject_type = expr_val.get_type(subject)
    if not isinstance(subject_type, (ClassicalArray, ClassicalTuple)) or not all(
        isinstance(element_type, (Integer, Real))
        for element_type in element_types(subject_type)
    ):
        raise ClassiqExpansionError(
            "Only classical numeric arrays may have quantum subscripts"
        )

    expr_val.set_quantum_subscript(node, subject, subscript)
    if not expr_val.has_value(subject):
        expr_val.set_type(node, QuantumNumeric())
        return

    items = expr_val.get_value(subject)
    numeric_types = [
        compute_arithmetic_result_type(str(num), {}, machine_precision) for num in items
    ]
    unified_numeric_type = register_info_to_quantum_type(
        aggregate_numeric_types(numeric_types)
    )
    expr_val.set_type(node, unified_numeric_type)
