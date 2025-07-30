import pytest
from ad9xdds.ad9915dev_umr232hm import Ad9915Dev


@pytest.mark.parametrize("ifreq, ofreq, expected", [
(1e9, 300e6, (1_288_490_188, 4, 5)),
(1e9, 260e6, (1_116_691_496, 24, 25)),
(2.5e9, 10e6, (17_179_869, 23, 125)),
])
def test_compute_modulus_parameters_basic(ifreq: float, ofreq: float, expected: list[int, int, int]):
    assert Ad9915Dev().compute_modulus_parameters(ifreq, ofreq) == expected


@pytest.mark.parametrize("ifreq, ftw, a, b, expected", [
(1e9, 1_288_490_188, 4, 5, 300e6),
(1e9, 1_116_691_496, 24, 25, 260e6),
])
def test__actual_ofreq_fine_basic(ifreq, ftw, a, b, expected):
    assert Ad9915Dev()._actual_ofreq_fine(ifreq, ftw, a, b) == expected


def test_compute_modulus_parameters_monoticity():
    ifreq = 2.5e9
    ofmin = 10e6
    ofmax = ofmin + 1e-6
    step = 1e-9

    _ofmin = int(ofmin / step)
    _ofmax = int(ofmax / step)
    ftw0 = 0
    ofreq0 = 0
    for ofreq in range(_ofmin, _ofmax):
        ofreq = ofreq * step
        ftw, a, b = Ad9915Dev().compute_modulus_parameters(ifreq, ofreq)
        assert ftw0 <= ftw 
        assert 0 <= a
        assert 0 < b
        ftw0 = ftw
        assert ofreq0 <= Ad9915Dev()._actual_ofreq_fine(ifreq, ftw, a, b), f"Monoticity error (ifreq, ftw, a, b): ({ifreq}, {ftw}, {a}, {b})"
        ofreq0 = ofreq