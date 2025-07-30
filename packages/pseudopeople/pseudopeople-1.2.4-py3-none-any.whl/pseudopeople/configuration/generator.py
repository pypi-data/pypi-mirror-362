from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd
import yaml
from layered_config_tree import LayeredConfigTree

from pseudopeople.configuration import NO_NOISE, Keys
from pseudopeople.configuration.validator import (
    validate_noise_level_proportions,
    validate_overrides,
)
from pseudopeople.constants.data_values import DEFAULT_DO_NOT_RESPOND_ROW_PROBABILITY
from pseudopeople.entity_types import RowNoiseType
from pseudopeople.noise_entities import NOISE_TYPES
from pseudopeople.schema_entities import COLUMNS, DATASETS, Dataset

# Define non-baseline default items
# NOTE: default values are defined in entity_types.RowNoiseType and entity_types.ColumnNoiseType
DEFAULT_NOISE_VALUES = {
    DATASETS.census.name: {
        Keys.ROW_NOISE: {
            NOISE_TYPES.do_not_respond.name: {
                Keys.ROW_PROBABILITY: DEFAULT_DO_NOT_RESPOND_ROW_PROBABILITY[
                    DATASETS.census.name
                ],
            }
        },
    },
    DATASETS.acs.name: {
        Keys.ROW_NOISE: {
            NOISE_TYPES.do_not_respond.name: {
                Keys.ROW_PROBABILITY: DEFAULT_DO_NOT_RESPOND_ROW_PROBABILITY[
                    DATASETS.acs.name
                ],
            },
        },
    },
    DATASETS.cps.name: {
        Keys.ROW_NOISE: {
            NOISE_TYPES.do_not_respond.name: {
                Keys.ROW_PROBABILITY: DEFAULT_DO_NOT_RESPOND_ROW_PROBABILITY[
                    DATASETS.cps.name
                ],
            },
        },
    },
    DATASETS.tax_w2_1099.name: {
        Keys.ROW_NOISE: {
            NOISE_TYPES.omit_row.name: {
                Keys.ROW_PROBABILITY: 0.005,
            },
        },
        Keys.COLUMN_NOISE: {
            COLUMNS.ssn.name: {
                NOISE_TYPES.copy_from_household_member.name: {
                    Keys.CELL_PROBABILITY: 0.00,
                }
            },
        },
    },
    DATASETS.wic.name: {
        Keys.ROW_NOISE: {
            NOISE_TYPES.omit_row.name: {
                Keys.ROW_PROBABILITY: 0.005,
            },
        },
    },
    # No noise of any kind for SSN in the SSA observer
    DATASETS.ssa.name: {
        Keys.COLUMN_NOISE: {
            COLUMNS.ssn.name: {
                noise_type.name: {
                    Keys.CELL_PROBABILITY: 0.0,
                }
                for noise_type in COLUMNS.ssn.noise_types
            },
        },
    },
}


def get_configuration(
    overrides: Optional[Union[Path, str, Dict]] = None,
    dataset: Dataset = None,
    user_filters: List[Tuple[Union[str, int, pd.Timestamp]]] = None,
) -> LayeredConfigTree:
    """
    Gets a noising configuration LayeredConfigTree, optionally overridden by a user-provided YAML.

    :param overrides: A path to the YAML file or a dictionary defining user overrides for the defaults
    :return: a LayeredConfigTree object of the noising configuration
    """

    if overrides == NO_NOISE:
        is_no_noise = True
        overrides = None
    elif isinstance(overrides, (Path, str)):
        with open(overrides, "r") as f:
            overrides = yaml.safe_load(f)
        is_no_noise = False
    else:
        is_no_noise = False
    noising_configuration = _generate_configuration(is_no_noise)
    if overrides is not None:
        add_overrides(noising_configuration, overrides, dataset, user_filters)

    return noising_configuration


