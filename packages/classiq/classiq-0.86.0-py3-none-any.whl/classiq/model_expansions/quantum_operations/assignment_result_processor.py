from typing import TYPE_CHECKING, Optional

from classiq.interface.exceptions import ClassiqExpansionError
from classiq.interface.generator.arith.arithmetic import compute_arithmetic_result_type
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.model.allocate import Allocate
from classiq.interface.model.bind_operation import BindOperation
from classiq.interface.model.block import Block
from classiq.interface.model.bounds import SetBoundsStatement
from classiq.interface.model.handle_binding import (
    ConcreteHandleBinding,
    HandleBinding,
    SubscriptHandleBinding,
)
from classiq.interface.model.quantum_expressions.arithmetic_operation import (
    ArithmeticOperation,
    ArithmeticOperationKind,
)
from classiq.interface.model.quantum_expressions.quantum_expression import (
    QuantumAssignmentOperation,
)
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_type import QuantumBitvector, QuantumNumeric
from classiq.interface.model.statement_block import StatementBlock
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)
from classiq.interface.model.within_apply_operation import WithinApply

from classiq.evaluators.quantum_type_utils import copy_type_information
from classiq.model_expansions.quantum_operations.arithmetic.explicit_boolean_expressions import (
    convert_assignment_bool_expression,
    validate_assignment_bool_expression,
)
from classiq.model_expansions.quantum_operations.emitter import Emitter
from classiq.model_expansions.scope import ClassicalSymbol
from classiq.model_expansions.transformers.ast_renamer import rename_variables
from classiq.qmod.builtins.functions.standard_gates import CX

if TYPE_CHECKING:
    from classiq.model_expansions.interpreters.base_interpreter import BaseInterpreter


