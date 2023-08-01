import argparse
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    payment_method_df = pd.read_csv(args.dataset_path + "/Application/Application.PaymentMethods.csv", delimiter=";")
    payment_method_df.rename(columns={"PaymentMethodName": "PaymentMethod"})
    payment_method_df.to_csv(args.output_path + "/dim_payment_method.csv", index=False, sep=";")