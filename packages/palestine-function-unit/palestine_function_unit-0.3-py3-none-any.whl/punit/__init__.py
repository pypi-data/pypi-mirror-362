from .core import (
    normalize_distance, normalize_energy,
    denormalize_distance, denormalize_energy
)
from .units import REFERENCE_VALUES, UNIT_CATEGORIES

def convert_units(value, from_unit, to_unit, depth=7):
    def get_category(unit):
        for cat, units in UNIT_CATEGORIES.items():
            if unit in units:
                return cat
        raise ValueError(f"Unit '{unit}' not categorized")

    from_cat = get_category(from_unit)
    to_cat = get_category(to_unit)

    # Step A: Get reference scale
    ref_from = REFERENCE_VALUES[from_unit]
    ref_to = REFERENCE_VALUES[to_unit]

    # Step B: Normalize to P-Units using correct method
    if from_cat in ['distance']:
        punit_from = normalize_distance(ref_from, depth)
    else:
        punit_from = normalize_energy(ref_from, depth)

    punit_scaled = punit_from * value

    # Step C: Denormalize to target unit
    if to_cat in ['distance']:
        real_result = denormalize_distance(punit_scaled, depth)
    else:
        real_result = denormalize_energy(punit_scaled, depth)

    result = real_result / ref_to

    return result
