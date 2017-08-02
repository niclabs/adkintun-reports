from app.app import application, db
from models.tiny_models import Person, VIP
from test import base_test
from app.migrate_data import upgrade_to_vip


class TestMigration(base_test.BaseTest):

    def test_upgrade_to_vip(self):
        with application.app_context():
            person = Person(10, 'Morgan', 'Freeman', 80)
            db.session.add(person)
            db.session.commit()
            upgrade_to_vip(10)
            vip = VIP.query.filter_by(id=10).first()
            self.assertIsNotNone(vip)
            self.assertEqual(person.id, vip.id)
            self.assertEqual(person.nombre, vip.nombre)
            self.assertNotEqual(person.apellido, vip.apellido)
            self.assertEqual(person.edad, vip.edad)
