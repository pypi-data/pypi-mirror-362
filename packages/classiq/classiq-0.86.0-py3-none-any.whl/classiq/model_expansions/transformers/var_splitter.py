import ast
from dataclasses import dataclass
from itertools import chain
from typing import TYPE_CHECKING, Callable, Optional

from classiq.interface.exceptions import (
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.model.bind_operation import BindOperation
from classiq.interface.model.handle_binding import (
    HandleBinding,
    NestedHandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)
from classiq.interface.model.quantum_type import (
    QuantumBitvector,
    QuantumScalar,
    QuantumType,
)
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)

from classiq.model_expansions.scope import QuantumSymbol, Scope
from classiq.model_expansions.transformers.model_renamer import (
    HandleRenaming,
    ModelRenamer,
)
from classiq.model_expansions.visitors.variable_references import VarRefCollector


@dataclass(frozen=True)
class SymbolPart(HandleRenaming):
    target_var_type: QuantumType


SymbolParts = dict[HandleBinding, list[SymbolPart]]
PartNamer = Callable[[str], str]


class VarSplitter(ModelRenamer):
    def __init__(self, scope: Scope):
        self._scope = scope

    def split_symbols(self, expression: Expression, namer: PartNamer) -> SymbolParts:
        vrc = VarRefCollector(ignore_duplicated_handles=True)
        vrc.visit(ast.parse(expression.expr))
        symbol_names_to_split = dict.fromkeys(
            handle.name
            for handle in vrc.var_handles
            if isinstance(self._scope[handle.name].value, QuantumSymbol)
            and isinstance(handle, NestedHandleBinding)
        )

        symbol_handles = {
            symbol: list(
                dict.fromkeys(
                    handle.collapse()
                    for handle in vrc.var_handles
                    if handle.name == symbol.handle.name
                )
            )
            for symbol_name in symbol_names_to_split
            if isinstance(
                symbol := self._scope[symbol_name].value,
                QuantumSymbol,
            )
        }

        return {
            symbol.handle: [
                SymbolPart(
                    source_handle=part.handle,
                    target_var_name=namer(part.handle.identifier),
                    target_var_type=part.quantum_type,
                )
                for part in self._get_symbol_parts(symbol, handles)
            ]
            for symbol, handles in symbol_handles.items()
        }

    def _get_symbol_parts(
        self, symbol: QuantumSymbol, target_parts: list[HandleBinding]
    ) -> list[QuantumSymbol]:
        for i in range(len(target_parts)):
            for j in range(i + 1, len(target_parts)):
                if target_parts[i].overlaps(target_parts[j]):
                    raise ClassiqInternalExpansionError(
                        f"Handles {str(target_parts[i])!r} and "
                        f"{str(target_parts[j])!r} overlapping in expression"
                    )
        return self._get_symbol_parts_unsafe(symbol, target_parts)

    def _get_symbol_parts_unsafe(
        self, symbol: QuantumSymbol, target_parts: list[HandleBinding]
    ) -> list[QuantumSymbol]:
        if all(
            symbol.handle == target_part or symbol.handle not in target_part.prefixes()
            for target_part in target_parts
        ) or isinstance(symbol.quantum_type, QuantumScalar):
            return [symbol]

        if isinstance(symbol.quantum_type, QuantumBitvector):
            return self._get_array_parts(symbol, target_parts)

        return self._get_struct_parts(symbol, target_parts)

    def _get_array_parts(
        self, symbol: QuantumSymbol, target_parts: list[HandleBinding]
    ) -> list[QuantumSymbol]:
        if TYPE_CHECKING:
            assert isinstance(symbol.quantum_type, QuantumBitvector)

        if not symbol.quantum_type.has_length:
            raise ClassiqExpansionError(
                f"Could not determine the length of quantum array " f"{symbol.handle}."
            )
        target_slices = self._get_target_slices(symbol, target_parts)

        symbol_parts: list[QuantumSymbol] = []
        idx = 0
        while idx < symbol.quantum_type.length_value:
            if idx in target_slices:
                stop = target_slices[idx]
                if stop <= idx:
                    raise ClassiqInternalExpansionError(
                        f"Illegal sliced handle {str(symbol[idx: stop].handle)!r}"
                    )
                symbol_parts.append(symbol[idx:stop])
                idx = stop
            else:
                symbol_parts.extend(
                    self._get_symbol_parts_unsafe(symbol[idx], target_parts)
                )
                idx += 1

        return symbol_parts

    def _get_target_slices(
        self, symbol: QuantumSymbol, target_parts: list[HandleBinding]
    ) -> dict[int, int]:
        if TYPE_CHECKING:
            assert isinstance(symbol.quantum_type, QuantumBitvector)
        target_items = {
            idx
            for idx in range(symbol.quantum_type.length_value)
            for target_part in target_parts
            if target_part
            in SubscriptHandleBinding(
                base_handle=symbol.handle, index=Expression(expr=str(idx))
            )
        }
        target_slices = {
            target_part.start.to_int_value(): target_part.end.to_int_value()
            for target_part in target_parts
            if isinstance(target_part, SlicedHandleBinding)
            and symbol.handle == target_part.base_handle
        }
        self._add_unused_indices_as_slices(symbol, target_items, target_slices)
        return target_slices

    @staticmethod
    def _add_unused_indices_as_slices(
        symbol: QuantumSymbol, target_items: set[int], target_slices: dict[int, int]
    ) -> None:
        if TYPE_CHECKING:
            assert isinstance(symbol.quantum_type, QuantumBitvector)
        last_unused_idx: Optional[int] = None
        array_length = symbol.quantum_type.length_value
        idx = 0

        while idx < array_length:
            if (
                idx in target_items or idx in target_slices
            ) and last_unused_idx is not None:
                target_slices[last_unused_idx] = idx
                last_unused_idx = None

            if idx in target_slices:
                if target_slices[idx] <= idx:
                    raise ClassiqInternalExpansionError
                idx = target_slices[idx]
                continue

            if idx not in target_items and last_unused_idx is None:
                last_unused_idx = idx

            idx += 1

        if last_unused_idx is not None:
            target_slices[last_unused_idx] = array_length

    def _get_struct_parts(
        self, symbol: QuantumSymbol, target_parts: list[HandleBinding]
    ) -> list[QuantumSymbol]:
        return list(
            chain.from_iterable(
                self._get_symbol_parts_unsafe(field_symbol, target_parts)
                for field_symbol in symbol.fields.values()
            )
        )

    @staticmethod
    def get_bind_ops(symbol_parts: SymbolParts) -> list[BindOperation]:
        return [
            BindOperation(
                in_handles=[handle],
                out_handles=[part.target_var_handle for part in parts],
            )
            for handle, parts in symbol_parts.items()
        ]

    @staticmethod
    def get_var_decls(symbol_parts: SymbolParts) -> list[VariableDeclarationStatement]:
        return [
            VariableDeclarationStatement(
                name=part.target_var_name,
                qmod_type=part.target_var_type,
            )
            for part in chain.from_iterable(symbol_parts.values())
        ]
