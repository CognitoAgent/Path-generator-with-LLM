import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = [
    #public API scopes, for authorizing app to access Google APIs
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

class SheetService:
    def __init__(self):
        #credentials
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

        #authorize client
        client = gspread.authorize(creds)

        #open the spreadsheet by name
        self.spreadsheet = client.open("REPLACE_WITH_SPREADSHEET_NAME")


    def updateWorksheet(self, data):
        #access worksheet number nr
        nr = 0 #everything is in one sheet
        sheet = self.spreadsheet.get_worksheet(nr)

        #find the next empty row (by checking column A)
        next_row = len(sheet.col_values(1)) + 1 #gets all the values from column A (column index 1)


        #update the row starting from column A
        sheet.update(f"A{next_row}:F{next_row}", [data])

        #sheet.update("A1:D1", [["Test ID", "Prompt", "Generated Path", "Image Link"]])

        print("Sheet is updated successfully!")
