"""Tests for params_to_sim module."""

from unittest.mock import Mock

from monaco_dict_utils.params_to_sim import (
    _key,
    case_vals_to_dict,
    output_to_case,
    outvals_to_dict,
    params_to_model,
    params_to_sim,
)


class TestKeyNormalization:
    """Test the _key function for normalizing parameter names."""

    def test_simple_key(self):
        assert _key("simple") == "simple"

    def test_uppercase_key(self):
        assert _key("UPPERCASE") == "uppercase"

    def test_spaces_replaced(self):
        assert _key("with spaces") == "with_spaces"

    def test_special_chars_removed(self):
        assert _key("with-special@chars!") == "withspecialchars"

    def test_mixed_formatting(self):
        assert _key("Mixed Case-With@Spaces!") == "mixed_casewithspaces"

    def test_leading_trailing_spaces(self):
        assert _key("  leading trailing  ") == "leading_trailing"


class TestParamsToSim:
    """Test the params_to_sim function."""

    def test_distribution_params(self):
        mock_sim = Mock()
        mock_param = Mock()
        mock_param.value = 0.5

        invars = {
            "x": {
                "dist": "uniform",
                "params": {"loc": mock_param, "scale": mock_param},
            },
        }

        result = params_to_sim(mock_sim, invars)

        mock_sim.addInVar.assert_called_once_with(
            name="x",
            dist="uniform",
            distkwargs={"loc": 0.5, "scale": 0.5},
        )
        assert result == mock_sim

    def test_constant_with_dict_params(self):
        mock_sim = Mock()
        mock_param = Mock()
        mock_param.value = 10

        invars = {
            "y": {
                "dist": "_constant",
                "params": {"param1": mock_param, "param2": mock_param},
            },
        }

        params_to_sim(mock_sim, invars)

        assert mock_sim.addConstVal.call_count == 2
        mock_sim.addConstVal.assert_any_call(name="param1", val=10)
        mock_sim.addConstVal.assert_any_call(name="param2", val=10)

    def test_constant_with_value_object(self):
        mock_sim = Mock()
        mock_param = Mock()
        mock_param.value = 42
        # Mock items to return False for hasattr check
        del mock_param.items

        invars = {
            "z": {
                "dist": "_constant",
                "params": mock_param,
            },
        }

        params_to_sim(mock_sim, invars)

        mock_sim.addConstVal.assert_called_once_with(name="z", val=42)

    def test_constant_with_plain_value(self):
        mock_sim = Mock()

        invars = {
            "w": {
                "dist": "_constant",
                "params": 100,
            },
        }

        params_to_sim(mock_sim, invars)

        mock_sim.addConstVal.assert_called_once_with(name="w", val=100)

    def test_mixed_params(self):
        mock_sim = Mock()
        mock_param = Mock()
        mock_param.value = 1.0

        invars = {
            "dist_var": {
                "dist": "normal",
                "params": {"loc": mock_param, "scale": mock_param},
            },
            "const_var": {
                "dist": "_constant",
                "params": 5,
            },
        }

        params_to_sim(mock_sim, invars)

        mock_sim.addInVar.assert_called_once_with(
            name="dist_var",
            dist="normal",
            distkwargs={"loc": 1.0, "scale": 1.0},
        )
        mock_sim.addConstVal.assert_called_once_with(name="const_var", val=5)


class TestCaseValsToDict:
    """Test the case_vals_to_dict function."""

    def test_case_vals_to_dict(self):
        mock_case = Mock()

        # Mock invals
        mock_inval = Mock()
        mock_inval.val = 10
        mock_case.invals = {"Input Value": mock_inval}

        # Mock constvals
        mock_case.constvals = {"Const Value": 20}

        result = case_vals_to_dict(mock_case)

        expected = ({"input_value": 10, "const_value": 20},)
        assert result == expected

    def test_empty_case(self):
        mock_case = Mock()
        mock_case.invals = {}
        mock_case.constvals = {}

        result = case_vals_to_dict(mock_case)

        assert result == ({},)

    def test_special_chars_in_keys(self):
        mock_case = Mock()

        mock_inval = Mock()
        mock_inval.val = 5
        mock_case.invals = {"Input-Value@Special!": mock_inval}
        mock_case.constvals = {"Const#Value$": 15}

        result = case_vals_to_dict(mock_case)

        expected = ({"inputvaluespecial": 5, "constvalue": 15},)
        assert result == expected


