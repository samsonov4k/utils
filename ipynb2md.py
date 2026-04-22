import os
import json


def make_str(l, param):
    t = ''
    for a in l:
        t += a  # +'\n'

    if param == 'code':
        t = "``` python\n" + t + "\n```"
    return t


def convert_ipynb_to_md(ipynb_path):
    """Конвертирует один ipynb в md (по стилю оригинала)."""
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        text = f.read()

    root = json.loads(text)

    res = ''
    for cell in root['cells']:
        if cell['cell_type'] == 'markdown':
            res += make_str(cell['source'], 'md') + '\n\n'
        elif cell['cell_type'] == 'code':
            res += make_str(cell['source'], 'code') + '\n\n'
        else:
            print(cell)

    md_path = ipynb_path.replace('.ipynb', '.md')

    with open(md_path, 'w', encoding='utf-8') as file:
        file.write(res)

    print("Converted:", ipynb_path, "->", md_path)


def convert_ipynb_or_dir(path):
    """Если путь — файл ipynb, конвертируем его. Если папка — обходим все .ipynb."""
    if os.path.isfile(path):
        if path.endswith(".ipynb"):
            convert_ipynb_to_md(path)
        else:
            print("Not an .ipynb file:", path)
    elif os.path.isdir(path):
        for entry in os.scandir(path):
            if entry.is_file() and entry.name.endswith(".ipynb"):
                convert_ipynb_to_md(entry.path)
    else:
        print("Invalid path:", path)


# --- Основной блок вызова ---
if __name__ == "__main__":
    # Пример 1: один файл
    filename = r"c:\Проекты\ПроектыML\Занятие02\LRegression.ipynb"
    convert_ipynb_or_dir(filename)

    # Пример 2: папка (раскомментировать при желании)
    # folder = r"c:\Проекты\ПроектыML\Занятие02"
    # convert_ipynb_or_dir(folder)