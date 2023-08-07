import os
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

path = "/home/pvini/projeto/.venv/data/base"

def consulta_faturamento_lucro_e_vendas(mes_ano: datetime):
    invoice_lines_df_base = pd.read_csv(os.path.join(path, "Sales/Sales.InvoiceLines.csv"), sep=";")
    invoices_df = pd.read_csv(os.path.join(path, "Sales/Sales.Invoices.csv"), sep=";")

    invoices_df["InvoiceDate"] = pd.to_datetime(invoices_df["InvoiceDate"], format="%d/%m/%Y")
    mes_anterior = mes_ano - relativedelta(months=1)

    filtro_mes_atual = ((invoices_df["InvoiceDate"].dt.month == mes_ano.month) & (invoices_df["InvoiceDate"].dt.year == mes_ano.year))
    filtro_mes_anterior = ((invoices_df["InvoiceDate"].dt.month == mes_anterior.month) & (invoices_df["InvoiceDate"].dt.year == mes_anterior.year))

    ids_mes_atual = invoices_df[filtro_mes_atual]["InvoiceID"]
    ids_mes_anterior = invoices_df[filtro_mes_anterior]["InvoiceID"]

    invoice_lines_df = invoice_lines_df_base[invoice_lines_df_base["InvoiceID"].isin(ids_mes_atual)]
    previous_invoice_lines_df = invoice_lines_df_base[invoice_lines_df_base["InvoiceID"].isin(ids_mes_anterior)]

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

def consulta_categoria_cliente(periodo_inicio: datetime, periodo_fim: datetime, categoria: int):
    invoice_lines_df = pd.read_csv(os.path.join(path, "Sales/Sales.InvoiceLines.csv"), sep=";")
    invoices_df = pd.read_csv(os.path.join(path, "Sales/Sales.Invoices.csv"), sep=";")
    invoices_df["InvoiceDate"] = pd.to_datetime(invoices_df["InvoiceDate"], format="%d/%m/%Y")

    customers = pd.read_csv(os.path.join(path, "Sales/Sales.Customers.csv"), sep=";")
    customers_ids = customers[(customers["CustomerCategoryID"] == categoria)]["CustomerID"]

    filtro = ((invoices_df["InvoiceDate"] >= periodo_inicio) & (invoices_df["InvoiceDate"]<= periodo_fim) & invoices_df["CustomerID"].isin(customers_ids))

    vendas_periodo = invoices_df[filtro]["InvoiceID"]
    invoice_lines_df = invoice_lines_df[invoice_lines_df["InvoiceID"].isin(vendas_periodo)]

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
    estoque.sort_values(by="QuantityOnHand", inplace=True, ignore_index=True)

    item_id = estoque.iloc[0]["StockItemID"]
    item = pd.read_csv(os.path.join(path, "Warehouse/Warehouse.StockItems.csv"), sep=";")
    descricao = item[(item["StockItemID"] == item_id)].iloc[0]["StockItemName"]
    quantidade = estoque.iloc[0]["QuantityOnHand"]
    nivel_de_reabastecimento = estoque.iloc[0]["ReorderLevel"]
    return (descricao, quantidade, nivel_de_reabastecimento)

def consulta_lead_time(data: datetime):
    orders_df = pd.read_csv(os.path.join(path, "Sales/Sales.Orders.csv"), sep=";")
    invoices_df = pd.read_csv(os.path.join(path, "Sales/Sales.Invoices.csv"), sep=";")

    invoices_df = invoices_df[["InvoiceID", "OrderID", "InvoiceDate",  "ConfirmedDeliveryTime"]]
    orders_df = orders_df[["OrderID", "OrderDate", "ExpectedDeliveryDate"]]

    invoices_df = invoices_df.merge(orders_df, how="left", on="OrderID")

    invoices_df["InvoiceDate"] = pd.to_datetime(invoices_df["InvoiceDate"], format="%d/%m/%Y")
    invoices_df = invoices_df[invoices_df["ConfirmedDeliveryTime"].notna()]

    invoices_df["OrderDate"] = pd.to_datetime(invoices_df["OrderDate"], format="%d/%m/%Y")
    invoices_df["ExpectedDeliveryDate"] = pd.to_datetime(invoices_df["ExpectedDeliveryDate"], format="%d/%m/%Y")
    invoices_df["ConfirmedDeliveryTime"] = pd.to_datetime(invoices_df["ConfirmedDeliveryTime"], format="%Y-%m-%d %H:%M:%S.%f")

    invoices_df["LeadTime"] = (invoices_df["ConfirmedDeliveryTime"] - invoices_df["OrderDate"]).dt.days
    invoices_df["LeadTimeEsperado"] = (invoices_df["ExpectedDeliveryDate"] - invoices_df["OrderDate"]).dt.days

    lead_time = invoices_df[(invoices_df["InvoiceDate"] == data)]["LeadTime"].mean()
    lead_time_esperado = invoices_df[(invoices_df["InvoiceDate"] == data)]["LeadTimeEsperado"].mean()

    return (round(lead_time), round(lead_time_esperado))

