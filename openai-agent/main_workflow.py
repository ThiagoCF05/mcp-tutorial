import experiments.investment_house.analyst as investment
import finbr.dias_uteis as dus

from datetime import datetime, timedelta
from db import get_stock_report, get_stock_composition, get_stock_daily_info
from experiments import ExperimentMetadata, Model, Intensity
from experiments.reinventa.config import STOCKS
from financial_agents.financial_analyst import (
    IndicatorOutput,
)


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
            daily_stock_price = get_stock_daily_info(
                stock_id=stock.stock_id, date=analysis_date
            )

            # Get last quarter reports of the stock (previous 3 months)
            report_date = get_last_stock_report_date(analysis_date)
            report = get_stock_report(cnpj=stock.cnpj, date=report_date)
            composition = get_stock_composition(cnpj=stock.cnpj, date=report_date)

            # Get previous reports of the stock (previous 6 months)
            previous_report_date = report_date - timedelta(days=90)
            previous_report = get_stock_report(
                cnpj=stock.cnpj, date=previous_report_date
            )
            previous_composition = get_stock_composition(
                cnpj=stock.cnpj, date=previous_report_date
            )

            # get first day of a month that is not weekend
            date = datetime(2023, month, 1)
            while date.weekday() > 4:
                date += timedelta(days=1)

            result = investment.run(
                stock=stock,
                stock_price=stock.price,
                date=date,
                experiment_metadata=experiment,
            )
            print(result.final_output)
