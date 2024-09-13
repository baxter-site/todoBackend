import json
import os

# --- печтать элемента в консоль с указанным отступом
def print_with_indent(value, indent=0):
    print('\t' * indent + str(value))

# --- класс - отдельный элемент
# в переменной entries может содержать элементы этого же класса (рекурсия наоборот, получается фрактальное дервео)
class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []        # лиск с элементами класса Entry
        self.title = title      # название
        self.entries = entries  # список записей
        self.parent = parent    # родитель

    # при обращении к классу, возращаю название
    # без этого метода возращается адрес объект типа <__main__.Entry object at 0x000001BDA4ED7040>
    def __str__(self):
        return self.title

    # --- возращаю dict {}
    # метод возвращакт запись (объект класса Entry) в формате dict
    # c двумя ключами: title и entries.
    def json(self):
        res = {
            'title': self.title,
            "entries": [entrie.json() for entrie in self.entries]  # у объекта entrie есть метод json()
        }
        return res

    # --- добавляю элемент в лист entries
    # метод add_entry, который принимает в себя новую запись (объект класса Entry) и добавлять его в лист entries текущей записи
    def add_entry(self, entry):
        self.entries.append(entry)  # добавляю элемент в лист
        entry.parent = self         # добавляю родителя, уровень выше

    # --- печать всего списка в консоль с отступом используя рекурсию
    # метод выводит в консоль все элементы по одному в строчке (другими словами, для каждого элемента свой print).
    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        indent += 1
        for entry in self.entries:
            entry.print_entries(indent)  # у объета entry класса Entry() есть метод print_entries() 

    # --- из json получаю Entry
    @classmethod
    def from_json(cls, value: dict):
        new_entry = cls(value['title'])
        for item in value.get("entries", []):  # .get проверяет есть ли значение "entries", если нет, тога путой []
            new_entry.add_entry(cls.from_json(item))
        return new_entry

    # --- сохранить дерево в файл json
    # def save(self, path):
    #     filename = '/tmp/' + f'{self.title}.json'
    #     with open(filename, 'w') as f:
    #         content = self.json()            # получил dict перевел в json (тут у меня ошибка, dict надо получить один раз вне цикла )
    #         value_str = json.dumps(content)  # перевели dict в str (тут все правильно, получил объект)
    #         f.write(value_str)               # записали в файл (... записал объект в файл)

    def save(self, path):
        filename = os.path.join(path, self.title)  # полный путь к месту на диске передаю извне
        content_json = self.json()                 # получил dict перевел в json
        with open(f'{filename}.json', 'w') as f:   # открыаю файл для записи (, encoding='utf-8')
            json.dump(content_json, f)             # (здесь получаю объект и записываю в файл одной строкой)

    # --- загружаю из файла в dict
    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            content = json.load(f)    # читаю из фалй json
        return cls.from_json(content) # из json перевожу в dict своим методом


# ----------------------------- EntryManager -----------------------------
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


# ------------------------------ тесты ----------------------------------
if __name__ == '__main__': # выплнять только если запуск из текущего файла
    #--- из Entry получаю строку в формате json
    # category = Entry('Еда')
    # category.add_entry(Entry('Морковь'))
    # category.add_entry(Entry('Капуста'))
    # category.json()
    # print(category.json())

    # --- Зададим список продуктов с двумя уровнями вложенности
    # groceries = Entry('Продукты')
    # category = Entry('Мясное')
    # category.add_entry(Entry('Курица'))
    # category.add_entry(Entry('Говядина'))
    # category.add_entry(Entry('Колбаса'))
    # groceries.add_entry(category)
    # groceries.print_entries()

    # --- из строки формата json получаю Entry
    # entry = {"title": "Дела по дому", "entries": []}
    # category = Entry.from_json(entry)
    # print(category)

    # --- создаю объект
    # item = Entry("Помидор")
    # print(item)

    # ------------- тест на зкрузку выгрузку --------------
    # вложенность как у входящего JSON
    grocery_list = {
      "title": "Продукты",
      "entries": [
        {
          "title": "Молочные",
          "entries": [
            {
              "title": "Йогурт",
              "entries": []
            },
            {
              "title": "Сыр",
              "entries": []
            }
          ]
        }
      ]
    }

    new_entrye = Entry.from_json(grocery_list) # сначала загружаю из строки формата json в объект класса Entry
    new_entrye.print_entries()                 # печатаю объект класса Entry методом печати в консоль
    print('------------------------')
    print(new_entrye.json())                   # из объекта класса Entry формирую строку в формате json