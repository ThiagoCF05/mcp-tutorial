from agents import function_tool
from typing_extensions import TypedDict

DB_PATH = "/Users/thiagocastroferreira/Desktop/kubernetes/mcp-tutorial/cvm.db"


class QueryInput(TypedDict):
    sql_query: str


@function_tool
def cvm_base_query(inp: QueryInput) -> dict:
    """Consultar um Banco de Dados SQL de Formulários de Demonstrações Financeiras Padronizadas (DFP) e Formulário de Informações Trimestrais (ITR) do Mercado de Ações Brasileiro com o seguinte esquema:

    CREATE TABLE IF NOT EXISTS DFP_ITR_CVM (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
            CNPJ TEXT NOT NULL, # CNPJ da empresa
            REPORT_DATE DATETIME NOT NULL, # Data do relatório
            COMPANY_NAME TEXT NOT NULL, # Nome da empresa
            CVM_CODE TEXT NOT NULL, # CVM Code
            DFP_GROUP TEXT NOT NULL, # Grupo DFP
            VERSION TEXT NOT NULL, # Versão
            CURRENCY TEXT NOT NULL, # Moeda
            ANALYSIS_START_PERIOD_DATE DATETIME, # Data de Início do Período de Análise
            ANALYSIS_END_PERIOD_DATE DATETIME NOT NULL, # Data de Fim do Período de Análise
            ACCOUNT_NUMBER TEXT NOT NULL, # Número da Conta
            ACCOUNT_NAME TEXT NOT NULL, # Nome da Conta
            ACCOUNT_VALUE FLOAT NOT NULL, # Valor da Conta
            IS_FIXED_ACCOUNT TEXT # Conta Fixa?
    )

    Observações:
    - As informações estão disponibilizadas trimestralmente (Março, Junho, Setembro e Dezembro), conforme a data de início do período de análise.
    - Para o balanço anual, consultar análises de Dezembro.
    """
    import sqlite3

    try:
        sql_query = inp.get("sql_query")
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
