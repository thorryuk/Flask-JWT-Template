#model 
import requests
from flask import Flask, jsonify, request, make_response
from ..database import conn, select, select2, insert, insert2, row_count2, select_limit , select_row

#Class 
class Data:
	def __init__(self):
		self.mydb = conn()

	#Fungsi ambil data dokter
	def get_data(self, query, values):
		return select(query, values, self.mydb)

	def get_data2(self, query, values):
		return select2(query, values, self.mydb)	

	def get_data_row(self, query, values):
		return select_row(query, values, self.mydb)	
	
	def get_data_lim(self, query, values, page):
		return select_limit(query, values, self.mydb, page)

	#Fungsi ambil data dokter
	def insert_data(self, query, val):
		return insert(query, val, self.mydb)

	def insert_data_last_row(self, query, val):
		return insert2(query, val, self.mydb)

	def row_count(self, query , val ):
		return row_count2(query , val, self.mydb)

	def kirim_email(self, judul, isi, penerima, pengirim):
		url = "https://tellhealth.ai/tellhealth_mail/index.php/mail"

		payload = {
		"pengirim":pengirim,
		"penerima":penerima,
		"isi":isi,
		"judul":judul
		}

		headers = {
		  'X-API-KEY': 'f99aecef3d12e02dcbb6260bbdd35189c89e6e73'
		}

		response = requests.request("POST", url, headers=headers, data = payload)

		return str(response)
