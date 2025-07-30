# palestine_function_unit/__init__.py
from .core import (
    compute_persistence,
    normalize_distance,
    normalize_energy,
    normalize_mass,
    normalize_time,
    denormalize_distance,
    denormalize_energy,
    denormalize_mass,
    denormalize_time
)

from .units import (
    REFERENCE_VALUES,
    UNIT_CATEGORIES
)

__all__ = [
    'convert_units',
    'compute_persistence',
    'REFERENCE_VALUES',
    'UNIT_CATEGORIES'
]

from .units import REFERENCE_VALUES, UNIT_CATEGORIES

def convert_units(value, from_unit, to_unit, depth=7):
    def get_category(unit):
        for cat, units in UNIT_CATEGORIES.items():
            if unit in units:
                return cat
        raise ValueError(f"Unit '{unit}' not categorized")

    from_cat = get_category(from_unit.lower())
    to_cat = get_category(to_unit.lower())

    # Step A: Get reference scale
    ref_from = REFERENCE_VALUES[from_unit.lower()]
    ref_to = REFERENCE_VALUES[to_unit.lower()]

    # Step B: Normalize to P-Units using correct method
    if from_cat == 'distance':
        punit_from = normalize_distance(ref_from, depth)
    elif from_cat == 'mass':
        punit_from = normalize_mass(ref_from, depth)
    elif from_cat == 'time':
        punit_from = normalize_time(ref_from, depth)
    else:
        punit_from = normalize_energy(ref_from, depth)

    punit_scaled = punit_from * value

    # Step C: Denormalize to target unit
    if to_cat == 'distance':
        real_result = denormalize_distance(punit_scaled, depth)
    elif to_cat == 'mass':
        real_result = denormalize_mass(punit_scaled, depth)
    elif to_cat == 'time':
        real_result = denormalize_time(punit_scaled, depth)
    else:
        real_result = denormalize_energy(punit_scaled, depth)

    result = real_result / ref_to

    return result

