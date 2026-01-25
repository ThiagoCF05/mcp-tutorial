import os
import experiments.investment_house.fundamental_analyst as fundamental_analyst
import experiments.investment_house.manager as financial_manager
import finbr.dias_uteis as dus
import json
import pandas as pd
import time

from agents import RunResult
from datetime import datetime, timedelta
from db import get_stock_daily_info
from db.base_query import ResponseFormat
from experiments import ExperimentMetadata, Model, Intensity
from experiments.reinventa.config import STOCKS
from experiments.utils import get_result
from financial_agents.financial_analyst import (
    IndicatorOutput,
)
from dotenv import load_dotenv

load_dotenv()

WRITE_FOLDER = "/Users/thiagocastroferreira/Desktop/kubernetes/results/manager"


def _get_first_workday(year, month):
    date = datetime(year, month, 1)
    while date.weekday() > 4 or not dus.dia_util(date):
        date += timedelta(days=1)
    return date


def get_last_stock_report_date(date: datetime) -> datetime:
    if date.month <= 3:
        year = date.year - 1
        return datetime(year, 9, 30)
    elif 3 < date.month <= 6:
        year = date.year - 1
        return datetime(year, 12, 31)
    elif 6 < date.month <= 9:
        return datetime(date.year, 3, 31)
    else:
        return datetime(date.year, 6, 30)


def _parse_fundamental_analyst_output(result: RunResult, elapsed_time: float) -> dict:
    """
    Return a dictionary containing the fundamental analysis indicators and their values.

    Parameters
    ----------
    result : RunResult
        The result of the financial analysis.
    elapsed_time : float
        The elapsed time of the analysis.

    Returns
    -------
    dict
        A dictionary containing the fundamental analysis indicators and their values.
    """
    fundamental_analysis = get_result(result, elapsed_time)

    fundamental_indicators = {
        str(f["indicator"]): f["value"]
        for f in fundamental_analysis.get("output", {}).get("indicators", [])
    }
    return fundamental_indicators


def _parse_financial_manager_output(
    result: RunResult, analysis_date: str, elapsed_time: float
) -> dict:
    manager_result = get_result(result, elapsed_time).get("output", {})
    manager_result["analysis_date"] = analysis_date.strftime("%Y-%m-%d")
    return manager_result


def _get_daily_price_info(
    stock_id: str, daily_stock_info: dict, report_date: str
) -> dict:
    """
    Return a dictionary containing the daily price information of a stock.

    Parameters
    ----------
    stock_id : str
        The ID of the stock.
    daily_stock_info : dict
        A dictionary containing the daily price information of the stock.

    Returns
    -------
    dict
        A dictionary containing the daily price information of the stock.
    """
    price_info = {}
    price_info["ACAO"] = stock_id
    price_info["DATA_DO_PREGAO"] = daily_stock_info["DATA_DO_PREGAO"]
    price_info["PRECO_DE_ABERTURA"] = daily_stock_info["PRECO_DE_ABERTURA"]
    price_info["PRECO_MINIMO"] = daily_stock_info["PRECO_MINIMO"]
    price_info["PRECO_MAXIMO"] = daily_stock_info["PRECO_MAXIMO"]
    price_info["PRECO_ULTIMO_NEGOCIO"] = daily_stock_info["PRECO_ULTIMO_NEGOCIO"]
    price_info["PRECO_MEDIO"] = daily_stock_info["PRECO_MEDIO"]
    price_info["PRECO_MELHOR_OFERTA_DE_COMPRA"] = daily_stock_info[
        "PRECO_MELHOR_OFERTA_DE_COMPRA"
    ]
    price_info["QUANTIDADE_NEGOCIADA"] = daily_stock_info["QUANTIDADE_NEGOCIADA"]
    price_info["VOLUME_TOTAL_NEGOCIADO"] = daily_stock_info["VOLUME_TOTAL_NEGOCIADO"]
    price_info["DATA_BALANCO_PROCESSADO"] = report_date.strftime("%Y-%m-%d")
    return price_info


def _get_last_manager_decision(decisions: list) -> dict:
    if len(decisions) == 0:
        return {
            "JUSTIFICATIVA_PREVIA": "N/A",
            "PRECO_ALVO_ANTERIOR": "N/A",
            "RECOMENDACAO_ANTERIOR": "N/A",
        }
    return {
        "JUSTIFICATIVA_PREVIA": decisions[-1]["justification"],
        "PRECO_ALVO_ANTERIOR": decisions[-1]["target_price"],
        "RECOMENDACAO_ANTERIOR": decisions[-1]["recommendation"],
    }


