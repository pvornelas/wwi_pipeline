import argparse
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    transaction_type_df = pd.read_csv(args.dataset_path + "/Application/Application.TransactionTypes.csv", delimiter=";")
    transaction_type_df.rename(columns={"TransactionTypeName": "TransactionType"}, inplace=True)
    transaction_type_df.to_csv(args.output_path + "/dim_transaction_type.csv", index=False, sep=";")