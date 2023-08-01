import argparse
import pandas as pd
from pandas.api.types import is_object_dtype

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    stock_item_df = pd.read_csv(args.dataset_path + "/Warehouse/Warehouse.StockItems.csv", delimiter=";")
    colors_df = pd.read_csv(args.dataset_path + "/Warehouse/Warehouse.Colors.csv", delimiter=";")
    package_types_df = pd.read_csv(args.dataset_path + "/Warehouse/Warehouse.PackageTypes.csv", delimiter=";")

    colors_df.rename(columns={"ColorName": "Color"}, inplace=True)
    package_type_mapper = package_types_df.set_index('PackageTypeID')['PackageTypeName'].to_dict()

    stock_item_df = stock_item_df.merge(colors_df, how="left", on="ColorID")
    stock_item_df['SellingPackage'] = stock_item_df["UnitPackageID"].map(package_type_mapper)
    stock_item_df['BuyingPackage'] = stock_item_df["OuterPackageID"].map(package_type_mapper)

    stock_item_df.rename(columns={"StockItemName": "StockItem"}, inplace=True)
    stock_item_df = stock_item_df[["StockItemID", "StockItem", "Color", "SellingPackage", "BuyingPackage",
                                   "Brand", "Size", "LeadTimeDays", "QuantityPerOuter", "IsChillerStock",
                                   "Barcode", "TaxRate", "UnitPrice", "RecommendedRetailPrice",
                                   "TypicalWeightPerUnit"]]

    for col in stock_item_df.columns:
        if is_object_dtype(stock_item_df[col]):
            stock_item_df[col].fillna(value="N/A", inplace=True)

    stock_item_df.to_csv(args.output_path + "/dim_stock_item.csv", index=False, sep=";")