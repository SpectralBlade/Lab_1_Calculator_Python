from src.power import calculate_expression
import pytest

class TestCalculateExpression:

    # Верные выражения

    @pytest.mark.parametrize("expression, expected_result", [
        # Стандартные выражения
        ('3 4 +', 7),
        ('15 4 -', 11),
        ('3 10 *', 30),
        ('50 5 /', 10),
        ('5 8 9 + -', -12),
        ('9 6 4 2 / - *', 36),
        ('3 3 **', 27),
        ('34 3 %', 1),
        ('58 7 //', 8),

        # Выражения с унарными операторами

        ('7 ~ 3 +', -4),
        ('7 $ 3 +', 10),
        ('3 7 * ~', -21),
        ('35 5 ~ /', -7),
        ('6 ~ 5 -', -11),
        ('( 5 ~ )', -5),

        # Выражения со скобками

        ('( 3 5 + )', 8),
        ('4 ( 5 9 * ) +', 49),
        ('( 18 2 / ) 6 *', 54),
        ('( 5 ( 25 3 5 * // ) + ) 3 /', 2),
        ('9 ( 8 6 * ) ( 8 5 % ) + * 17 /', 27)

    ])
    def test_calculate(self, expression, expected_result):
        assert calculate_expression(expression) == expected_result

    def test_wrong_expressions(self):
        with pytest.raises(SyntaxError):
            calculate_expression('')
            calculate_expression('( 5 8 +')
            calculate_expression('3 9 - )')
            calculate_expression('GOIDA')
            calculate_expression('RULETKA')
            calculate_expression('5 9 + -')
            calculate_expression('~ + 97')
            calculate_expression('4 ( 5 6 + - )')
            calculate_expression('( )')

        with pytest.raises(ValueError):
            calculate_expression('3 0 /')
            calculate_expression('5 ( 8 3 5 + - ) //')
            calculate_expression('68 ( 4 1 5 - + ) %')
            calculate_expression('5 3.5 //')
            calculate_expression('10 2.1 %')
