# Ferma Congress
This is a Python package built for Internal Purposes of ZoomRx - Ferma Congress which does some operation related in planning.

## 🔐 Authentication Setup

To access the Ferma API, you need a `.env` file with your Authorized Ferma  credentials.

### ✅ Option 1: Non-Encoded Credentials (default)

```env
FERMA_USERNAME=your_email@domain.com
FERMA_PASSWORD=your_password
```

### ✅ Option 2: Base64-Encoded Credentials (for `format="ENCODED"`)

```env
FERMA_USERNAME_ENC=encoded_username
FERMA_PASSWORD_ENC=encoded_password
```

Then use:

```python
from FermaCongress.ExtractFerma import *

login("path/to/.env") # Default: In Case of Non-Encoded Credentials

login("path/to/.env", format="ENCODED") # Encoded: In Case of Encoded Credentials
```

---

# ExtractFerma

To use the `ExtractFerma` functionality, you must first authenticate using the `login()` function. Once authenticated, you can call various data extraction functions to retrieve Ferma Congress data. Each function returns a `pandas.DataFrame` for easy analysis or export.

```python
from FermaCongress.ExtractFerma import *

get_all_sessions(congress_id)                         # Fetches Session-Level Metadata
get_skg(congress_id)                                  # Fetches Session Entities Data
get_tweets(congress_id)                               # Fetches tweet-level data linked to sessions
get_priority(congress_id, include=None, exclude=None) # Fetches session priorities across planners
```

```python
# Usage Examples
from FermaCongress.ExtractFerma import *

get_all_sessions("217")

get_skg("217")

get_tweets("217")

get_priority("217")
get_priority("217", include=["ClientA", "ClientB"])   # Include only specific clients
get_priority("217", exclude=["ClientX"])              # Exclude specific clients
```

---

# FormatExcel

The `FormatExcel` utility is used to apply styling and export your Ferma data (from a DataFrame or input file) into a clean, Ferma-styled Excel format.

```python
from FermaCongress.FormatExcel import format

format(dataframe=df, output_path="priority_report.xlsx")  # Format from a DataFrame

format(input_path="raw_sessions.xlsx", output_path="formatted_sessions.xlsx")  # Format from Excel file

format(input_path="raw_data.csv", output_path="formatted_output.xlsx")  # Format from CSV file
```


| Parameter      | Type                         | Description                                                                                |
| -------------- | ---------------------------- | ------------------------------------------------------------------------------------------ |
| `input_path`   | `str`                        | Path to an input Excel or CSV file.                                                        |
| `dataframe`    | `pandas.DataFrame`           | DataFrame to format.                                                                       |
| `output_path`  | `str`                        | File path to save the formatted Excel output.                                              |
| `headers`      | `bool`                       | True to convert headers to proper casing (e.g., buzz_score → Buzz Score).                  |
| `input_sheet`  | `str`                        | Name of the sheet to read from (Excel only). Optional if only one sheet.                   |
| `output_sheet` | `str`                        | Name of the sheet to write into in the output Excel file.                                  |

---