import argparse
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    customer_df = pd.read_csv(args.dataset_path + "/Sales/Sales.Customers.csv", delimiter=";")
    buying_groups_df = pd.read_csv(args.dataset_path + "/Sales/Sales.BuyingGroups.csv", delimiter=";")
    customer_category_df = pd.read_csv(args.dataset_path + "/Sales/Sales.CustomerCategories.csv", delimiter=";")
    people_df = pd.read_csv(args.dataset_path + "/Application/Application.People.csv", delimiter=";")

    buying_groups_df = buying_groups_df[["BuyingGroupID", "BuyingGroupName"]]
    customer_category_df = customer_category_df[["CustomerCategoryID", "CustomerCategoryName"]]
    people_df = people_df[["PersonID", "FullName"]].rename(columns={"PersonID": "PrimaryContactPersonID", "FullName": "PrimaryContact"})
    bill_to_customer_df = customer_df[["CustomerID", "CustomerName"]].rename(columns={"CustomerID": "BillToCustomerID", "CustomerName": "BillToCustomer"})

    customer_df = customer_df.merge(bill_to_customer_df, how="left", on="BillToCustomerID")
    customer_df = customer_df.merge(buying_groups_df, how="left", on="BuyingGroupID")
    customer_df = customer_df.merge(customer_category_df, how="left", on="CustomerCategoryID")
    customer_df = customer_df.merge(people_df, how="left", on="PrimaryContactPersonID")

    customer_df = customer_df[["CustomerID", "CustomerName", "BillToCustomer", "CustomerCategoryName", "BuyingGroupName", "PrimaryContact", "DeliveryLocationLat", "DeliveryLocationLong"]]
    customer_df["DeliveryLocationLat"] = customer_df["DeliveryLocationLat"].str.replace(",", ".")
    customer_df["DeliveryLocationLong"] = customer_df["DeliveryLocationLong"].str.replace(",", ".")
    customer_df.rename(columns={
        "CustomerName": "Customer",
        "CustomerCategoryName": "Category",
        "BuyingGroupName": "BuyingGroup"
    }, inplace=True)

    customer_df.to_csv(args.output_path + "/dim_customer.csv", index=False, sep=";")
