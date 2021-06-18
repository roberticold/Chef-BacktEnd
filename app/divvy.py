import pandas as pd
from app import app, db,
from datetime import datetime


class Divvy(db.Model):
    trip_id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String(80), nullable=False)
    stop_time = db.Column(db.String(80), nullable=False)
    bike_id = db.Column(db.Integer(), nullable=False)
    from_station_id = db.Column(db.Integer(), nullable=False)
    from_station_name = db.Column(db.String(80), nullable=False)
    to_station_id = db.Column(db.Integer(), nullable=False)
    to_station_name = db.Column(db.String(80), nullable=False)
    user_type = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80))
    birthday = db.Column(db.String(80))
    trip_duration = db.Column(db.Integer())

    def __init__(self, trip_id, start_time, stop_time, bike_id, from_station_id, from_station_name, to_station_id, to_station_name, user_type, gender, birthday, trip_duration):
        self.trip_id = trip_id
        self.start_time = start_time
        self.stop_time = stop_time
        self.bike_id = bike_id
        self.from_station_id = from_station_id
        self.from_station_name = from_station_name
        self.to_station_id = to_station_id
        self.to_station_name = to_station_name
        self.user_type = user_type
        self.gender = gender
        self.birthday = birthday
        self.tritrip_durationp_id = trip_duration


df = pd.read_csv('app\static\images\DivvyChallenge.csv')
print(df.head())
for row in df.itertuples():
    divvyobject = Divvy(row[0], row[1], row[2], row[3], row[4],
                        row[5], row[6], row[7], row[8], row[9], row[10], row[11])
    db.session.add(divvyobject)
    db.session.commit()


@app.route('/divvy/<string:starttime>/<string:endtime>', methods=['GET'])
def average():

    pass
