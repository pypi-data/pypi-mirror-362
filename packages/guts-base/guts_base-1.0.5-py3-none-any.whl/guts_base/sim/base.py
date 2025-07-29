import os
import glob
from functools import partial
from copy import deepcopy
import importlib
import tempfile
import warnings
import numpy as np
import xarray as xr
from diffrax import Dopri5
from typing import Literal, Optional, List, Dict, Mapping, Sequence, Tuple
import pandas as pd
import pint

from pymob import SimulationBase
from pymob.sim.config import (
    DataVariable, Param, string_to_list, string_to_dict, NumericArray
)

from pymob.solvers import JaxSolver
from pymob.solvers.base import rect_interpolation
from expyDB.intervention_model import (
    Treatment, Timeseries, select, from_expydb
)


from guts_base.sim.utils import GutsBaseError
from guts_base import mod
from guts_base.data import (
    to_dataset, reduce_multiindex_to_flat_index, create_artificial_data, 
    create_database_and_import_data_main, design_exposure_scenario, ExposureDataDict
)
from guts_base.sim.report import GutsReport

ureg = pint.UnitRegistry()

class GutsBase(SimulationBase):
    """
    Initializes GUTS models from a variety of data sources 

    Initialization follows a couple of steps
    1. check if necessary entries are made in the configuration, otherwise add defaults
    2. read data or take from input
    3. process data (add dimensions, or add indices)
    4. Prepare model input
    """
    solver = JaxSolver
    Report = GutsReport
    results_interpolation: Tuple[float,float,int] = (np.nan, np.nan, 100)
    _skip_data_processing: bool = False
    ecx_mode: Literal["mean", "draws"] = "mean"

    def initialize(self, input: Optional[Dict] = None):
        """Initiaization goes through a couple of steps:

        1. Configuration: This makes case-study specific changes to the configuration
            file or sets state variables that are relevant for the simulation
            TODO: Ideally everything that is configurable ends up in the config so it
            can be serialized

        2. Import data: This method consists of submethods that can be adapted or 
            overwritten in subclass methods.
            - .read_data
            - .save_observations
            - .process_data
            process_data itself utilizes the submethods _create_indices and 
            _indices_to_dimensions which are empty methods by default, but can be used
            in subclasses if needed

        3. Initialize the simulation input (parameters, y0, x_in). This can 

        By splitting up the simulation init method, into these three steps, modifcations
        of the initialize method allows for higher granularity in subclasses.
        """

        # 1. Configuration
        self.configure_case_study()

        # 2. Import data
        self.observations = self.read_data()
        # FIXME: Saving observations here is not intuituve. If i export a simulation,
        # I want to use the last used state, not some obscure intermediate state
        # self.save_observations(filename="observations.nc", directory=self.output_path, force=True)
        if not self._skip_data_processing:
            self.process_data()

        # 3. prepare y0 and x_in
        self.prepare_simulation_input()

    def configure_case_study(self):
        """Modify configuration file or set state variables
        TODO: This should only modify the configuration file, so that changes
        are transparent.
        """
        if self._model_class is not None:
            self.model = self._model_class._rhs_jax
            self.solver_post_processing = self._model_class._solver_post_processing

        self.unit_time: Literal["day", "hour", "minute", "second"] = "day"
        if hasattr(self.config.simulation, "unit_time"):
            self.unit_time = self.config.simulation.unit_time  # type: ignore

        if hasattr(self.config.simulation, "skip_data_processing"):
            self._skip_data_processing = bool(self.config.simulation.skip_data_processing)  # type: ignore

        if hasattr(self.config.simulation, "results_interpolation"):
            results_interpolation_string = string_to_list(self.config.simulation.results_interpolation)
            self.results_interpolation = (
                float(results_interpolation_string[0]),
                float(results_interpolation_string[1]),
                int(results_interpolation_string[2])
            )

        self._determine_background_mortality_parameter()

    def prepare_simulation_input(self):
        x_in = self.parse_input(input="x_in", reference_data=self.observations, drop_dims=[])
        y0 = self.parse_input(input="y0", reference_data=self.observations, drop_dims=["time"])
        
        # add model components
        if self.config.simulation.forward_interpolate_exposure_data: # type: ignore
            self.model_parameters["x_in"] = rect_interpolation(x_in)
        else:
            self.model_parameters["x_in"] = x_in

        self.model_parameters["y0"] = y0
        self.model_parameters["parameters"] = self.config.model_parameters.value_dict

    def construct_database_statement_from_config(self):
        """returns a statement to be used on a database"""
        substance = self.config.simulation.substance # type:ignore
        exposure_path = self.config.simulation.exposure_path # type:ignore
        return (
            select(Timeseries, Treatment)
            .join(Timeseries)
        ).where(
            Timeseries.variable.in_([substance]),  # type: ignore
            Timeseries.name == {exposure_path}
        )

    def read_data(self) -> xr.Dataset:
        """Reads data and returns an xarray.Dataset. 
        
        GutsBase supports reading data from
        - netcdf (.nc) files
        - expyDB (SQLite databases)
        - excel  (directories of excel files)

        expyDB and excel operate by converting data to xarrays while netcdf directly
        loads xarray Datasets. For highest control over your data, you should always use
        .nc files, because they are imported as-is.
        """
        # TODO: Update to new INTERVENTION MODEL
        dataset = str(self.config.case_study.observations)
        
        # read from a directory
        if os.path.isdir(os.path.join(self.config.case_study.data_path, dataset)):
            # This looks for xlsx files in the folder and imports them as a database and
            # then proceeds as normal
            files = glob.glob(os.path.join(
                self.config.case_study.data_path, 
                dataset, "*.xlsx"
            ))

            tempdir = tempfile.TemporaryDirectory()
            dataset = self.read_data_from_xlsx(data=files, tempdir=tempdir)

        ext = dataset.split(".")[-1]
        
        if not os.path.exists(dataset):
            dataset = os.path.join(self.data_path, dataset)
            
        if ext == "db":
            statement = self.construct_database_statement_from_config()
            observations = self.read_data_from_expydb(dataset, statement)
            
            # TODO: Integrate interventions in observations dataset

        elif ext == "nc":
            observations = xr.load_dataset(dataset)

        else:
            raise NotImplementedError(
                f"Dataset extension '.{ext}' is not recognized. "+
                "Please use one of '.db' (mysql), '.nc' (netcdf)."
            )
        
        return observations
        
    def read_data_from_xlsx(self, data, tempdir):
        database = os.path.join(tempdir.name, "import.db")

        if hasattr(self.config.simulation, "data_preprocessing"):
            preprocessing = self.config.simulation.data_preprocessing
        else:
            preprocessing = None

        create_database_and_import_data_main(
            datasets_path=data, 
            database_path=database, 
            preprocessing=preprocessing,
            preprocessing_out=os.path.join(tempdir.name, "processed_{filename}")
        )

        return database    


    def read_data_from_expydb(self, database, statement) -> xr.Dataset:

        observations_idata, interventions_idata = from_expydb(
            database=f"sqlite:///{database}",
            statement=statement
        )

        dataset = to_dataset(
            observations_idata, 
            interventions_idata,
            unit_time=self.unit_time
        )
        dataset = reduce_multiindex_to_flat_index(dataset)

        # "Continue here. I want to return multidimensional datasets for data coming "+
        # "from the database. The method can be implemented in any class. Currently I'm looking "+
        # "at guts base"

        filtered_dataset = self.filter_dataset(dataset)

        return filtered_dataset

    def process_data(self):
        """
        Currently these methods, change datasets, indices, etc. in-place.
        This is convenient, but more difficult to re-arragen with other methods
        TODO: Make these methods static if possible
        """
        self._create_indices()
        self._indices_to_dimensions()
        # define tolerance based on the sovler tolerance
        self.observations = self.observations.assign_coords(eps=self.config.jaxsolver.atol * 10)

        self._reindex_time_dim()

        if "survival" in self.observations:
            if "subject_count" not in self.observations.coords:
                self.observations = self.observations.assign_coords(
                    subject_count=("id", self.observations["survival"].isel(time=0).values, )
                )
            self.observations = self._data.prepare_survival_data_for_conditional_binomial(
                observations=self.observations
            )

        if "exposure" in self.observations:
            self.config.data_structure.exposure.observed=False

    def _convert_exposure_units(self):
        """
        TODO: Here I need to decide what to do. Work with rescaled units is dangerous
        because fitting might be complicated with weird quantities.
        It would be better to rescale output parameters
        """
        if not hasattr(self.config.simulation, "unit_exposure"):
            return
         
        units, unit_conversion_factors = self._convert_units(
            self.observations.unit.reset_coords("unit", drop=True),
            target_units=self.config.simulation.unit_exposure 
        )

        self.observations = self.observations.assign_coords({
            "unit": units,
            "unit_conversion_factors": unit_conversion_factors
        })

        self.observations[self.config.simulation.substance] =\
              self.observations[self.config.simulation.substance] * unit_conversion_factors

    @staticmethod
    def _unique_unsorted(values):
        _, index = np.unique(values, return_index=True)
        return tuple(np.array(values)[sorted(index)])

    @staticmethod
    def _convert_units(
        units: xr.DataArray, 
        target_units: Dict[str,str]
    ) -> Tuple[xr.DataArray, xr.DataArray]:
        """Converts units of values associated with the exposure dimension
        TODO: Converting before inference could be problem for the calibration, because
        it is usually good if the values are both not too small and not too large 
        """

        if len(units.dims) != 1:
            raise GutsBaseError(
                "GutsBase_convert_exposure_units only supports 1 dimensional exposure units"
            )
        
        _dim = units.dims[0]
        _coordinates = units.coords[_dim]

        converted_units = {}
        _target_units = {}

        for coord in _coordinates.values:
            unit = str(units.sel({_dim: coord}).values)
            
            # get item from config
            unit_mapping =  string_to_dict(target_units)
            # split transformation expression from target expression
            transform, target = unit_mapping[coord].split("->")
            # insert unit from observations coordinates
            transform = transform.format(x=unit)
            
            # parse and convert units
            new_unit = ureg.parse_expression(transform).to(target)
            converted_units.update({coord: new_unit})
            _target_units.update({coord: target})
            
        _units = {k: f"{cu.units:C}" for k, cu in converted_units.items()}

        # assert whether the converted units are the same as the target units
        # so the target units can be used, because the converted units may reduce
        # to dimensionless quantities.
        if not all([
            cu.units == ureg.parse_expression(tu) 
            for cu, tu in zip(converted_units.values(), _target_units.values())
        ]):
            raise GutsBaseError(
                f"Mismatch between target units {_target_units} and converted units " +
                f"{converted_units}."
            )

        _conversion_factors = {k: cu.magnitude for k, cu in converted_units.items()}
        new_unit_coords = xr.Dataset(_target_units).to_array(dim=_dim)
        conversion_factor_coords = xr.Dataset(_conversion_factors).to_array(dim=_dim)

        return new_unit_coords, conversion_factor_coords

    def _create_indices(self):
        """Use if indices should be added to sim.indices and sim.observations"""
        pass

    def _indices_to_dimensions(self):
        pass

    def filter_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        return dataset

    def _reindex_time_dim(self):
        if self.config.simulation.model is not None:
            if "_it" in self.config.simulation.model.lower():
                self.logger.info(msg=(
                    "Redindexing time vector to increase resolution, because model has "+
                    "'_it' (individual tolerance) in it's name"
                ))
                if not hasattr(self.config.simulation, "n_reindexed_x"): 
                    self.config.simulation.n_reindexed_x = 100

                new_time_index = np.unique(np.concatenate([
                    self.coordinates["time"],
                    np.linspace(
                        0, np.max(self.coordinates["time"]), 
                        int(self.config.simulation.n_reindexed_x) # type: ignore
                    )
                ]))
                self.observations = self.observations.reindex(time = new_time_index)
                return

        self.logger.info(msg=(
            "No redindexing of time vector to, because model name did not contain "+
            "'_it' (individual tolerance), or model was not given by name. If an IT model "
            "is calculated without a dense time resolution, the estimates can be biased!"
        ))

    def _determine_background_mortality_parameter(self):
        if "hb" in self.config.model_parameters.all:
            self.background_mortality = "hb"
        elif "h_b" in self.config.model_parameters.all:
            self.background_mortality = "h_b"
        else:
            raise GutsBaseError(
                "The background mortality parameter is not defined as 'hb' or 'h_b'. " +
                f"The defined parameters are {self.config.model_parameters.all}"
            )


    def recompute_posterior(self):
        """This function interpolates the posterior with a given resolution
        posterior_predictions calculate proper survival predictions for the
        posterior.

        It also makes sure that the new interpolation does not include fewer values
        than the original dataset
        """

        ri = self.results_interpolation

        # generate high resolution posterior predictions
        if self.results_interpolation is not None:
            time_interpolate = np.linspace(
                start=float(self.observations["time"].min()) if np.isnan(ri[0]) else ri[0],
                stop=float(self.observations["time"].max()) if np.isnan(ri[0]) else ri[1],
                num=self.results_interpolation[2] 
            )

            # combine original coordinates and interpolation. This 
            # a) helps error checking during posterior predictions.
            # b) makes sure that the original time vector is retained, which may be
            #    relevant for the simulation success (e.g. IT model)
            obs = self.observations.reindex(
                time=np.unique(np.concatenate(
                    [time_interpolate, self.observations["time"]]
                )),
            )

            obs["survivors_before_t"] = obs.survivors_before_t.ffill(dim="time").astype(int)
            obs["survivors_at_start"] = obs.survivors_at_start.ffill(dim="time").astype(int)
            self.observations = obs
            
        self.dispatch_constructor()
        _ = self._prob.posterior_predictions(self, self.inferer.idata) # type: ignore
        self.inferer.store_results(output=f"{self.output_path}/numpyro_posterior_interp.nc") # type: ignore
        self.logger.info("Recomputed posterior and storing in `numpyro_posterior_interp.nc`")


    def prior_predictive_checks(self, **plot_kwargs):
        super().prior_predictive_checks(**plot_kwargs)

        self._plot.plot_prior_predictions(self, data_vars=["survival"])

    def posterior_predictive_checks(self, **plot_kwargs):
        super().posterior_predictive_checks(**plot_kwargs)

        self.recompute_posterior()
        # TODO: Include posterior_predictive group once the survival predictions are correctly working
        self._plot.plot_posterior_predictions(self, data_vars=["survival"], groups=["posterior_model_fits"])


    def plot(self, results):
        self._plot.plot_survival(self, results)

    def predefined_scenarios(self):
        """
        TODO: Fix timescale to observations
        TODO: Incorporate extra exposure patterns (constant, pulse_1day, pulse_2day)
        """
        # get the maximum possible time to provide exposure scenarios that are definitely
        # long enough
        time_max = max(
            self.observations[self.config.simulation.x_dimension].max(), 
            *self.Report.ecx_estimates_times
        )

        # this produces a exposure x_in dataset with only the dimensions ID and TIME
        standard_dimensions = (
            self.config.simulation.batch_dimension,
            self.config.simulation.x_dimension, 
        )

        # get dimensions different from standard dimensions
        exposure_dimension = [
            d for d in self.observations.exposure.dims if d not in 
            standard_dimensions
        ]

        # raise an error if the number of extra dimensions is larger than 1
        if len(exposure_dimension) > 1:
            raise ValueError(
                f"{type(self).__name__} can currently handle one additional dimension for "+
                f"the exposure beside {standard_dimensions}. You provided an exposure "+ 
                f"array with the dimensions: {self.observations.exposure.dims}"
            )
        else:
            exposure_dimension = exposure_dimension[0]

        # iterate over the coordinates of the exposure dimensions to 
        exposure_coordinates = self.observations.exposure[exposure_dimension].values

        scenarios = {}
        for coord in exposure_coordinates:
            concentrations = np.where(coord == exposure_coordinates, 1.0, 0.0)

            exposure_dict = {
                coord: ExposureDataDict(start=0, end=1, concentration=conc)
                for coord, conc in zip(exposure_coordinates, concentrations)
            }

            scenario = design_exposure_scenario(
                exposures=exposure_dict,
                t_max=time_max,
                dt=1/24,
                exposure_dimension=exposure_dimension
            )

            scenarios.update({
                f"1day_exposure_{coord}": scenario
            })

        return scenarios

    @staticmethod
    def _exposure_data_to_xarray(exposure_data: Dict[str, pd.DataFrame], dim: str):
        """
        TODO: Currently no rect interpolation
        """
        arrays = {}
        for key, df in exposure_data.items():
            # this override is necessary to make all dimensions work out
            df.index.name = "time"
            arrays.update({
                key: df.to_xarray().to_dataarray(dim="id", name=key)
            }) 

        exposure_array = xr.Dataset(arrays).to_array(dim=dim, name="exposure")
        exposure_array = exposure_array.transpose("id", "time", ...)
        return xr.Dataset({"exposure": exposure_array})

    @staticmethod
    def _survival_data_to_xarray(survival_data: pd.DataFrame):
        # TODO: survival name is currently not kept because the raw data is not transferred from the survival
        survival_data.index.name = "time"
        
        survival_array = survival_data.to_xarray().to_dataarray(dim="id", name="survival")
        survival_array = survival_array.transpose("id", "time", ...)
        arrays = {"survival": survival_array}
        return xr.Dataset(arrays)

    @property
    def _exposure_dimension(self):
        standard_dims = [
            self.config.simulation.batch_dimension, 
            self.config.simulation.x_dimension
        ]
        
        extra_dims = []
        for k in self.config.data_structure["exposure"].dimensions:
            if k not in standard_dims:
                extra_dims.append(k)
            else:
                pass

        if len(extra_dims) > 1:
            raise GutsBaseError(
                "Guts Base can currently only handle one exposure dimension beside" +
                "the standard dimensions."
            )
        else:
            return extra_dims[0]
        

    def expand_batch_like_coordinate_to_new_dimension(self, coordinate, variables):
        """This method will take an existing coordinate of a dataset that has the same
        coordinate has the batch dimension. It will then re-express the coordinate as a
        separate dimension for the given variables, by duplicating the N-Dimensional array
        times the amount of unique names in the specified coordinate to create an 
        N+1-dimensional array. This array will be filled with zeros along the batch dimension
        where the specified coordinate along the ID dimension coincides with the new (unique)
        coordinate of the new dimension. 

        This process is entirely reversible
        """
        old_coords = self.observations[coordinate]
        batch_dim = self.config.simulation.batch_dimension

        # old coordinate before turning it into a dimension
        obs = self.observations.drop(coordinate)

        # create unique coordinates of the new dimension, preserving the order of the
        # old coordinate
        _, index = np.unique(old_coords, return_index=True)
        coords_new_dim = tuple(np.array(old_coords)[sorted(index)])

        for v in variables:
            # take data variable and extract dimension order
            data_var = obs[v]
            dim_order = data_var.dims

            # expand the dimensionality, then transpose for new dim to be last
            data_var = data_var.expand_dims(coordinate).transpose(..., batch_dim, coordinate)

            # create a dummy dimension to broadcast the new array 
            # dummy_3d = np.ones((1, len(coords_new_dim)))
            dummy_categorical = pd.get_dummies(old_coords).astype(int).values

            # apply automatic broadcasting to increase the size of the new dimension
            # data_var_np1_d = data_var * dummy_3d
            data_var_np1_d = data_var * dummy_categorical
            data_var_np1_d.attrs = data_var.attrs

            # annotate coordinates of the new dimension
            data_var_np1_d = data_var_np1_d.assign_coords({
                coordinate: list(coords_new_dim)
            })

            # transpose back to original dimension order with new dim as last dim
            data_var_np1_d = data_var_np1_d.transpose(*dim_order, coordinate)
            obs[v] = data_var_np1_d

        return obs

    def map_batch_coordinates_to_extra_dim_coordinates(
        self, 
        observations: xr.Dataset, 
        target_dimension: str,
        coordinates: Optional[List[str]] = None
    ) -> xr.Dataset:
        """Iterates over coordinates and reduces those coordinates to the new dimension
        which have the same number of unique coordinates as the new dimension has coordinates
        """
        if coordinates is None:
            coordinates = list(observations.coords.keys())

        for key, coord in observations.coords.items():
            # skips coords, if not specified in coordinates
            if key not in coordinates:
                continue

            if self.config.simulation.batch_dimension in coord.dims and key not in observations.dims:
                if len(coord.dims) == 1:
                    dim_coords = self._unique_unsorted(coord.values)
                    if len(dim_coords) == len(observations[target_dimension]):
                        observations[key] = (target_dimension, list(dim_coords))
                    else:
                        pass
                else:
                    warnings.warn(
                        f"Coordinate '{key}' is has dimensions {coord.dims}. " +
                        "Mapping coordinates with more than 1 dimension to the extra " +
                        f"dimension '{target_dimension}' is not supported yet."
                    )
                    pass

        return observations
                

    def reduce_dimension_to_batch_like_coordinate(self, dimension, variables):
        """This method takes an existing dimension from a N-D array and reduces it to an
        (N-1)-D array, by writing a new coordinate from the reducible dimension in the way
        that the new batch-like coordinate takes the coordinate of the dimension, where
        the data of the N-D array was not zero. After it has been asserted that there is
        only a unique candidate for the each coordinate along the batch dimension 
        (i.e. only one value is non-zero for a given batch-coordinate), the dimension will
        be reduced by summing over the given dimension.

        The method is contingent on having no overlap in batch dimension in the dataset
        """
        pass

    def initialize_from_script(self):
        pass

    @property
    def _model_class(self):
        if hasattr(self.config.simulation, "model_class"):
            module, attr = self.config.simulation.model_class.rsplit(".", 1)
            _module = importlib.import_module(module)
            return getattr(_module, attr)
        else:
            return None

    ### API methods ###


    def point_estimate(
        self, 
        estimate: Literal["mean", "map"] = "map",  
        to: Literal["xarray", "dict"] = "xarray"
    ):
        """Returns a point estimate of the posterior. If you want more control over the posterior
        use the attribute: sim.inferer.idata.posterior and summarize it or select from it
        using the arviz (https://python.arviz.org/en/stable/index.html) and the 
        xarray (https://docs.xarray.dev/en/stable/index.html) packages

        Parameters
        ----------

        estimate : Literal["map", "mean"]
            Point estimate to return. 
            - map: Maximum a Posteriori. The sample that has the highest posterior probability.
              This sample considers the correlation structure of the posterior
            - mean: The average of all marginal parameter distributions.

        to : Literal["xarray", "dict"]
            Specifies the representation to transform the summarized data to. dict can
            be used to insert parameters in the .evaluate() method. While xarray is the
            standard view. Defaults to xarray

        Example
        -------

        >>> sim.best_estimate(to='dict')
        """
        if estimate == "mean":
            best_estimate = self.inferer.idata.posterior.mean(("chain", "draw"))

        elif estimate == "map":
            loglik = self.inferer.idata.log_likelihood\
                .sum(["id", "time"])\
                .to_array().sum("variable")
            
            sample_max_loglik = loglik.argmax(dim=("chain", "draw"))
            best_estimate = self.inferer.idata.posterior.sel(sample_max_loglik)
        else:
            raise GutsBaseError(
                f"Estimate '{estimate}' not implemented. Choose one of ['mean', 'map']"
            )


        if to == "xarray":
            return best_estimate
            
        elif to == "dict":
            return {k: v.values for k, v in best_estimate.items()}

        else:
            raise GutsBaseError(
                "PymobConverter.best_esimtate() supports only return types to=['xarray', 'dict']" +
                f"You used {to=}"
            )


    def evaluate(
        self, 
        parameters: Mapping[str, float|NumericArray|Sequence[float]] = {}, 
        y0: Mapping[str, float|NumericArray|Sequence[float]] = {}, 
        x_in: Mapping[str, float|NumericArray|Sequence[float]] = {}, 
    ):
        """Evaluates the model along the coordinates of the observations with given
        parameters, x_in, and y0. The dictionaries passed to the function arguments
        only overwrite the existing default parameters; which makes the usage very simple.

        Note that the first run of .evaluate() after calling the .dispatch_constructor()
        takes a little longer, because the model and solver are jit-compiled to JAX for
        highly efficient computations.

        Parameters
        ----------

        theta : Dict[float|Sequence[float]]
            Dictionary of model parameters that should be changed for dispatch.
            Unspecified model parameters will assume the default values, 
            specified under config.model_parameters.NAME.value

        y0 : Dict[float|Sequence[float]]
            Dictionary of initial values that should be changed for dispatch.
        
        x_in : Dict[float|Sequence[float]]
            Dictionary of model input values that should be changed for dispatch.


        Example
        -------

        >>> sim.dispatch_constructor()  # necessary if the sim object has been modified
        >>> # evaluate setting the background mortaltiy to zero
        >>> sim.evaluate(parameters={'hb': 0.0})  

        """
        evaluator = self.dispatch(theta=parameters, x_in=x_in, y0=y0)
        evaluator()
        return evaluator.results

    def load_exposure_scenario(
        self, 
        data: str|Dict[str,pd.DataFrame],
        sheet_name_prefix: str = "",
        rect_interpolate=False

    ):

        if isinstance(data, str):
            _data, time_unit = read_excel_file(
                path=data, 
                sheet_name_prefix=sheet_name_prefix,
                convert_time_to=self.unit_time
            )
        else:
            _data = data


        self._obs_backup = self.observations.copy(deep=True)

        # read exposure array from file
        exposure_dim = [
            d for d in self.config.data_structure.exposure.dimensions
            if d not in (self.config.simulation.x_dimension, self.config.simulation.batch_dimension)
        ]
        exposure = self._exposure_data_to_xarray(
            exposure_data=_data, 
            dim=exposure_dim[0]
        )

        # combine with observations
        new_obs = xr.combine_by_coords([
            exposure,
            self.observations.survival
        ]).sel(id=exposure.id)
        
        self.observations = new_obs.sel(time=[t for t in new_obs.time if t <= exposure.time.max()])
        self.config.simulation.x_in = ["exposure=exposure"]
        self.model_parameters["x_in"] = self.parse_input("x_in", exposure).ffill("time")  # type: ignore
        self.model_parameters["y0"] = self.parse_input("y0", drop_dims=["time"])

        self.dispatch_constructor()

    def export(self, directory: Optional[str] = None):
        self.config.simulation.skip_data_processing = False
        super().export(directory=directory)

    def copy(self):
        """Creates a copy of a SimulationBase object by deepcopying all loose references
        TODO: If this works out well integrate into pymob. I have the feeling there will
        still be some problems down the line.
        """
        with warnings.catch_warnings(action="ignore"):
            # create the tempdir in the output path, because on the remote cluster
            # the default temporary directory may not have enough space. Using the output
            # path here resolves any path issues.
            tmp_basedir = os.path.join(self.output_path, "tmp")
            os.makedirs(tmp_basedir, exist_ok=True)
            with tempfile.TemporaryDirectory(dir=tmp_basedir) as name:
                self.export(directory=name)
                print(f"Exported files ({name}):", os.listdir(name))
                sim_copy = type(self).from_directory(name)

        return sim_copy

    @staticmethod
    def _condition_posterior(
        posterior: xr.Dataset, 
        parameter: str, 
        value: float, 
        exception: Literal["raise", "warn"]="raise"
    ):
        """TODO: Provide this method also to SimulationBase"""
        if parameter not in posterior:
            keys = list(posterior.keys())
            msg = (
                f"{parameter=} was not found in the posterior {keys=}. " +
                f"Unable to condition the posterior to {value=}. Have you "+
                "requested the correct parameter for conditioning?"
            )

            if exception == "raise":
                raise GutsBaseError(msg)
            elif exception == "warn":
                warnings.warn(msg)
            else:
                raise GutsBaseError(
                    "Use one of exception='raise' or exception='warn'. " +
                    f"Currently using {exception=}"
                )

        # broadcast value so that methods like drawing samples and hdi still work
        broadcasted_value = np.full_like(posterior[parameter], value)

        return posterior.assign({
            parameter: (posterior[parameter].dims, broadcasted_value)
        })