def consulta_dados_do_mapa(regiao: int):
    invoices_df = pd.read_csv(os.path.join(path, "Sales/Sales.Invoices.csv"), sep=";")
    invoice_lines_df = pd.read_csv(os.path.join(path, "Sales/Sales.InvoiceLines.csv"), sep=";")

    customers = pd.read_csv(os.path.join(path, "Sales/Sales.Customers.csv"), sep=";")
    customers = customers[["CustomerID", "DeliveryCityID"]]

    invoices_df = invoices_df.merge(customers, how="left", on="CustomerID")

    cities = pd.read_csv(os.path.join(path, "Application/Application.Cities.csv"), sep=";")
    cities = cities[["CityID", "StateProvinceID"]].rename(columns={"CityID": "DeliveryCityID"})

    invoices_df = invoices_df.merge(cities, how="left", on="DeliveryCityID")
    invoice_lines_df = invoice_lines_df.merge(invoices_df, how="left", on="InvoiceID")

    dados_geral = invoice_lines_df.groupby("StateProvinceID").agg({
        "ExtendedPrice": 'sum',
    }).reset_index().rename(columns={
        "ExtendedPrice": "Faturamento",
    })

    faturamento_geral = dados_geral["Faturamento"].sum()

    dados_florida = invoice_lines_df[(invoice_lines_df["StateProvinceID"] == regiao)].agg({
        "ExtendedPrice": 'sum',
        "TaxAmount": 'sum',
        "LineProfit": 'sum',
        "CustomerID": lambda x: len(x.unique()),
        "InvoiceID": lambda x: len(x.unique()),
    }).rename(index={
        "ExtendedPrice": "Faturamento",
        "TaxAmount": "Imposto",
        "LineProfit": "Lucro",
        "CustomerID": "Total Clientes",
        "InvoiceID": "Total Vendas"
    })
    pc_participacao = (dados_florida["Faturamento"] / faturamento_geral).round(5)
    dados_florida["% Participação no Faturamento"] = pc_participacao
    dados_florida["Faturamento Líquido"] = dados_florida["Faturamento"] - dados_florida["Imposto"]
    return dados_florida

def consulta_participacao_empregado_faturamento(id_vendedor: int):
    invoices_df = pd.read_csv(os.path.join(path, "Sales/Sales.Invoices.csv"), sep=";")
    invoice_lines_df = pd.read_csv(os.path.join(path, "Sales/Sales.InvoiceLines.csv"), sep=";")

    invoice_lines_df = invoice_lines_df.merge(invoices_df, how="left", on="InvoiceID")

    faturamento_total = invoice_lines_df["ExtendedPrice"].sum()
    faturamento_funcionario = invoice_lines_df[(invoice_lines_df["SalespersonPersonID"] == id_vendedor)]["ExtendedPrice"].sum()
    return round(faturamento_funcionario / faturamento_total, 4)

def consulta_media_de_saida_do_produto(id_produto: int):
    estoque = pd.read_csv(os.path.join(path, "Warehouse/Warehouse.StockItemTransactions.csv"), sep=";")
    saidas = estoque[(estoque["TransactionTypeID"] == 10) & (estoque["StockItemID"] == id_produto)]["Quantity"].mean()
    return round(abs(saidas), 2)