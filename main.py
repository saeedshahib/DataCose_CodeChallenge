import requests
from decouple import config
import datetime


class Contact:
    def __init__(self, airtable_id="", first_name="", last_name="", date_of_birth="", email="", lifetime_value=None):
        self.airtable_id = airtable_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email = email
        self.lifetime_value = lifetime_value

    def post_contact_to_contacts(self):
        url = "https://challenge-automation-engineer-xij5xxbepq-uc.a.run.app/contacts/"
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        json = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthdate": self.date_of_birth,
            "email": self.email,
            "custom_properties": {
                "airtable_id": self.airtable_id,
                "lifetime_value": self.lifetime_value
            }
        }
        username = config('USERNAME')
        password = config('PASSWORD')
        response = requests.post(url=url, headers=headers, auth=(username, password), json=json)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'error: {response.text}')


class Person:
    def __init__(self, id="", first_name="", last_name="", date_of_birth="", email="", lifetime_value=""):
        self.id = id
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.date_of_birth = date_of_birth
        self.email = email
        self.lifetime_value = lifetime_value

    @staticmethod
    def get_people():
        people_response = Person.request_api_to_get_people()
        people = []
        for person in people_response:
            fields = person['fields']
            people.append(Person(id=person.get("id"),
                                 first_name=fields.get('firstName'),
                                 last_name=fields.get('lastName'),
                                 date_of_birth=fields.get('dateOfBirth'),
                                 email=fields.get('email'),
                                 lifetime_value=fields.get('lifetime_value')))
        return people

    @staticmethod
    def request_api_to_get_people():
        url = "https://challenge-automation-engineer-xij5xxbepq-uc.a.run.app/people/"
        token = config("BEARER_TOKEN")  # gets the token from env variables
        headers = {
            "Authorization": f"Bearer {token}",
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"error: {response.text}")

    def convert_to_contact(self):
        date_of_birth_object = datetime.datetime.strptime(self.date_of_birth, '%d-%m-%Y')
        contact_day = date_of_birth_object.day if len(str(date_of_birth_object.day)) > 1 else f'0{date_of_birth_object.day}'
        contact_month = date_of_birth_object.month if len(str(date_of_birth_object.month)) > 1 else f'0{date_of_birth_object.month}'
        contact_date_of_birth = f'{date_of_birth_object.year}-{contact_month}-{contact_day}'
        contact_lifetime_value = float(self.lifetime_value.replace("$", ""))
        return Contact(airtable_id=self.id, first_name=self.first_name, last_name=self.last_name,
                       date_of_birth=contact_date_of_birth, email=self.email, lifetime_value=contact_lifetime_value)


if __name__ == '__main__':
    people = Person.get_people()
    for person in people:
        contact = person.convert_to_contact()
        print(contact.date_of_birth)
        print(contact.post_contact_to_contacts())
