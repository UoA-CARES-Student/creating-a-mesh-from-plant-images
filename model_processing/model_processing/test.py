import time
from utils import print_progress_bar

# A List of Items
items = list(range(0, 57))
l = len(items)

# Initial call to print 0% progress
print_progress_bar(0, l, prefix="Progress:", suffix="Complete", length=50)
for i, item in enumerate(items):
    # Do stuff...
    time.sleep(0.1)
    # Update Progress Bar
    print_progress_bar(i + 1, l, prefix="Progress:", suffix="Complete", length=50)

    print_progress_bar(0, l, prefix="Seperate:", length=50)

    for i_2, item_2 in enumerate(items):
        # Do stuff...
        time.sleep(0.1)
        # Update Progress Bar
        print_progress_bar(i_2 + 1, l, prefix="Seperate:", suffix="Complete", length=50)
