from collections import UserDict
from datetime import datetime, date


class Field:
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError
        self.__value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if not self.is_valid(value):
            raise ValueError
        self.__value = value

    def __str__(self):
        return str(self.value)
    
    def is_valid(self, value):
        return True
    

class Name(Field):
    # реалізація класу
    pass


class Phone(Field):
    # реалізація класу
    def is_valid(self, value):
        return value.isdigit() and len(value) == 10
    
            
class Birthday(Field):
    # реалізація класу
    def is_valid(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return True
        except ValueError:
            return False


class Record:
    # реалізація класу
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        if phone:
            self.phones.append(Phone(phone))
        self.birthday = Birthday(birthday) if birthday else None
    
    def add_phone(self, phone: str):
        phone = Phone(phone)
        if phone not in self.phones:
            self.phones.append(phone)

    def remove_phone(self, phone: str):
        for i in self.phones:
            if i.value == phone:
                self.phones.remove(i)

    def edit_phone(self, phone: str, new_phone):
        new_phone = Phone(new_phone)
        for i in self.phones:
            if i.value == phone:
                i.value = new_phone.value
                return          
        raise ValueError
                
    def find_phone(self, phone: str):
        for i in self.phones:
            if i.value == phone:
                return i
        return None
    
    def days_to_birthday(self):
        if self.birthday:
            today = date.today()
            next_birthday = datetime.strptime(str(self.birthday), '%d.%m.%Y')
            birthday_day = date(year=today.year, month=next_birthday.month, day=next_birthday.day)

            if today > birthday_day:
                birthday_day = date(year=today.year + 1, month=next_birthday.month, day=next_birthday.day)

            days = birthday_day - today
            return days.days
        return None
        
    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    # реалізація класу
    def add_record(self, record):
        if record.name.value in self.data:
            return self.data[record.name.value]
        self.data[record.name.value] = record
        return record

    def find(self, name):
        for record in self.data.values():
            if name in record.name.value:
                return record

    def delete(self, record):
        try:
            del self.data[record]
        except KeyError:
            print('Contact not found')

    def iterator(self, n=1):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i: i+n]

    def __str__(self) -> str:
        return '\n'.join(str(r) for r in self.data.values())

