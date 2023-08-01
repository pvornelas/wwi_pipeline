import argparse
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("output_path", type=str)
    args = parser.parse_args()

    cities_df = pd.read_csv(args.dataset_path + "/Application/Application.Cities.csv", sep=";")
    countries_df = pd.read_csv(args.dataset_path + "/Application/Application.Countries.csv", sep=";")
    state_provinces_df = pd.read_csv(args.dataset_path + "/Application/Application.StateProvinces.csv", sep=";")

    countries_df = countries_df[["CountryID", "CountryName", "Continent"]]
    state_provinces_df = state_provinces_df.merge(countries_df, how="left", on="CountryID")

    state_provinces_df.drop(labels=["CountryID"], axis=1, inplace=True)
    cities_df.to_csv(args.output_path + "/dim_city.csv", index=False, sep=";")
    state_provinces_df.to_csv(args.output_path + "/dim_state_province.csv", index=False, sep=";")