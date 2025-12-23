def device_energy(power_w, hours, days, quantity):
    """
    Physics-based energy calculation
    E = (P × h × d × n) / 1000
    """
    return (power_w * hours * days * quantity) / 1000


def temperature_adjustment(energy, temperature, alpha=0.03):
    """
    ODE-based thermal correction
    """
    return energy * (1 + alpha * (temperature - 22) / 22)
