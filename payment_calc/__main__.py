import argparse
import os
import sys

from payment_calc.models import Scenario
from payment_calc.calculator import build_projected_debt_reduction
from payment_calc.save import default_output_fp


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('scenario_file', type=str)
    parser.add_argument('--output-fp', type=str, default=None)
    parser.add_argument('--sort', type=str, default='debt_total')
    parser.add_argument('--sort-reverse', action='store_true', default=False)
    args = parser.parse_args()

    scenario = Scenario.of(args.scenario_file)
    output_fp=args.output_fp or default_output_fp(args.scenario_file)
    build_projected_debt_reduction(
        scenario,
        output_fp=output_fp,
        sort_key=args.sort,
        reverse=args.sort_reverse
    )

