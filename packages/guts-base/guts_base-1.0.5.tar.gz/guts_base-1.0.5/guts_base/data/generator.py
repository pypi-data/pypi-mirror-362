import numpy as np
import xarray as xr
from typing import TypedDict, Dict, Optional, Sequence

class ExposureDataDict(TypedDict):
    start: int
    end: int
    exposure: float|Sequence[float]

def create_artificial_data(
    t_max, 
    dt, 
    exposure_paths=["oral", "topical", "contact"],
    intensity=[0.1, 0.5, 0.05],
    seed=1,
):
    rng = np.random.default_rng(1)
    time = np.arange(0, t_max, step=dt)  # daily time resolution

    # calculate potential exposure based on a lognormal distribution
    oral = rng.lognormal(mean=np.log(intensity[0]), sigma=0.5, size=len(time))
    # and include a random exposure days
    oral *= rng.binomial(n=1, p=1, size=len(time))


    # calculate potential exposure based on a lognormal distribution
    topical = rng.lognormal(mean=np.log(intensity[1]), sigma=1, size=len(time))
    # and include a random exposure days
    topical *= rng.binomial(n=1, p=0.25, size=len(time))


    # calculate potential exposure based on a lognormal distribution
    contact = rng.lognormal(mean=np.log(intensity[2]), sigma=0.1, size=len(time))
    # and include a random exposure days
    contact *= rng.binomial(n=1, p=0.8, size=len(time))



    exposures = xr.Dataset(
        data_vars={
            "exposure": (("time", "exposure_path"), np.column_stack([oral, topical, contact])),
        },
        coords={"time": time, "exposure_path": ["oral", "topical", "contact"]}
    )

    return exposures.sel(exposure_path=exposure_paths)


def design_exposure_timeseries(time: Sequence[float], exposure: ExposureDataDict, eps: float):
    if exposure is None:
        return
    
    exposure["end"] = time[-1] if exposure["end"] is None else exposure["end"]

    return np.where(
        np.logical_and(time >= exposure["start"], time < exposure["end"]),
        exposure["concentration"],
        0
    )

def design_exposure_scenario(
    t_max: float, 
    dt: float, 
    exposures: Dict[str,ExposureDataDict],
    eps: float = 1e-8,
    exposure_dimension: str = "exposure_type",
):
    """
    TODO: tmax, dt and eps are probably not necessary
    """
    # add dt so that tmax is definitely inclded
    time = np.arange(0, t_max+dt, step=dt)  # daily time resolution
    time = np.unique(np.concatenate([time] + [
        np.array([time[-1] if vals["end"] is None else vals["end"]])
        for key, vals in exposures.items()

    ]))

    treatments = {}
    for key, expo in exposures.items():
        treat = design_exposure_timeseries(time, expo, eps)
        treatments.update({key: treat})

    data = np.column_stack(list(treatments.values()))
    data = np.expand_dims(data, axis=0)

    coords = {"id": [0], "time": time}
    
    coords.update({exposure_dimension: list(treatments.keys())})

    exposures_dataset = xr.Dataset(
        data_vars={"exposure": (tuple(coords.keys()), data)},
        coords=coords
    )

    return exposures_dataset