class TestOutputToCase:
    """Test the output_to_case function."""

    def test_output_to_case(self):
        mock_case = Mock()
        output = {"time_savings": 100, "cost_reduction": 50}

        output_to_case(mock_case, output)

        mock_case.addOutVal.assert_any_call(name="Time_Savings", val=100)
        mock_case.addOutVal.assert_any_call(name="Cost_Reduction", val=50)
        assert mock_case.addOutVal.call_count == 2

    def test_single_word_output(self):
        mock_case = Mock()
        output = {"profit": 1000}

        output_to_case(mock_case, output)

        mock_case.addOutVal.assert_called_once_with(name="Profit", val=1000)

    def test_multiple_underscores(self):
        mock_case = Mock()
        output = {"net_present_value": 2000}

        output_to_case(mock_case, output)

        mock_case.addOutVal.assert_called_once_with(name="Net_Present_Value", val=2000)

    def test_empty_output(self):
        mock_case = Mock()
        output = {}

        output_to_case(mock_case, output)

        mock_case.addOutVal.assert_not_called()


class TestParamsToModel:
    """Test the params_to_model function."""

    def test_params_to_model_with_dict_values(self):
        mock_factory = Mock(return_value=lambda x: x * 2)
        mock_param = Mock()
        mock_param.value = 10

        factory_vars = {"Parameter Name": {"params": mock_param}}

        result = params_to_model(mock_factory, factory_vars)

        mock_factory.assert_called_once_with(parameter_name=10)
        assert result == mock_factory.return_value

    def test_params_to_model_with_plain_values(self):
        mock_factory = Mock(return_value=lambda x: x * 3)

        factory_vars = {"Simple Param": 20}

        result = params_to_model(mock_factory, factory_vars)

        mock_factory.assert_called_once_with(simple_param=20)
        assert result == mock_factory.return_value

    def test_params_to_model_mixed_values(self):
        mock_factory = Mock(return_value=lambda x: x)
        mock_param = Mock()
        mock_param.value = 5

        factory_vars = {
            "Dict Param": {"params": mock_param},
            "Plain Param": 15,
        }

        result = params_to_model(mock_factory, factory_vars)

        mock_factory.assert_called_once_with(dict_param=5, plain_param=15)
        assert result == mock_factory.return_value

    def test_key_normalization(self):
        mock_factory = Mock(return_value=lambda: None)

        factory_vars = {"Complex-Key@Name!": 100}

        params_to_model(mock_factory, factory_vars)

        mock_factory.assert_called_once_with(complexkeyname=100)


class TestOutvalsToDict:
    """Test the outvals_to_dict function."""

    def test_outvals_to_dict(self):
        mock_sim = Mock()

        mock_outvar1 = Mock()
        mock_outvar1.nums = [1, 2, 3]
        mock_outvar2 = Mock()
        mock_outvar2.nums = [4, 5, 6]

        mock_sim.outvars = {"var1": mock_outvar1, "var2": mock_outvar2}

        result = outvals_to_dict(mock_sim)

        expected = {"var1": [1, 2, 3], "var2": [4, 5, 6]}
        assert result == expected

    def test_empty_outvars(self):
        mock_sim = Mock()
        mock_sim.outvars = {}

        result = outvals_to_dict(mock_sim)

        assert result == {}

    def test_single_outvar(self):
        mock_sim = Mock()

        mock_outvar = Mock()
        mock_outvar.nums = [10, 20, 30]
        mock_sim.outvars = {"single_var": mock_outvar}

        result = outvals_to_dict(mock_sim)

        expected = {"single_var": [10, 20, 30]}
        assert result == expected
