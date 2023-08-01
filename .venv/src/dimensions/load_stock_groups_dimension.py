import argparse
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    stock_groups_df = pd.read_csv(args.dataset_path + "/Warehouse/Warehouse.StockGroups.csv", delimiter=";")
    stock_item_stock_groups_df = pd.read_csv(args.dataset_path + "/Warehouse/Warehouse.StockItemStockGroups.csv", delimiter=";")

    stock_groups_df.to_csv(args.output_path + "/dim_stock_groups.csv", index=False, sep=";")
    stock_item_stock_groups_df.to_csv(args.output_path + "/dim_stock_item_stock_groups.csv", index=False, sep=";")