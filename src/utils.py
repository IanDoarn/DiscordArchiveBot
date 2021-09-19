import os
from typing import Dict, Hashable, Any
import zipfile
import yaml
import logging


def create_zip_file(filename: str, zipfile_path: str) -> None:
    logging.info(f"Creating zip archive: {filename}")
    zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(zipfile_path):
        logging.info(root)
        for file in files:
            logging.info(f"Writing {file} to {filename}")
            zipf.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(zipfile_path, '..')))
    logging.info("Zip file complete")
    zipf.close()


def load_yaml_file(file: str) -> Dict[Hashable, Any]:
    with open(file, 'r') as f:
        return yaml.safe_load(f)
