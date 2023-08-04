import os
import pandas as pd
import argparse
from prophet import Prophet
from datetime import datetime
from sklearn.metrics import mean_absolute_percentage_error

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
    train_data_faturamento = historico_faturamento[historico_faturamento['ds'] < datetime(2015, 1, 1)]
    test_data_faturamento = historico_faturamento[historico_faturamento['ds'] >= datetime(2015, 1, 1)]

    model_faturamento = Prophet(weekly_seasonality=True)
    model_faturamento.fit(train_data_faturamento)

    future_revenue = model_faturamento.make_future_dataframe(periods=517, include_history=False)
    previsao_faturamento = model_faturamento.predict(future_revenue)

    previsao_faturamento = previsao_faturamento[previsao_faturamento["ds"].isin(test_data_faturamento["ds"])]

    mape_faturamento = mean_absolute_percentage_error(test_data_faturamento["y"], previsao_faturamento["yhat"])
    print(mape_faturamento)

    # Previsão Lucro
    train_data_lucro = historico_lucro[historico_lucro['ds'] < datetime(2015, 1, 1)]
    test_data_lucro = historico_lucro[historico_lucro['ds'] >= datetime(2015, 1, 1)]

    model_lucro = Prophet(weekly_seasonality=True)
    model_lucro.fit(train_data_lucro)

    future_profit = model_lucro.make_future_dataframe(periods=517, include_history=False)
    previsao_lucro = model_lucro.predict(future_profit)

    previsao_lucro = previsao_lucro[previsao_lucro["ds"].isin(test_data_lucro["ds"])]

    mape_lucro = mean_absolute_percentage_error(test_data_lucro["y"], previsao_lucro["yhat"])
    print(mape_lucro)

    # Previsão Vendas
    train_data_vendas = historico_vendas[historico_vendas['ds'] < datetime(2015, 1, 1)]
    test_data_vendas = historico_vendas[historico_vendas['ds'] >= datetime(2015, 1, 1)]

    model_vendas = Prophet(weekly_seasonality=True)
    model_vendas.fit(train_data_vendas)

    future_sales = model_vendas.make_future_dataframe(periods=517, include_history=False)
    previsao_vendas = model_vendas.predict(future_sales)

    previsao_vendas = previsao_vendas[previsao_vendas["ds"].isin(test_data_vendas["ds"])]

    mape_vendas = mean_absolute_percentage_error(test_data_vendas["y"], previsao_vendas["yhat"])
    print(mape_vendas)