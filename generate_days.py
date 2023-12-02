import os
import shutil

for day in range(1, 26):
    directory_name = f"day{day:02}"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        shutil.copy("solve_template.py", f"{directory_name}/solve.py")
        open(f"{directory_name}/__init__.py", "a").close()
