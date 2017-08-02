from app.app import application, db
from models.tiny_models import Person, VIP
from test import base_test


class TestConnection(base_test.BaseTest):

    def test_first_db(self):

        with application.app_context():
            person = Person(0, 'Javier', 'Morales', 21)
            db.session.add(person)
            db.session.commit()
            result = Person.query.filter_by(id=0, nombre='Javier', apellido='Morales', edad=21).first()
            self.assertIsNotNone(result)
            self.assertEqual(person.id, result.id)
            self.assertEqual(person.nombre, result.nombre)
            self.assertEqual(person.apellido, result.apellido)
            self.assertEqual(person.edad, result.edad)

    def test_second_db(self):

        with application.app_context():
            vip = VIP(1, 'Lucho', 'Jara', 50)
            db.session.add(vip)
            db.session.commit()
            result = VIP.query.filter_by(id=1, nombre='Lucho', apellido='Jara', edad=50).first()
            self.assertIsNotNone(result)
            self.assertEqual(vip.id, result.id)
            self.assertEqual(vip.nombre, result.nombre)
            self.assertEqual(vip.apellido, result.apellido)
            self.assertEqual(vip.edad, result.edad)
