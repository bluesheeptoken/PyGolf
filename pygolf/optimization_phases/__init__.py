from typing import List

from .always_apply_phase import AlwaysApplyPhase
from .phase import Phase
from .rename_phase import RenamePhase

all_phases: List[Phase] = [AlwaysApplyPhase(), RenamePhase()]
