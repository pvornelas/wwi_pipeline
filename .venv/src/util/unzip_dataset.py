import os
import zipfile
import shutil

if __name__ == "__main__":
    for root, dirs, files in os.walk("/home/pvini/projeto/.venv/data/base"):
        for filename in files:
           if filename.endswith(".zip"):
                with zipfile.ZipFile(os.path.join(root, filename), 'r') as zip_ref:
                    zip_ref.extractall("/home/pvini/projeto/.venv/data/base")

    if os.path.exists("/home/pvini/projeto/.venv/data/base/datasets"):
        shutil.rmtree("/home/pvini/projeto/.venv/data/base/datasets")