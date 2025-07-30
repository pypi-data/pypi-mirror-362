from typing import Optional

from classiq.interface.model.handle_binding import HandleBinding, NestedHandleBinding

from classiq.evaluators.qmod_annotated_expression import (
    QmodAnnotatedExpression,
    QmodExprNodeId,
)


def rename_handles_in_expression(
    expr_val: QmodAnnotatedExpression,
    renaming: dict[HandleBinding, HandleBinding],
) -> str:
    if len(renaming) == 0:
        return expr_val.to_qmod_expr()
    all_vars = expr_val.get_classical_vars() | expr_val.get_quantum_vars()
    for node_id, var in all_vars.items():
        renamed_var = _rename_var(renaming, var)
        if renamed_var is not None:
            expr_val.set_var(node_id, renamed_var)
    return expr_val.to_qmod_expr()


def _rename_var(
    renaming: dict[HandleBinding, HandleBinding], var: HandleBinding
) -> Optional[HandleBinding]:
    if (renamed_var := renaming.get(var)) is not None:
        return renamed_var
    if not isinstance(var, NestedHandleBinding):
        return None
    renamed_inner = _rename_var(renaming, var.base_handle)
    if renamed_inner is None:
        return None
    return var.model_copy(update=dict(base_handle=renamed_inner))


def rename_nodes_in_expression(
    expr_val: QmodAnnotatedExpression,
    renaming: dict[QmodExprNodeId, HandleBinding],
) -> str:
    for node_id, renamed_var in renaming.items():
        expr_val.set_var(node_id, renamed_var)
    return expr_val.to_qmod_expr()
