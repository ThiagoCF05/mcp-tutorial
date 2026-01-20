import experiments.investment_house.analyst as investment
import finbr.dias_uteis as dus

from datetime import datetime, timedelta
from db import get_stock_daily_info
from db.base_query import ResponseFormat
from experiments import ExperimentMetadata, Model, Intensity
from experiments.reinventa.config import STOCKS
from financial_agents.financial_analyst import (
    IndicatorOutput,
)
from dotenv import load_dotenv

load_dotenv()


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


if __name__ == "__main__":
    experiment = ExperimentMetadata(
        model=Model.GPT_5_MINI,
        write_folder="./",
        max_turns=30,
        structured_output=IndicatorOutput.model_json_schema(),
        reasoning=Intensity.MEDIUM,
        verbosity=Intensity.MEDIUM,
        reflection=True,
    )
    for year in [2024, 2025]:
        for month in range(1, 12):
            analysis_date = _get_first_workday(year, month)
            stock = STOCKS[1]

            # Get stock price in the day
            daily_stock_info = get_stock_daily_info(
                stock_id=stock.stock_id,
                date=analysis_date,
                response_format=ResponseFormat.DICT,
            )
            if len(daily_stock_info) == 0:
                continue
            daily_stock_price = float(daily_stock_info[0]["PRECO_DE_ABERTURA"])

            # Get last quarter reports date (previous 3 months)
            report_date = get_last_stock_report_date(analysis_date)

            result = investment.run(
                stock=stock,
                stock_price=daily_stock_price,
                date=report_date,
                experiment_metadata=experiment,
            )
            print(result.final_output)
