import itertools

import pandas as pd
import pytest
import yaml

from pseudopeople.configuration import NO_NOISE, Keys, get_configuration
from pseudopeople.configuration.generator import DEFAULT_NOISE_VALUES
from pseudopeople.configuration.interface import get_config
from pseudopeople.configuration.validator import ConfigurationError
from pseudopeople.entity_types import ColumnNoiseType, RowNoiseType
from pseudopeople.noise_entities import NOISE_TYPES
from pseudopeople.schema_entities import COLUMNS, DATASETS

PROBABILITY_VALUE_LOGS = [
    ("a", "must be floats or ints"),
    (-0.01, "must be between 0 and 1"),
    (1.01, "must be between 0 and 1"),
]
COLUMN_NOISE_TYPES = [
    noise_type for noise_type in NOISE_TYPES if isinstance(noise_type, ColumnNoiseType)
]
ROW_NOISE_TYPES = [
    noise_type
    for noise_type in NOISE_TYPES
    if isinstance(noise_type, RowNoiseType) and noise_type.name != "duplicate_with_guardian"
]


def test_get_default_configuration(mocker):
    """Tests that the default configuration can be retrieved."""
    mock = mocker.patch("pseudopeople.configuration.generator.LayeredConfigTree")
    _ = get_configuration()
    mock.assert_called_once_with(layers=["baseline", "default", "user"])


def test_default_configuration_structure():
    """Test that the default configuration structure is correct"""
    config = get_configuration()
    # Check datasets
    assert set(f.name for f in DATASETS) == set(config.keys())
    for dataset in DATASETS:
        # Check row noise
        for row_noise in dataset.row_noise_types:
            config_probability = config[dataset.name][Keys.ROW_NOISE][row_noise.name]
            validate_noise_type_config(dataset, row_noise, config_probability)
        for col in dataset.columns:
            for noise_type in col.noise_types:
                config_level = config[dataset.name].column_noise[col.name][noise_type.name]
                validate_noise_type_config(dataset, noise_type, config_level, col)


def validate_noise_type_config(dataset, noise_type, config_level, column=None):
    # FIXME: Is there a way to allow for adding new keys when they
    #  don't exist in baseline? eg the for/if loops below depend on their
    #  being row_noise, token_noise, and additional parameters at the
    #  baseline level ('noise_type in col.noise_types')
    #  Would we ever want to allow for adding non-baseline default noise?
    noise_key = Keys.ROW_NOISE if isinstance(noise_type, RowNoiseType) else Keys.COLUMN_NOISE
    if noise_type.probability:
        config_probability = config_level[Keys.CELL_PROBABILITY]
        if isinstance(noise_type, RowNoiseType):
            default_probability = (
                DEFAULT_NOISE_VALUES.get(dataset.name, {})
                .get(noise_key, {})
                .get(noise_type.name, {})
                .get(noise_type.probability_key, "no default")
            )
        else:
            default_probability = (
                DEFAULT_NOISE_VALUES.get(dataset.name, {})
                .get(noise_key, {})
                .get(column.name, {})
                .get(noise_type.name, {})
                .get(noise_type.probability_key, "no default")
            )
        if default_probability == "no default":
            assert config_probability == noise_type.probability
        else:
            assert config_probability == default_probability
    if noise_type.additional_parameters:
        config_additional_parameters = {
            k: v for k, v in config_level.to_dict().items() if k != noise_type.probability_key
        }
        if isinstance(noise_type, RowNoiseType):
            default_additional_parameters = (
                DEFAULT_NOISE_VALUES.get(dataset.name, {})
                .get(noise_key, {})
                .get(noise_type.name, {})
            )
        else:
            default_additional_parameters = (
                DEFAULT_NOISE_VALUES.get(dataset.name, {})
                .get(noise_key, {})
                .get(column.name, {})
                .get(noise_type.name, {})
            )
        default_additional_parameters = {
            k: v
            for k, v in default_additional_parameters.items()
            if k != noise_type.probability_key
        }
        if default_additional_parameters == {}:
            assert config_additional_parameters == noise_type.additional_parameters
        else:
            # Confirm config includes default values
            for key, value in default_additional_parameters.items():
                assert config_additional_parameters[key] == value
            # Check that non-default values are baseline
            baseline_keys = [
                k
                for k in config_additional_parameters
                if k not in default_additional_parameters
            ]
            for key, value in config_additional_parameters.items():
                if key not in baseline_keys:
                    continue
                assert noise_type.additional_parameters[key] == value


