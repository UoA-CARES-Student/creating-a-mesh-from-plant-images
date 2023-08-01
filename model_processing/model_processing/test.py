import time
import os
import glob
from utils import print_progress_bar

absolute_path = os.path.abspath("..")
image_paths_single_digit = glob.glob(
    absolute_path + "/Data/13-42-50-tree/13a/[0-9]_image_color.png"
)
image_paths_double_digit = glob.glob(
    absolute_path + "/Data/13-42-50-tree/13a/[0-9][0-9]_image_color.png"
)

all_paths = image_paths_double_digit + image_paths_single_digit

print(all_paths)


image_paths = glob.glob(
    absolute_path + "/Data/13-42-50-tree/13a//^\d{1,2}$/_image_color.png"
)
print(image_paths)

# # A List of Items
# items = list(range(0, 57))
# l = len(items)

# # Initial call to print 0% progress
# print_progress_bar(0, l, prefix="Progress:", suffix="Complete", length=50)
# for i, item in enumerate(items):
#     # Do stuff...
#     time.sleep(0.1)
#     # Update Progress Bar
#     print_progress_bar(i + 1, l, prefix="Progress:", suffix="Complete", length=50)
