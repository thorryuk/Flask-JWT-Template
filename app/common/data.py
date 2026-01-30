#model 
from .database import conn, select, select2, insert, insert2, select_row
from flask import current_app

#Class 
class Data:
	#Fungsi ambil data
	def get_data(self, query, values):
		db = conn(current_app)
		return select(query, values, db)

	def get_data_row(self, query, values):
		db = conn(current_app)
		return select_row(query, values, db)	

	#Fungsi ambil data
	def insert_data(self, query, val):
		db = conn(current_app)
		return insert(query, val, db)

	def insert_data_last_row(self, query, val):
		db = conn(current_app)
		return insert2(query, val, db)

	#Fungsi ambil data login
	def get_login(self, query, values):
		db = conn(current_app)
		mycursor = db.cursor()
		mycursor.execute(query, values)
		row_headers = [x[0] for x in mycursor.description]
		myresult = mycursor.fetchall()
		return myresult

	#Fungsi ambil data user
	def get_user(self, query, values):
		db = conn(current_app)
		return select(query, values, db)