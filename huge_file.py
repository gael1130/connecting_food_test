import pandas as pd
from functions import *
import time as t


start = t.time()
column_names = [
    "producer_id",
    "producer_name",
    "product_id",
    "product_name",
    "product_unit",
    "quantity",
    "specifications_id",
    "delivery_datetime",
    "destination_country_code"
]
product_id = '10001'
max_lines_amount = 10000

df = pd.read_csv("data/huge.csv",
                 names=column_names,
                 dtype={
                     "producer_id": "category",
                     "producer_name": "category",
                     "product_id": "category",
                     "product_name": "category",
                     "product_unit": "category",
                     "quantity": "int32",
                     "specifications_id": "int32",
                     # "delivery_datetime": "datetime64[ns]",
                     "destination_country_code": "category"},
                 parse_dates=["delivery_datetime"],
                 )

# Keeping only valid data
unique_countries = df["destination_country_code"].unique()
iso_codes_list = unique_valid_iso_codes(unique_countries)

# what do we do for UK?
df = df.loc[(df["product_id"] == product_id) & (df["destination_country_code"].isin(iso_codes_list))]
df.reset_index(drop=True, inplace=True)

df.sort_values(by=["destination_country_code", "delivery_datetime"], inplace=True)
df.reset_index(drop=True, inplace=True)

# create a new df for each valid iso code in order to save it as csv:
list_df = []
for elem in df["destination_country_code"].unique():
    valid_df = df[df["destination_country_code"] == elem]
    list_df.append(valid_df)

# for each of those dfs, check the dates and create a new df for each date
for elem in list_df:
    unique_dates = elem["delivery_datetime"].dt.date.unique()
    country_code = elem.iloc[0]["destination_country_code"]

    for date in unique_dates:
        formatted_date = date.strftime("%Y%m%d")
        filepath = f"huge_output/{formatted_date}_{country_code}"
        df_to_save = elem[elem["delivery_datetime"].dt.date == date]

        if check_df_size(df=df_to_save, max_lines_amount=max_lines_amount, filepath=filepath):
            print("*** slicing done ***")
        else:
            df_to_save.to_csv(f"{filepath}.csv",
                              header=False,
                              index=False)

print(f"it took {round((t.time() - start), 2)} seconds to run the script")
