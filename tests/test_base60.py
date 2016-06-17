import pytest
from shortener.service import UrlShortener


@pytest.fixture()
def shortener():
    return UrlShortener()


@pytest.mark.usefixtures("shortener")
class TestBaseConversion:
    def test_check0(self, shortener):
        assert shortener.numtosxg(0) == '0'

    def test_check1(self, shortener):
        assert shortener.numtosxg(1) == '1'

    def test_check60(self, shortener):
        assert shortener.numtosxg(60) == '10'


@pytest.mark.usefixtures("shortener")
class TestBaseConversionReverse:
    def test_check0(self, shortener):
        assert shortener.sxgtonum('0') == 0

    def test_check1(self, shortener):
        assert shortener.sxgtonum('1') == 1

    def test_check60(self, shortener):
        assert shortener.sxgtonum('10') == 60

    def test_check1337(self, shortener):
        assert shortener.sxgtonum('NH') == 1337

    def test_checkl(self, shortener):
        assert shortener.sxgtonum('l') == 1

    def test_checkI(self, shortener):
        assert shortener.sxgtonum('I') == 1

    def test_checkO(self, shortener):
        assert shortener.sxgtonum('O') == 0

    def test_checkpipe(self, shortener):
        assert shortener.sxgtonum('|') == 0

    def test_checkcomma(self, shortener):
        assert shortener.sxgtonum(',') == 0


@pytest.mark.usefixtures("shortener")
class TestRoundtripCheck:
    def test_roundtrip(self, shortener):
        #  sxgtonum(numtosxg(n))==n for all n 
        for integer in range(0, 6000):
            sxg = shortener.numtosxg(integer)
            result = shortener.sxgtonum(sxg)
            assert integer == result
