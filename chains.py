import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import openai
import os
import re
from dotenv import load_dotenv

# -------------- ENV & API KEY SETUP ----------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing OPENAI_API_KEY in .env file!")
openai.api_key = api_key

# -------------- SCHEMA / DB INFO -------------------
DATABASES = {
    "student.db": {
        "tables": {
            "STUDENT": ["NAME", "CLASS", "AGE", "MARKS"]
        }
    },
    "employees.db": {
        "tables": {
            "EMPLOYEES": ["NAME", "DEPARTMENT", "SALARY", "EXPERIENCE"]
        }
    },
    "sales.db": {
        "tables": {
            "SALES": ["PRODUCT", "REGION", "SALES", "REVENUE"]
        }
    }
}
ALL_DB_NAMES = list(DATABASES.keys())

# -------------- PROMPT / AI LOGIC ------------------
def build_system_prompt(conversation_history=None):
    schema_instructions = """
    Databases and their tables:
    1. student.db → STUDENT (NAME, CLASS, AGE, MARKS)
    2. employees.db → EMPLOYEES (NAME, DEPARTMENT, SALARY, EXPERIENCE)
    3. sales.db → SALES (PRODUCT, REGION, SALES, REVENUE)
    """
    rules = """
    Rules:
    - Use case-insensitive matching for columns in sales.db (e.g., LOWER(PRODUCT)).
    - If the user asks for columns that exist in multiple DBs, pick the one that best fits the context.
    - If the user references columns that do NOT exist in any DB, or if the query is just a greeting, respond with normal chat text (no DB or SQL).
    - Otherwise, return the format: <DB_NAME> | <SQL_QUERY>
    - Only use existing columns and tables from the schema above.
    """
    base_prompt = f"""
    You are an expert in converting English questions into SQL queries and determining the correct database.
    
    {schema_instructions}
    
    {rules}
    """
    return base_prompt.strip()

def parse_ai_response(ai_text):
    try:
        db_name, sql_query = ai_text.split("|", 1)
        db_name = db_name.strip()
        sql_query = sql_query.strip()
        if db_name in ALL_DB_NAMES:
            return db_name, sql_query
        else:
            return None, ai_text
    except ValueError:
        return None, ai_text

def extract_columns_from_sql(sql_query):
    query_lower = sql_query.lower()
    columns = set()
    match_select = re.search(r"select\s+(.*?)\s+from", query_lower)
    if match_select:
        parts = match_select.group(1).split(",")
        for p in parts:
            columns.add(p.strip())
    match_where = re.search(r"where\s+(.*)", query_lower)
    if match_where:
        where_part = re.split(r"\s+group\s+by|\s+order\s+by|\s+;", match_where.group(1))[0]
        possible_cols = re.findall(r"(?:lower\()?([a-z_]+)(?:\))?\s*=", where_part)
        for c in possible_cols:
            columns.add(c.strip())
    columns.discard("*")
    columns = {c.replace("(", "").replace(")", "") for c in columns}
    return columns

def check_table_existence(db_name, sql_query):
    match_from = re.search(r"from\s+([a-z_]+)", sql_query.lower())
    if match_from:
        table_in_query = match_from.group(1).upper()
        if table_in_query in DATABASES[db_name]["tables"]:
            return True
        else:
            return False
    return True

def validate_sql(db_name, sql_query):
    used_cols = extract_columns_from_sql(sql_query)
    if not used_cols:
        return check_table_existence(db_name, sql_query)
    all_db_columns = set()
    for table, cols in DATABASES[db_name]["tables"].items():
        for c in cols:
            all_db_columns.add(c.lower())
    for col in used_cols:
        if col not in all_db_columns:
            return False
    return check_table_existence(db_name, sql_query)

def get_sql_query_and_db(user_message):
    system_prompt = build_system_prompt()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        ai_text = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return None, f"OpenAI API error: {e}"
    db_name, sql_query = parse_ai_response(ai_text)
    if db_name is None:
        return None, sql_query
    if not validate_sql(db_name, sql_query):
        return None, ai_text
    return db_name, sql_query

# -------------- SUMMARIZATION FUNCTION ------------------
def summarize_findings(findings_text):
    """
    Uses OpenAI to produce a concise summary of the provided findings.
    """
    prompt = f"Please provide a concise summary of the following findings:\n\n{findings_text}\n\nSummary:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
        )
        summary = response["choices"][0]["message"]["content"].strip()
        return summary
    except Exception as e:
        return f"Summarization error: {e}"

# -------------- SQL EXECUTION & CHARTS ------------------
def get_response_from_db(sql_query, db_path):
    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(sql_query, conn)
            return df
    except Exception as e:
        st.error(f"SQL Error: {e}")
        return None

def chart_type_from_question(question):
    question_lower = question.lower()
    if "bar" in question_lower:
        return "bar"
    elif "histogram" in question_lower:
        return "histogram"
    elif "scatter" in question_lower:
        return "scatter"
    elif "line" in question_lower:
        return "line"
    elif "pie" in question_lower:
        return "pie"
    return None

def determine_chart_type(df):
    if df is None or df.empty:
        return None
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if not numeric_cols:
        return None
    if categorical_cols and numeric_cols:
        if len(numeric_cols) == 1 and len(df[categorical_cols[0]].unique()) <= 5:
            return "pie"
        return "bar"
    elif len(numeric_cols) == 1:
        return "histogram"
    elif len(numeric_cols) == 2:
        return "scatter"
    else:
        return "line"

def generate_chart(df, chart_type):
    if df is None or df.empty or not chart_type:
        st.warning("No chart to display.")
        return
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    fig, ax = plt.subplots(figsize=(7, 4))
    if chart_type == "bar":
        if categorical_cols and numeric_cols:
            df.plot(kind="bar", x=categorical_cols[0], y=numeric_cols[0], ax=ax)
        else:
            st.warning("Bar chart requires at least one categorical and one numeric column.")
    elif chart_type == "histogram":
        if numeric_cols:
            df[numeric_cols[0]].plot(kind="hist", ax=ax, bins=10)
        else:
            st.warning("Histogram requires at least one numeric column.")
    elif chart_type == "scatter":
        if len(numeric_cols) >= 2:
            df.plot(kind="scatter", x=numeric_cols[0], y=numeric_cols[1], ax=ax)
        else:
            st.warning("Scatter plot requires at least two numeric columns.")
    elif chart_type == "line":
        if len(numeric_cols) >= 2:
            df.plot(kind="line", x=numeric_cols[0], y=numeric_cols[1], ax=ax)
        else:
            st.warning("Line chart requires at least two numeric columns.")
    elif chart_type == "pie":
        if categorical_cols and numeric_cols:
            if len(df[categorical_cols[0]].unique()) <= 10:
                df.set_index(categorical_cols[0])[numeric_cols[0]].plot(kind="pie", autopct="%1.1f%%", ax=ax)
                plt.ylabel("")
            else:
                st.warning("Pie chart requires ≤10 unique categories.")
        else:
            st.warning("Pie chart requires at least one categorical and one numeric column.")
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(fig)
