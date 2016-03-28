from app import db

class Comments(db.Model):
	__tablename__ = 'comments'
	#Columns
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	furniture_name = db.Column(db.String(100))
	comment = db.Column(db.String(1000))
	vote_up = db.Column(db.Integer)
	vote_down = db.Column(db.Integer)

class Clicks(db.Model):
	__tablename__ = 'clicks'
	#Columns
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	furniture_one = db.Column(db.String(100))
	furniture_two = db.Column(db.String(100))