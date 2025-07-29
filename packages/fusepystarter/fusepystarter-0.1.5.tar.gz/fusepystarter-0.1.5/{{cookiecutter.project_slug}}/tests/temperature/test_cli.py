from src.temperature._cli import Main


class TestMainCLI:
    def test_celsius_to_fahrenheit(self):
        cli = Main()
        assert cli.celsius_to_fahrenheit(0) == 32.0
        assert cli.celsius_to_fahrenheit(100) == 212.0

    def test_fahrenheit_to_celsius(self):
        cli = Main()
        assert cli.fahrenheit_to_celsius(32) == 0.0
        assert cli.fahrenheit_to_celsius(212) == 100.0

    def test_faulty_converter_c_to_f(self):
        cli = Main()
        result = cli.faulty_temp.convert(0, "C", "F")
        expected = 32.0 - cli.faulty_temp.calibration_error
        assert result == expected

    def test_advanced_converter_f_to_c(self):
        cli = Main()
        result = cli.advance_temp.convert(212, "F", "C")
        expected = (212 - 32) * 5 / 9
        assert result == expected