class GutsSimulationConstantExposure(GutsBase):
    t_max = 10
    def initialize_from_script(self):
        self.config.data_structure.B = DataVariable(dimensions=["time"], observed=False)
        self.config.data_structure.D = DataVariable(dimensions=["time"], observed=False)
        self.config.data_structure.H = DataVariable(dimensions=["time"], observed=False)
        self.config.data_structure.survival = DataVariable(dimensions=["time"], observed=False)

        # y0
        self.config.simulation.y0 = ["D=Array([0])", "H=Array([0])", "survival=Array([1])"]
        self.model_parameters["y0"] = self.parse_input(input="y0", drop_dims=["time"])

        # parameters
        self.config.model_parameters.C_0 = Param(value=10.0, free=False)
        self.config.model_parameters.k_d = Param(value=0.9, free=True)
        self.config.model_parameters.h_b = Param(value=0.00005, free=True)
        self.config.model_parameters.b = Param(value=5.0, free=True)
        self.config.model_parameters.z = Param(value=0.2, free=True)

        self.model_parameters["parameters"] = self.config.model_parameters.value_dict
        self.config.simulation.model = "guts_constant_exposure"

        self.coordinates["time"] = np.linspace(0,self.t_max)

    def use_jax_solver(self):
        # =======================
        # Define model and solver
        # =======================

        self.coordinates["time"] = np.array([0,self.t_max])
        self.config.simulation.model = "guts_constant_exposure"

        self.solver = JaxSolver

        self.dispatch_constructor(diffrax_solver=Dopri5)

    def use_symbolic_solver(self):
        # =======================
        # Define model and solver
        # =======================

        self.coordinates["time"] = np.array([0,self.t_max])
        self.config.simulation.model = "guts_sympy"

        self.solver = mod.PiecewiseSymbolicSolver

        self.dispatch_constructor(diffrax_solver=Dopri5)


