import os
import json
import hashlib
import logging

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_script_dir, "../..")) #change
temp_file_dir = os.path.join(project_root, "data/cache")

logger = logging.getLogger('Info Logger')


def save_register(register, name):
    path = os.path.join(temp_file_dir, name)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(register, file, ensure_ascii=False, indent=4)


def load_register(register_name):
    register_path = os.path.join(temp_file_dir, register_name)
    if not os.path.exists(temp_file_dir):
        os.makedirs(temp_file_dir)
        return {}
    else:
        if not os.path.exists(register_path):
            with open(register_path, 'w',  encoding="utf-8") as file:
                json.dump({}, file, ensure_ascii=False, indent=4)
            return {}
        else:
            with open(register_path, 'r', encoding="utf-8") as file:
                hash_reg = json.load(file)
            return hash_reg


def hash_generate(content_type=None, hasher=hashlib.md5(), **kwargs):
    if content_type == "pdf":
        hasher = hashlib.md5()
        with open(kwargs.get("content",""), 'rb') as pdf_file:
            buf = pdf_file.read()
            hasher.update(buf)
        return hasher.hexdigest()
    else:
        content = kwargs.get('content', '')
        if isinstance(content, str):
            hasher.update(content.encode("utf-8"))
        else:
            hasher.update(content)
        return hasher.hexdigest()

def clear_register(register_name):
    try:
        path = os.path.join(temp_file_dir, register_name)
        with open(path, 'w') as file:
            json.dump({}, file)
    except Exception as e:
        logger.error("Couldn't clear cache because the cache file was not created during the execution.")


def clean_temp_files():
    clear_register("image_register.json")
    clear_register("pdf_register.json")
    clear_register("webpage_register.json")