import argparse
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    people_df = pd.read_csv(args.dataset_path + "/Application/Application.People.csv", delimiter=";")
    employee_df = people_df.query("IsEmployee == 1")
    employee_df = employee_df[["PersonID", "FullName", "PreferredName"]].rename(columns={
        "PersonID": "EmployeeID",
        "FullName": "Employee"
    })
    employee_df.to_csv(args.output_path + "/dim_employee.csv", index=False, sep=";")