class GutsSimulationVariableExposure(GutsSimulationConstantExposure):
    t_max = 10
    def initialize_from_script(self):
        super().initialize_from_script()
        del self.coordinates["time"]
        exposure = create_artificial_data(
            t_max=self.t_max, dt=1, 
            exposure_paths=["topical"]
        ).squeeze()
        self.observations = exposure

        self.config.data_structure.exposure = DataVariable(dimensions=["time"], observed=True)

        self.config.simulation.x_in = ["exposure=exposure"]
        x_in = self.parse_input(input="x_in", reference_data=exposure, drop_dims=[])
        x_in = rect_interpolation(x_in=x_in, x_dim="time")
        self.model_parameters["x_in"] = x_in

        # parameters
        self.config.model_parameters.remove("C_0")

        self.model_parameters["parameters"] = self.config.model_parameters.value_dict
        self.config.simulation.solver_post_processing = "red_sd_post_processing"
        self.config.simulation.model = "guts_variable_exposure"


    def use_jax_solver(self):
        # =======================
        # Define model and solver
        # =======================

        self.model = self._mod.guts_variable_exposure
        self.solver = JaxSolver

        self.dispatch_constructor(diffrax_solver=Dopri5)

    def use_symbolic_solver(self, do_compile=True):
        # =======================
        # Define model and solver
        # =======================

        self.model = self._mod.guts_sympy
        self.solver = self._mod.PiecewiseSymbolicSolver

        self.dispatch_constructor(do_compile=do_compile, output_path=self.output_path)

