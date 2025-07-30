from collections.abc import Sequence

from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.functions.type_modifier import TypeModifier
from classiq.interface.model.port_declaration import AnonPortDeclaration
from classiq.interface.model.quantum_function_declaration import AnonPositionalArg
from classiq.interface.model.quantum_type import QuantumNumeric

from classiq.evaluators.quantum_type_utils import copy_type_information
from classiq.model_expansions.scope import Evaluated, QuantumVariable


def add_information_from_output_arguments(
    parameters: Sequence[AnonPositionalArg],
    args: list[Evaluated],
) -> None:
    """
    This function propagates the quantum type information from the output arguments
    to the arguments that were passed to it.
    Example:
        ...
        p = QArray("p", QBit)
        allocate(4, p)
        other statements with p...

    In the other statements with p, the size of 4 will be part of p's type info.
    """
    for parameter, argument in zip(parameters, args):
        if not isinstance(parameter, AnonPortDeclaration):
            continue

        argument_as_quantum_symbol = argument.as_type(QuantumVariable)

        if parameter.direction != PortDeclarationDirection.Output:
            continue

        if parameter.quantum_type.is_evaluated:
            copy_type_information(
                parameter.quantum_type,
                argument_as_quantum_symbol.quantum_type,
                str(argument_as_quantum_symbol),
            )


def handle_args_numeric_bounds(
    parameters: Sequence[AnonPositionalArg],
    args: list[Evaluated],
) -> None:
    for parameter, argument in zip(parameters, args):
        if not isinstance(parameter, AnonPortDeclaration):
            continue

        argument_as_quantum_symbol = argument.as_type(QuantumVariable)

        if (
            parameter.direction != PortDeclarationDirection.Output
            and parameter.type_modifier != TypeModifier.Const
            and isinstance(argument_as_quantum_symbol.quantum_type, QuantumNumeric)
        ):
            argument_as_quantum_symbol.quantum_type.reset_bounds()
