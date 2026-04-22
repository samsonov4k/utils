import os, re
import json


def normalize_lines(text):
    """
    1. Удаляет \n+ в начале строки → \n
    2. Удаляет пробелы в конце строки → \n\n
    """
    # Шаг 1: начало текста
    text = re.sub(r'^\n*', '\n', text)
   
    # # Шаг 2: конец ткекста 
    text.rstrip()+'\n\n'

    return text

def make_str(l, param):
    t = ""
    for a in l:
        t += a
    if param == "md":
        # markdown → комментарии в .py
        lines = t.strip().splitlines()

        return normalize_lines("\n".join("# " + line for line in lines) )
    
    elif param == "code":
        return normalize_lines(t)
    return t


def convert_ipynb_to_py(ipynb_path):
    """Конвертирует один ipynb в py."""
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        text = f.read()

    root = json.loads(text)

    res = ""
    for cell in root['cells']:
        if cell['cell_type'] == 'markdown':
            res += make_str(cell['source'], "md") + "\n"
        elif cell['cell_type'] == 'code':
            res += make_str(cell['source'], "code") + "\n"

    py_path = ipynb_path.replace('.ipynb', '.py')
    with open(py_path, 'w', encoding='utf-8') as file:
        file.write(res)

    print("Converted:", ipynb_path, "->", py_path)


def convert_ipynb_or_dir(path):
    """Если путь — файл ipynb, конвертируем его. Если папка — обходим все .ipynb."""
    if os.path.isfile(path):
        if path.endswith(".ipynb"):
            convert_ipynb_to_py(path)
        else:
            print("Not an .ipynb file:", path)
    elif os.path.isdir(path):
        for entry in os.scandir(path):
            if entry.is_file() and entry.name.endswith(".ipynb"):
                convert_ipynb_to_py(entry.path)
    else:
        print("Invalid path:", path)


# --- Основной блок вызова ---
if __name__ == "__main__":
    # Пример 1: один файл
    filename = r"c:\Проекты\ПроектыML\Занятие02"
    convert_ipynb_or_dir(filename)

    # Пример 2: папка (раскомментировать при желании)
    # folder = r"c:\Проекты\ПроектыML\Занятие02"
    # convert_ipynb_or_dir(folder)