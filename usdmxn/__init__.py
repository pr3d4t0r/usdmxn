#!/usr/bin/env python3

# See: https://github.com/pr3d4t0r/usdmxn/blob/master/LICENSE.txt


from datetime import date
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


def helpUser(unitTest = False):
   if not unitTest:
    print('Invalid arguments list - syntax:')
    print('usdmxn ip.add.re.ss\n')
    print('ip.add.re.ss is an octet-format IPv4 address.  It may also be a host name.')

    exit(1)


def die(message, exitCode, unitTest = False):
  if not unitTest:
    print(message)
    sys.exit(exitCode)


def assertAPIKeyInEnv(unitTest = False):
    if unitTest:
        return True

    if not BANXICO_API_KEY:
        die('BANXICO_API_KEY not set - get a free key from Banco de México', 1)
    return True


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

    return today.strftime('%Y/%m/%d')


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
    title = data['titulo'] # yuk spelling
    print('date\tprice')
    today = _todayISO()
    for datum in data['datos'][-3:]:
        xDate = _convertMXDateToISO(datum['fecha'])
        if xDate == today:
            print('%s\t%s' % (xDate, datum['dato']))
    return True


def _main(unitTest = False):
    assertAPIKeyInEnv(unitTest = unitTest)
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

