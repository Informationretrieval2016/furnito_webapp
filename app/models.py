from app import db

class Comments(db.Model):
	__tablename__ = 'comments'
	#Columns
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	furniture_name = db.Column(db.String(200))
	comment = db.Column(db.String(1000))
	vote_up = db.Column(db.Integer)
	vote_down = db.Column(db.Integer)

class Clicks(db.Model):
	__tablename__ = 'clicks'
	#Columns
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	furniture_one = db.Column(db.String(200))
	furniture_two = db.Column(db.String(200))
	age = db.Column(db.String(10))
	favoritestyle = db.Column(db.String(50))
	gender = db.Column(db.String(10))

	def __init__(self,furniture_one = None,furniture_two = None,age = None,favoritestyle = None,gender =None):
		self.furniture_one = furniture_one
		self.furniture_two = furniture_two
		self.age = age
		self.favoritestyle = favoritestyle
		self.gender = gender

class User(db.Model):
	__tablename__ = 'userinfos'
	#Columns
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	username = db.Column(db.String(16))
	password = db.Column(db.String(16))
	age = db.Column(db.String(10))
	favoritestyle = db.Column(db.String(50))
	gender = db.Column(db.String(10))

	def __init__(self,username = None,password = None,age = None,favoritestyle = None,gender =None):
		self.username = username
		self.password = password
		self.age = age
		self.favoritestyle = favoritestyle
		self.gender = gender