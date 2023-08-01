import argparse
import pandas as pd
from datetime import datetime

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    orders_df = pd.read_csv(args.dataset_path + "/Sales/Sales.Orders.csv", delimiter=";")
    orders_df["OrderDate"] = pd.to_datetime(orders_df["OrderDate"], format="%d/%m/%Y")

    min_order_date: datetime = orders_df["OrderDate"].min()
    max_order_date: datetime = orders_df["OrderDate"].max()

    str_start_date = min_order_date.strftime("%d/%m/%Y")
    str_end_date = max_order_date.strftime("%d/%m/%Y")

    calendar_dim_df = pd.DataFrame({"Date": pd.date_range(str_start_date, str_end_date)})
    calendar_dim_df.to_csv(args.output_path + "/dim_calendar.csv", index=False, sep=";")