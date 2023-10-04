#!/usr/bin/env python3

# See: https://github.com/pr3d4t0r/usdmxn/blob/master/LICENSE.txt


from datetime import date
from datetime import timedelta
from urllib.request import HTTPError

import json
import os
import sys
import urllib.parse
import urllib.request


__VERSION__ = '1.0.0'


# *** constants ***

BANXICO_API_KEY = os.environ.get('BANXICO_API_KEY', '')
BANXICO_URI = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF60653/datos?token=%s' % BANXICO_API_KEY
USDMXN_TOOL_INVALID = 999
USDMXN_TOOL_UA = 'usdmxn/'+__VERSION__+' ('+sys.platform+')'


# *** functions ***


def die(message, exitCode, unitTest = False):
  if not unitTest:
    print(message)
    sys.exit(exitCode)



def helpUser(unitTest = False):
    if not unitTest:
        die('Usage:  usdmxn [all]', 4)


def assertAPIKeyInEnv(unitTest = False):
    if unitTest:
        return True

    if not BANXICO_API_KEY:
        die('BANXICO_API_KEY not set - get a free key from Banco de México', 1)
    return True


def assertArgList(unitTest = False):
    if unitTest:
        return

    if len(sys.argv) not in range(1, 3):
        helpUser()
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action.lower() not in [ 'all', 'DOF', ] and action[0] not in [ 'a', 'd' ]:
            helpUser()


def fetchLatestExchangeRates():
    request = urllib.request.Request(
        BANXICO_URI,
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': USDMXN_TOOL_UA,
        },
        method = 'GET')
    payload = None

    try:
        input   = urllib.request.urlopen(request)
        payload = input.read()
        status  = input.code
        input.close()
    except HTTPError as e:
        status = e.code
        print('request - %s' % request)
        die(e.headers, 2)
    except Exception as e:
        status = USDMXN_TOOL_INVALID
        print('request - %s' % request)
        die(e.headers, 3)

    return status, json.loads(payload)


def _todayISO() -> str:
    today = date.today()
    tomorrow = today+timedelta(days = 1)

    return today.strftime('%Y/%m/%d'), tomorrow.strftime('%Y/%m/%d')


def _convertMXDateToISO(date: str) -> str:
    # Takes DD/MM/YYYY, returns YYYY/MM/DD - Excel always treats it as a date.
    if not date:
        return None
    if len(date) != 10:
        return None
    parts = date.split('/')
    if len(parts) != 3:
        return None

    return '/'.join([ parts[2], parts[1], parts[0], ])


def displayResultsIn(payload):
    # Displays a TSV table contrived to fit into Excel cells for dynamic updates
    data = payload['bmx']['series'][0]
    print('date\tprice')
    today, tomorrow = _todayISO()
    showAll = sys.argv[1].lower() == 'all' or sys.argv[1].lower() == 'a' if len(sys.argv) == 2 else False
    showTomorrow = sys.argv[1].lower() == 'dof' or sys.argv[1].lower() == 'd' if len(sys.argv) == 2 else False
    listSlice = 0 if showAll else -10
    # TODO:  De-fuglify this at the briefest chance:
    for datum in data['datos'][listSlice:]:
        xDate = _convertMXDateToISO(datum['fecha'])
        if xDate == today and not showTomorrow:
            print('%s\t%s' % (xDate, datum['dato']))
        elif xDate == tomorrow and showTomorrow:
            print('%s\t%s' % (today, datum['dato']))
        elif showAll:
            print('%s\t%s' % (xDate, datum['dato']))
    return True


def _main(unitTest = False):
    assertAPIKeyInEnv(unitTest = unitTest)
    assertArgList(unitTest)
    status, payload = fetchLatestExchangeRates()
    if 200 == status:
        displayResultsIn(payload)

    return 0


# *** main ***

if __name__ == '__main__':
  try:
    _main()
  except KeyboardInterrupt:
    pass

