"""
Model of contagion in a population.
"""
from typing import List
from mvc import Listenable
import random
import enum

# States we will track, and state transitions

class DiseaseState(enum.Enum):
    """States an individual can be in.
    Each individual begins vulnerable.  If
    they are affected, they are first asymptomatic
    but later become symptomatic.  After some time
    they either recover (and are immune) or die.
    """
    vulnerable = enum.auto()
    asymptomatic = enum.auto()
    symptomatic = enum.auto()
    recovered = enum.auto()
    dead = enum.auto()

# Clock definition for state transitions. The tick unit
# is a fraction or multiple of the clock.
TICK = 0.5

# Disease characteristics
TIME_ASYMPTOMATIC = 2  # Time units until symptoms appear (4 ticks)
TIME_SYMPTOMATIC = 3   # Time units until cured or dead (6 ticks)
P_DEATH = 0.02    # If I'm sick, what is the chance I'll die?
P_TRANSMIT = 0.05 # Chance I'll transmit it on an encounter with a neighbor


class Individual(Listenable):
    """An individual in the population,
    e.g., a person who might get and spread a disease.
    The 'state' instance variable is public read-only, e.g.,
    listeners can check it.
    """

    def __init__(self):
        super().__init__()
        # Initially we are 'vulnerable', not yet infected
        self._time_in_state = 0   # How long in this state?
        self.state = DiseaseState.vulnerable

    # In this first simple prototype, we just hardwire
    # the state machine.
    def tick(self):
        """Passage of time"""
        self._time_in_state += TICK
        # State transitions
        prior_state = self.state
        if self.state == DiseaseState.asymptomatic:
            if self._time_in_state > TIME_ASYMPTOMATIC:
                self.state = DiseaseState.symptomatic
        if self.state == DiseaseState.symptomatic:
            if self._time_in_state > TIME_SYMPTOMATIC:
                if random.random() < P_DEATH:
                    self.state = DiseaseState.dead
                else:
                    self.state = DiseaseState.recovered
        # Whenever state changes ...
        if self.state != prior_state:
            self._time_in_state = 0
            self.notify_all("newstate")

        # Are we quarantining?  Are we social distancing?
        self.social_behavior()


    def infect(self):
        """Called by another individual spreading germs.
        May also be called on "patient 0" to start simulation.
        """
        if self.state == DiseaseState.vulnerable:
            self.state = DiseaseState.asymptomatic
            self._time_in_state = 0
            self.notify_all("newstate")


    def meet(self, other: "Individual"):
        """On each tick, with some probability we may perform
        some social behaviors, which may depend on our state.
        Social behaviors are partly mediated by our neighborhood.
        In the simplest version of the model, interaction
        (meeting neighbors) is driven by the neighborhood alone,
        and the individual (this object) just determines whether
        it spreads the contagion.
        """
        if self._is_contagious() and other.state == DiseaseState.vulnerable:
            if random.random() < P_TRANSMIT:
                other.infect()



    def _is_contagious(self) -> bool:
        """Is this individual currently contagious?
        In some diseases, only symptomatic individuals
        can spread virus.  In some other diseases, apparently
        including SARS Corona Virus 2, asymptomatic individuals
        can spread virus.
        """
        if self.state == DiseaseState.symptomatic:
            return True
        if self.state == DiseaseState.asymptomatic:
            return True
        return False









