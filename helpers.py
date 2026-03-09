from flask import render_template
import os

risky_headers = [
    # Authentication
    "password",
    "pass",
    "pwd",
    "password_hash",
    "token",
    "access_token",
    "refresh_token",
    "api_key",
    "secret",

    # Personal Identifiable Information
    "email",
    "phone",
    "phone_number",
    "address",
    "full_name",
    "first_name",
    "last_name",
    "dob",
    "birthdate",
    "ssn",
    "national_id",

    # Financial
    "credit_card",
    "card_number",
    "cvv",
    "iban",
    "bank_account",
    "routing_number",

    # Medical / highly sensitive
    "medical_record",
    "diagnosis",
    "insurance_number"
]

def check_csv(file):
    if not file:
        return False
        
    _, extension = os.path.splitext(file.filename)

    if extension != ".csv":
        print("Only csv")
        return False
    else:
        return True
    
def create_mockup(df):
    # Get 4 rows as example
    sample_df = df.head(4).copy()

    header = list(sample_df.columns)
    new_examples = []

    new_examples.append(header)

    for _, row in sample_df.iterrows():
        new_row = []

        for column in sample_df.columns:
            cell = row[column]
            cell_str = str(cell)

            if column.lower() in risky_headers:
                new_cell = "X"
            else:
                new_cell = ""
                for character in cell_str:
                    if character.isdigit():
                        new_cell += "X"
                    else:
                        new_cell += character

            new_row.append(new_cell)

        new_examples.append(new_row)

    return new_examples