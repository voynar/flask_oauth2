from flask import Flask, render_template
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
from flask import Flask, request
# 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
load_dotenv()
app = Flask(__name__)

# Load Google Sheets API credentials
credentials = service_account.Credentials.from_service_account_file(
    '/Users/Haldur/Downloads/dynamicdata-412611-69bee72313c0.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)

# Google Sheets API spreadsheet ID and range
spreadsheet_id = '1Ixbw0-YvhuIWj0ZSn0L-3nnSkWKznvUjYwpiBQsILYk'
range_name = 'A1:H173' # Didn't work with "SoloTaco!A1:H173"

# Fetch data from Google Sheets
def get_data():
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values

@app.route('/table')
def table():
    data = get_data()
    headings = data[0] if data else [] # Assuming the first row contains headings
    data = data[1:] # Exclude the first row as it contains headings
    return render_template('table.html', headings=headings, data=data)

if __name__ == "__main__":
    app.run(debug=True)

# headings = ("Name", "Role", "Salary") # tuple
# data = (                              # tuple of tuples
#     ("Lou Scarpelli", "CEO", "$99,999.99"),
#     ("Justin Scarpelli", "Custodian", "$12,345.67"),
#     ("Hillary X", "Finance", "66,666.66"),
#     ("Keedro Hydro", "HR", "$65,432.10")
# )
# @app.route("/")
# def table():
#     return render_template("table.html", headings=headings, data=data)
