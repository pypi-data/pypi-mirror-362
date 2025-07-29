import pytest
from guts_base import GutsBase
from guts_base.sim import construct_sim_from_config

# run tests with the Simulation fixtures
def test_setup(sim):
    """Tests the construction method"""
    assert True


def test_simulation(sim):
    """Tests if a forward simulation pass can be computed"""
    sim.dispatch_constructor()
    evaluator = sim.dispatch()
    evaluator()
    evaluator.results

    assert True
            
def test_copy(sim):
    sim.dispatch_constructor()
    e_orig = sim.dispatch()
    e_orig()
    e_orig.results

    sim_copy = sim.copy()
    
    sim_copy.dispatch_constructor()
    e_copy = sim_copy.dispatch()
    e_copy()

    assert (e_copy.results == e_orig.results).all().to_array().all().values


@pytest.mark.slow
@pytest.mark.parametrize("backend", ["numpyro"])
def test_inference(sim: GutsBase, backend):
    """Tests if prior predictions can be computed for arbitrary backends"""
    sim.dispatch_constructor()
    sim.set_inferer(backend)

    sim.config.inference.n_predictions = 2
    sim.prior_predictive_checks()
    
    sim.config.inference_numpyro.kernel = "svi"
    sim.config.inference_numpyro.svi_iterations = 10
    sim.config.inference_numpyro.svi_learning_rate = 0.05
    sim.config.inference_numpyro.draws = 10
    sim.config.inference.n_predictions = 10

    sim.inferer.run()

    sim.posterior_predictive_checks()

    sim.config.report.debug_report = True
    sim.report()


if __name__ == "__main__":
    # test_inference(sim=construct_sim_from_config("red_sd", GutsBase), backend="numpyro")
    test_inference(sim=construct_sim_from_config("red_sd_da", GutsBase), backend="numpyro")
