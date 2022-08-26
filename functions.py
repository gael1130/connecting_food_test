# For downloads
import shutil
import urllib.request
import os

import pycountry
import pandas as pd


def download_file(url, local_file):
    # check if data folder exists, otherwise create it
    if not os.path.exists("data"):
        os.makedirs("data")
        print("data folder created")
    # if the file already exists, don't download it again
    if not os.path.exists(local_file):
        with urllib.request.urlopen(url) as response, open(local_file, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    else:
        print("File already exists. Skipping download.")


# checking the country code: refacto with a list of iso countries in a json file?
def unique_valid_iso_codes(unique_countries):
    valid_list = []
    for country_code in unique_countries:
        if pycountry.countries.get(alpha_2=country_code):
            # print(country_code, "is valid")
            valid_list.append(country_code)
        # else:
            # print(f"{country_code} is not a valid country code")
    return valid_list

# print(check_country_code("AF"))
# print(check_country_code("WW"))
# print(check_country_code("UK"))
# UK is not valid, it is "GB" now


def check_df_size(df, max_lines_amount, filepath):
    """
    Check the size of the dataframe and slice it if it is too big
    :return:
    """
    number_of_lines = df.shape[0]
    if number_of_lines > max_lines_amount:
        number_of_files = number_of_lines // max_lines_amount
        remainder = number_of_lines % max_lines_amount
        if remainder > 0:
            number_of_files += 1
            print(f"df is too big with {df.shape[0]} lines, it will be sliced into {number_of_files} files:\n"
                  f"{number_of_files - 1} files of {max_lines_amount} lines each,\n"
                  f"1 file of {remainder} lines.")
        else:
            print(f"df is too big with {df.shape[0]} lines, it will be sliced into "
                  f"{number_of_files} files of {max_lines_amount} lines each.")

        slice_df(df, max_lines_amount, number_of_files, remainder, filepath)

        return True
    else:
        # print(f"df is small enough with {df.shape[0]} lines.")
        return False


def slice_df(df, max_lines_amount, number_of_files, remainder, filepath):
    """
    Slice a dataframe into smaller dataframes with a certain amount of lines
    :param df:
    :param max_lines_amount:
    :param number_of_files:
    :param remainder:
    :return:
    """
    if remainder > 0:
        for i in range(number_of_files):
            if i == number_of_files - 1:
                df_slice = df.iloc[i * max_lines_amount: (i * max_lines_amount) + remainder]
                # print("number of rows in last file: ", df_slice.shape[0])
            else:
                df_slice = df.iloc[i * max_lines_amount: (i + 1) * max_lines_amount]
                # print("number of rows in current file: ", df_slice.shape[0])
            df_slice.to_csv(f"{filepath}_{i+1}.csv", header=False, index=False)
            # "sandbox_outputs/{formatted_date}_{elem.iloc[0]['destination_country_code']}.csv"

            print(f"{filepath}_{i+1}.csv has been written to file")
    else:
        for i in range(number_of_files):
            df_slice = df.iloc[i * max_lines_amount: (i + 1) * max_lines_amount]
            # print("number of rows in current file: ", df_slice.shape[0])
            df_slice.to_csv(f"{filepath}_{i+1}.csv", header=False, index=False)
            print(f"{filepath}_{i+1}.csv has been written to file")

    print(f"Big DF has been sliced and saved into smaller csv files of no more than {max_lines_amount} lines each")
    return f"Done"





