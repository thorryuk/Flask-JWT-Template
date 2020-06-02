from flask import Blueprint, jsonify, request, make_response
from flask_jwt import JWT, jwt_required, current_identity
from flask import current_app as app
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import hashlib
import datetime
import requests
import cv2
from models import Data
from time import gmtime, strftime
import os
import numpy as np
import base64
import random
import warnings
from werkzeug.datastructures import ImmutableMultiDict
import string
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes



now = datetime.datetime.now()

user = Blueprint('user', __name__, static_folder = '../../upload/foto_user', static_url_path="/media")
#UNTUK SAVE GAMBAR
def save(encoded_data, filename):
	arr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
	img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
	return cv2.imwrite(filename, img)

def tambahLogs(logs):
	f = open(app.config['LOGS'] + "/" + secure_filename(strftime("%Y-%m-%d"))+ ".txt", "a")
	f.write(logs)
	f.close()

def encrypt(data):
	#encode
	key = "tWBbsFB6EN5FXYhz"
	iv = "4CDxzzA0K4f5SsAH"
	# key1 = get_random_bytes(16)
	# key2 = get_random_bytes(16)
	word = data

	def set_text(text):
	    t = []
	    for i in text:
	        t.append(i)

	    min = 16 - (len(t) % 16) -1
	    if str(min) != "0":
	        new = ''.join(random.choice(string.ascii_uppercase) for _ in range(min))
	        text = text+"#"+new
	    return text

	text16 = set_text(word)

	decryptor = AES.new(key, AES.MODE_CBC, iv)
	aes_enc = decryptor.encrypt(text16)

	# key1 = base64.b64encode(key1).decode('utf-8')
	# key2 = base64.b64encode(key2).decode('utf-8')

	key = base64.b64encode(key).decode('utf-8')
	iv = base64.b64encode(iv).decode('utf-8')

	# print("key1 : %s \nkey2 : %s" % (key1,key2))
	print("key : %s \niv : %s" % (key,iv))

	encoded = base64.b64encode(aes_enc).decode('utf-8')
	print("encode : %s" % encoded)
	return encoded



# ========================= GET AREA ===============================
@user.route('/get_user', methods=['GET', 'OPTIONS'])
# @jwt_required()
@cross_origin()
def get_user():
	query = "SELECT * FROM user WHERE 1"
	values = ()

	page = request.args.get("page")
	is_aktif = request.args.get("is_aktif")
	q = request.args.get("q")

	if (page == None):
		page = 1
	if is_aktif:
		query = query + " AND is_aktif = %s "
		values = values + (is_aktif, )
	if q:
		query += " AND CONCAT_WS('|', judul, deskripsi) LIKE %s "
		values += ('%'+q+'%',)
	
	dt = Data()
	rowCount = dt.row_count(query, values)
	hasil = dt.get_data_lim(query, values, page)
	hasil_akhir = encrypt(hasil)
	hasil = {'data': hasil_akhir , 'status_code': 200, 'page': page, 'offset': '10', 'row_count': rowCount}
	########## INSERT LOG ##############
	imd = ImmutableMultiDict(request.args)
	imd = imd.to_dict()
	param_logs = "[" + str(imd) + "]"
	logs = "{'action':'Lihat user','params':'"+ param_logs +"','date':'"+secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+"'}\n"
	tambahLogs(logs)
	####################################
	return make_response(jsonify(hasil),200)

# ================================= POST AREA ==============================
@user.route('/insert_user', methods=['POST', 'OPTIONS'])
# @jwt_required()
@cross_origin()
# @check_roles(permission='1')
def insert_user():
	query = ""
	values = ()
	try:
		data = request.json
		user1 = data['user1']
		foto = data['foto']
		
		filename = secure_filename(strftime("%Y-%m-%d %H:%M:%S")+"_foto_user.png")
		save(foto, os.path.join(app.config['UPLOAD_FOLDER_GAMBAR_user'], filename))

		dt = Data()
		values = (user1, pass_ency, nama, no_telepon, alamat, filename, jk, tanggal_lahir)
		dt.insert_data(query,values)

		hasil = "berhasil"
		param_logs = "[" + str(data) + "]"
		logs = "{'id_user':'"+ "str(current_identity['user_id'])" +"','roles':'"+ "str(current_identity['roles'])" +"','action':'Tambah Artikel','date':'"+secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+"'}\n"
		tambahLogs(logs)
	except Exception as e:
			return make_response(jsonify({'description':str(e),'error': 'Bad Request','status_code':400}), 400)
	return make_response(jsonify({'status_code':200, 'description': hasil } ), 200)

# ================================ UPDATE AREA =================================
@user.route('/update_user', methods=['PUT', 'OPTIONS'])
# @jwt_required()
@cross_origin()
# @check_roles(permission='1')
def update_user():
	tableName = "user"
	try:
		dt = Data()
		data = request.json

		query = "UPDATE "+tableName+" SET id_user = id_user"

		values = ()

		id_user = data['id_user']

		if 'user1' in data:
			user1 = data["user1"]
			query = query + ", user1 = %s"
			values = values + (user1, )
		if 'foto' in data:
			foto = data["foto"]
			query = query + ", foto = %s"

			filename = secure_filename(strftime("%Y-%m-%d %H:%M:%S")+"_foto_user.png")
			save(foto, os.path.join(app.config['UPLOAD_FOLDER_GAMBAR_user'], filename))
			
			values = values + (filename, )

		query = query + " WHERE id_user = %s "
		values = values + (id_user, )
		dt = Data()
		dt.insert_data(query,values)

		
		hasil = "berhasil"
		if "" in data:
			del data['foto']
		param_logs = "[" + str(data) + "]"
		logs = "{'id_user':'"+ "str(current_identity['user_id'])" +"','roles':'"+ "str(current_identity['roles'])" +"','action':'Update artikel','params':'"+ param_logs +"','date':'"+secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+"'}\n"
		tambahLogs(logs)
	except Exception as e:
		return make_response(jsonify({'description':str(e),'error': 'Bad Request','status_code':400}), 400)
	return make_response(jsonify({'status_code':200, 'description': hasil } ), 200)
