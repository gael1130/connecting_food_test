import pandas as pd
from functions import *
import time as t

# I want to measure the performance (time and memory)
start = t.time()
# Let's explore first, I am adding column names to understand data better
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

# I test the large df to see big differences in memory
# original_df = pd.read_csv("data/large.csv", names=column_names)
# print(original_df.dtypes)
"""                       before optimization | After (changing dtypes)
                Total Memory (deep) 455.33 Mb | 21.0 Mb
producer_id                 object | 70.57 Mb | 0.96
producer_name               object | 65.91 Mb | 0.96
product_id                  object | 59.13 Mb | 0.95
product_name                object | 59.92 Mb | 0.95
product_unit                object | 55.79 Mb | 0.95
quantity                     int64 | 7.63 Mb  | 3.81
specifications_id            int64 | 7.63 Mb  | 3.81
delivery_datetime           object | 72.48 Mb | 7.63
destination_country_code    object | 56.27 Mb | 0.95
"""
# print(f"Total memory usage (in MB, rounded to 2): {round(original_df.memory_usage(deep=True).sum() / 1024**2, 2)} MB")
# print(f"Memory usage by column (in MB, rounded to 2):\n{round(original_df.memory_usage(deep=True) / 1024**2, 2)} MB")
df = pd.read_csv("data/large.csv",
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

# print(f"Total memory usage (in MB, rounded to 2): {round(df.memory_usage(deep=True).sum() / 1024**2, 2)} MB")
# 21.0 MB
# print(f"Memory usage by column (in MB, rounded to 2):\n{round(df.memory_usage(deep=True) / 1024**2, 2)} MB")


""" counting the number of errors ('xxxxx') in product_id:
df["product_id"] = pd.to_numeric(df["product_id"], downcast="integer", errors="coerce")
if df["product_id"].isnull().sum():
    print(f"{df['product_id'].isnull().sum()} error values in product_id")

# 166'703 error values in product_id column for the large file.
"""

"""
# counting the number of unique values in destination_country_code:
print(f"unique values in destination_country_code: {df['destination_country_code'].nunique()}")
# 9
print("list of unique countries in destination_country_code:", df["destination_country_code"].unique())
# ['IT', 'WW', 'UK', 'BE', 'ES', 'CN', 'FR', 'DE', 'US']
# number of occurences of each unique value in destination_country_code:
print(f"number of occurences of each unique value in destination_country_code:\n{df['destination_country_code'].value_counts()}")
In the large file, there are multiple errors in iso codes:
UK    110'980
WW    110'839

"""
# Manipulating the data
unique_countries = df["destination_country_code"].unique()
iso_codes_list = unique_valid_iso_codes(unique_countries)

# what do we do for UK?
df = df.loc[(df["product_id"] == product_id) & (df["destination_country_code"].isin(iso_codes_list))]
# print(f"Total memory usage (in MB, rounded to 2): {round(df.memory_usage(deep=True).sum() / 1024**2, 2)} MB")
# 3.74 MB
# print(f"Memory usage by column (in MB, rounded to 2):\n{round(df.memory_usage(deep=True) / 1024**2, 2)} MB")
""" I just kept the most important values
Index                       0.99 Mb
delivery_datetime           0.99 Mb
"""
# After sorting values, the index are reorganized and take too much memory, so I drop it (it will reset it)
df.reset_index(drop=True, inplace=True)
# print(f"Total memory usage (in MB, rounded to 2): {round(df.memory_usage(deep=True).sum() / 1024**2, 2)} MB")
# 2.75 MB
# print(f"Memory usage by column (in MB, rounded to 2):\n{round(df.memory_usage(deep=True) / 1024**2, 2)} MB")
# Index                       0.00

# before I was converting with coerce the product_id to int, but this gives me empty rows (Nan) for the errors (xxxx)
# with category I do not have this issue, but I can keep it to see how many errors I have
# comparing different types for product_id:
"""
# print(df["product_id"].dtype)
# print(df["product_id"].memory_usage(deep=True))

# df["product_id"] = df["product_id"].astype("category")
# 1 170 458

# df["product_id"] = df["product_id"].astype(int)
# int32
# 1 560 384

# df["product_id"] = pd.to_numeric(df["product_id"], downcast="integer", errors="coerce")
# int16
# 1 300 320
"""

# sort values by destination first, then delivery datetime
df.sort_values(by=["destination_country_code", "delivery_datetime"], inplace=True)

# again the index is taking almost 1 MB of memory so I drop it
df.reset_index(drop=True, inplace=True)
# print(f"Total memory usage (in MB, rounded to 2): {round(df.memory_usage(deep=True).sum() / 1024**2, 2)} MB")
# # 2.75 MB
# print(f"Memory usage by column (in MB, rounded to 2):\n{round(df.memory_usage(deep=True) / 1024**2, 2)} MB")


# create a new df for each valid iso code:
list_df = []
for elem in df["destination_country_code"].unique():
    valid_df = df[df["destination_country_code"] == elem]
    list_df.append(valid_df)

# for each of those dfs, check the dates and create a new df for each date

max_lines_amount = 10000

for elem in list_df:
    unique_dates = elem["delivery_datetime"].dt.date.unique()
    country_code = elem.iloc[0]["destination_country_code"]

    for date in unique_dates:
        formatted_date = date.strftime("%Y%m%d")
        filepath = f"test_outputs/{formatted_date}_{country_code}"
        df_to_save = elem[elem["delivery_datetime"].dt.date == date]

        if check_df_size(df=df_to_save, max_lines_amount=max_lines_amount, filepath=filepath):
            print("*** slicing done ***")
        else:
            df_to_save.to_csv(f"{filepath}.csv",
                              header=False,
                              index=False)


print(f"it took {round((t.time() - start), 2)} seconds to run the script")
