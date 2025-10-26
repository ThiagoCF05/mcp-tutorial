import asyncio
import json
import os
import pandas as pd
import time

from agents import ModelSettings, Runner
from openai.types.shared import Reasoning
from tools import code_interpreter, cvm_composition_query, cvm_base_query
from servers import get_aws_mcp_server
from financial_agents import get_agent
from financial_agents.financial_analyst import AGENT_INSTRUCTIONS
from dotenv import load_dotenv

load_dotenv()

write_folder = "experiments/session3"
os.makedirs(write_folder, exist_ok=True)

price_file = "/Users/thiagocastroferreira/Desktop/kubernetes/mcp-tutorial/fundamental_analysis/2025-04-17/fundamental_analysis.csv"
price_df = pd.read_csv(price_file)

stocks = [
    {
        "id": "AFLT3",
        "cnpj": "10.338.320/0001-00",
        "name": "Afluente Transmissão de Energia",
    },
    {"id": "ALUP11", "cnpj": "08.364.948/0001-38", "name": "Alupar Investimento"},
    {"id": "AURE3", "cnpj": "28.594.234/0001-23", "name": "Auren Energia"},
    {"id": "CBEE3", "cnpj": "33.050.071/0001-58", "name": "Ampla Energia e Serviços"},
    {"id": "CEEB3", "cnpj": "15.139.629/0001-94", "name": "COELBA"},
    {
        "id": "CPLE3",
        "cnpj": "76.483.817/0001-20",
        "name": "Companhia Paranaense de Energia",
    },
    {"id": "EGIE3", "cnpj": "02.474.103/0001-19", "name": "Engie Brasil Energia"},
    {
        "id": "COCE3",
        "cnpj": "07.047.251/0001-70",
        "name": "Companhia Energértica do Ceará",
    },
    {"id": "EKTR4", "cnpj": "02.328.280/0001-97", "name": "Elektro Redes"},
    {"id": "ELET3", "cnpj": "00.001.180/0001-26", "name": "Eletrobrás"},
    {"id": "ENEV3", "cnpj": "04.423.567/0001-21", "name": "Eneva"},
    {"id": "ENGI3", "cnpj": "00.864.214/0001-06", "name": "Energisa"},
    {"id": "ENMT3", "cnpj": "03.467.321/0001-99", "name": "Energisa Mato Grosso"},
    {"id": "EQTL3", "cnpj": "03.220.438/0001-73", "name": "Equatorial"},
    {"id": "ISAE3", "cnpj": "02.998.611/0001-04", "name": "ISA Energia Brasil"},
    {"id": "LIGT3", "cnpj": "03.378.521/0001-75", "name": "Light"},
    {"id": "NEOE3", "cnpj": "01.083.200/0001-18", "name": "Neoenergia"},
    {"id": "RNEW11", "cnpj": "08.534.605/0001-74", "name": "Renova Energia"},
    {"id": "SRNA3", "cnpj": "42.500.384/0001-51", "name": "Serena Energia"},
]

TEMPLATE_INPUT = """Fazer análise fundamentalista da empresa {name} (CNPJ {cnpj}) em Dezembro de 2024 com cotação a {price_str} reais. 

Interpretar resultados e dar recomendações de compra, neutralidade ou venda."""

EXPERIMENT_METADATA = {
    "model": "gpt-5",
    "reasoning": "medium",
    "verbosity": "medium",
    "max_turns": 30,
    "template": str(TEMPLATE_INPUT),
    "planning": False,
}
with open(f"""{write_folder}/experiment_metadata.json""", "w") as f:
    json.dump(EXPERIMENT_METADATA, f, indent=4)


async def analyse(name: str, cnpj: str, stock_id: str, price: float):
    price_str = f"{price:.2f}".replace(".", ",")
    server = await get_aws_mcp_server()
    await server.connect()
    agent = get_agent(
        name="financial_analyst",
        instructions=AGENT_INSTRUCTIONS,
        tools=[
            code_interpreter,
            cvm_base_query,
            cvm_composition_query,
        ],
        servers=[],
        model=EXPERIMENT_METADATA["model"],
        model_settings=ModelSettings(
            reasoning=Reasoning(effort=EXPERIMENT_METADATA["reasoning"]),
            verbosity=EXPERIMENT_METADATA["verbosity"],
        ),
    )

    inp_data = TEMPLATE_INPUT.format(name=name, cnpj=cnpj, price_str=price_str)
    start = time.time()
    result = await Runner.run(
        agent, input=inp_data, max_turns=EXPERIMENT_METADATA["max_turns"]
    )
    end = time.time()

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
                "time": end - start,
            },
            f,
            indent=4,
        )

    with open(f"{write_folder}/{stock_id}.txt", "w") as f:
        f.write(result.final_output)
    await server.cleanup()


if __name__ == "__main__":
    for stock in stocks:
        name, cnpj, stock_id = stock["name"], stock["cnpj"], stock["id"]
        if os.path.exists(f"{write_folder}/{stock_id}.txt"):
            continue
        print(stock)
        price = float(price_df[price_df["Papel"] == stock_id].iloc[0]["Cotação"])
        asyncio.run(analyse(name=name, cnpj=cnpj, stock_id=stock_id, price=price))
