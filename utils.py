import re
import sqlite3
from typing import Optional, Tuple

import pandas as pd

FORBIDDEN = re.compile(
    r'\b(DROP|DELETE|TRUNCATE|ALTER|INSERT|UPDATE|CREATE|REPLACE|ATTACH|DETACH)\b',
    re.IGNORECASE,
)


def extract_sql(text: str) -> Optional[str]:
    match = re.search(r'```(?:sql)?\s*(.*?)```', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r'(SELECT\s+.+?)(?:;|$)', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip() + ";"
    return None


def validate_sql(sql: Optional[str]) -> Tuple[bool, str]:
    if not sql:
        return False, "No SQL query found in the model response."
    if FORBIDDEN.search(sql):
        return False, "Query contains forbidden operations (DROP/DELETE/INSERT/UPDATE/etc.)."
    if not re.match(r'^\s*SELECT', sql, re.IGNORECASE):
        return False, "Only SELECT queries are permitted."
    return True, ""


def execute_sql(db_path: str, sql: str) -> Tuple[Optional[pd.DataFrame], str]:
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df, ""
    except Exception as e:
        return None, str(e)
