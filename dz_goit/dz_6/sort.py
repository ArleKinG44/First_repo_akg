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


# Функція для обробки новостворених папок
def process_new_folders(path):
    
    sufix = {
            '.png','.jpeg','.jpg','.svg','.avi','.mp4','.mov','.mkv','.doc',
            '.docx','.txt','.pdf','.xlsx','.pptx','.mp3','.ogg','.wav','.amr','.zip','.gz','.tar'
            }

    folder_name = {"images", "video", "documents", "audio"}

    
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        
        if os.path.isdir(file_path) and filename in folder_name:

            # Якщо це файл, то застосовуємо функцію normalize
            if os.path.isfile(file_path) and os.path.splitext(filename)[1] in sufix:
                normalized_name = normalize(filename)
                normalized_path = os.path.join(path, normalized_name)

                # Перевіряємо, чи існує файл з таким іменем
                if os.path.exists(normalized_path):
                    i = 1
                    while os.path.exists(normalized_path + str(i)):
                        i += 1
                    normalized_path += str(i)

                # Перейменовуємо файл
                os.rename(file_path, normalized_path)
           
            elif os.path.isdir(file_path):
                process_new_folders(file_path)


# Функція для обробки файлів в папці
def process_files_in_folder(path):
   
    extensions = {
        "images": ['.png', '.jpeg', '.jpg', '.svg'],
        "video": ['.avi', '.mp4', '.mov', '.mkv'],
        "documents": ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
        "audio": ['.mp3', '.ogg', '.wav', '.amr'],
        "archives": ['.zip', '.gz', '.tar']
    }

    known_extensions = set()
    unknown_extensions = set()

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)

        # Якщо це файл
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1]

            # Перевіряємо, чи є розширення файлу в нашому словнику extensions
            for folder, exts in extensions.items():
                if file_ext in exts:

                    shutil.move(file_path, os.path.join(path, folder, filename))
                    extensions[folder].append(file_ext)
                    known_extensions.add(file_ext)

                    # Якщо файл є архівом, то розпаковуємо його
                    if folder == 'archives':
                        shutil.unpack_archive(os.path.join(path, folder, filename), os.path.join(path, folder))
                else:
                    unknown_extensions.add(file_ext)

        elif os.path.isdir(file_path):
            process_files_in_folder(file_path)

    print("Відомі розширення:", known_extensions)
    print("Невідомі розширення:", unknown_extensions)

    # Виводимо список файлів в кожній категорії
    for folder in extensions.keys():
        print(f"Файли в категорії {folder}:")
        for filename in os.listdir(os.path.join(path, folder)):
            print(filename)

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

        process_files_in_folder(folder)
        process_new_folders(folder)
        remove_empty_folders(folder)
    else:
        print("Будь ласка, вкажіть ім'я папки як аргумент при запуску скрипта.")

if __name__ == "__main__":
    main()