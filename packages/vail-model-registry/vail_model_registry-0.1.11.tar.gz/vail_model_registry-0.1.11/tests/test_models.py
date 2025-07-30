"""
Test module for the models module.
"""

import traceback
from datetime import datetime, timedelta

import pytest

from vail.registry import Model as RegistryModel
from vail.registry.models import ModelFilterCriteria
from vail.utils.env import load_env

# Load test environment variables
load_env("test")


@pytest.fixture
def valid_huggingface_source():
    return {
        "source_type": "huggingface_api",
        "requires_auth": False,
        "source_identifier": '{"loader_class": "AutoModelForCausalLM", "checkpoint": "deepcogito/cogito-v1-preview-llama-3B"}',
    }


@pytest.fixture
def valid_onnx_source():
    return {
        "source_type": "onnx_file",
        "source_identifier": {"file_path": "path/to/model.onnx"},
        "requires_auth": False,
    }


@pytest.fixture
def invalid_source():
    return {
        "source_type": "invalid_type",
        "source_identifier": {},
        "requires_auth": False,
    }


def test_validate_source_huggingface(valid_huggingface_source):
    """Test validate_source with a valid Hugging Face source"""
    try:
        assert RegistryModel.validate_source(valid_huggingface_source) is True
    except Exception:
        print("\nError in test_validate_source_huggingface:")
        print(traceback.format_exc())
        raise


def test_validate_source_onnx(valid_onnx_source):
    """Test validate_source with a valid ONNX source"""
    try:
        assert RegistryModel.validate_source(valid_onnx_source) is True
    except Exception:
        print("\nError in test_validate_source_onnx:")
        print(traceback.format_exc())
        raise


def test_validate_source_invalid(invalid_source):
    """Test validate_source with an invalid source type"""
    try:
        assert RegistryModel.validate_source(invalid_source) is False
    except Exception:
        print("\nError in test_validate_source_invalid:")
        print(traceback.format_exc())
        raise


def test_validate_source_missing_required_fields():
    """Test validate_source with missing required fields"""
    try:
        invalid_source = {
            "source_type": "huggingface_api",
            "source_identifier": {},  # Missing required fields
        }
        assert RegistryModel.validate_source(invalid_source) is False
    except Exception:
        print("\nError in test_validate_source_missing_required_fields:")
        print(traceback.format_exc())
        raise


def test_validate_source_missing_source_type():
    """Test validate_source with missing source_type"""
    try:
        invalid_source = {
            "source_identifier": {
                "loader_class": "AutoModelForCausalLM",
                "checkpoint": "mistralai/Mistral-7B-v0.1",
            }
        }
        assert RegistryModel.validate_source(invalid_source) is False
    except Exception:
        print("\nError in test_validate_source_missing_source_type:")
        print(traceback.format_exc())
        raise


def test_validate_source_missing_source_identifier():
    """Test validate_source with missing source_identifier"""
    try:
        invalid_source = {"source_type": "huggingface_api"}
        assert RegistryModel.validate_source(invalid_source) is False
    except Exception:
        print("\nError in test_validate_source_missing_source_identifier:")
        print(traceback.format_exc())
        raise


def test_validate_source_with_auth_required():
    """Test validate_source with authentication required"""
    try:
        source_with_auth = {
            "source_type": "huggingface_api",
            "source_identifier": {
                "loader_class": "AutoModelForCausalLM",
                "checkpoint": "microsoft/Phi-3-mini-4k-instruct",
            },
            "requires_auth": True,
        }

        assert RegistryModel.validate_source(source_with_auth) is True
    except Exception:
        print("\nError in test_validate_source_with_auth_required:")
        print(traceback.format_exc())
        raise


def test_model_filter_criteria():
    """Test ModelFilterCriteria dataclass"""
    criteria = ModelFilterCriteria(
        maker="Mistral",
        params_count_eq=1000000,
        quantization="8-bit",
        updated_since=datetime.now() - timedelta(days=1),
    )

    assert criteria.maker == "Mistral"
    assert criteria.params_count_eq == 1000000


