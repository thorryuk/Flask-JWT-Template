from flask import Flask, jsonify, request, make_response, render_template, redirect
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS, cross_origin
import json
import datetime
from time import gmtime, strftime
import os
import base64
import random
import hashlib
import warnings
from data import Data
from werkzeug.utils import secure_filename

# from contoh.controllers import contoh
from user.controllers import user

import sys
#########################
from keras.models import load_model
import cv2
import numpy as np
#########################

warnings.simplefilter("ignore", DeprecationWarning)

#--------------------- CONFIGURATION ------------------------
app = Flask(__name__, static_url_path=None) #panggil modul flask

cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['SECRET_KEY'] 							= 'R4h4s!A D0n6' #secret key API
app.config['CORS_HEADERS']							= 'Content-Type'
app.config['JWT_EXPIRATION_DELTA'] 					= datetime.timedelta(days=1)#1 hari token expired
app.config['JWT_DEFAULT_REALM'] 					= 'Login Required'
app.config['LOGS'] 									= "/var/www/refi/refi/logs/"

# app.config['UPLOAD_FOLDER_GAMBAR_CONTOH'] 		= '/var/www/refi/refi/upload/foto_contoh/'
# app.config['UPLOAD_FOLDER_GAMBAR_USER'] 		= '/var/www/refi/refi/upload/foto_user/'
# app.config['UPLOAD_FOLDER_GAMBAR_GNERAL'] 		= '/var/www/refi/refi/upload/foto_gneral/'
#-------------------- END CONFIGURATION ------------------------
class User(object): #Class USer untuk API Auth
	def __init__(self, id):
		self.id = id
	def __str__(self):
		return "User(id='%s')" % self.id


#@app.route('/verip',methods=['POST'])
def verify(username, password): #menerima input JSON
	if not (username and password): #jika username dan password kosong
	  return False
	pass_ency = hashlib.md5(password.encode('utf-8')).hexdigest() #ubah password jadi md5 karena db jg md5

	values 	= (username, pass_ency)
	roles 	= "1" # user
	query 	= "SELECT a.id_user FROM user a, customer b WHERE a.id_user = b.id_user AND a.email = %s AND a.password= %s"
	dt 		= Data()
	hasil 	= dt.get_data_row(query, values)
	if len(hasil) == 0:
		query 	= "SELECT a.id_user, b.role FROM user a, admin b WHERE a.id_user = b.id_user AND email = %s AND password = %s"
		dt 		= Data()
		hasil 	= dt.get_data_row(query, values)
		roles 	= "2" #admin
		if hasil[0]["role"] == 1:
			roles 	= "3" # super admin
		if len(hasil) == 0:
			return False

	# if hasil[0]["email"]==username and hasil[0]["password"]==pass_ency:
	id_ = str(hasil[0]["id_user"])+'#'+str(roles)
	logs = "{'id_user':'"+ str(hasil[0]["id_user"]) +"','roles':'"+ str(roles) + "','action':'login','date':'"+secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+"'}\n"
	tambahLogs(logs)
	return User(id=id_)

def identity(payload): #funhsi payload
    id_ = payload['identity'].split("#") #identity payload berisi user id
    return {"user_id": id_[0],"roles":id_[1]} #kembalikan dalam bentuk json

jwt = JWT(app, verify, identity) #panggil Java Web Token
#--------------------- JWT AUTHENTICATION ------------------------

@app.route('/aktivasi/<token>',methods=['GET'])
def aktivasi(token):
	q = token
	email = base64.b64decode(q)
	result = ""

	dt = Data()
	query = "select * from user where email = %s"
	values = (email, )

	hasil = dt.get_data_row(query,values)
	if len(hasil) == 0:
		return make_response(jsonify({"hasil":"gagal"}))

	query1 = "UPDATE `user` SET `is_aktif` = '1' WHERE email=%s"
	values1 = (email, )
	dt.insert_data(query1, values1)

	return redirect('https://bisa.ai/')


@app.route('/cek_credential', methods=['GET', 'OPTIONS']) #Link
@jwt_required() #menandakan harus memasukan token credential
@cross_origin()
def cek_credential():
    values = (str(current_identity['user_id']),)
    query = "SELECT a.*, b.email, b.nama, b.no_telepon, b.alamat, b.foto, b.jk, b.tanggal_lahir, b.is_aktif FROM customer a, user b WHERE a.id_user = b.id_user AND b.is_aktif = '1' AND a.id_user = %s" 
    dt = Data()
    hasil = dt.get_data(query, values)
    if len(hasil) == 0:
        query = "SELECT a.id_admin, a.id_user, a.posisi, b.email, b.nama, b.no_telepon, b.alamat, b.foto, b.jk, b.tanggal_lahir, b.is_aktif as is_aktif_user, a.is_aktif as is_aktif_admin FROM admin a, user b WHERE a.id_user = b.id_user AND a.is_aktif = 1 AND b.is_aktif = 1 AND a.id_user = %s" # cari admin
        dt = Data()
        hasil = dt.get_data(query, values)
        if len(hasil) == 0:
        	return False
    return jsonify(hasil)

#-------------------- END JWT AUTHENTICATION ------------------------
#--------------------- ERROR HANDLER ------------------------
# fungsi error handle Halaman Tidak Ditemukan
@app.errorhandler(404)
@cross_origin()
def not_found(error):
	return make_response(jsonify({'error': 'Tidak Ditemukan','status_code':404}), 404)

#fungsi error handle Halaman internal server error
@app.errorhandler(500)
@cross_origin()
def not_found(error):
	return make_response(jsonify({'error': 'Error Server','status_code':500}), 500)
#-------------------- END ERROR HANDLER ------------------------
def tambahLogs(logs):
    f = open(app.config['LOGS'] + "/" + secure_filename(strftime("%Y-%m-%d"))+ ".txt", "a")
    f.write(logs)
    f.close()

#--------------------- REGISTER BLUEPRINT ------------------------
# app.register_blueprint(contoh, url_prefix='/contoh')
app.register_blueprint(user, url_prefix='/user')
#--------------------- END REGISTER BLUEPRINT ------------------------