def test_get_configuration_with_user_override(mocker):
    """Tests that the default configuration get updated when a user configuration is supplied."""
    mock = mocker.patch("pseudopeople.configuration.generator.LayeredConfigTree")
    config = {
        DATASETS.census.name: {
            Keys.ROW_NOISE: {NOISE_TYPES.omit_row.name: {Keys.ROW_PROBABILITY: 0.05}},
            Keys.COLUMN_NOISE: {
                "first_name": {NOISE_TYPES.make_typos.name: {Keys.CELL_PROBABILITY: 0.05}}
            },
        }
    }
    _ = get_configuration(config)
    mock.assert_called_once_with(layers=["baseline", "default", "user"])
    update_calls = [
        call
        for call in mock.mock_calls
        if ".update({" in str(call) and "layer='user'" in str(call)
    ]
    assert len(update_calls) == 1


def test_loading_from_yaml(tmp_path):
    overrides = {
        DATASETS.census.name: {
            Keys.COLUMN_NOISE: {
                COLUMNS.age.name: {
                    NOISE_TYPES.misreport_age.name: {
                        Keys.CELL_PROBABILITY: 0.5,
                    },
                },
            },
        },
    }
    filepath = tmp_path / "user_dict.yaml"
    with open(filepath, "w") as file:
        yaml.dump(overrides, file)

    default_config = get_configuration()[DATASETS.census.name][Keys.COLUMN_NOISE][
        COLUMNS.age.name
    ][NOISE_TYPES.misreport_age.name].to_dict()
    updated_config = get_configuration(filepath)[DATASETS.census.name][Keys.COLUMN_NOISE][
        COLUMNS.age.name
    ][NOISE_TYPES.misreport_age.name].to_dict()

    assert (
        default_config[Keys.POSSIBLE_AGE_DIFFERENCES]
        == updated_config[Keys.POSSIBLE_AGE_DIFFERENCES]
    )
    # check that 1 got replaced with 0 probability
    assert updated_config[Keys.CELL_PROBABILITY] == 0.5


@pytest.mark.parametrize(
    "age_differences, expected",
    [
        ([-2, -1, 2], {-2: 1 / 3, -1: 1 / 3, 1: 0, 2: 1 / 3}),
        ({-2: 0.3, 1: 0.5, 2: 0.2}, {-2: 0.3, -1: 0, 1: 0.5, 2: 0.2}),
    ],
    ids=["list", "dict"],
)
def test_format_miswrite_ages(age_differences, expected):
    """Test that user-supplied dictionary properly updates LayeredConfigTree object.
    This includes zero-ing out default values that don't exist in the user config
    """
    overrides = {
        DATASETS.census.name: {
            Keys.COLUMN_NOISE: {
                COLUMNS.age.name: {
                    NOISE_TYPES.misreport_age.name: {
                        Keys.POSSIBLE_AGE_DIFFERENCES: age_differences,
                    },
                },
            },
        },
    }

    config = get_configuration(overrides)[DATASETS.census.name][Keys.COLUMN_NOISE][
        COLUMNS.age.name
    ][NOISE_TYPES.misreport_age.name][Keys.POSSIBLE_AGE_DIFFERENCES].to_dict()

    assert config == expected


@pytest.mark.parametrize(
    "object_bad_type",
    [
        None,
        "foo",
        True,
        4,
        5.5,
    ],
)
def test_type_checking_all_levels(object_bad_type):
    # At the top level only:
    # - A string can be passed, in which case it is interpreted as a file path
    # - None can be passed, in which case the defaults will be used
    if not isinstance(object_bad_type, str) and object_bad_type is not None:
        with pytest.raises(ConfigurationError, match="Invalid configuration type"):
            get_configuration(object_bad_type)

    with pytest.raises(ConfigurationError, match="must be a Dict"):
        get_configuration({DATASETS.acs.name: object_bad_type})

    with pytest.raises(ConfigurationError, match="must be a Dict"):
        get_configuration({DATASETS.acs.name: {Keys.ROW_NOISE: object_bad_type}})

    with pytest.raises(ConfigurationError, match="must be a Dict"):
        get_configuration(
            {
                DATASETS.acs.name: {
                    Keys.ROW_NOISE: {NOISE_TYPES.do_not_respond.name: object_bad_type}
                }
            }
        )

    with pytest.raises(ConfigurationError, match="must be a Dict"):
        get_configuration({DATASETS.acs.name: {Keys.COLUMN_NOISE: object_bad_type}})

    with pytest.raises(ConfigurationError, match="must be a Dict"):
        get_configuration(
            {DATASETS.acs.name: {Keys.COLUMN_NOISE: {COLUMNS.age.name: object_bad_type}}}
        )

    with pytest.raises(ConfigurationError, match="must be a Dict"):
        get_configuration(
            {
                DATASETS.acs.name: {
                    Keys.COLUMN_NOISE: {
                        COLUMNS.age.name: {NOISE_TYPES.leave_blank.name: object_bad_type}
                    }
                }
            }
        )


