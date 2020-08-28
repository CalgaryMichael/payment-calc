import os
import sys

from payment_calc.models import Scenario
from payment_calc.payment_calc import decrease_debt


if __name__ == '__main__':
    file_loc = os.path.abspath(sys.argv[1])
    scenario = Scenario.of(file_loc)
    decrease_debt(scenario, sort_key='payments', reverse=True)

