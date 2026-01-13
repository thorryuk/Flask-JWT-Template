#model 
from database import conn, select, select2, insert, insert2, select_row

#Class 
class Data:
	def __init__(self):
		self.mydb = conn()

	#Fungsi ambil data dokter
	def get_data(self, query, values):
		return select(query, values, self.mydb)

	def get_data_row(self, query, values):
		return select_row(query, values, self.mydb)	

	#Fungsi ambil data dokter
	def insert_data(self, query, val):
		return insert(query, val, self.mydb)

	def insert_data_last_row(self, query, val):
		return insert2(query, val, self.mydb)

	#Fungsi ambil data login
	def get_login(self, query, values):
		mycursor = self.mydb.cursor()
		mycursor.execute(query, values)
		row_headers = [x[0] for x in mycursor.description]
		myresult = mycursor.fetchall()
		return myresult

	#Fungsi ambil data user
	def get_user(self, query, values):
		return select(query, values, self.mydb)