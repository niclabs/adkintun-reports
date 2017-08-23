from app import db1

class User(db1.Model):
    id = db1.Column(db1.Integer, primary_key=True)
    first_name = db1.Column(db1.String(100))
    last_name = db1.Column(db1.String(100))
    login = db1.Column(db1.String(80), unique=True)
    email = db1.Column(db1.String(120))
    password = db1.Column(db1.String(120))

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