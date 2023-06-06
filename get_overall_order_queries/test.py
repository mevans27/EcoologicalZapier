from main import *


def test_get_taxable():
    assert (get_taxable('CA') is True)
    assert (get_taxable('TX') is False)


def test_get_calculated_total():
    assert (get_calculated_total(100, 10) == 90)
    assert (get_calculated_total(68.74, 10.13) == 58.61)


def test_get_tax_percent():
    assert (get_tax_percent(0.8, True, 10, 0) == 8.0)
    assert (get_tax_percent(0.8, False, 10, 0) == 8.0)
    assert (get_tax_percent(20, True, 424.85, 50) == 5.34)


def test_get_formatted_discount_text():
    assert (get_formatted_discount_text(0) == 0)
    assert (get_formatted_discount_text(10) == -10)