import argparse
import pandas as pd
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    order_lines_df = pd.read_csv(args.dataset_path + "/Sales/Sales.OrderLines.csv", delimiter=";")
    orders_df = pd.read_csv(args.dataset_path + "/Sales/Sales.Orders.csv", delimiter=";")
    invoice_lines_df = pd.read_csv(args.dataset_path + "/Sales/Sales.InvoiceLines.csv", delimiter=";")
    invoices_df = pd.read_csv(args.dataset_path + "/Sales/Sales.Invoices.csv", delimiter=";")
    package_type_df = pd.read_csv(args.dataset_path + "/Warehouse/Warehouse.PackageTypes.csv", delimiter=";")
    customer_df = pd.read_csv(args.dataset_path + "/Sales/Sales.Customers.csv", sep=";")

    invoice_lines_df = invoice_lines_df[["InvoiceID", "StockItemID", "Description", "PackageTypeID", "TaxRate", "TaxAmount", "LineProfit",
                                          "ExtendedPrice", "Quantity", "UnitPrice"]]
    invoices_df = invoices_df[["InvoiceID", "CustomerID", "OrderID", "InvoiceDate", "TotalDryItems", "TotalChillerItems",
                                "ConfirmedDeliveryTime", "SalespersonPersonID"]]

    orders_df = orders_df[["OrderID", "BackorderOrderID", "OrderDate", "ExpectedDeliveryDate", "PickingCompletedWhen", "PickedByPersonID"]]

    invoices_df = invoices_df.merge(orders_df, how="left", on="OrderID")
    invoice_lines_df = invoice_lines_df.merge(invoices_df, how="left", on="InvoiceID")

    customer_city_mapper = customer_df.set_index("CustomerID")["DeliveryCityID"].to_dict()
    invoice_lines_df["CityID"] = invoice_lines_df['CustomerID'].map(customer_city_mapper)

    package_type_mapper = package_type_df.set_index("PackageTypeID")["PackageTypeName"].to_dict()
    invoice_lines_df['Package'] = invoice_lines_df['PackageTypeID'].map(package_type_mapper)

    invoice_lines_df = invoice_lines_df[["InvoiceID", "OrderID", "BackorderOrderID", "CustomerID", "CityID", "StockItemID",
                                     "Description", "Package", "OrderDate", "ExpectedDeliveryDate", "PickingCompletedWhen",
                                     "InvoiceDate", "ConfirmedDeliveryTime", "SalespersonPersonID", "PickedByPersonID", "Quantity", "TotalDryItems",
                                     "TotalChillerItems", "UnitPrice", "TaxRate", "TaxAmount", "LineProfit", "ExtendedPrice"]]

    invoice_lines_df.rename(columns={
        "PickingCompletedWhen": "PickedDate",
        "SalespersonPersonID": "SalespersonID",
        "PickedByPersonID": "PickerID",
        "ExtendedPrice": "TotalIncludingTax"
    }, inplace=True)

    invoice_lines_df["OrderDate"] = pd.to_datetime(invoice_lines_df["OrderDate"], format="%d/%m/%Y")
    invoice_lines_df["ExpectedDeliveryDate"] = pd.to_datetime(invoice_lines_df["ExpectedDeliveryDate"], format="%d/%m/%Y")
    invoice_lines_df["InvoiceDate"] = pd.to_datetime(invoice_lines_df["InvoiceDate"], format="%d/%m/%Y")
    invoice_lines_df["PickedDate"] = pd.to_datetime(invoice_lines_df["PickedDate"], format="%Y-%m-%d %H:%M:%S.%f")
    invoice_lines_df["ConfirmedDeliveryTime"] = pd.to_datetime(invoice_lines_df["ConfirmedDeliveryTime"], format="%Y-%m-%d %H:%M:%S.%f")

    conversor = {
        "InvoiceID": np.int64,
        "BackorderOrderID": np.int64,
        "PickerID": np.int64,
        "TotalDryItems": np.int64,
        "TaxRate": np.float64,
        "TaxAmount": np.float64,
        "TotalChillerItems": np.int64,
        "LineProfit": np.float64,
        "TotalIncludingTax": np.float64,
    }

    for key in conversor:
        invoice_lines_df[key].fillna(0, inplace=True)
        invoice_lines_df[key] = invoice_lines_df[key].astype(conversor[key])

    invoice_lines_df.to_csv(args.output_path + "/fact_order_sale.csv", sep=";", index=False)