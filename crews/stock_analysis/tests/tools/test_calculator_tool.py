"""
Comprehensive tests for CalculatorTool.

This test suite covers:
- Tool metadata (name, description)
- Basic arithmetic operations
- Complex expressions
- Order of operations
- Unary operators
- Error handling with message validation
- Edge cases
"""

import pytest
from src.stock_analysis.tools.calculator_tool import CalculatorTool


class TestCalculatorToolMetadata:
    """Test tool metadata attributes."""

    @pytest.fixture
    def calculator(self):
        return CalculatorTool()

    def test_tool_name(self, calculator):
        """Verify tool has correct name."""
        assert calculator.name == "Calculator tool"

    def test_tool_description_exists(self, calculator):
        """Verify tool has a description."""
        assert calculator.description
        assert isinstance(calculator.description, str)
        assert len(calculator.description) > 0

    def test_tool_description_content(self, calculator):
        """Verify tool description contains expected content and starts correctly."""
        description = calculator.description
        # Check for key phrases from the actual description
        assert "mathematical calculations" in description.lower()
        assert "200*7" in description  # Example from description
        assert "5000/2*10" in description  # Example from description
        # Verify it contains "Useful" and starts properly (not "XXUseful")
        assert "Useful to perform" in description, f"Description should contain 'Useful to perform' but got: {description[:100]}"
        # Verify no XX prefix/suffix was added
        assert not description.startswith("XX"), "Description should not start with XX"
        assert "XXUseful" not in description, "Description should not contain XXUseful"


class TestCalculatorBasicOperations:
    """Test basic arithmetic operations."""

    @pytest.fixture
    def calculator(self):
        return CalculatorTool()

    def test_addition(self, calculator):
        assert calculator._run("5 + 3") == 8
        assert calculator._run("100 + 200") == 300
        assert calculator._run("0 + 0") == 0

    def test_subtraction(self, calculator):
        assert calculator._run("10 - 3") == 7
        assert calculator._run("100 - 200") == -100
        assert calculator._run("0 - 0") == 0

    def test_multiplication(self, calculator):
        assert calculator._run("5 * 3") == 15
        assert calculator._run("200 * 7") == 1400
        assert calculator._run("0 * 100") == 0

    def test_division(self, calculator):
        assert calculator._run("10 / 2") == 5
        assert calculator._run("5000 / 2") == 2500
        assert calculator._run("7 / 2") == 3.5

    def test_power(self, calculator):
        assert calculator._run("2 ** 3") == 8
        assert calculator._run("10 ** 2") == 100
        assert calculator._run("5 ** 0") == 1

    def test_modulo(self, calculator):
        assert calculator._run("10 % 3") == 1
        assert calculator._run("100 % 7") == 2
        assert calculator._run("8 % 2") == 0


class TestCalculatorComplexExpressions:
    """Test complex mathematical expressions."""

    @pytest.fixture
    def calculator(self):
        return CalculatorTool()

    def test_order_of_operations(self, calculator):
        # Multiplication before addition
        assert calculator._run("2 + 3 * 4") == 14
        # Division before subtraction
        assert calculator._run("10 - 8 / 2") == 6
        # Power before multiplication
        assert calculator._run("2 * 3 ** 2") == 18

    def test_parentheses(self, calculator):
        assert calculator._run("(2 + 3) * 4") == 20
        assert calculator._run("10 - (8 / 2)") == 6
        assert calculator._run("((5 + 3) * 2) / 4") == 4

    def test_nested_parentheses(self, calculator):
        assert calculator._run("((2 + 3) * (4 + 1))") == 25
        assert calculator._run("(10 - (3 + 2)) * 2") == 10

    def test_mixed_operations(self, calculator):
        assert calculator._run("5000 / 2 * 10") == 25000
        assert calculator._run("100 + 50 - 25 * 2") == 100
        assert calculator._run("(100 + 200) / 3") == 100