def _generate_configuration(is_no_noise: bool) -> LayeredConfigTree:
    default_config_layers = [
        "baseline",
        "default",
        "user",
    ]
    noising_configuration = LayeredConfigTree(layers=default_config_layers)
    # Instantiate the configuration file with baseline values
    baseline_dict = {}
    # Loop through each dataset
    for dataset in DATASETS:
        dataset_dict = {}
        row_noise_dict = {}
        column_dict = {}

        # Loop through row noise types
        for row_noise in dataset.row_noise_types:
            row_noise_type_dict = get_noise_type_dict(row_noise, is_no_noise)
            if row_noise_type_dict:
                row_noise_dict[row_noise.name] = row_noise_type_dict

        # Loop through columns and their applicable column noise types
        for column in dataset.columns:
            column_noise_dict = {}
            for noise_type in column.noise_types:
                column_noise_type_dict = get_noise_type_dict(noise_type, is_no_noise)
                if column_noise_type_dict:
                    column_noise_dict[noise_type.name] = column_noise_type_dict
            if column_noise_dict:
                column_dict[column.name] = column_noise_dict

        # Compile
        if row_noise_dict:
            dataset_dict[Keys.ROW_NOISE] = row_noise_dict
        if column_dict:
            dataset_dict[Keys.COLUMN_NOISE] = column_dict

        # Add the dataset's dictionary to baseline
        if dataset_dict:
            baseline_dict[dataset.name] = dataset_dict

    noising_configuration.update(baseline_dict, layer="baseline")

    # Update configuration with non-baseline default values
    if not is_no_noise:
        noising_configuration.update(DEFAULT_NOISE_VALUES, layer="default")
    return noising_configuration


def get_noise_type_dict(noise_type, is_no_noise: bool) -> Dict:
    noise_type_dict = {}
    if noise_type.probability is not None:
        noise_level = 0.0 if is_no_noise else noise_type.probability
        noise_type_dict[noise_type.probability_key] = noise_level
    if noise_type.additional_parameters is not None:
        for key, value in noise_type.additional_parameters.items():
            # FIXME: This makes a big assumption that the additional parameters are all floats
            # If we were to add a noise type or additional parameter key that was a list or dict
            # like we have in some column noise types this would not work.
            noise_level = (
                0.0 if is_no_noise and isinstance(noise_type, RowNoiseType) else value
            )
            noise_type_dict[key] = noise_level
    return noise_type_dict


def add_overrides(
    noising_configuration: LayeredConfigTree,
    overrides: Dict,
    dataset: Dataset = None,
    user_filters: List[Tuple[Union[str, int, pd.Timestamp]]] = None,
) -> None:
    validate_overrides(overrides, noising_configuration)
    overrides = _format_overrides(noising_configuration, overrides)
    noising_configuration.update(overrides, layer="user")
    # Note: dataset and user_filters should both be None when using the get_config wrapper
    # or both be inputs from generate_XXX functions.
    if (dataset is not None) and (user_filters is not None):
        # TODO: refactor validate_noise_level_proportions to take overrides as arg and live in validate overrides
        # Note: validate_noise_level_proportions must happen after user layer configuration update
        validate_noise_level_proportions(noising_configuration, dataset, user_filters)


def _format_overrides(default_config: LayeredConfigTree, user_dict: Dict) -> Dict:
    """Formats the user's configuration file as necessary, so it can properly
    update noising configuration to be used
    """
    user_dict = _format_misreport_age_perturbations(default_config, user_dict)
    return user_dict


def _format_misreport_age_perturbations(
    default_config: LayeredConfigTree, user_dict: Dict
) -> Dict:
    # Format any age perturbation lists as a dictionary with uniform probabilities
    for dataset in user_dict:
        user_perturbations = (
            user_dict[dataset]
            .get(Keys.COLUMN_NOISE, {})
            .get("age", {})
            .get(NOISE_TYPES.misreport_age.name, {})
            .get(Keys.POSSIBLE_AGE_DIFFERENCES, {})
        )
        if not user_perturbations:
            continue
        formatted = {}
        default_perturbations = default_config[dataset][Keys.COLUMN_NOISE]["age"][
            NOISE_TYPES.misreport_age.name
        ][Keys.POSSIBLE_AGE_DIFFERENCES]
        # Replace default configuration with 0 probabilities
        for perturbation in default_perturbations:
            formatted[perturbation] = 0
        if isinstance(user_perturbations, list):
            # Add user perturbations with uniform probabilities
            uniform_prob = 1 / len(user_perturbations)
            for perturbation in user_perturbations:
                formatted[perturbation] = uniform_prob
        else:
            for perturbation, prob in user_perturbations.items():
                formatted[perturbation] = prob

        user_dict[dataset][Keys.COLUMN_NOISE]["age"][NOISE_TYPES.misreport_age.name][
            Keys.POSSIBLE_AGE_DIFFERENCES
        ] = formatted

    return user_dict
