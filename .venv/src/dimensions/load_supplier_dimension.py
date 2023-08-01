import argparse
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    suppliers_df = pd.read_csv(args.dataset_path + "/Purchasing/Purchasing.Suppliers.csv", delimiter=";")
    suppliers_category_df = pd.read_csv(args.dataset_path + "/Purchasing/Purchasing.SupplierCategories.csv", delimiter=";")
    people_df = pd.read_csv(args.dataset_path + "/Application/Application.People.csv", delimiter=";")

    suppliers_category_df.rename(columns={"SupplierCategoryName": "Category"}, inplace=True)
    people_df = people_df[["PersonID", "FullName"]].rename(columns={
        "PersonID": "PrimaryContactPersonID",
        "FullName": "PrimaryContact"
    })

    suppliers_df = suppliers_df.merge(suppliers_category_df, how="left", on="SupplierCategoryID")
    suppliers_df = suppliers_df.merge(people_df, how="left", on="PrimaryContactPersonID")

    suppliers_df.rename(columns={"SupplierName": "Supplier"}, inplace=True)
    suppliers_df = suppliers_df[["SupplierID", "Supplier", "Category", "PrimaryContact",
                                  "PaymentDays", "DeliveryLocationLat", "DeliveryLocationLong"]]

    suppliers_df["DeliveryLocationLat"] = suppliers_df["DeliveryLocationLat"].str.replace(",", ".")
    suppliers_df["DeliveryLocationLong"] = suppliers_df["DeliveryLocationLong"].str.replace(",", ".")

    suppliers_df.to_csv(args.output_path + "/dim_suppliers.csv", index=False, sep=";")