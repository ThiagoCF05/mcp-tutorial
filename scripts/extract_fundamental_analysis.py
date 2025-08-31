import json
import os

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import pandas as pd
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from tqdm import tqdm

def extract_stock_ids() -> list[str]:
    stock_ids = []
    for i in tqdm(range(43)):
        try:
            with sync_playwright() as p:
                browser = p.firefox.launch(headless=True)
                url = f"https://www.fundamentus.com.br/resultado.php?setor={i+1}"
                page = browser.new_page()
                page.goto(url)
                
                html = BeautifulSoup(page.inner_html(selector="#resultado"))
                trs = html.find("tbody").find_all("tr")
                for tr in trs:
                    row = [td.text.strip() for td in tr.find_all("td")]
                    stock_ids.append(row[0])
                browser.close()
        except Exception as e:
            logger.error(f"Error extracting stock ids for setor {i+1}: {e}")
        time.sleep(1)
    return stock_ids

def extract_fundamental_analysis(stock_id: str) -> dict:
    with sync_playwright() as p:
        url = f"https://www.fundamentus.com.br/detalhes.php?papel={stock_id}"
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        soup = BeautifulSoup(page.inner_html(selector=".conteudo"))
            
        columns_to_ignore = ["Dia", "Mês", "30 dias", "12 meses", "2025", "2024", "2023", "2022", "2021", "2020"]

        label, value = "Geral", None
        data = {}
        for td in soup.find_all("td"):
            class_ = td.attrs["class"]
            if "label" in class_:
                label = td.text.strip().replace("?", "")
            elif "data" in class_:
                value = td.text.strip().replace(".", "").replace(",", ".").replace("%", "").strip()
                try:
                    value = float(value)
                except:
                    pass
            else:
                label, value = None, None
            
            if label and value:
                if label in data:
                    label = f"{label} (3 meses)"
                if label not in columns_to_ignore:
                    data[label] = value
                label, value = None, None

        browser.close()
    
    return data

if __name__ == "__main__":
    logger.info("Extracting stock ids")
    if os.path.exists("stock_ids.json"):
        with open("stock_ids.json", "r") as f:
            stock_ids = json.load(f)
    else:
        stock_ids = extract_stock_ids()
        with open("stock_ids.json", "w") as f:
            json.dump(stock_ids, f)
    logger.info(f"Extracted {len(stock_ids)} stock ids")
    analysis = []
    for stock_id in tqdm(stock_ids):
        try:
            data = extract_fundamental_analysis(stock_id)
            analysis.append(data)
        except Exception as e:
            logger.error(f"Error extracting fundamental analysis for {stock_id}: {e}")
    df = pd.DataFrame(analysis)
    df = df.drop(columns=["2016", "2017", "2018", "2019"])
    df = df[~df["Últ balanço processado"].isin(["30/09/2022", "30/09/2021", "31/12/2021", "30/09/2023"])]
    df.to_csv("fundamental_analysis.csv", index=False)