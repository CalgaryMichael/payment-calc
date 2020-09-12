import io
import collections
import dataclasses
import json
import os
from typing import List

from .models import Outcome


def write_outcomes_to_file(
        output_fp: str,
        outcomes: List[Outcome],
        transpose: bool=False
) -> None:
    outcome_data = build_output_data_shape(outcomes, transpose)
    with io.open(output_fp, 'w+') as file_:
        json.dump(outcome_data, file_, indent=2, default=str)


def build_output_data_shape(outcomes: List[Outcome], transpose: bool) -> list:
    if transpose:
        transposed_data = collections.defaultdict(list)
        for outcome in outcomes:
            for debt_outcome in outcome.debt_outcomes:
                transposed_data[debt_outcome.debt_name].append(dict(
                    effective_date=outcome.effective_date,
                    debt_total=debt_outcome.debt_total,
                    payment_sum=debt_outcome.payment_sum
                ))
        output_data = list({'debt_name': k, 'debt_total': v} for k, v in transposed_data.items())
    else:
        output_data = list(dataclasses.asdict(o) for o in outcomes)
    return output_data


def default_output_fp(input_fp: str) -> str:
    """Get the default output path based off of the input path"""
    file_name = os.path.basename(input_fp)
    return os.path.abspath(f'./outputs/{file_name}')

