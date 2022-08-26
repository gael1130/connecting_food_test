import os
import time as t
from functions import *

start = t.time()

directories = ["data", "small_output", "medium_output", "large_output", "huge_output", "test_outputs"]
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"{directory} directory created")
    else:
        print(f"{directory} directory already exists")

# ======= download the files ===============
small_url = "https://media.githubusercontent.com/media/Connecting-Food/technical-test/master/small.csv"
medium_url = "https://media.githubusercontent.com/media/Connecting-Food/technical-test/master/medium.csv"
large_url = "https://media.githubusercontent.com/media/Connecting-Food/technical-test/master/large.csv"

download_list = [small_url, medium_url, large_url]
for url in download_list:
    download_file(url, "data/" + url.split("/")[-1])
# it took 70.62 to download the files 😱😱😱

# check if huge file exists, otherwise create it:
if not os.path.exists("data/huge.csv"):
    large_df = pd.read_csv("data/large.csv")
    list_df = []
    for i in range(11):
        list_df.append(large_df)

    huge_df = pd.concat(list_df)

    rows_in_millions = round((huge_df.shape[0] / 1000000), 1)
    print(f"the huge df just created from the large file has {rows_in_millions} million rows")
    huge_df.to_csv("data/huge.csv", index=False)

"""
print(f"it took {round((t.time() - start), 2)} seconds to create the directories and files")
# it took 47.13 seconds to create the directories and files (without download)
"""
# it took 127.69 seconds to do it all