from flask import Flask, request
from flask import Response
from flask import request
import sys
import json
import os, ibm_db_dbi as dbi, pandas as pd
import numpy as np
import os

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello New World!"


@app.route("/other/")
def other_hello():
    return "Hello my other World!"

#/order?number=1234&status=finalized
@app.route('/order/', methods=('get', 'post'))
def fetch_order():
    dbCon = db_connection()
    orderNum = request.args.get('orderNum') 
    status = request.args.get('newStatus') 

    return orderNum

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
    #print(df)
    ''' 
    df_data = df.to_string(index=False)
    data = {}
    data["id"] = 1
    df1 = df[["PURCHASEORDERID", "ORDERSTATUS"]]
    print(df1)
    data["orders"] = df1.to_json()
    print(df1.to_json())

    # df_data = data.to_string(index=False)
    # json_data = json.dumps(df_data)
    # htmlCode = df.to_html()
    # return htmlCode
    return Response(json.dumps(data), mimetype="application/json")
    ''' 
    df_data = df.to_string(index=False)
    data = {}
    data["id"] = 1
    df1 = df[["PURCHASEORDERID", "ORDERSTATUS"]]

    result = "\n"
    for index, row in df.iterrows():
        result += str(row["PURCHASEORDERID"])
        result += ":"
        result += row["ORDERSTATUS"] + "\n"
    # print(df1)
    data["orders"] = result
    print(result)
    # df_data = data.to_string(index=False)
    # json_data = json.dumps(df_data)
    # htmlCode = df.to_html()
    # return htmlCode
    return Response(json.dumps(data), mimetype="application/json")


@app.route("/health")
def health():
    data = {}
    data["id"] = 1
    data["health"] = "ok"
    json_data = json.dumps(data)
    # return json_data
    return Response(json_data, mimetype="application/json")
    # return json_data, 200, {"Content-Type": "application/json; charset=utf-8"}

def db_connection():
    db2_dsn = "DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;UID={uid};PWD={pwd};SECURITY=SSL".format(
    "bludb",
    "fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud",
    "32731",
    uid="ktx43420",
    pwd="Zbtqco8TYB0mzMui",
    )
    db2_connection = dbi.connect(db2_dsn)
    return db2_connection


if __name__ == "__main__":
    port = os.environ.get("FLASK_PORT") or 8080
    port = int(port)

    app.run(port=port, host="0.0.0.0")
