import os
import shutil

for day in range(1, 26):
    directory_name = str(day)
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        shutil.copy("solve_template.py", f"{day}/solve.py")
