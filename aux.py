"""
Module to hold auxiliary fuctions
"""

import pandas as pd
import psycopg2
from flask import jsonify
from psycopg2.extras import RealDictCursor
from db_values import HOST, DBNAME, USER, PASSWORD


def convert_nan_to_none(value):
    """Convert pandas NaN to None."""
    return value if not pd.isna(value) else None

def connect_to_db():
    try:
        # Set up the connection parameters to PostgreSQL
        conn = psycopg2.connect(
            dbname=DBNAME,  
            user=USER,         
            password=PASSWORD,     
            host=HOST,             
        )
        print("Connection to database established.")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
    
def execute_query_with_params(query, params=None):
    """Execute SQL query with or without parameters and return results."""
    conn = connect_to_db()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        if params:
            cur.execute(query, params)  
        else:
            cur.execute(query)

        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    except Exception as e:
        return {"error": str(e)}, 500
    