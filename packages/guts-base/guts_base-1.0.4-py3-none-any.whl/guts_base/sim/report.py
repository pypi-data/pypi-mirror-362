import os
import itertools as it
from typing import List, Dict
import numpy as np
import pandas as pd
import xarray as xr

from pymob import SimulationBase
from pymob.sim.report import Report, reporting

from guts_base.plot import plot_survival_multipanel, plot_exposure_multipanel
from guts_base.sim.ecx import ECxEstimator

class GutsReport(Report):
    ecx_estimates_times: List = [1, 2, 4, 10]
    ecx_estimates_x: List = [0.1, 0.25, 0.5, 0.75, 0.9]
    ecx_draws: int = 250
    ecx_force_draws: bool = False
    set_background_mortality_to_zero = True

    def additional_reports(self, sim: "SimulationBase"):
        super().additional_reports(sim=sim)
        self.model_fits(sim)
        self.LCx_estimates(sim)

    @reporting
    def model_input(self, sim: SimulationBase):
        self._write("### Exposure conditions")
        self._write(
            "These are the exposure conditions that were assumed for parameter inference. "+
            "Double check if they are aligned with your expectations. Especially short " +
            "exposure durations may not be perceivable in this view. In this case it is "+
            "recommended to have a look at the exposure conditions in the numerical "+
            "tables provided below." 
        )
        
        out_mp = plot_exposure_multipanel(
            sim=sim,
            results=sim.model_parameters["x_in"],
            ncols=6,
        )

        lab = self._label.format(placeholder='exposure')
        self._write(f"![Exposure model fits.\label{{{lab}}}]({os.path.basename(out_mp)})")

        return out_mp

    @reporting
    def model_fits(self, sim: SimulationBase):
        self._write("### Survival model fits")
        
        self._write(
            "Survival observations on the unit scale with model fits. The solid line is "+
            "the average of individual survival probability predictions from multiple "+
            "draws from the posterior parameter distribution. In case a point estimator "+
            "was used the solid line indicates the best fit. Grey uncertainty intervals "+
            "indicate the uncertainty in survival probabilities. Note that the survival "+
            "probabilities indicate the probability for a given individual or population "+
            "to be alive when observed at time t."
        )

        out_mp = plot_survival_multipanel(
            sim=sim,
            results=sim.inferer.idata.posterior_model_fits,
            ncols=6,
        )

        lab = self._label.format(placeholder='survival_fits')
        self._write(f"![Surival model fits.\label{{{lab}}}]({os.path.basename(out_mp)})")

        return out_mp
    
    @reporting
    def LCx_estimates(self, sim):
        X = self.ecx_estimates_x
        T = self.ecx_estimates_times
        P = sim.predefined_scenarios()

        if self.set_background_mortality_to_zero:
            conditions = {sim.background_mortality: 0.0}

        estimates = pd.DataFrame(
            it.product(X, T, P.keys()), 
            columns=["x", "time", "scenario"]
        )

        ecx = []

        for i, row in estimates.iterrows():
            ecx_estimator = ECxEstimator(
                sim=sim,
                effect="survival", 
                x=row.x,
                time=row.time, 
                x_in=P[row.scenario], 
                conditions_posterior=conditions
            )
            
            ecx_estimator.estimate(
                mode=sim.ecx_mode,
                draws=self.ecx_draws,
                force_draws=self.ecx_force_draws,
                show_plot=False
            )

            ecx.append(ecx_estimator.results.copy(deep=True))
            
            # remove ecx_estimator to not blow up temp files.
            # This triggers the __del__ method of ECxEstimator,
            # which cleans up a temporary directory if it was
            # created during init
            del ecx_estimator

        results = pd.DataFrame(ecx)
        estimates[results.columns] = results

        out = self._write_table(tab=estimates, label_insert="$LC_x$ estimates")
        
        return out


class ParameterConverter:
    def __init__(
        self,
        sim: SimulationBase,
    ):
        self.sim = sim.copy()

        # this converts the units of exposure in the copied simulation 
        # and scales the exposure dataarray
        self.sim._convert_exposure_units()
        self.convert_parameters()
        self.sim.prepare_simulation_input()
        self.sim.dispatch_constructor()

        # self.plot_exposure_and_effect(self.sim, sim, _id=7, data_var="D")

        # if parameters are not rescaled this method should raise an error
        self.validate_parameter_conversion_default_params(sim_copy=self.sim, sim_orig=sim)
        self.validate_parameter_conversion_posterior_mean(sim_copy=self.sim, sim_orig=sim)
        self.validate_parameter_conversion_posterior_map(sim_copy=self.sim, sim_orig=sim)

    def convert_parameters(self):
        raise NotImplementedError


    @staticmethod
    def plot_exposure_and_effect(sim_copy, sim_orig, _id=1, data_var="survival"):
        from matplotlib import pyplot as plt
        fig, (ax1, ax2) = plt.subplots(2,1)
        results_copy = sim_copy.evaluate(parameters=sim_copy.config.model_parameters.value_dict)
        results_orig = sim_orig.evaluate(parameters=sim_orig.config.model_parameters.value_dict)

        ax1.plot(results_orig.time, results_orig["exposure"].isel(id=_id), color="red", label="unscaled")
        ax1.plot(results_copy.time, results_copy["exposure"].isel(id=_id), color="blue", ls="--", label="scaled")
        ax2.plot(results_orig.time, results_orig[data_var].isel(id=_id), color="red", label="unscaled")
        ax2.plot(results_copy.time, results_copy[data_var].isel(id=_id), color="blue", ls="--", label="scaled")
        ax1.legend()
        ax2.legend()
        return fig

    @staticmethod
    def validate_parameter_conversion_default_params(sim_copy, sim_orig):
        results_copy = sim_copy.evaluate(parameters=sim_copy.config.model_parameters.value_dict)
        results_orig = sim_orig.evaluate(parameters=sim_orig.config.model_parameters.value_dict)

        np.testing.assert_allclose(results_copy.H, results_orig.H, atol=0.001, rtol=0.001)

    @staticmethod
    def validate_parameter_conversion_posterior_mean(sim_copy, sim_orig):
        results_copy = sim_copy.evaluate(parameters=sim_copy.point_estimate("mean", to="dict"))
        results_orig = sim_orig.evaluate(parameters=sim_orig.point_estimate("mean", to="dict"))

        np.testing.assert_allclose(results_copy.H, results_orig.H, atol=0.001, rtol=0.001)

    @staticmethod
    def validate_parameter_conversion_posterior_map(sim_copy, sim_orig):
        results_copy = sim_copy.evaluate(parameters=sim_copy.point_estimate("map", to="dict"))
        results_orig = sim_orig.evaluate(parameters=sim_orig.point_estimate("map", to="dict"))

        np.testing.assert_allclose(results_copy.H, results_orig.H, atol=0.001, rtol=0.001)