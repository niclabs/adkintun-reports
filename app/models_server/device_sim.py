from app import db1
from sqlalchemy import PrimaryKeyConstraint

# Table to manage many to many relationship between device and sims
devices_sims = db1.Table('devices_sims',
                        db1.Column('device_id', db1.String(50), db1.ForeignKey('devices.device_id')),
                        db1.Column('sim_id', db1.String(50), db1.ForeignKey('sims.serial_number')),
                        PrimaryKeyConstraint('device_id', 'sim_id', name='device_sim_id'),
                        )
