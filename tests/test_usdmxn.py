# See: https://github.com/pr3d4t0r/usdmxn/blob/master/LICENSE.txt


from datetime import date
from datetime import timedelta

from usdmxn import BANXICO_API_KEY
from usdmxn import _convertMXDateToISO
from usdmxn import _main
from usdmxn import _todayISO
from usdmxn import assertAPIKeyInEnv
from usdmxn import die
from usdmxn import displayResultsIn
from usdmxn import fetchLatestExchangeRates
from usdmxn import helpUser


# +++ globals +++

_payload = None


# *** run tests ***


def test_helpUser():
    helpUser(unitTest = True)


def test_die():
    die("foo", 42, unitTest = True)


def test_assertAPIKeyInEnv():
    # Happy path, BANXICO_API_KEY is set
    assert len(BANXICO_API_KEY)
    assert assertAPIKeyInEnv()

    # No BANXICO_API_KEY defined:
    assert assertAPIKeyInEnv(unitTest = True)


def test_assertArgList():
    pass


def test_fetchLatestExchangeRates():
    global _payload

    # Happy path, BANXICO_API_KEY is set
    assert len(BANXICO_API_KEY)
    status, _payload = fetchLatestExchangeRates()
    assert 200 == status
    assert len(_payload)


def test__convertMXDateToISO():
    assert not _convertMXDateToISO(None)
    assert not _convertMXDateToISO('00/00')
    assert not _convertMXDateToISO('00000000000000000000')
    assert not _convertMXDateToISO('27/09')
    date = _convertMXDateToISO('27/09/2023')
    assert date == '2023/09/27'


def test__todayISO():
    today = date.today()
    tomorrow = (today+timedelta(days = 1)).strftime('%Y/%m/%d')
    today = today.strftime('%Y/%m/%d')

    d, t = _todayISO()
    assert d == today
    assert t == tomorrow


def test_displayResultsIn():
    displayResultsIn(_payload)


def test__main():
    assert _main(unitTest = True) == 0 # UNIX exit OK