class TestCalculatorUnaryOperators:
    """Test unary operators (negative/positive)."""

    @pytest.fixture
    def calculator(self):
        return CalculatorTool()

    def test_negative_numbers(self, calculator):
        assert calculator._run("-5") == -5
        assert calculator._run("-10 + 5") == -5
        assert calculator._run("10 + -5") == 5

    def test_positive_numbers(self, calculator):
        assert calculator._run("+5") == 5
        assert calculator._run("+10 - 3") == 7

    def test_double_negative(self, calculator):
        assert calculator._run("--5") == 5
        assert calculator._run("10 - -5") == 15


class TestCalculatorErrorHandling:
    """Test error handling for invalid inputs."""

    @pytest.fixture
    def calculator(self):
        return CalculatorTool()

    def test_division_by_zero(self, calculator):
        with pytest.raises(ValueError, match="Calculation error"):
            calculator._run("10 / 0")

    def test_invalid_characters_letters(self, calculator):
        with pytest.raises(ValueError, match="Calculation error: Invalid characters in mathematical expression"):
            calculator._run("5 + abc")

    def test_invalid_characters_function_call(self, calculator):
        # Test that function calls are rejected (security test)
        with pytest.raises(ValueError, match="Calculation error: Invalid characters in mathematical expression"):
            calculator._run("print(5)")

    def test_invalid_characters_import(self, calculator):
        with pytest.raises(ValueError, match="Calculation error: Invalid characters in mathematical expression"):
            calculator._run("import os")

    def test_invalid_syntax_incomplete(self, calculator):
        with pytest.raises(ValueError, match="^Calculation error:"):
            calculator._run("5 +")
        with pytest.raises(ValueError, match="^Calculation error:"):
            calculator._run("* 5")

    def test_invalid_syntax_unmatched_parentheses(self, calculator):
        with pytest.raises(ValueError, match="^Calculation error:"):
            calculator._run("(5 + 3")

    def test_empty_expression(self, calculator):
        with pytest.raises(ValueError, match="Calculation error:"):
            calculator._run("")

    def test_only_whitespace(self, calculator):
        with pytest.raises(ValueError, match="Calculation error:"):
            calculator._run("   ")


class TestCalculatorEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.fixture
    def calculator(self):
        return CalculatorTool()

    def test_zero_operations(self, calculator):
        assert calculator._run("0 + 0") == 0
        assert calculator._run("0 * 100") == 0
        assert calculator._run("0 / 1") == 0

    def test_single_number(self, calculator):
        assert calculator._run("42") == 42
        assert calculator._run("0") == 0

    def test_decimal_results(self, calculator):
        result = calculator._run("7 / 2")
        assert result == 3.5
        result = calculator._run("1 / 3")
        assert abs(result - 0.3333333333333333) < 1e-10

    def test_large_numbers(self, calculator):
        assert calculator._run("1000000 * 1000000") == 1000000000000
        assert calculator._run("999999 + 1") == 1000000

    def test_whitespace_handling(self, calculator):
        assert calculator._run("5+3") == 8
        assert calculator._run("5 + 3") == 8
        # Leading/trailing whitespace causes issues with ast.parse
        # This is a known limitation
        with pytest.raises(ValueError):
            calculator._run("  5  +  3  ")


class TestCalculatorRealWorldExamples:
    """Test examples from the tool's description."""

    @pytest.fixture
    def calculator(self):
        return CalculatorTool()

    def test_documented_examples(self, calculator):
        # Examples from the tool's description
        assert calculator._run("200*7") == 1400
        assert calculator._run("5000/2*10") == 25000

    def test_financial_calculations(self, calculator):
        # Common financial calculations
        # Simple interest: Principal * Rate
        assert calculator._run("10000 * 0.05") == 500
        # Percentage: (part / total) * 100
        assert calculator._run("(250 / 1000) * 100") == 25
        # Growth rate: ((new - old) / old) * 100
        assert calculator._run("((150 - 100) / 100) * 100") == 50
