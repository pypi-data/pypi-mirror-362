from classiq.interface.model.quantum_expressions.arithmetic_operation import (
    ArithmeticOperation,
)

from classiq.model_expansions.quantum_operations.emitter import Emitter
from classiq.model_expansions.scope import ClassicalSymbol


class ClassicalVarEmitter(Emitter[ArithmeticOperation]):
    def emit(self, op: ArithmeticOperation, /) -> bool:
        result_symbol = self._interpreter.evaluate(op.result_var).value
        if not isinstance(result_symbol, ClassicalSymbol):
            return False
        op._classical_assignment = True
        self.emit_statement(op)
        return True
