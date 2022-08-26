import time as t
start = t.time()
# import config
# import small_file
# import medium_file
# import large_file
# import huge_file


print("all done")
print(f"it took {round((t.time() - start), 2)} seconds to do it all")
# 113.41 seconds for config from scratch (download included)
# 1.04 seconds for smaller_file | 0.16 seconds
# 1.62 seconds for medium_file  | 0.43 seconds after optimization
# 6.91 seconds for large_file   | 3.0 seconds after optimization
# 83.19 seconds for huge_file   | 32.84 seconds after optimization
