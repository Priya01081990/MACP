import pandas as pd
from typing import Dict


def chcek_login(db:pd.DataFrame, username:str, password:str) -> bool:
    b = False
    # Check if user exists in the loaded data
    user_row = db[(db['username'] == username) & (db['password'] == password)]
    return user_row.empty


def get_user_data_by_username(db:pd.DataFrame, username:str) -> Dict:
    row = db[(db.username == username)]
    return {
        "username":username,
        "name":row.name.tolist()[0],
        "contact_no":row.contact_no.tolist()[0],
        "address":row.address.tolist()[0]
    }


