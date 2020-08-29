import io
import dataclasses
import json
import os
from typing import List

from .models import Outcome


def write_outcomes_to_file(output_fp: str, outcomes: List[Outcome]) -> None:
    outcome_data = list(dataclasses.asdict(o) for o in outcomes)
    with io.open(output_fp, 'w+') as file_:
        json.dump(outcome_data, file_, indent=2, default=str)


def default_output_fp(input_fp: str) -> str:
    """Get the default output path based off of the input path"""
    file_name = os.path.basename(input_fp)
    return os.path.abspath(f'./outputs/{file_name}')

