import argparse
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    stock_item_transactions_df = pd.read_csv(args.dataset_path + "/Warehouse/Warehouse.StockItemTransactions.csv", delimiter=";")
    stock_item_transactions_df.rename(columns={"TransactionOccurredWhen": "TransactionDate"}, inplace=True)
    stock_item_transactions_df = stock_item_transactions_df.to_csv(args.output_path + "/fact_movement.csv", sep=";", index=False)