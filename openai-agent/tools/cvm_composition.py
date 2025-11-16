from agents import function_tool
from typing_extensions import TypedDict

DB_PATH = "/Users/thiagocastroferreira/Desktop/kubernetes/mcp-tutorial/cvm.db"


class QueryInput(TypedDict):
    sql_query: str


def cvm_composition_query(inp: QueryInput) -> dict:
    import sqlite3

    try:
        sql_query = inp["sql_query"]
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)

            # Fetch column names
            columns = (
                [description[0] for description in cursor.description]
                if cursor.description
                else []
            )

            # Fetch results
            rows = cursor.fetchall()

            # Format results as markdown table
            if not rows:
                return "No data found with given query"

            # Create markdown table
            output = "| " + " | ".join(columns) + " |\n"
            output += "| " + " | ".join(["---" for _ in columns]) + " |\n"
            for row in rows:
                output += (
                    "| "
                    + " | ".join(
                        [str(cell) if cell is not None else "" for cell in row]
                    )
                    + " |\n"
                )

            return {"status": "success", "report": output}
    except Exception as e:
        return {"status": "error", "report": f"Failed to get table schema: {e}"}


@function_tool
def cvm_composition_query_tool(inp: QueryInput) -> dict:
    """Consultar um Banco de Dados SQL com o relatório de composição de ações das empresas do Mercado de Ações Brasileiro. Esquema:

    CREATE TABLE IF NOT EXISTS CVM_SHARE_COMPOSITION (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        CNPJ TEXT NOT NULL, # CNPJ da empresa (Formato 00.000.000/0000-00)
        REPORT_DATE DATETIME NOT NULL, # Data do relatório
        COMPANY_NAME TEXT NOT NULL, # Nome da empresa
        VERSION TEXT NOT NULL, # Versão
        ORDINARY_SHARES_ISSUED INTEGER NOT NULL, # Ações Ordinárias Emitidas
        ORDINARY_SHARES_TREASURY INTEGER NOT NULL, # Ações Ordinárias na Tesouraria
        PREFERRED_SHARES_ISSUED INTEGER NOT NULL, # Ações Preferenciais Emitidas
        PREFERRED_SHARES_TREASURY INTEGER NOT NULL, # Ações Preferenciais na Tesouraria
        TOTAL_SHARES_ISSUED INTEGER NOT NULL, # Total de Ações Emitidas
        TOTAL_SHARES_TREASURY INTEGER NOT NULL # Total de Ações na Tesouraria
    )

    Observações:
    - As informações estão disponibilizadas trimestralmente (Março, Junho, Setembro e Dezembro), conforme a data de início do período de análise.
    - Para o balanço anual, consultar análises de Dezembro.
    """
    return cvm_composition_query(inp)