@pytest.mark.parametrize(
    "config, match",
    [
        ({"fake_dataset": {}}, "Invalid dataset '.*' provided. Valid datasets are "),
        (
            {DATASETS.acs.name: {"other_noise": {}}},
            "Invalid configuration key '.*' provided for dataset '.*'. ",
        ),
        (
            {DATASETS.acs.name: {Keys.ROW_NOISE: {"fake_noise": {}}}},
            "Invalid noise type '.*' provided for dataset '.*'. ",
        ),
        (
            {
                DATASETS.acs.name: {
                    Keys.ROW_NOISE: {NOISE_TYPES.do_not_respond.name: {"fake": {}}}
                }
            },
            "Invalid parameter '.*' provided for dataset '.*' and noise type '.*'. ",
        ),
        (
            {DATASETS.acs.name: {Keys.COLUMN_NOISE: {"fake_column": {}}}},
            "Invalid column '.*' provided for dataset '.*'. ",
        ),
        (
            {DATASETS.acs.name: {Keys.COLUMN_NOISE: {COLUMNS.age.name: {"fake_noise": {}}}}},
            "Invalid noise type '.*' provided for dataset '.*' for column '.*'. ",
        ),
        (
            {
                DATASETS.acs.name: {
                    Keys.COLUMN_NOISE: {
                        COLUMNS.age.name: {NOISE_TYPES.leave_blank.name: {"fake": 1}}
                    }
                }
            },
            "Invalid parameter '.*' provided for dataset '.*' for column '.*' and noise type '.*'",
        ),
    ],
    ids=[
        "invalid dataset",
        "invalid noise type",
        "invalid row noise type",
        "Invalid row noise type parameter",
        "Invalid column",
        "Invalid column noise type",
        "Invalid column noise type parameter",
    ],
)
def test_overriding_nonexistent_keys_fails(config, match):
    with pytest.raises(ConfigurationError, match=match):
        get_configuration(config)


def get_noise_type_configs(noise_names: list):
    configs = list(itertools.product(noise_names, PROBABILITY_VALUE_LOGS))
    return [(x[0], x[1][0], x[1][1]) for x in configs]


@pytest.mark.parametrize(
    "row_noise_type, value, match",
    get_noise_type_configs(ROW_NOISE_TYPES),
)
def test_validate_standard_parameters_failures_row_noise(row_noise_type, value, match):
    """
    Tests valid configuration values for probability for row noise types.
    """
    dataset_name = [
        dataset for dataset in DATASETS if row_noise_type in dataset.row_noise_types
    ][0].name
    with pytest.raises(ConfigurationError, match=match):
        get_configuration(
            {
                dataset_name: {
                    Keys.ROW_NOISE: {
                        row_noise_type.name: {
                            Keys.ROW_PROBABILITY: value,
                        },
                    },
                },
            },
        )


@pytest.mark.parametrize(
    "column_noise_type, value, match",
    get_noise_type_configs(COLUMN_NOISE_TYPES),
)
def test_validate_standard_parameters_failures_column_noise(column_noise_type, value, match):
    """Test that a runtime error is thrown if a user provides bad standard
    probability values

    NOTE: This also includes cell_probability values and technically any
    other values not provided a unique validation function.
    """
    column_name = [
        column
        for column in COLUMNS
        if column_noise_type in column.noise_types and column in DATASETS.census.columns
    ][0].name
    with pytest.raises(ConfigurationError, match=match):
        get_configuration(
            {
                DATASETS.census.name: {
                    Keys.COLUMN_NOISE: {
                        column_name: {
                            column_noise_type.name: {
                                Keys.CELL_PROBABILITY: value,
                            },
                        },
                    },
                },
            },
        )


