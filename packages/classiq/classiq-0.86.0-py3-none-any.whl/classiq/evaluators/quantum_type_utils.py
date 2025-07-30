from classiq.interface.exceptions import (
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.concrete_types import ConcreteQuantumType
from classiq.interface.generator.functions.type_name import (
    TypeName,
)
from classiq.interface.model.bind_operation import BindOperation
from classiq.interface.model.inplace_binary_operation import BinaryOperation
from classiq.interface.model.quantum_type import (
    QuantumBit,
    QuantumBitvector,
    QuantumNumeric,
    QuantumScalar,
    QuantumType,
)

from classiq.model_expansions.scope import QuantumSymbol, Scope


def copy_type_information(
    from_type: QuantumType,
    to_type: QuantumType,
    to_param_name: str,
) -> None:
    if isinstance(to_type, QuantumBit):
        set_size(to_type, from_type.size_in_bits, to_param_name)
    elif isinstance(to_type, QuantumNumeric):
        if to_type.size is None and isinstance(from_type, QuantumNumeric):
            to_type.is_signed = Expression(expr=str(from_type.sign_value))
            to_type.fraction_digits = Expression(
                expr=str(from_type.fraction_digits_value)
            )
        set_size(to_type, from_type.size_in_bits, to_param_name)
        set_bounds(from_type, to_type)
    elif isinstance(to_type, QuantumBitvector):
        if isinstance(from_type, QuantumBitvector) and type(  # noqa: E721
            from_type.element_type
        ) == type(to_type.element_type):
            copy_type_information(
                from_type.element_type, to_type.element_type, to_param_name
            )
        set_size(to_type, from_type.size_in_bits, to_param_name)
    elif isinstance(to_type, TypeName):
        if isinstance(from_type, TypeName) and from_type.name == to_type.name:
            for field in from_type.fields:
                copy_type_information(
                    from_type.fields[field], to_type.fields[field], to_param_name
                )
        set_size(to_type, from_type.size_in_bits, to_param_name)
    else:
        raise ClassiqInternalExpansionError


def set_size(quantum_type: QuantumType, size: int, param_name: str) -> None:
    if size <= 0:
        raise ClassiqExpansionError(
            f"Size for {param_name!r} was deduced to be non-positive: {size!r}"
        )

    if quantum_type.has_size_in_bits and quantum_type.size_in_bits != size:
        raise ClassiqExpansionError(
            f"Size mismatch for variable {param_name!r} between declared size {quantum_type.size_in_bits} and assigned size {size}"
        )

    if isinstance(quantum_type, QuantumNumeric):
        quantum_type.size = Expression(expr=str(size))
        if not quantum_type.has_sign or not quantum_type.has_fraction_digits:
            quantum_type.is_signed = Expression(expr="False")
            quantum_type.fraction_digits = Expression(expr="0")
    elif isinstance(quantum_type, QuantumBitvector):
        if quantum_type.has_length:
            if size % quantum_type.length_value != 0:
                raise ClassiqExpansionError(
                    f"Size mismatch for variable {param_name!r}. Cannot fit {size} "
                    f"qubits into an array of {quantum_type.length_value} elements."
                )
            set_size(
                quantum_type.element_type,
                size // quantum_type.length_value,
                param_name,
            )
        set_length_by_size(quantum_type, size, param_name)
    elif isinstance(quantum_type, TypeName):
        fields_without_size = [
            field_type
            for field_type in quantum_type.fields.values()
            if not field_type.has_size_in_bits
        ]
        if len(fields_without_size) > 1:
            raise ClassiqInternalExpansionError(
                f"QuantumStruct should have at most one field without "
                f"predetermined size. Found {fields_without_size}."
            )
        if len(fields_without_size) == 1:
            predetermined_size_part = sum(
                field_type.size_in_bits if field_type.has_size_in_bits else 0
                for field_type in quantum_type.fields.values()
            )
            set_size(fields_without_size[0], size - predetermined_size_part, param_name)


def set_element_type(
    quantum_array: QuantumBitvector, element_type: ConcreteQuantumType
) -> None:
    quantum_array.element_type = element_type


def set_length(quantum_array: QuantumBitvector, length: int) -> None:
    quantum_array.length = Expression(expr=str(length))


def set_length_by_size(
    quantum_array: QuantumBitvector, size: int, param_name: str
) -> None:
    if size <= 0:
        raise ClassiqExpansionError(
            f"Size for {param_name!r} was deduced to be non-positive: {size!r}"
        )

    if quantum_array.has_size_in_bits and quantum_array.size_in_bits != size:
        raise ClassiqExpansionError(
            f"Size mismatch for variable {param_name!r} between declared size "
            f"{quantum_array.size_in_bits} ({quantum_array.length_value} elements of "
            f"size {quantum_array.element_type.size_in_bits}) and assigned size {size}."
        )

    if not quantum_array.element_type.has_size_in_bits:
        raise ClassiqExpansionError(
            f"Could not infer element size for array {param_name!r}."
        )
    element_size = quantum_array.element_type.size_in_bits

    if size % element_size != 0:
        raise ClassiqExpansionError(
            f"Size mismatch for variable {param_name!r}. Cannot fit elements of type "
            f"{quantum_array.element_type.qmod_type_name} (size {element_size}) into "
            f"{size} qubits."
        )

    quantum_array.length = Expression(expr=str(size // element_size))


def validate_bind_targets(bind: BindOperation, scope: Scope) -> None:
    illegal_qnum_bind_targets = []
    for out_handle in bind.out_handles:
        out_var = scope[out_handle.name].as_type(QuantumSymbol)
        out_var_type = out_var.quantum_type
        if not isinstance(out_var_type, QuantumNumeric):
            continue
        if not out_var_type.has_size_in_bits:
            illegal_qnum_bind_targets.append(str(out_var.handle))
        elif not out_var_type.has_sign:
            assert not out_var_type.has_fraction_digits
            illegal_qnum_bind_targets.append(str(out_var.handle))
    if len(illegal_qnum_bind_targets) > 0:
        raise ClassiqExpansionError(
            f"QNum bind targets {illegal_qnum_bind_targets!r} must be declared or initialized with size, sign, and fraction digits"
        )


def get_inplace_op_scalar_as_numeric(
    var: QuantumSymbol, operation: BinaryOperation, var_kind: str
) -> QuantumNumeric:
    if not isinstance(var.quantum_type, QuantumScalar):
        raise ClassiqExpansionError(
            f"Cannot perform inplace {operation.name.lower()} with non-scalar {var_kind} {var.handle}"
        )
    if isinstance(var.quantum_type, QuantumNumeric):
        return var.quantum_type
    if isinstance(var.quantum_type, QuantumBit):
        return QuantumNumeric(
            size=Expression(expr="1"),
            is_signed=Expression(expr="False"),
            fraction_digits=Expression(expr="0"),
        )
    raise ClassiqInternalExpansionError(f"Unexpected scalar type {var.quantum_type}")


def set_bounds(from_type: QuantumType, to_type: QuantumNumeric) -> None:
    if not isinstance(from_type, QuantumNumeric):
        to_type.reset_bounds()
        return

    if from_type.is_evaluated and to_type.is_evaluated:
        same_attributes = to_type.sign_value == from_type.sign_value and (
            to_type.fraction_digits_value == from_type.fraction_digits_value
        )
    else:
        same_attributes = (
            (from_type.is_signed is not None and from_type.fraction_digits is not None)
            and (to_type.is_signed is not None and to_type.fraction_digits is not None)
            and (to_type.is_signed.expr == from_type.is_signed.expr)
            and (to_type.fraction_digits.expr == from_type.fraction_digits.expr)
        )

    if same_attributes:
        to_type.set_bounds(from_type.get_bounds())
    else:
        to_type.reset_bounds()
