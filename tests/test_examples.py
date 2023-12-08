"""
Run simplest tests
"""

# %% Imports and settings
import stisim as ss
import matplotlib.pyplot as plt
import scipy.stats as sps
import numpy as np

def test_sir():
    ppl = ss.People(10000)
    ppl.networks = ss.ndict(ss.RandomNetwork(n_contacts=sps.poisson(mu=4)))

    sir_pars = {
        'dur_inf': sps.norm(loc=10), # Override the default distribution
    }
    sir = ss.SIR(sir_pars)

    # You can also change the parameters of the default lognormal distribution directly!
    #sir.pars['dur_inf'].kwds['loc'] = 5 
    
    # Or why not put a lambda here for fun!
    sir.pars['dur_inf'].kwds['loc'] = lambda self, sim, uids: sim.people.age[uids]/10

    sir.pars['beta'] = {'randomnetwork': 0.1}
    sim = ss.Sim(people=ppl, diseases=sir)
    sim.run()

    plt.figure()
    plt.stackplot(
        sim.yearvec,
        sir.results.n_susceptible,
        sir.results.n_infected,
        sir.results.n_recovered,
        sim.results.new_deaths.cumsum(),
    )
    plt.legend(['Susceptible', 'Infected', 'Recovered', 'Dead'])
    plt.xlabel('Year')
    plt.title('SIR')
    return

#@pytest.mark.skip(reason="Haven't converted yet")
def test_ncd():
    ppl = ss.People(10000)
    ppl.networks = None
    ncd = ss.NCD()
    sim = ss.Sim(people=ppl, diseases=ncd)
    sim.run()

    plt.figure()
    plt.stackplot(
        sim.yearvec,
        ncd.results.n_not_at_risk,
        ncd.results.n_at_risk-ncd.results.n_affected,
        ncd.results.n_affected,
        sim.results.new_deaths.cumsum(),
    )
    plt.legend(['Not at risk','At risk','Affected', 'Dead'])
    plt.xlabel('Year')
    plt.title('NCD')
    return


if __name__ == '__main__':
    ss.options(multirng=False)
    sim1 = test_sir()
    sim2 = test_ncd()
    plt.show()