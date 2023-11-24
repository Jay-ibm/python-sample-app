from flask import Flask
import sys
import json
import os, ibm_db_dbi as dbi, pandas as pd
import requests
import numpy as np
import os

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello New World!"


@app.route("/other/")
def other_hello():
    return "Hello my other World!"


@app.route("/orders/")
def fetch_orders():
    db2_dsn = "DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;UID={uid};PWD={pwd};SECURITY=SSL".format(
        "bludb",
        "fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud",
        "32731",
        uid="ktx43420",
        pwd="Zbtqco8TYB0mzMui",
    )

    db2_connection = dbi.connect(db2_dsn)
    query = "SELECT * FROM PROCUREMENT"
    print(query)
    df = pd.read_sql_query(query, con=db2_connection)
    print(df)
    return df


if __name__ == "__main__":
    port = os.environ.get("FLASK_PORT") or 8080
    port = int(port)

    app.run(port=port, host="0.0.0.0")
