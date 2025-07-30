from classiq.model_expansions.arithmetic import NumericAttributes


def compute_result_attrs_assign(
    source: NumericAttributes,
    machine_precision: int,
) -> NumericAttributes:
    if machine_precision >= source.fraction_digits:
        return source

    trimmed_digits = source.fraction_digits - machine_precision
    return NumericAttributes(
        size=source.size - trimmed_digits,
        is_signed=source.is_signed,
        fraction_digits=machine_precision,
        bounds=source.bounds,
        trim_bounds=True,
    )


def compute_result_attrs_bitwise_invert(
    arg: NumericAttributes,
    machine_precision: int,
) -> NumericAttributes:
    fraction_digits = min(arg.fraction_digits, machine_precision)
    trimmed_bits = arg.fraction_digits - fraction_digits
    return NumericAttributes(
        size=arg.size - trimmed_bits,
        is_signed=arg.is_signed,
        fraction_digits=fraction_digits,
    )


def compute_result_attrs_negate(
    arg: NumericAttributes,
    machine_precision: int,
) -> NumericAttributes:
    lb = -arg.ub
    ub = -arg.lb

    if arg.size == 1:
        return NumericAttributes(
            size=1,
            is_signed=lb < 0,
            fraction_digits=arg.fraction_digits,
            bounds=(lb, ub),
        )
    else:
        return NumericAttributes.from_bounds(
            lb, ub, arg.fraction_digits, machine_precision
        )


def compute_result_attrs_add(
    left: NumericAttributes,
    right: NumericAttributes,
    machine_precision: int,
) -> NumericAttributes:
    lb = left.lb + right.lb
    ub = left.ub + right.ub
    fraction_places = max(left.fraction_digits, right.fraction_digits)
    return NumericAttributes.from_bounds(lb, ub, fraction_places, machine_precision)


def compute_result_attrs_subtract(
    left: NumericAttributes,
    right: NumericAttributes,
    machine_precision: int,
) -> NumericAttributes:
    tmp = compute_result_attrs_negate(right, machine_precision)
    return compute_result_attrs_add(left, tmp, machine_precision)
