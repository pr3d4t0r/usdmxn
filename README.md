# usdmxn

Fetches the latest exchange rate USD:MXN and dumps it to stdout.  This is a data
feeder for an Excel Power Query data source.

This tool returns the current latest USD:MXN exchange rate for fulfillment of 
obligations.  Is the official exchange rate for international payments.


---
## Requirements

- Python 3.9.9 or later
- A Banco de México API key

API keys are free to any petitioner, available from https://www.banxico.org.mx/SieAPIRest/service/v1/token
_Token de consulta_ is Spanish for API key or API token.


---
## Executing `usdmxn`

```zsh
export BANXICO_API_KEY="42b4n0...69bbq"
```

Run the command.  It doesn't take any arguments.  Output:

```
date    price
2023/09/28      17.4758
```

The output is a tab-delimited table with a single entry.  Simpler import into
Excel or into a pandas DataFrame.

- The date is in ISO/Japanese format to avoid ambiguity; the Banco de México API
  returns a date in Mexican / European format dd/mm/yyyy
- The original data source uses 4-decimal precision

