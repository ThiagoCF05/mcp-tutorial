from pydantic import BaseModel, Field
from enum import StrEnum

MANAGER_INSTRUCTIONS = """Você é um gerente de mercado que recebe informações financeiras de empresas para ajudar a tomar decisões de investimento.

Observações:
- Use o interpretador Python como calculadora caso seja necessário.
- Se não souber a resposta ou não encontrar a informação, responda com "N/A"."""

MANAGER_DESCRIPTION = "A financial manager agent for the Brazilian stock market"


class FinanceRecommendation(StrEnum):
    BUY = "Comprar"
    SELL = "Vender"


class FinanceOutput(BaseModel):
    interpretation: str = Field(
        alias="interpretation", description="Interpretação dos Resultados"
    )
    recommendation: FinanceRecommendation = Field(
        alias="recommendation", description="Recomendação"
    )
    justification: str = Field(
        alias="justification", description="Justificativa da Recomendação"
    )
