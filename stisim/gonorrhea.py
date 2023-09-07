"""
Defne gonorrhea
"""

import numpy as np
import stisim as ss


__all__ = ['Gonorrhea']


class Gonorrhea(ss.Disease):

    def __init__(self, pars=None):
        super().__init__(pars)

        self.susceptible    = ss.State('susceptible', bool, True)
        self.infected       = ss.State('infected', bool, False)
        self.ti_infected    = ss.State('ti_infected', float, 0)
        self.ti_recovered   = ss.State('ti_recovered', float, 0)
        self.ti_dead        = ss.State('ti_dead', float, np.nan)  # Death due to gonorrhea

        self.rng_prog       = ss.Stream('prog_dur')
        self.rng_dead       = ss.Stream('dead')
        self.rng_dur_inf    = ss.Stream('dur_inf')

        self.pars = ss.omerge({
            'dur_inf': 3,  # not modelling diagnosis or treatment explicitly here
            'p_death': 0.2,
            'initial': 3,
            'eff_condoms': 0.7,
        }, self.pars)

        return

    def update_states(self, sim):
        # What if something in here should depend on another module?
        # I guess we could just check for it e.g., 'if HIV in sim.modules' or
        # 'if 'hiv' in sim.people' or something
        gonorrhea_deaths = self.ti_dead <= sim.ti
        sim.people.alive[gonorrhea_deaths] = False
        sim.people.ti_dead[gonorrhea_deaths] = sim.ti

        self.results.new_deaths += len(gonorrhea_deaths)

        return
    
    def update_results(self, sim):
        super(Gonorrhea, self).update_results(sim)
        return
    
    def make_new_cases(self, sim):
        super(Gonorrhea, self).make_new_cases(sim)
        return

    def set_prognoses(self, sim, to_uids, from_uids=None):
        self.susceptible[to_uids] = False
        self.infected[to_uids] = True
        self.ti_infected[to_uids] = sim.ti

        #dur = sim.ti + self.rng_dur_inf.poisson(self.pars['dur_inf']/sim.pars.dt, len(to_uids)) # By whom infected from??? TODO
        dur = sim.ti + self.rng_dur_inf.poisson(self.pars['dur_inf']/sim.pars.dt, to_uids) # By whom infected from??? TODO
        dead = self.rng_dead.bernoulli(self.pars.p_death, to_uids)

        self.ti_recovered[to_uids[~dead]] = dur[~dead]
        self.ti_dead[to_uids[dead]] = dur[dead]
        return
