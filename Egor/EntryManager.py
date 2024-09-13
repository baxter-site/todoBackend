import os

from resources import Entry


# Entry - это одна запись, одно дерево
# EntryManager - класс для управления деревьями

class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path  # путь, где лежат файлы .json (путь к данным, принимаемый извне при инициализации)
        self.entries = []           # объекты класса Entry (изначально пустой лист (потом мы туда положим записи))

    # сохраняю каждый объет из списка entries класса Entry в файл
    def save(self):
        for entry in self.entries:      # перебираю объекты класса Entry
            entry.save(self.data_path)  # объекты класса Entry имеют метод .save

    # загружаю из папкки все объекты класса Entry в список entries
    def load(self):
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path)
        else:
            for filejson in os.listdir(self.data_path):
                if filejson.endswith('json'):
                    entry = Entry.load(os.path.join(self.data_path, filejson))
                    self.entries.append(entry)
        return self

    # добавляю объект класса Entry в список entries класса EntryManager
    def add_entry(self, title: str):
        self.entries.append(Entry(title))

# --- проверка каласса EntryManager

# --- список продуктов с двумя уровнями вложенности
# groceries = Entry('Продукты')
# category = Entry('Мясное')
# category.add_entry(Entry('Курица'))
# category.add_entry(Entry('Говядина'))
# category.add_entry(Entry('Колбаса'))
# groceries.add_entry(category)
# groceries.print_entries()
# groceries.save('C:\\Temp\\') # записал в файл json

# --- объект калсса EntryManager
# e = EntryManager('C:\\Temp\\') #  объект класса EntryManager с указанием папки
# e.load() # читаю из фалов .json данные в self.entries.append(entry)
# e.add_entry('Продукты') добавляю пустой Entry в self.entries = []
# e.save() сохраняю в файл
# print(e.entries)

# читаю из файла и вывожу в консоль
tree = Entry.load('C:\\Temp\\Продукты.json')  # сначала загружаю из строки формата json в объект класса Entry
tree.print_entries()  # печатаю объект класса Entry методом печати в консоль

# --- тест, записываю файл в папку
# import json
# content = {'test': 'passed'}
# f = 'C:\Temp\\' + 'my_file.json'
# with open(f, 'w', encoding='utf-8') as f:
#     json.dump(content, f)

#--- из Entry получаю строку в формате json
# category = Entry('Еда')
# category.add_entry(Entry('Морковь'))
# category.add_entry(Entry('Капуста'))
# category.json()
# print(category.json())

# --- из строки формата json получаю Entry ---
# entry = {"title": "Дела по дому", "entries": []}
# category = Entry.from_json(entry)
# print(category)

