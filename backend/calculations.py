from models import TransmissionRequest
import math
from typing import List, Dict, Tuple

# Constantes
G = 9.81  # gravité
ROULEMENT_COEFF = 0.004
AIR_DENSITY = 1.225
CD_A = 0.4  # coefficient de traînée x surface (m²)
VELOCITY_UNIT_CONV = 3.6  # m/s to km/h

# Tables des niveaux cyclistes
POWER_PROFILE = {
    "débutant": (1.3, 2.0),
    "récréatif": (2.0, 2.7),
    "intermédiaire": (2.7, 3.3),
    "confirmé": (3.3, 4.0),
    "régional": (4.0, 4.7),
    "élite": (4.7, 5.3),
    "worldtour": (5.5, 6.5),
}


def wkg_range_from_profile(profile: str) -> Tuple[float, float]:
    return POWER_PROFILE.get(profile.lower(), (1.5, 2.5))


def compute_velocity(cadence_rpm: float, development_m: float) -> float:
    return (cadence_rpm / 60) * development_m


def compute_development(plateau: int, pignon: int, wheel_circumference: float = 2.1) -> float:
    ratio = plateau / pignon
    return wheel_circumference * ratio


def compute_total_power(mass_total: float, slope: float, velocity: float) -> float:
    slope_rad = math.atan(slope / 100)
    v_ms = velocity  # en m/s
    P_gravity = mass_total * G * math.sin(slope_rad) * v_ms
    P_roll = mass_total * G * math.cos(slope_rad) * ROULEMENT_COEFF * v_ms
    P_aero = 0.5 * AIR_DENSITY * CD_A * (v_ms ** 3)
    return P_gravity + P_roll + P_aero


def calculate_wkg_for_all_gears(data: TransmissionRequest
) -> Dict:
    cyclist = data.cyclist
    bike = data.bike
    # route = data.route


    total_mass = cyclist.weight + bike.bike_weight
    wkg_min, wkg_max = wkg_range_from_profile(cyclist.profile)

    slopes = []
    for i in range(13):
        slopes.append(i)


    results = {
        "cyclist": {
            "weight": cyclist.weight,
            "profile": cyclist.profile,
            "wkg_range": [round(wkg_min, 2), round(wkg_max, 2)],
        },
        "cadence_rpm": cyclist.prefered_cadence,
        "pente_values": slopes,
        "gears": [],
        "wkg_data": []
    }

    for chainring in bike.chainring:
        for cassette in bike.cassette:
            gear_label = f"{chainring}x{cassette}"
            development = compute_development(chainring, cassette)
            wkg_list = []

            for slope in slopes:
                v = compute_velocity(cyclist.prefered_cadence, development)  # m/s
                power = compute_total_power(total_mass, slope, v)
                wkg = power / cyclist.weight
                wkg_list.append(round(wkg, 2))

            results["gears"].append({
                "plateau": chainring,
                "pignon": cassette
            })
            results["wkg_data"].append({
                "gear": gear_label,
                "wkg_values": wkg_list
            })

    return results
