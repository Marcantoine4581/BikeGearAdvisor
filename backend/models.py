from pydantic import BaseModel, Field
from typing import List, Optional, Tuple


class CyclistInput(BaseModel):
    weight: float = Field(..., gt=0, description="Poids du cycliste en kg")
    prefered_cadence: int = Field(..., gt=0, description="Cadence préférée du cycliste en tours / minute")
    profile: str
    height: Optional[float] = Field(None, gt=0, description="Taille du cycliste en cm")
    sex: Optional[str] = Field(None, description="Sexe (H/F/Autre)")


class BikeInput(BaseModel):
    bike_weight: float = Field(..., gt=0, description="Poids du vélo en kg")
    wheel_diameter: float = Field(0.7, gt=0, description="Diamètre de la roue en m (par défaut 700c)")
    crank_length: Optional[float] = Field(0.17, description="Longueur de manivelle en m")
    cassette: List[int] = Field(..., description="Dents des pignons (ex: [11, 13, 15, 17, 19, 21])")
    chainring: List[int] = Field(..., description="Dents des plateaux (ex: [34, 50])")


class RouteInput(BaseModel):
    distance: float = Field(..., gt=0, description="Distance en km")
    elevation_gain: float = Field(..., ge=0, description="Dénivelé positif en mètres")
    avg_slope: Optional[float] = Field(None, description="Pente moyenne en %")
    wind_speed: Optional[float] = Field(0, description="Vent en m/s (positif = face, négatif = dos)")
    rolling_resistance: float = Field(0.004, description="Coefficient de résistance au roulement")
    drag_coefficient: float = Field(0.88, description="Coefficient aérodynamique CdA")

# Entrée complète de l'API
class TransmissionRequest(BaseModel):
    cyclist: CyclistInput
    bike: BikeInput
    # route: RouteInput


# Modèle de sortie de l’API
class CyclistModel(BaseModel):
    weight: float
    profile: str
    wkg_range: Tuple[float, float]


class GearModel(BaseModel):
    plateau: int
    pignon: int


class WkgDataModel(BaseModel):
    gear: str
    wkg_values: List[float]


class TransmissionAnalysisOutput(BaseModel):
    cyclist: CyclistModel
    cadence_rpm: float
    pente_values: List[float]
    gears: List[GearModel]
    wkg_data: List[WkgDataModel]
