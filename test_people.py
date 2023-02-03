from main import Person, Contact
import pytest


class TestPerson:
    def test_get_people(self):
        people = Person.get_people()
        for person in people:
            assert person.first_name is not None
            assert person.last_name is not None
            assert person.email is not None
            assert person.id is not None
            assert person.date_of_birth is not None
            assert person.lifetime_value is not None

    def test_convert_person_to_contact(self):
        person = Person(id="test1",
                        first_name=" james ",
                        last_name=f" Doe",
                        date_of_birth="25-08-1991",
                        email="test@test.com",
                        lifetime_value="$122.25")
        contact = person.convert_to_contact()

        assert contact.airtable_id == "test1"
        assert contact.first_name == "james"
        assert contact.last_name == "Doe"
        assert contact.date_of_birth == "1991-08-25"
        assert contact.email == "test@test.com"
        assert contact.lifetime_value == 122.25


class TestContact:

    def test_success_post_contact_to_contacts(self):
        people = Person.get_people()
        for person in people:
            contact = person.convert_to_contact()
            response = contact.post_contact_to_contacts()
            assert response is not None

    def test_failed_post_contact_to_contacts(self):
        contact = Contact(airtable_id="test1",
                          first_name="David",
                          last_name="Grimes",
                          date_of_birth="1991-31-05",
                          email="test@test.com",
                          lifetime_value=12.45)

        with pytest.raises(Exception) as ve:
            contact.post_contact_to_contacts()

        contact.date_of_birth = "1991-05-31"
        contact.lifetime_value = "$12.45"

        with pytest.raises(Exception) as ve:
            contact.post_contact_to_contacts()

        contact.lifetime_value = 12.45
        response = contact.post_contact_to_contacts()
        assert response is not None
