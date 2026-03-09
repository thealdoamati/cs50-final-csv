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
        return render_template("index.html")
        
    _, extension = os.path.splitext(file.filename)

    if extension != ".csv":
        print("Only csv")
        return render_template("index.html")
    
def create_mockup(reader):
    rows = []
    # Get header and 4 examples
    for i, row in enumerate(reader):
        if i == 4:
            break
        rows.append(row)
    
    header = rows[0]
    new_examples = []
    
    for example in rows:            
        new_example = []
        
        for col_index, cell in enumerate(example):
            
            # If this column header is risky
            if header[col_index].lower in risky_headers:
                new_cell = "X"   
                             
            else:
                new_cell = "" 
                for character in cell:
                    new_character = ""
                    if character.isdigit():
                        new_character = "X"
                    else:
                        new_character = character
                    new_cell += new_character
                    
            new_example.append(new_cell)
            
        new_examples.append(new_example)
        
    return new_examples