def test_model_filter_criteria_to_sql_filters():
    """Test ModelFilterCriteria to_sql_filters method for different styles and aliases."""
    now = datetime.now()
    criteria_full = ModelFilterCriteria(
        maker="Mistral",
        params_count_eq=1000000,
        params_count_gt=500000,
        params_count_lte=2000000,
        quantization="8-bit",
        updated_since=now,
    )

    # Test case 1: DuckDB style ('?') without alias
    where_clause, params = criteria_full.to_sql_filters(placeholder_style="?")
    expected_where_duckdb = (
        "model_maker = ? AND "
        "params_count = ? AND params_count > ? AND params_count <= ? AND "
        "quantization = ? AND last_updated >= ?"
    )
    assert where_clause == expected_where_duckdb
    assert params == ["Mistral", 1000000, 500000, 2000000, "8-bit", now]

    # Test case 2: PostgreSQL style ('%s') without alias
    where_clause, params = criteria_full.to_sql_filters(placeholder_style="%s")
    expected_where_postgres = (
        "model_maker = %s AND "
        "params_count = %s AND params_count > %s AND params_count <= %s AND "
        "quantization = %s AND last_updated >= %s"
    )
    assert where_clause == expected_where_postgres
    assert params == ["Mistral", 1000000, 500000, 2000000, "8-bit", now]

    # Test case 3: DuckDB style ('?') with alias 'm'
    where_clause, params = criteria_full.to_sql_filters(
        table_alias="m", placeholder_style="?"
    )
    expected_where_duckdb_alias = (
        "m.model_maker = ? AND "
        "m.params_count = ? AND m.params_count > ? AND m.params_count <= ? AND "
        "m.quantization = ? AND m.last_updated >= ?"
    )
    assert where_clause == expected_where_duckdb_alias
    assert params == ["Mistral", 1000000, 500000, 2000000, "8-bit", now]

    # Test case 4: PostgreSQL style ('%s') with alias 'm'
    where_clause, params = criteria_full.to_sql_filters(
        table_alias="m", placeholder_style="%s"
    )
    expected_where_postgres_alias = (
        "m.model_maker = %s AND "
        "m.params_count = %s AND m.params_count > %s AND m.params_count <= %s AND "
        "m.quantization = %s AND m.last_updated >= %s"
    )
    assert where_clause == expected_where_postgres_alias
    assert params == ["Mistral", 1000000, 500000, 2000000, "8-bit", now]

    # Test case 5: No filters set
    criteria_empty = ModelFilterCriteria()
    where_clause, params = criteria_empty.to_sql_filters()
    assert where_clause == "1=1"
    assert params == []

    # Test case 6: Single filter (maker)
    criteria_single = ModelFilterCriteria(maker="TestMaker")
    where_clause, params = criteria_single.to_sql_filters(
        table_alias="x", placeholder_style="%s"
    )
    assert where_clause == "x.model_maker = %s"
    assert params == ["TestMaker"]

    # Test case 7: Single filter (params_count_eq), default placeholder
    criteria_single_params = ModelFilterCriteria(params_count_eq=500)
    where_clause, params = criteria_single_params.to_sql_filters()
    assert where_clause == "params_count = ?"
    assert params == [500]

    # Test case 8: Single filter (params_count_gt)
    criteria_gt = ModelFilterCriteria(params_count_gt=1000)
    where_clause, params = criteria_gt.to_sql_filters(
        table_alias="t", placeholder_style="%s"
    )
    assert where_clause == "t.params_count > %s"
    assert params == [1000]

    # Test case 9: Single filter (params_count_lte)
    criteria_lte = ModelFilterCriteria(params_count_lte=2000)
    where_clause, params = criteria_lte.to_sql_filters(placeholder_style="?")
    assert where_clause == "params_count <= ?"
    assert params == [2000]


# ===== CANONICAL ID TESTS =====


def test_generate_canonical_id_standalone():
    """Test the standalone generate_canonical_id function."""
    from vail.registry.models import generate_canonical_id

    # Test normal cases
    assert (
        generate_canonical_id("microsoft/phi-3-mini", 42) == "microsoft/phi-3-mini_42"
    )
    assert (
        generate_canonical_id("meta-llama/Llama-3.1-8B", 789)
        == "meta-llama/Llama-3.1-8B_789"
    )

    # Test with float global_id (should convert to int then string)
    assert (
        generate_canonical_id("bigcode/starcoderbase-1b", 161.0)
        == "bigcode/starcoderbase-1b_161"
    )

    # Test with string global_id (should work as-is)
    assert (
        generate_canonical_id("microsoft/DialoGPT-large", "123")
        == "microsoft/DialoGPT-large_123"
    )

    # Test works with model name that already has an underscore
    assert (
        generate_canonical_id("EleutherAI/pythia-1.4b_deduped", 143)
        == "EleutherAI/pythia-1.4b_deduped_143"
    )