@pytest.mark.parametrize(
    "perturbations, match",
    [
        (-1, "must be a Dict or List"),
        ([], "empty"),
        ({}, "empty"),
        ([-1, 0.4, 1], "must be a List of ints"),
        ({-1: 0.5, 0.4: 0.2, 1: 0.3}, "must be a List of ints"),
        ([-1, 0, 1], "cannot include 0"),
        ({-1: 0.5, 4: 0.2, 0: 0.3}, "cannot include 0"),
        ({-1: 0.1, 1: 0.8}, "must sum to 1"),
        ({-1: 0.1, 1: "a"}, "must be floats or ints"),
        ({-1: -0.2, 1: 1.2}, "must be between 0 and 1"),
    ],
    ids=[
        "bad type",
        "empty list",
        "empty dict",
        "non-int keys list",
        "non-int keys dict",
        "include 0 list",
        "include 0 dict",
        "not sum to 1",
        "non-float values",
        "out of range",
    ],
)
def test_validate_miswrite_ages_failures(perturbations, match):
    """Test that a runtime error is thrown if the user provides bad possible_age_differences"""
    with pytest.raises(ConfigurationError, match=match):
        get_configuration(
            {
                DATASETS.census.name: {
                    Keys.COLUMN_NOISE: {
                        COLUMNS.age.name: {
                            NOISE_TYPES.misreport_age.name: {
                                Keys.CELL_PROBABILITY: 1,
                                Keys.POSSIBLE_AGE_DIFFERENCES: perturbations,
                            },
                        },
                    },
                },
            },
        )


@pytest.mark.parametrize(
    "probabilities, match",
    [
        (0.2, "must be a List"),
        ([0.5, 0.5, 0.5, 0.5], "must be a List of 5"),
        ([0.2, 0.2, "foo", 0.2, 0.2], "must be floats or ints"),
        ([-0.1, 0.2, 0.2, 0.2, 0.2], "must be between 0 and 1"),
        ([1.01, 0.2, 0.2, 0.2, 0.2], "must be between 0 and 1"),
    ],
)
def test_validate_miswrite_zipcode_digit_probabilities_failures(probabilities, match):
    """Test that a runtime error is thrown if the user provides bad zipcode_digit_probabilities"""
    with pytest.raises(ConfigurationError, match=match):
        get_configuration(
            {
                DATASETS.census.name: {
                    Keys.COLUMN_NOISE: {
                        COLUMNS.zipcode.name: {
                            NOISE_TYPES.write_wrong_zipcode_digits.name: {
                                Keys.CELL_PROBABILITY: 1,
                                Keys.ZIPCODE_DIGIT_PROBABILITIES: probabilities,
                            },
                        },
                    },
                },
            },
        )


def test_get_config(caplog):
    config_1 = get_config()
    assert isinstance(config_1, dict)
    assert not caplog.records

    with pytest.raises(FileNotFoundError, match="No such file or directory"):
        get_config("Bad_file_path")

    config_2 = get_config(overrides=NO_NOISE)
    for dataset in config_2.keys():
        row_noise_dict = config_2[dataset][Keys.ROW_NOISE]
        column_dict = config_2[dataset][Keys.COLUMN_NOISE]
        for row_noise in row_noise_dict:
            for key, value in row_noise_dict[row_noise].items():
                assert row_noise_dict[row_noise][key] == 0.0
        for column in column_dict:
            column_noise_dict = column_dict[column]
            for column_noise in column_noise_dict:
                assert column_noise_dict[column_noise][Keys.CELL_PROBABILITY] == 0.0


def test_validate_choose_wrong_option_configuration(caplog):
    """
    Tests that warning is thrown if cell probability is higher than possible given the
    number of options.
    """
    column_maximums = {
        "sex": 1 / 2,  # even if you noise all of the cells, only 1 / 2 will actually be wrong
        "state": 50 / 51,  # likewise, but with many more categories (51)
    }
    config_values = [0.1, 0.4, 0.5, 0.6, 1]
    for column, maximum in column_maximums.items():
        caplog.clear()
        for config_value in config_values:
            get_configuration(
                {
                    DATASETS.census.name: {
                        Keys.COLUMN_NOISE: {
                            column: {
                                NOISE_TYPES.choose_wrong_option.name: {
                                    Keys.CELL_PROBABILITY: config_value,
                                },
                            },
                        },
                    },
                },
            )
            if config_value <= maximum:
                assert not caplog.records
            else:
                assert (
                    "This maximum will be used instead of the configured value" in caplog.text
                )


