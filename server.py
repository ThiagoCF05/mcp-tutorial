# server.py
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

DATABASE_PATH = "fundamental_analysis.db"

@mcp.tool
def query_fundamental_analysis(sql_query: str) -> str:
    """Query a SQL Database about Fundamental Analysis of the Brazilian Stock market with the following schema:
    
CREATE TABLE fundamental_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	Papel VARCHAR(10) NOT NULL, # Código da Ação
	Cotacao FLOAT NOT NULL, # Preço da Ação
	Tipo VARCHAR(10) NOT NULL, # Tipo da Ação
	DataUltimaCotacao DATETIME NOT NULL, # Data da última cotação
	Empresa VARCHAR(100) NOT NULL, # Nome da Empresa
	Min52Sem FLOAT NOT NULL, # Cotação Mínima nas últimas 52 semanas
	Setor VARCHAR(100) NOT NULL, # Setor da Empresa
	Max52Sem FLOAT NOT NULL, # Cotação Máxima nas últimas 52 semanas
	Subsetor VARCHAR(100) NOT NULL, # Subsetor da Empresa
	VolumeMedio2M FLOAT NOT NULL, # Volume médio de negociações nos últimos 2 meses
	ValorMercado FLOAT NOT NULL, # Valor de Mercado da Empresa
	UltimoBalancoProcessado DATETIME NOT NULL, # Último Balanço patrimonial Processado
	ValorFirma FLOAT NOT NULL, # Valor da Firma
	NumeroAcoes INTEGER NOT NULL, # Número Total de Ações
	CrescimentoReceita5a FLOAT NOT NULL, # Crescimento da Receita nos últimos 5 anos
	Ativo FLOAT NOT NULL, # Ativo dos últimos 12 meses
	DividaBruta FLOAT NOT NULL, # Dívida Bruta dos últimos 12 meses
	Disponibilidades FLOAT NOT NULL, # Disponibilidades dos últimos 12 meses
	DividaLiquida FLOAT NOT NULL, # Dívida Líquida dos últimos 12 meses
	AtivoCirculante FLOAT NOT NULL, # Ativo Circulante dos últimos 12 meses
	PatrimonioLiquido FLOAT NOT NULL, # Patrimônio Líquido
	ReceitaLiquida FLOAT NOT NULL, # Receita Líquida dos últimos 12 meses
	ReceitaLiquida3Meses FLOAT NOT NULL, # Receita Líquida dos últimos 3 meses
	EBIT FLOAT NOT NULL, # EBIT dos últimos 12 meses
	EBIT3Meses FLOAT NOT NULL, # EBIT dos últimos 3 meses
	LucroLiquido FLOAT NOT NULL, # Lucro Líquido dos últimos 12 meses
	LucroLiquido3Meses FLOAT NOT NULL, # Lucro Líquido dos últimos 3 meses
	DivYield FLOAT NOT NULL, # Dividend Yield
	Depositos FLOAT NOT NULL, # Depósitos
	CartaoCredito FLOAT NOT NULL, # Cartao Credito
	ResultadoIntFinanceiro FLOAT NOT NULL,
	ResultadoIntFinanceiro3Meses FLOAT NOT NULL,
	ReceitaServicos FLOAT NOT NULL,
	ReceitaServicos3Meses FLOAT NOT NULL
)
"""
    import sqlite3
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            
            # Fetch column names
            columns = [description[0] for description in cursor.description] if cursor.description else []

            # Fetch results
            rows = cursor.fetchall()
            
            # Format results as markdown table
            if not rows:
                return "No data found with given query"

            # Create markdown table
            output = "| " + " | ".join(columns) + " |\n"
            output += "| " + " | ".join(["---" for _ in columns]) + " |\n"
            for row in rows:
                output += "| " + " | ".join([str(cell) if cell is not None else "" for cell in row]) + " |\n"

            return output
    except Exception as e:
        return f"Failed to get table schema: {e}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8080, path="/mcp", host="0.0.0.0")