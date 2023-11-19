import os
import sys
import shutil
import re

# Функція для транслітерації й заміщення символів
def normalize(name):

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    
    TRANS = {ord(c.upper()): l.upper() for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION)}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

        translate_name = "".join(TRANS.get(ord(c), c) for c in name.lower())
        normalized_name = re.sub('[^a-zA-Z0-9]', '_', translate_name)

    return normalized_name.title()

# Функція сортування 
def sort_files(start_path):
    extensions = {
        "images": ['.png', '.jpeg', '.jpg', '.svg'],
        "video": ['.avi', '.mp4', '.mov', '.mkv'],
        "documents": ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
        "audio": ['.mp3', '.ogg', '.wav', '.amr'],
        "archives": ['.zip', '.gz', '.tar'],
        "Eny_trash": []
    }

    known_extensions = set(val for sublist in extensions.values() for val in sublist)
    found_extensions = {category: [] for category in extensions}

    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in extensions]

        for file in files:
            file_ext = os.path.splitext(file)[-1]
            moved = False

            for category, exts in extensions.items():
                if file_ext in exts:
                    shutil.move(os.path.join(root, file), os.path.join(start_path, category, file))
                    found_extensions[category].append(file_ext)
                    moved = True
                    break

            if not moved:
                shutil.move(os.path.join(root, file), os.path.join(start_path, "Eny_trash", file))
                found_extensions["Eny_trash"].append(file_ext)

    unknown_extensions = set(val for sublist in found_extensions.values() for val in sublist) - known_extensions

    print("Відомі розширення:", set(val for sublist in found_extensions.values() for val in sublist))
    print("Невідомі розширення:", unknown_extensions)

# Функція для обробки нових папок
def sort_files_new(start_path):
    folders = ["images", "video", "documents", "audio", "archives"]

    for folder in folders:
        folder_path = os.path.join(start_path, folder)
        for filename in os.listdir(folder_path):
            old_file_path = os.path.join(folder_path, filename)
            new_file_name = normalize(filename)
            new_file_path = os.path.join(folder_path, new_file_name)
            os.rename(old_file_path, new_file_path)

        # Не виводимо файли в папці 'archives'
        if folder != 'archives':
            print(f"Файли в папці {folder}:")
            for filename in os.listdir(folder_path):
                print(filename)

    archives_folder = os.path.join(start_path, 'archives')
    for filename in os.listdir(archives_folder):
        file_path = os.path.join(archives_folder, filename)
        try:
            shutil.unpack_archive(file_path, archives_folder)
            os.remove(file_path)
        except Exception as e:
            print(f"Не вдалося розпакувати файл {filename}. Помилка: {e}")
            os.remove(file_path)


# Функція для видалення порожніх папок 
def remove_empty_folders(path):
    for dirpath, dirnames, files in os.walk(path, topdown=False):
        if not dirnames and not files:
            os.rmdir(dirpath)

def main():

    if len(sys.argv) == 2:
        folder = sys.argv[1]

        folders = ["images", "video", "documents", "audio", "archives", "Eny_trash"]

        for subfolder in folders:
            os.makedirs(os.path.join(folder, subfolder), exist_ok=True)

        sort_files(folder)
        sort_files_new(folder)
        remove_empty_folders(folder)

    else:
        print("Будь ласка, вкажіть ім'я папки як аргумент при запуску скрипта.")

if __name__ == "__main__":
    main()