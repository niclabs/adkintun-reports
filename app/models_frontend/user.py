from app import db2


class User(db2.Model):
    __bind_key__ = 'nothing'
    id = db2.Column(db2.Integer, primary_key=True)
    first_name = db2.Column(db2.String(100))
    last_name = db2.Column(db2.String(100))
    login = db2.Column(db2.String(80), unique=True)
    email = db2.Column(db2.String(120))
    password = db2.Column(db2.String(120))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username
