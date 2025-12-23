def build_features(base_energy, temperature, month, is_company):
    return {
        "base_energy": base_energy,
        "temperature": temperature,
        "month": month,
        "is_company": int(is_company)
    }
