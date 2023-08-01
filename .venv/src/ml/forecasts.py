import os
import pandas as pd
import numpy as np
import argparse
from prophet import Prophet

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    sales = pd.read_csv(os.path.join(args.output_path, "fact_order_sale.csv"), sep=";")

    # Pré-Processamento
    sales = sales[sales["InvoiceDate"].notna()]
    sales["OrderDate"] = pd.to_datetime(sales["OrderDate"], format="%Y-%m-%d")

    historico_faturamento = sales[["OrderDate", "TotalIncludingTax"]].groupby(["OrderDate"]).agg({"TotalIncludingTax": "sum"}).reset_index()
    historico_faturamento.sort_values(by="OrderDate", inplace=True, ignore_index=True)

    historico_lucro = sales[["OrderDate", "LineProfit"]].groupby(["OrderDate"]).agg({"LineProfit": "sum"}).reset_index()
    historico_lucro.sort_values(by="OrderDate", inplace=True, ignore_index=True)

    historico_vendas = sales[["OrderDate", "InvoiceID"]].groupby(["OrderDate"]).agg({"InvoiceID": pd.Series.nunique}).reset_index()
    historico_vendas.sort_values(by="OrderDate", inplace=True, ignore_index=True)

    historico_faturamento.rename(columns={'OrderDate': 'ds', 'TotalIncludingTax': 'y'}, inplace=True)
    historico_lucro.rename(columns={'OrderDate': 'ds', 'LineProfit': 'y'}, inplace=True)
    historico_vendas.rename(columns={'OrderDate': 'ds', 'InvoiceID': 'y'}, inplace=True)

    # Previsão de faturamento
    model_faturamento = Prophet()
    model_faturamento.fit(historico_faturamento)

    future_revenue = model_faturamento.make_future_dataframe(periods=365)
    previsao_faturamento = model_faturamento.predict(future_revenue)

    # Previsão de lucro
    model_lucro = Prophet()
    model_lucro.fit(historico_lucro)

    future_profit = model_lucro.make_future_dataframe(periods=365)
    previsao_lucro = model_lucro.predict(future_profit)

    # Previsão de vendas
    model_vendas = Prophet()
    model_vendas.fit(historico_vendas)

    future_sales = model_vendas.make_future_dataframe(periods=365)
    previsao_vendas = model_vendas.predict(future_sales)

    max_date = sales["OrderDate"].max()
    previsao_faturamento = previsao_faturamento[(previsao_faturamento["ds"] > max_date)][["ds", "yhat"]]
    previsao_lucro = previsao_lucro[(previsao_lucro["ds"] > max_date)][["ds", "yhat"]]
    previsao_vendas = previsao_vendas[(previsao_vendas["ds"] > max_date)][["ds", "yhat"]]

    previsao_faturamento.rename(columns={"ds": "ForecastDate", "yhat": "RevenueForecast"}, inplace=True)
    previsao_lucro.rename(columns={"ds": "ForecastDate", "yhat": "ProfitForecast"}, inplace=True)
    previsao_vendas.rename(columns={"ds": "ForecastDate", "yhat": "SalesForecast"}, inplace=True)

    resultado = pd.merge(previsao_faturamento, previsao_lucro, how="inner", on="ForecastDate")
    resultado = pd.merge(resultado, previsao_vendas, how="inner", on="ForecastDate")
    resultado["RevenueForecast"] = resultado["RevenueForecast"].round(2)
    resultado["ProfitForecast"] = resultado["ProfitForecast"].round(2)
    resultado["SalesForecast"] = resultado["SalesForecast"].astype(np.int64)
    resultado.to_csv(os.path.join(args.output_path, "fact_forecast.csv"), index=False, sep=";")