from app.app import db
from models.tiny_models import Person, VIP


def upgrade_to_vip(an_id):
    person = Person.query.filter_by(id=an_id).first()
    vip = VIP(person.id, person.nombre, person.apellido, person.edad)
    db.session.add(vip)
    db.session.commit()
