REFERENCE_VALUES = {
    # Distance
    'meter': 1,
    'kilometer': 1000,
    'centimeter': 0.01,
    'millimeter': 0.001,
    'micrometer': 1e-6,
    'nanometer': 1e-9,
    'mile': 1609.34,
    'yard': 0.9144,
    'foot': 0.3048,
    'inch': 0.0254,
    'lightyear': 9.461e15,

    # Time
    'second': 1,
    'minute': 60,
    'hour': 3600,
    'day': 86400,
    'week': 604800,
    'month': 2592000,
    'year': 31536000,

    # Mass
    'gram': 0.001,
    'kilogram': 1,
    'milligram': 1e-6,
    'pound': 0.453592,
    'ounce': 0.0283495,

    # Energy
    'joule': 1,
    'kilojoule': 1000,
    'calorie': 4.184,
    'kilocalorie': 4184,
    'electronvolt': 1.60218e-19,
    'btu': 1055.06,

    # Force
    'newton': 1,
    'dyne': 1e-5,

    # Pressure
    'pascal': 1,
    'bar': 1e5,
    'psi': 6894.76,
    'atmosphere': 101325,

    # Temperature
    'kelvin': 1,
    'celsius': 1,
    'fahrenheit': 1,

    # Electric Charge
    'coulomb': 1,
    'elementary_charge': 1.602176634e-19,

    # Area
    'square_meter': 1,
    'square_kilometer': 1e6,
    'acre': 4046.86,
    'hectare': 10000,

    # Volume
    'liter': 0.001,
    'milliliter': 1e-6,
    'gallon': 0.00378541,
    'quart': 0.000946353,
    'pint': 0.000473176,
    'fluid_ounce': 2.95735e-5,

    # Data (bytes)
    'byte': 1,
    'kilobyte': 1024,
    'megabyte': 1024**2,
    'gigabyte': 1024**3,

    # Speed
    'meter_per_second': 1,
    'kilometer_per_hour': 0.277778,
    'mile_per_hour': 0.44704,
}

# Categories for normalization
UNIT_CATEGORIES = {
    'distance': [
        'meter', 'kilometer', 'centimeter', 'millimeter',
        'micrometer', 'nanometer', 'mile', 'yard', 'foot',
        'inch', 'lightyear', 'square_meter', 'square_kilometer',
        'acre', 'hectare', 'liter', 'milliliter', 'gallon',
        'quart', 'pint', 'fluid_ounce'
    ],
    'time': [
        'second', 'minute', 'hour', 'day', 'week',
        'month', 'year'
    ],
    'mass': [
        'gram', 'kilogram', 'milligram', 'pound', 'ounce'
    ],
    'energy': [
        'joule', 'kilojoule', 'calorie', 'kilocalorie',
        'electronvolt', 'btu', 'newton', 'dyne', 'pascal',
        'bar', 'psi', 'atmosphere', 'kelvin', 'celsius',
        'fahrenheit', 'coulomb', 'elementary_charge',
        'byte', 'kilobyte', 'megabyte', 'gigabyte',
        'meter_per_second', 'kilometer_per_hour', 'mile_per_hour'
    ],
}
