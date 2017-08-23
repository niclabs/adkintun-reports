from app import db1

# Tabla para manejar la relacion many_to_many entre antenas y eventos gsm
antennas_gsm_events = db1.Table('antennas_gsm_events',
                               db1.Column('antenna_id', db1.Integer, db1.ForeignKey('antennas.id')),
                               db1.Column('gsm_event_id', db1.Integer, db1.ForeignKey('gsm_events.id'))
                               )
