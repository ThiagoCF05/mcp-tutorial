import asyncio
import json
import os
import pandas as pd
import time

from agents import ModelSettings, Runner
from openai.types.shared import Reasoning
from tools import code_interpreter, cvm_composition_query_tool, cvm_base_query_tool

# from servers import get_aws_mcp_server
from financial_agents import get_agent
from financial_agents.financial_analyst import (
    FINANCIAL_ANALYST_INSTRUCTION,
    IndicatorOutput,
    Indicator,
)

# from financial_agents.financial_manager import MANAGER_INSTRUCTIONS, FinanceOutput
from dotenv import load_dotenv

load_dotenv(".env")

price_file = "/Users/thiagocastroferreira/Desktop/kubernetes/mcp-tutorial/fundamental_analysis/2025-04-17/fundamental_analysis.csv"
price_df = pd.read_csv(price_file)

stocks = [
    {"id": "ALUP11", "cnpj": "08.364.948/0001-38", "name": "Alupar Investimento"},
    {"id": "AURE3", "cnpj": "28.594.234/0001-23", "name": "Auren Energia"},
    {
        "id": "CPLE3",
        "cnpj": "76.483.817/0001-20",
        "name": "Companhia Paranaense de Energia",
    },
    {"id": "EGIE3", "cnpj": "02.474.103/0001-19", "name": "Engie Brasil Energia"},
    {"id": "ELET3", "cnpj": "00.001.180/0001-26", "name": "Eletrobrás"},
    {"id": "ENEV3", "cnpj": "04.423.567/0001-21", "name": "Eneva"},
    {"id": "ENGI3", "cnpj": "00.864.214/0001-06", "name": "Energisa"},
    {"id": "EQTL3", "cnpj": "03.220.438/0001-73", "name": "Equatorial"},
    {"id": "ISAE3", "cnpj": "02.998.611/0001-04", "name": "ISA Energia Brasil"},
    {"id": "LIGT3", "cnpj": "03.378.521/0001-75", "name": "Light"},
    {"id": "NEOE3", "cnpj": "01.083.200/0001-18", "name": "Neoenergia"},
    {"id": "RNEW11", "cnpj": "08.534.605/0001-74", "name": "Renova Energia"},
    {"id": "SRNA3", "cnpj": "42.500.384/0001-51", "name": "Serena Energia"},
]

TEMPLATE_INPUT = """Fazer análise fundamentalista da empresa {name} (CNPJ {cnpj}) em Dezembro de 2024 com cotação a {price_str} reais.

Feedback: {feedback}"""

EXPERIMENT_METADATA = {
    "model": "gpt-5-mini",
    "reasoning": "medium",
    "verbosity": "medium",
    "max_turns": 30,
    "template": str(TEMPLATE_INPUT),
    "planning": False,
    "structured_output": IndicatorOutput.model_json_schema(),
    "reflection": False,
}

write_folder = f"experiments/{EXPERIMENT_METADATA['model']}/regular"
os.makedirs(write_folder, exist_ok=True)
with open(f"""{write_folder}/experiment_metadata.json""", "w") as f:
    json.dump(EXPERIMENT_METADATA, f, indent=4)


def save_results(stock_id, result, elapsed_time):
    usage = result.context_wrapper.usage
    nrequests = usage.requests
    input_tokens = usage.input_tokens
    output_tokens = usage.output_tokens
    total_tokens = usage.total_tokens
    steps = [item.to_input_item() for item in result.new_items]

    with open(f"{write_folder}/{stock_id}.json", "w") as f:
        json.dump(
            {
                "steps": steps,
                "usage": {
                    "requests": nrequests,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": total_tokens,
                },
                "time": elapsed_time,
            },
            f,
            indent=4,
        )

    with open(f"{write_folder}/{stock_id}_output.json", "w") as f:
        json.dump(result.final_output.model_dump(), f, indent=4)


def analyse(name: str, cnpj: str, stock_id: str, price: float):
    price_str = f"{price:.2f}".replace(".", ",")
    feedback = "Compute todos os indicadores fundamentalistas disponíveis"
    # server = await get_aws_mcp_server()
    # await server.connect()

    model_settings = ModelSettings(tool_choice="required")
    if (
        "reasoning" in EXPERIMENT_METADATA
        and EXPERIMENT_METADATA["reasoning"] is not None
    ):
        reasoning = Reasoning(effort=EXPERIMENT_METADATA["reasoning"])
        model_settings = ModelSettings(
            reasoning=reasoning,
            verbosity=EXPERIMENT_METADATA["verbosity"],
        )

    agent = get_agent(
        name="financial_analyst",
        instructions=FINANCIAL_ANALYST_INSTRUCTION,
        tools=[
            code_interpreter,
            cvm_base_query_tool,
            cvm_composition_query_tool,
        ],
        servers=[],
        model=EXPERIMENT_METADATA["model"],
        model_settings=model_settings,
        output_type=IndicatorOutput,
    )

    inp_data = TEMPLATE_INPUT.format(
        name=name, cnpj=cnpj, price_str=price_str, feedback=feedback
    )
    start = time.time()
    # agent
    result = asyncio.run(
        Runner.run(agent, input=inp_data, max_turns=EXPERIMENT_METADATA["max_turns"])
    )
    # guardrail
    all_indicators = [str(i) for i in Indicator]
    missing_indicators = [
        str(i.indicator)
        for i in result.final_output.indicators
        if str(i.indicator) not in all_indicators or i.value == 0
    ]
    if len(missing_indicators) > 0 and EXPERIMENT_METADATA["reflection"] is True:
        # reflection
        feedback = f"Compute SOMENTE os seguintes indicadores fundamentalistas: {missing_indicators}"
        inp_data = TEMPLATE_INPUT.format(
            name=name, cnpj=cnpj, price_str=price_str, feedback=feedback
        )
        reflected_result = asyncio.run(
            Runner.run(
                agent, input=inp_data, max_turns=EXPERIMENT_METADATA["max_turns"]
            )
        )
        for i in reflected_result.final_output.indicators:
            if str(i.indicator) in missing_indicators:
                result.final_output.indicators = [
                    i_
                    for i_ in result.final_output.indicators
                    if str(i.indicator) != str(i_.indicator)
                ]
                result.final_output.indicators.append(i)

    end = time.time()

    # await server.cleanup()
    save_results(stock_id=stock_id, result=result, elapsed_time=end - start)


if __name__ == "__main__":
    for stock in stocks:
        name, cnpj, stock_id = stock["name"], stock["cnpj"], stock["id"]
        if os.path.exists(f"{write_folder}/{stock_id}.json"):
            continue
        print(stock)
        price = float(price_df[price_df["Papel"] == stock_id].iloc[0]["Cotação"])
        analyse(name=name, cnpj=cnpj, stock_id=stock_id, price=price)
