import math

def compute_persistence(n, p0=1.2):
    p = p0
    for _ in range(n):
        p = p ** p
    return p

def density_scaling_factor(p):
    """For distance, area, volume, density"""
    return math.pi / (p ** (1 / math.pi))

def energy_scaling_factor(p):
    """For energy, mass, time"""
    return (p ** (1 / math.pi)) / math.pi

# --- Normalizers ---

def normalize_distance(real_value, depth=7):
    p = compute_persistence(depth)
    d_n = density_scaling_factor(p)
    return real_value / d_n

def normalize_energy(real_value, depth=7):
    p = compute_persistence(depth)
    e_n = energy_scaling_factor(p)
    return real_value / e_n

# --- Denormalizers ---

def denormalize_distance(punit_value, depth=7):
    p = compute_persistence(depth)
    d_n = density_scaling_factor(p)
    return punit_value * d_n

def denormalize_energy(punit_value, depth=7):
    p = compute_persistence(depth)
    e_n = energy_scaling_factor(p)
    return punit_value * e_n
