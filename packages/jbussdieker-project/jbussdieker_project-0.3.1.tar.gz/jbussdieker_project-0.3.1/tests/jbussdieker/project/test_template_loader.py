import unittest
from unittest.mock import patch, mock_open
from pathlib import Path

from jbussdieker.project.template_loader import (
    load_template,
    substitute_template,
    load_and_substitute,
)


class TestTemplateLoader(unittest.TestCase):
    def test_load_template_with_tpl_extension(self):
        """Test loading a template that already has .tpl extension."""
        template_content = "Hello %%NAME%%"
        with patch("builtins.open", mock_open(read_data=template_content)):
            with patch("pathlib.Path.exists", return_value=True):
                result = load_template("test.tpl")
                self.assertEqual(result, template_content)

    def test_load_template_without_tpl_extension(self):
        """Test loading a template without .tpl extension."""
        template_content = "Hello %%NAME%%"
        with patch("builtins.open", mock_open(read_data=template_content)):
            with patch("pathlib.Path.exists", return_value=True):
                result = load_template("test")
                self.assertEqual(result, template_content)

    def test_load_template_file_not_found(self):
        """Test loading a template that doesn't exist."""
        with patch("pathlib.Path.exists", return_value=False):
            with self.assertRaises(FileNotFoundError) as cm:
                load_template("nonexistent")
            self.assertIn("Template 'nonexistent.tpl' not found", str(cm.exception))

    def test_substitute_template_single_variable(self):
        """Test substituting a single variable in template."""
        template = "Hello %%NAME%%"
        result = substitute_template(template, NAME="World")
        self.assertEqual(result, "Hello World")

    def test_substitute_template_multiple_variables(self):
        """Test substituting multiple variables in template."""
        template = "Hello %%NAME%%, you are %%AGE%% years old"
        result = substitute_template(template, NAME="Alice", AGE="30")
        self.assertEqual(result, "Hello Alice, you are 30 years old")

    def test_substitute_template_no_variables(self):
        """Test substituting with no variables."""
        template = "Hello World"
        result = substitute_template(template)
        self.assertEqual(result, "Hello World")

    def test_substitute_template_non_string_values(self):
        """Test substituting non-string values."""
        template = "Count: %%COUNT%%, Active: %%ACTIVE%%"
        result = substitute_template(template, COUNT=42, ACTIVE=True)
        self.assertEqual(result, "Count: 42, Active: True")

    def test_load_and_substitute(self):
        """Test loading and substituting in one step."""
        template_content = "Hello %%NAME%%, you are %%AGE%% years old"
        with patch("builtins.open", mock_open(read_data=template_content)):
            with patch("pathlib.Path.exists", return_value=True):
                result = load_and_substitute("test", NAME="Bob", AGE="25")
                self.assertEqual(result, "Hello Bob, you are 25 years old")


if __name__ == "__main__":
    unittest.main()