class AssignmentResultProcessor(Emitter[QuantumAssignmentOperation]):
    def __init__(
        self, interpreter: "BaseInterpreter", replace_assignment_if_needed: bool = False
    ) -> None:
        super().__init__(interpreter)
        self._replace_assignment_if_needed = replace_assignment_if_needed

    def emit(self, op: QuantumAssignmentOperation, /) -> bool:
        result_symbol = self._interpreter.evaluate(op.result_var).value
        if isinstance(result_symbol, ClassicalSymbol):
            return False
        result_type = result_symbol.quantum_type

        if not (
            isinstance(op, ArithmeticOperation)
            and op.operation_kind == ArithmeticOperationKind.Assignment
        ):
            if isinstance(result_type, QuantumNumeric):
                result_type.reset_bounds()
            return False

        validate_assignment_bool_expression(
            result_symbol, op.expression.expr, op.operation_kind
        )
        convert_assignment_bool_expression(op)

        inferred_result_type = self._infer_result_type(op)
        if inferred_result_type is None:
            return False

        if not isinstance(result_type, QuantumNumeric):
            copy_type_information(
                inferred_result_type, result_symbol.quantum_type, str(op.result_var)
            )
            return False

        self._copy_numeric_attributes(result_type, inferred_result_type)
        if self._same_numeric_attributes(result_type, inferred_result_type):
            return False

        self._validate_declared_attributes(
            result_type, inferred_result_type, str(op.result_var)
        )
        if self._replace_assignment_if_needed:
            self._assign_to_inferred_var_and_bind(op, result_type, inferred_result_type)
            return True
        else:
            return False

    def _infer_result_type(self, op: ArithmeticOperation) -> Optional[QuantumNumeric]:
        expr = self._evaluate_expression(op.expression)
        if len(self._get_classical_vars_in_expression(expr)):
            return None

        symbols = self._get_symbols_in_expression(expr)
        if any(not symbol.quantum_type.is_instantiated for symbol in symbols):
            return None

        expr_str = rename_variables(
            expr.expr,
            {str(symbol.handle): symbol.handle.identifier for symbol in symbols}
            | {symbol.handle.qmod_expr: symbol.handle.identifier for symbol in symbols},
        )
        for symbol in symbols:
            expr_str = expr_str.replace(
                symbol.handle.qmod_expr, symbol.handle.identifier
            )
        return compute_arithmetic_result_type(
            expr_str,
            {symbol.handle.identifier: symbol.quantum_type for symbol in symbols},
            self._machine_precision,
        )

    @staticmethod
    def _copy_numeric_attributes(
        result_type: QuantumNumeric, inferred_result_type: QuantumNumeric
    ) -> None:
        if not result_type.has_size_in_bits:
            result_type.size = Expression(expr=str(inferred_result_type.size_in_bits))
        if not result_type.has_sign:
            result_type.is_signed = Expression(
                expr=str(inferred_result_type.sign_value)
            )
        if not result_type.has_fraction_digits:
            result_type.fraction_digits = Expression(
                expr=str(inferred_result_type.fraction_digits_value)
            )
        result_type.set_bounds(inferred_result_type.get_bounds())

    @staticmethod
    def _same_numeric_attributes(
        result_type: QuantumNumeric, inferred_result_type: QuantumNumeric
    ) -> bool:
        return (
            result_type.size_in_bits == inferred_result_type.size_in_bits
            and result_type.sign_value == inferred_result_type.sign_value
            and result_type.fraction_digits_value
            == inferred_result_type.fraction_digits_value
        )

    @classmethod
    def _validate_declared_attributes(
        cls, result_type: QuantumNumeric, inferred_result_type: QuantumNumeric, var: str
    ) -> None:
        result_size, result_sign, result_fractions = (
            result_type.size_in_bits,
            result_type.sign_value,
            result_type.fraction_digits_value,
        )
        inferred_size, inferred_sign, inferred_fractions = (
            inferred_result_type.size_in_bits,
            inferred_result_type.sign_value,
            inferred_result_type.fraction_digits_value,
        )
        result_integers = result_size - result_fractions
        inferred_integers = inferred_size - inferred_fractions

        if (
            (result_integers < inferred_integers)
            or (result_fractions < inferred_fractions)
            or (not result_sign and inferred_sign)
            or (
                result_sign
                and not inferred_sign
                and result_integers == inferred_integers
            )
        ):
            if (
                not result_sign
                and result_fractions == 0
                and not inferred_sign
                and inferred_fractions == 0
            ):
                result_size_str = f"size {result_size}"
                inferred_size_str = f"size {inferred_size}"
                hint = f"Hint: increase the size in the declaration of {var!r} or omit it to enable automatic inference."
            else:
                result_size_str = f"size {result_size}, {'signed' if result_sign else 'unsigned'}, and {result_fractions} fraction digits"
                inferred_size_str = f"size {inferred_size}, {'signed' if inferred_sign else 'unsigned'}, and {inferred_fractions} fraction digits"
                hint = f"Hint: omit the numeric attributes from the declaration of {var!r} to enable automatic inference."
            raise ClassiqExpansionError(
                f"Cannot assign an expression with inferred {inferred_size_str} to variable {var!r} with declared {result_size_str}. {hint}"
            )

    @staticmethod
    def _craft_size_string(size: int, is_signed: bool, fraction_digits: int) -> str:
        extra = (
            f", with {fraction_digits} fraction digits" if fraction_digits > 0 else ""
        )
        return f"{size} ({'signed' if is_signed else 'unsigned'}{extra})"

    def _assign_to_inferred_var_and_bind(
        self,
        op: ArithmeticOperation,
        result_type: QuantumNumeric,
        inferred_result_type: QuantumNumeric,
    ) -> None:
        stmts: StatementBlock = []
        handles: list[HandleBinding] = []

        extra_fraction_digits = (
            result_type.fraction_digits_value
            - inferred_result_type.fraction_digits_value
        )
        if extra_fraction_digits > 0:
            handles.append(
                self._declare_qarray(
                    "extra_fraction_digits", extra_fraction_digits, stmts
                )
            )

        inferred_result_name = self._counted_name_allocator.allocate("inferred_result")
        inferred_result_handle = HandleBinding(name=inferred_result_name)
        stmts.append(
            VariableDeclarationStatement(
                name=inferred_result_name, qmod_type=inferred_result_type
            )
        )
        handles.append(inferred_result_handle)
        modified_op = op.model_copy(update={"result_var": inferred_result_handle})
        self._interpreter.add_to_debug_info(modified_op)
        stmts.append(modified_op)

        result_integer_size = (
            result_type.size_in_bits - result_type.fraction_digits_value
        )
        inferred_result_integer_size = (
            inferred_result_type.size_in_bits
            - inferred_result_type.fraction_digits_value
        )
        extra_integers = result_integer_size - inferred_result_integer_size
        if extra_integers > 0:
            handles.append(
                self._declare_qarray("extra_integers", extra_integers, stmts)
            )

        stmts.append(BindOperation(in_handles=handles, out_handles=[op.result_var]))

        if (
            result_type.sign_value
            and inferred_result_type.sign_value
            and extra_integers > 0
        ):
            sign_idx = result_type.size_in_bits - extra_integers - 1
            self._sign_extension(
                op.result_var, sign_idx, result_type.size_in_bits, stmts
            )

        if (inferred_bounds := inferred_result_type.get_bounds()) is not None:
            lower_bound = Expression(expr=str(inferred_bounds[0]))
            upper_bound = Expression(expr=str(inferred_bounds[1]))
        else:
            lower_bound, upper_bound = None, None
        stmts.append(
            SetBoundsStatement(
                target=op.result_var,
                lower_bound=lower_bound,
                upper_bound=upper_bound,
            )
        )

        self._interpreter.emit(
            Block(
                statements=stmts,
                uuid=op.uuid,
                back_ref=op.back_ref,
            )
        )

    def _declare_qarray(
        self,
        prefix: str,
        size: int,
        stmts: StatementBlock,
        allocate: bool = True,
    ) -> HandleBinding:
        name = self._counted_name_allocator.allocate(prefix)
        handle = HandleBinding(name=name)
        quantum_type = QuantumBitvector(length=Expression(expr=str(size)))
        stmts.append(VariableDeclarationStatement(name=name, qmod_type=quantum_type))
        if allocate:
            stmts.append(Allocate(target=handle))
        return handle

    def _sign_extension(
        self,
        result_var: ConcreteHandleBinding,
        sign_idx: int,
        size: int,
        stmts: StatementBlock,
    ) -> None:
        aux = self._declare_qarray("inferred_result_aux", size, stmts, allocate=False)
        stmts.append(
            WithinApply(
                compute=[BindOperation(in_handles=[result_var], out_handles=[aux])],
                action=[
                    QuantumFunctionCall(
                        function=CX.func_decl.name,
                        positional_args=[
                            SubscriptHandleBinding(
                                base_handle=aux, index=Expression(expr=str(sign_idx))
                            ),
                            SubscriptHandleBinding(
                                base_handle=aux, index=Expression(expr=str(idx))
                            ),
                        ],
                    )
                    for idx in range(sign_idx + 1, size)
                ],
            )
        )
