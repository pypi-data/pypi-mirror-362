import math
import sympy as sp

def compute_persistence(n, p0=1.2):
    p = p0
    for _ in range(n):
        p = float(sp.Pow(p, p).evalf())
    return p

def density_scaling_factor(p):
    """For distance, area, volume, density"""
    return math.pi / (p ** (1 / math.pi))

def energy_scaling_factor(p):
    """For energy, mass, time"""
    return (p ** (1 / math.pi)) / math.pi

def time_scaling_factor(p):
    return (math.log(p + 1)) / math.pi

def mass_scaling_factor(p):
    return math.sqrt(p) / math.pi

# --- Normalizers ---

def normalize_mass(real_value, depth=7):
    p = compute_persistence(depth)
    m_n = mass_scaling_factor(p)
    return real_value / m_n

def normalize_time(real_value, depth=7):
    p = compute_persistence(depth)
    t_n = time_scaling_factor(p)
    return real_value / t_n

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

def denormalize_mass(punit_value, depth=7):
    p = compute_persistence(depth)
    m_n = mass_scaling_factor(p)
    return punit_value * m_n

def denormalize_time(punit_value, depth=7):
    p = compute_persistence(depth)
    t_n = time_scaling_factor(p)
    return punit_value * t_n