def _save_results(
    write_folder: str,
    stock_id: str,
    analysis_date: str,
    agent_role: str,
    result: RunResult,
    elapsed_time: float,
    experiment_id: int,
) -> None:
    write_folder = f"{write_folder}/{stock_id}"
    os.makedirs(write_folder, exist_ok=True)
    agent_result = get_result(result, elapsed_time)

    with open(
        f"{write_folder}/{analysis_date}_{agent_role}_{experiment_id}.json", "w"
    ) as f:
        json.dump(agent_result, f, indent=4)


if __name__ == "__main__":
    manager_decisions = []
    fundamental_analyses = []

    experiment = ExperimentMetadata(
        model=Model.GPT_5_MINI,
        write_folder=WRITE_FOLDER,
        max_turns=30,
        structured_output=IndicatorOutput.model_json_schema(),
        reasoning=Intensity.MEDIUM,
        verbosity=Intensity.MEDIUM,
        reflection=True,
    )
    for stock in STOCKS:
        for year in [2024, 2025]:
            for month in range(1, 13):
                analysis_date = _get_first_workday(year, month)
                print(f"Analisando {stock.stock_id} em {analysis_date}")

                if os.path.exists(
                    f"{experiment.write_folder}/{stock.stock_id}/{analysis_date.strftime('%Y-%m-%d')}_analyst_0.json"
                ):
                    continue

                start_time = time.time()

                # Get stock price in the day
                daily_stock_info = get_stock_daily_info(
                    stock_id=stock.stock_id,
                    date=analysis_date,
                    response_format=ResponseFormat.DICT,
                )
                if len(daily_stock_info) == 0:
                    continue
                daily_stock_price = float(daily_stock_info[0]["PRECO_ULTIMO_NEGOCIO"])

                # Get last quarter reports date (previous 3 months)
                report_date = get_last_stock_report_date(analysis_date)

                result = fundamental_analyst.run(
                    stock=stock,
                    stock_price=daily_stock_price,
                    date=report_date,
                    experiment_metadata=experiment,
                )

                end_time = time.time()

                _save_results(
                    write_folder=experiment.write_folder,
                    stock_id=stock.stock_id,
                    analysis_date=analysis_date.strftime("%Y-%m-%d"),
                    agent_role="analyst",
                    result=result,
                    elapsed_time=end_time - start_time,
                    experiment_id=0,
                )

                # Get fundamental indicators
                fundamental_indicators = _parse_fundamental_analyst_output(
                    result, end_time - start_time
                )
                # Get price info
                price_info = _get_daily_price_info(
                    stock_id=stock.stock_id,
                    daily_stock_info=daily_stock_info[0],
                    report_date=report_date,
                )
                # Last manager decision
                last_manager_decision = _get_last_manager_decision(manager_decisions)

                fundamental_analyses.append(
                    {**fundamental_indicators, **price_info, **last_manager_decision}
                )

                indicators = pd.DataFrame(fundamental_analyses)
                indicators = indicators[
                    indicators["ACAO"] == stock.stock_id
                ].sort_values("DATA_DO_PREGAO")

                decision = financial_manager.run(
                    stock=stock,
                    stock_price=daily_stock_price,
                    date=analysis_date,
                    experiment_metadata=experiment,
                    indicators=indicators.to_string(),
                )

                end_time = time.time()

                _save_results(
                    write_folder=experiment.write_folder,
                    stock_id=stock.stock_id,
                    analysis_date=analysis_date.strftime("%Y-%m-%d"),
                    agent_role="manager",
                    result=decision,
                    elapsed_time=end_time - start_time,
                    experiment_id=0,
                )

                decision = _parse_financial_manager_output(
                    decision, analysis_date, end_time - start_time
                )
                manager_decisions.append(decision)

                with open(f"{experiment.write_folder}/results_sample.json", "w") as f:
                    json.dump(fundamental_analyses, f, indent=4)

                with open(f"{experiment.write_folder}/decisions_sample.json", "w") as f:
                    json.dump(manager_decisions, f, indent=4)