def test_parse_canonical_id_standalone():
    """Test the standalone parse_canonical_id function."""
    from vail.registry.models import parse_canonical_id

    # Test normal cases
    model_name, global_id = parse_canonical_id("microsoft/phi-3-mini_42")
    assert model_name == "microsoft/phi-3-mini"
    assert global_id == 42

    model_name, global_id = parse_canonical_id("meta-llama/Llama-3.1-8B_789")
    assert model_name == "meta-llama/Llama-3.1-8B"
    assert global_id == 789

    # Test with hyphenated model names
    model_name, global_id = parse_canonical_id("bigcode/starcoderbase-1b_161")
    assert model_name == "bigcode/starcoderbase-1b"
    assert global_id == 161

    # Test with complex model names containing underscores
    model_name, global_id = parse_canonical_id("EleutherAI/pythia-1.4b_deduped_143")
    assert model_name == "EleutherAI/pythia-1.4b_deduped"
    assert global_id == 143


def test_parse_canonical_id_edge_cases():
    """Test parse_canonical_id with edge cases and error handling."""
    from vail.registry.models import parse_canonical_id

    # Test invalid formats (should raise ValueError)
    with pytest.raises(ValueError, match="Invalid canonical_id format"):
        parse_canonical_id("invalid-format")

    with pytest.raises(ValueError, match="Invalid global_registry_id"):
        parse_canonical_id("no_underscore_at_end")

    with pytest.raises(ValueError, match="Invalid global_registry_id"):
        parse_canonical_id("ends_with_underscore_")

    with pytest.raises(ValueError, match="Invalid global_registry_id"):
        parse_canonical_id("multiple_underscores_but_no_number_at_end_abc")

    # Test non-numeric global ID (should raise ValueError)
    with pytest.raises(ValueError, match="Invalid global_registry_id"):
        parse_canonical_id("model/name_not_a_number")


def test_model_get_canonical_id():
    """Test the Model instance method for getting canonical ID."""
    # Create a model instance with canonical_id in model_info (correct constructor signature)
    model_info = {
        "id": 1,
        "model_name": "microsoft/phi-3-mini",
        "canonical_id": "microsoft/phi-3-mini_42",
        "model_maker": "microsoft",
        "params_count": 3800000000,
        "sources": [
            {
                "source_type": "huggingface_api",
                "source_identifier": {
                    "loader_class": "AutoModelForCausalLM",
                    "checkpoint": "microsoft/phi-3-mini",
                },
                "requires_auth": False,
            }
        ],
    }

    model = RegistryModel(name="microsoft/phi-3-mini", model_info=model_info)
    assert model.get_canonical_id() == "microsoft/phi-3-mini_42"


def test_model_get_canonical_id_not_available():
    """Test Model.get_canonical_id() when canonical_id is not available."""
    # Create a model instance without canonical_id (correct constructor signature)
    model_info = {
        "id": 1,
        "model_name": "test/model",
        "model_maker": "test",
        "params_count": 1000000,
        "sources": [
            {
                "source_type": "huggingface_api",
                "source_identifier": {
                    "loader_class": "AutoModelForCausalLM",
                    "checkpoint": "test/model",
                },
                "requires_auth": False,
            }
        ],
    }

    model = RegistryModel(name="test/model", model_info=model_info)
    assert model.get_canonical_id() is None


def test_canonical_id_roundtrip():
    """Test that generating and parsing canonical IDs is consistent."""
    from vail.registry.models import generate_canonical_id, parse_canonical_id

    test_cases = [
        ("microsoft/phi-3-mini", 42),
        ("meta-llama/Llama-3.1-8B", 789),
        ("bigcode/starcoderbase-1b", 161),
        ("EleutherAI/pythia-1.4b_deduped", 143),
        ("company/model_with_many_underscores_in_name", 999),
    ]

    for original_name, original_id in test_cases:
        # Generate canonical ID
        canonical_id = generate_canonical_id(original_name, original_id)

        # Parse it back
        parsed_name, parsed_id = parse_canonical_id(canonical_id)

        # Should match original
        assert parsed_name == original_name
        assert parsed_id == original_id
