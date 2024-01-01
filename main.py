from datetime import date
import pandas as pd
from send_email_payment_reminder import send_email
from dotenv import load_dotenv
from pathlib import Path
import os


curr_dir = Path(__file__).resolve().parent if __file__ in locals() else Path.cwd()
env_file = curr_dir / ".env"

load_dotenv(env_file)

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")


SHEET_NAME = "Sheet1"
URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"


def load_df(url):
    parse_dates = ["due_date", "reminder_date"]
    df = pd.read_csv(url, parse_dates=parse_dates)

    return df


def query_data_send_email(df):
    present = date.today()
    email_counter = 0

    for _, row in df.iterrows():
        if (present >= row["reminder_date"].date()) and (row["has_paid"] == "no"):
            send_email(
                subject=f"[JCompany Technology Corp.] Invoice: {row['invoice_no']}",
                receiver_email=row["email"],
                name=row["name"],
                due_date=row["due_date"],
                invoice_no=row["invoice_no"],
                amount=row["amount"],
            )
            email_counter += 1

    return f"Total Emails sent: {email_counter}"


df = load_df(URL)
result = query_data_send_email(df)
print(result)
