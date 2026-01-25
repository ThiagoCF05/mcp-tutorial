import asyncio

from agents import Agent, ModelSettings, Runner, RunResult
from datetime import datetime
from experiments import ExperimentMetadata, StockInput
from openai.types.shared import Reasoning
from tools import code_interpreter
from financial_agents import get_agent
from financial_agents.financial_manager import (
    MANAGER_INSTRUCTIONS,
    FinanceOutput,
)

TEMPLATE_INPUT = """Empresa: {name} (CNPJ {cnpj})
Data: {date}
Cotação: {price_str}

{indicators}
"""


def init_agent(experiment_metadata: ExperimentMetadata) -> Agent:
    model_settings = ModelSettings(tool_choice="required")
    if experiment_metadata.reasoning:
        reasoning = Reasoning(effort=experiment_metadata.reasoning)
        model_settings = ModelSettings(
            reasoning=reasoning,
            verbosity=experiment_metadata.verbosity,
        )

    return get_agent(
        name="financial_manager",
        instructions=MANAGER_INSTRUCTIONS,
        tools=[
            code_interpreter,
        ],
        servers=[],
        model=experiment_metadata.model,
        model_settings=model_settings,
        output_type=FinanceOutput,
    )


def analyse(
    agent: Agent,
    name: str,
    cnpj: str,
    price: str,
    analysis_date: datetime,
    indicators: str,
    experiment_metadata: ExperimentMetadata,
) -> RunResult:
    inp_data = TEMPLATE_INPUT.format(
        name=name,
        cnpj=cnpj,
        date=analysis_date.strftime("%Y-%m-%d"),
        price_str=price,
        indicators=indicators,
    )

    return asyncio.run(
        Runner.run(agent, input=inp_data, max_turns=experiment_metadata.max_turns)
    )


def run(
    stock: StockInput,
    stock_price: float,
    date: str | datetime,
    indicators: str,
    experiment_metadata: ExperimentMetadata,
):
    agent = init_agent(experiment_metadata=experiment_metadata)

    result = analyse(
        agent=agent,
        name=stock.name,
        cnpj=stock.cnpj,
        price=str(stock_price),
        analysis_date=date,
        indicators=indicators,
        experiment_metadata=experiment_metadata,
    )

    return result
