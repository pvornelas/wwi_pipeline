import argparse
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    stock_item_holdings_df = pd.read_csv(args.dataset_path + "/Warehouse/Warehouse.StockItemHoldings.csv", delimiter=";")
    stock_item_holdings_df = stock_item_holdings_df.to_csv(args.output_path + "/fact_stock_holding.csv", sep=";", index=False)