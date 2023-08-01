import os
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

path = "/home/pvini/projeto/.venv/data/base"

def consulta_faturamento_lucro_e_vendas(mes_ano: datetime):
    orders_df = pd.read_csv(os.path.join(path, "Sales/Sales.Orders.csv"), sep=";")
    orders_df["OrderDate"] = pd.to_datetime(orders_df["OrderDate"], format="%d/%m/%Y")
    orders_selected = orders_df[(orders_df["OrderDate"].dt.month == mes_ano.month) & (orders_df["OrderDate"].dt.year == mes_ano.year)]
    mes_anterior = mes_ano - relativedelta(months=1)
    orders_previous_month = orders_df[(orders_df["OrderDate"].dt.month == mes_anterior.month) & (orders_df["OrderDate"].dt.year == mes_anterior.year)]

    invoices_df = pd.read_csv(os.path.join(path, "Sales/Sales.Invoices.csv"), sep=";")
    invoice_ids = invoices_df[invoices_df["OrderID"].isin(orders_selected["OrderID"])]["InvoiceID"]
    previous_invoice_ids = invoices_df[invoices_df["OrderID"].isin(orders_previous_month["OrderID"])]["InvoiceID"]

    invoice_lines_df_base = pd.read_csv(os.path.join(path, "Sales/Sales.InvoiceLines.csv"), sep=";")
    invoice_lines_df = invoice_lines_df_base[invoice_lines_df_base["InvoiceID"].isin(invoice_ids)]
    previous_invoice_lines_df = invoice_lines_df_base[invoice_lines_df_base["InvoiceID"].isin(previous_invoice_ids)]

    faturamento = invoice_lines_df["ExtendedPrice"].sum()
    imposto = invoice_lines_df["TaxAmount"].sum()
    faturamento_liquido = faturamento - imposto
    lucro = invoice_lines_df["LineProfit"].sum()
    vendas = invoice_lines_df["InvoiceID"].nunique()

    faturamento_anterior = previous_invoice_lines_df["ExtendedPrice"].sum()
    lucro_anterior = previous_invoice_lines_df["LineProfit"].sum()
    vendas_anterior = previous_invoice_lines_df["InvoiceID"].nunique()
    pc_faturamento = (faturamento - faturamento_anterior) / faturamento_anterior
    pc_lucro = (lucro - lucro_anterior) / lucro_anterior
    pc_vendas = (vendas - vendas_anterior) / vendas_anterior

    return (faturamento, imposto, faturamento_liquido, lucro, vendas, pc_faturamento, pc_lucro, pc_vendas)

def consulta_tooltip_regiao(periodo_inicio: datetime, periodo_fim: datetime, categoria: int):
    orders_df = pd.read_csv(os.path.join(path, "Sales/Sales.Orders.csv"), sep=";")
    orders_df["OrderDate"] = pd.to_datetime(orders_df["OrderDate"], format="%d/%m/%Y")
    orders_selected = orders_df[(orders_df["OrderDate"] >= periodo_inicio) & (orders_df["OrderDate"] <= periodo_fim)]

    customers = pd.read_csv(os.path.join(path, "Sales/Sales.Customers.csv"), sep=";")
    customers_ids = customers[(customers["CustomerCategoryID"] == categoria)]["CustomerID"]

    invoices_df = pd.read_csv(os.path.join(path, "Sales/Sales.Invoices.csv"), sep=";")
    invoice_ids = invoices_df[invoices_df["OrderID"].isin(orders_selected["OrderID"]) & invoices_df["CustomerID"].isin(customers_ids)]["InvoiceID"]

    invoice_lines_df = pd.read_csv(os.path.join(path, "Sales/Sales.InvoiceLines.csv"), sep=";")
    invoice_lines_df = invoice_lines_df[invoice_lines_df["InvoiceID"].isin(invoice_ids)]

    faturamento = invoice_lines_df["ExtendedPrice"].sum()
    imposto = invoice_lines_df["TaxAmount"].sum()
    faturamento_liquido = faturamento - imposto
    lucro = invoice_lines_df["LineProfit"].sum()
    vendas = invoice_lines_df["InvoiceID"].nunique()
    margem_de_lucro = lucro / faturamento
    ticket_medio = faturamento / vendas

    return (faturamento, imposto, faturamento_liquido, lucro, vendas, margem_de_lucro, ticket_medio)

def consulta_produto_em_nivel_de_reabastecimento():
    estoque = pd.read_csv(os.path.join(path, "Warehouse/Warehouse.StockItemHoldings.csv"), sep=";")
    estoque["Nivel"] = estoque["QuantityOnHand"] / estoque["ReorderLevel"]
    estoque = estoque[(estoque["Nivel"] < 1)]
    print(estoque)
    estoque.sort_values(by="QuantityOnHand", inplace=True, ignore_index=True)
    item_id = estoque.iloc[0]["StockItemID"]
    item = pd.read_csv(os.path.join(path, "Warehouse/Warehouse.StockItems.csv"), sep=";")
    descricao = item[(item["StockItemID"] == item_id)].iloc[0]["StockItemName"]
    quantidade = estoque.iloc[0]["QuantityOnHand"]
    nivel_de_reabastecimento = estoque.iloc[0]["ReorderLevel"]
    return (descricao, quantidade, nivel_de_reabastecimento)