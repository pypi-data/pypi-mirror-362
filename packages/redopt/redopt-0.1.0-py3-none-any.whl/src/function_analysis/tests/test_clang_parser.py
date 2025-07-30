"""
Tests for Clang parser.
"""

import pytest

from ..core.clang_parser import ClangParser


class TestClangParser:
    """Test cases for ClangParser."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = ClangParser()

    def test_parse_simple_function(self):
        """Test parsing a simple C function."""
        code = """
int add(int a, int b) {
    return a + b;
}
"""
        result = self.parser.parse_function(code)

        assert result is not None
        assert "metadata" in result
        assert "ast" in result

        metadata = result["metadata"]
        assert metadata.name == "add"
        assert metadata.return_type == "int"
        assert len(metadata.parameters) == 2
        assert metadata.parameters[0]["name"] == "a"
        assert metadata.parameters[0]["type"] == "int"
        assert metadata.parameters[1]["name"] == "b"
        assert metadata.parameters[1]["type"] == "int"

    def test_parse_void_function(self):
        """Test parsing a void function."""
        code = """
void print_hello(void) {
    printf("Hello, World!\\n");
}
"""
        result = self.parser.parse_function(code)

        metadata = result["metadata"]
        assert metadata.name == "print_hello"
        assert metadata.return_type == "void"
        assert len(metadata.parameters) == 0

    def test_parse_complex_function(self):
        """Test parsing a more complex function."""
        code = """
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}
"""
        result = self.parser.parse_function(code)

        metadata = result["metadata"]
        assert metadata.name == "factorial"
        assert metadata.return_type == "int"
        assert len(metadata.parameters) == 1

        # Check complexity calculation
        complexity = self.parser.calculate_complexity(result["ast"])
        assert complexity > 1  # Should have some complexity due to if statement

    def test_parse_function_with_structs(self):
        """Test parsing a function with struct parameters."""
        code = """
typedef struct {
    int x, y;
} Point;

int distance_squared(Point p1, Point p2) {
    int dx = p1.x - p2.x;
    int dy = p1.y - p2.y;
    return dx * dx + dy * dy;
}
"""
        result = self.parser.parse_function(code, "distance_squared")

        metadata = result["metadata"]
        assert metadata.name == "distance_squared"
        assert metadata.return_type == "int"
        assert len(metadata.parameters) == 2

    def test_invalid_code(self):
        """Test handling of invalid code."""
        code = "this is not valid C code"

        with pytest.raises(ValueError):
            self.parser.parse_function(code)

    def test_complexity_calculation(self):
        """Test complexity calculation for different constructs."""
        # Simple function (complexity = 1)
        simple_code = """
int simple(int x) {
    return x * 2;
}
"""
        result = self.parser.parse_function(simple_code)
        complexity = self.parser.calculate_complexity(result["ast"])
        assert complexity == 1.0

        # Function with if statement (complexity = 2)
        if_code = """
int with_if(int x) {
    if (x > 0) {
        return x;
    }
    return 0;
}
"""
        result = self.parser.parse_function(if_code)
        complexity = self.parser.calculate_complexity(result["ast"])
        assert complexity >= 2.0

        # Function with loop (complexity >= 2)
        loop_code = """
int with_loop(int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += i;
    }
    return sum;
}
"""
        result = self.parser.parse_function(loop_code)
        complexity = self.parser.calculate_complexity(result["ast"])
        assert complexity >= 2.0
