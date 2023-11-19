import json
import os
import re
import validators


def is_valid_name(name: str):
    return len(name) > 1 and name.isalpha()


def is_valid_telephone(tel: str):
    return (len(tel) == 12 and tel.startswith('+374') and tel[4:].isdigit()) or \
        (len(tel) == 9 and tel.startswith('0') and tel.isdigit())


def is_valid_address(address: str):
    pattern = r"^[a-zA-Z0-9\s/]+$"
    return re.match(pattern, address)


def is_valid_url(url: str):
    return validators.url(url)


def is_valid_mail(mail: str):
    pattern = r"[a-zA-Z0-9._-]+@[a-zA-Z0-9]+\.[a-zA-Z]+"
    return re.match(pattern, mail)


class ContactDescriptor:

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.name not in instance.__dict__:
            raise AttributeError(f"'{owner.__name__}' object has no attribute '{self.name}'")
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class Contact:
    name = ContactDescriptor()
    surname = ContactDescriptor()
    mid_name = ContactDescriptor()
    telephone = ContactDescriptor()
    mail = ContactDescriptor()
    address = ContactDescriptor()
    url = ContactDescriptor()

    def __init__(self, name, mid_name, surname, telephone, mail, address, url):
        self.name = name
        self.mid_name = mid_name
        self.surname = surname
        self.telephone = telephone
        self.mail = mail
        self.address = address
        self.url = url
        self.dict_form = dict(name=self.name, mid_name=self.mid_name, surname=self.surname, telephone=self.telephone,
                              mail=self.mail, address=self.address, url=self.url)


class Addressbook:
    def __init__(self):
        self.contacts = []

    def search_contact(self, searching_word: str):
        for cont in self.contacts:
            for key in cont.dict_form:
                if searching_word.lower() in cont.dict_form[key].lower():
                    print(cont.dict_form)
                    break
            else:
                print('Nothing was found!')

    def add_contact(self, filename):
        name = input('Enter a name: ')
        if not is_valid_name(name):
            return 'Invalid name!'
        mid_name = input('Enter a middle name: ')
        if not is_valid_name(mid_name):
            return 'Invalid middle name!'
        surname = input('Enter a surname: ')
        if not is_valid_name(surname):
            return 'Invalid surname!'
        telephone = input('Enter a telephone: ')
        if not is_valid_telephone(telephone):
            return 'Invalid telephone!'
        mail = input('Enter a mail: ')
        if not is_valid_mail(mail):
            return 'Invalid mail!'
        address = input('Enter an address: ')
        if not is_valid_address(address):
            return 'Invalid address!'
        url = input('Enter a url: ')
        if not is_valid_url(url):
            return 'Invalid url!'
        contact = Contact(name, mid_name, surname, telephone, mail, address, url)
        self.contacts.append(contact)
        with open(f'{filename}.txt', 'a') as f:
            json.dump(contact.dict_form, f)
        return 'Contact added successfully!'

    def update_contact(self, filename):
        if len(self.contacts) == 0:
            print('Before update a contact you must create it.')
            return
        index = 0
        nm = input('Enter a contact name whose information you want to update: ')
        for cont in self.contacts:
            if nm.lower() == cont.dict_form['name'].lower():
                index = self.contacts.index(cont)
                break
        else:
            print('No contact was found with that name!')
            return

        field = input('Enter a field you want to update (ex. name,mid_name,surname,telephone,mail,address,url): ')
        updated_value = input('Enter an updated value: ')
        for i in self.contacts[index].dict_form.keys():
            if i == field.lower():
                self.contacts[index].dict_form[i] = updated_value

                with open(f'{filename}.txt', 'w') as f:
                    for cont in self.contacts:
                        json.dump(cont.dict_form, f)
                print('Updated successfully!')
                break
        else:
            print('No such field in contact.')

    def delete_contact(self, filename):
        if len(self.contacts) == 0:
            print('No contacts to delete')
            return
        index = 0
        nm = input('Enter a contact name you want to delete: ')
        for cont in self.contacts:
            if nm.lower() == cont.dict_form['name'].lower():
                del cont
                with open(f'{filename}.txt', 'w') as f:
                    for cont in self.contacts:
                        json.dump(cont.dict_form, f)
                print('Deleted successfully!')
                break
        else:
            print('No contact was found with that name!')
            return


def create_addressbook():
    filename = input('Enter a name for addressbook: ')
    with open(f'{filename}.txt', 'a') as f:
        f.write('Welcome to addressbook!\n')
    print('Created successfully!')
    return Addressbook()


def delete_addressbook(filename):
    try:
        os.remove(f'{filename}.txt')
        print("Deleted successfully")
    except FileNotFoundError:
        print("File not found.")


def main():
    num = 0
    while True:
        print('\nHere are available options:')
        print('1 - Add contact\n2 - Update contact\n3 - Delete contact\n4 - Search '
              'contact\n5 - Create new addressbook\n6 - Delete addressbook\n7 - End program')

        opt = input('Please choose one of these option numbers: ')
        if opt == '1':
            cont = Contact('name', 'mid name', 'surname', 'address', 'mail', 'telephone', 'url')
            filename = input('Enter addressbook name:')
            try:
                print(addressbook.add_contact(filename))
            except:
                print("Before adding contact you must create addressbook")
        elif opt == '2':
            try:
                addressbook.update_contact(filename)
            except:
                print('Before update a contact you must to create it.')

        elif opt == '3':
            filename = input('Enter addressbook name:')
            try:
                addressbook.delete_contact(filename)
            except:
                print('Before deleting a contact you must create addressbook and add contact')
        elif opt == '4':
            searching_word = input('Enter searching word: ')
            addressbook.search_contact(searching_word)
        elif opt == '5':
            addressbook = create_addressbook()
        elif opt == '6':
            filename = input('Type the name of addressbook you want to delete: ')
            try:
                delete_addressbook(filename)
            except ValueError:
                print('No such addressbook')

        elif opt == '7':
            break
        else:
            print('Please choose one of these numbers only, from 1 to 6! ')


if __name__ == '__main__':
    main()
