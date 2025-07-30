import io

import pandas as pd
from sqlalchemy.engine import Engine

COPY_QUERY = (
    "COPY {table_name} FROM STDIN WITH (FORMAT csv, HEADER TRUE,  DELIMITER '\t');"
)


class PostgresUtils:
    @staticmethod
    def copy(engine: Engine, table_name: str, df: pd.DataFrame):
        csv_content = io.StringIO()
        df.to_csv(csv_content, sep="\t", header=True, index=False)
        csv_content.seek(0)
        conn = engine.raw_connection()
        cur = conn.cursor()
        cur.copy_expert(COPY_QUERY.format(table_name=table_name), csv_content)
        conn.commit()
        cur.close()
        conn.close()
