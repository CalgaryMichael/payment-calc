import argparse
import os
import sys

from payment_calc.models import Scenario
from payment_calc.payment_calc import decrease_debt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('scenario_file', type=str)
    parser.add_argument('--sort', type=str, default='debt_total')
    parser.add_argument('--sort-reverse', action='store_true', default=False)
    args = parser.parse_args()

    scenario = Scenario.of(args.scenario_file)
    decrease_debt(scenario, sort_key=args.sort, reverse=args.sort_reverse)


if __name__ == '__main__':
    main()