def test_no_noise():
    # Tests that passing the sentinal no noise value results in a configuration
    # where all noise levels are 0.0
    no_noise_config = get_configuration("no_noise")

    for dataset in no_noise_config.keys():
        dataset_dict = no_noise_config[dataset]
        dataset_row_noise_dict = dataset_dict[Keys.ROW_NOISE]
        dataset_column_dict = dataset_dict[Keys.COLUMN_NOISE]
        for row_noise_type in dataset_row_noise_dict.keys():
            for key, value in dataset_row_noise_dict[row_noise_type].items():
                assert dataset_row_noise_dict[row_noise_type][key] == 0.0
        for column in dataset_column_dict.keys():
            column_noise_dict = dataset_column_dict[column]
            for column_noise_type in column_noise_dict.keys():
                assert column_noise_dict[column_noise_type][Keys.CELL_PROBABILITY] == 0.0


@pytest.mark.parametrize(
    "column, noise_type, noise_level",
    [
        ("age", "copy_from_household_member", 0.2),
        ("age", "copy_from_household_member", 0.95),
        ("first_name", "use_nickname", 0.05),
        ("first_name", "use_nickname", 0.85),
        ("date_of_birth", "copy_from_household_member", 0.15),
        ("date_of_birth", "copy_from_household_member", 0.90),
    ],
)
def test_validate_noise_level_proportions(caplog, column, noise_type, noise_level):
    """
    Tests that a warning is thrown when a user provides configuration overrides that are higher
    than the calculated metadata proportions for that column noise type pairing.
    """
    census = DATASETS.get_dataset("decennial_census")
    user_filters = [
        (census.date_column_name, "==", 2020),
        (census.state_column_name, "==", "WA"),
    ]
    # Making guardian duplication 0.0 so that we can test the other noise types only
    get_configuration(
        {
            DATASETS.census.name: {
                Keys.COLUMN_NOISE: {
                    column: {
                        noise_type: {
                            Keys.CELL_PROBABILITY: noise_level,
                        },
                    },
                },
            },
        },
        census,
        user_filters,
    )
    if noise_level < 0.5:
        assert not caplog.records
    else:
        assert "Noising as many rows as possible" in caplog.text


@pytest.mark.parametrize(
    "value_1, value_2",
    [
        (0.0, 0.1),
        (0.2, 0.5),
        (0.5, 0.8),
    ],
)
def test_duplicate_with_guardian_configuration(value_1, value_2):
    """
    Tests config is set correctly for each group in guardian duplication.
    """

    config = get_config(
        {
            DATASETS.census.name: {
                Keys.ROW_NOISE: {
                    NOISE_TYPES.duplicate_with_guardian.name: {
                        Keys.ROW_PROBABILITY_IN_HOUSEHOLDS_UNDER_18: value_1,
                        Keys.ROW_PROBABILITY_IN_COLLEGE_GROUP_QUARTERS_UNDER_24: value_2,
                    },
                },
            },
        },
    )

    row_noise_dict = config[DATASETS.census.name][Keys.ROW_NOISE][
        NOISE_TYPES.duplicate_with_guardian.name
    ]
    assert row_noise_dict[Keys.ROW_PROBABILITY_IN_HOUSEHOLDS_UNDER_18] == value_1
    assert row_noise_dict[Keys.ROW_PROBABILITY_IN_COLLEGE_GROUP_QUARTERS_UNDER_24] == value_2


@pytest.mark.parametrize(
    "key",
    [
        (Keys.ROW_PROBABILITY),
        ("over_24_in_group_quarters"),
    ],
)
def test_bad_duplicate_with_guardian_config(key):
    # Tests error is thrown for keys that are not a valid configuration for duplicate with guardian
    with pytest.raises(ConfigurationError, match=f"Invalid parameter '{key}' provided"):
        get_configuration(
            {
                DATASETS.census.name: {
                    Keys.ROW_NOISE: {
                        NOISE_TYPES.duplicate_with_guardian.name: {
                            key: 0.5,
                        },
                    },
                },
            },
        )
