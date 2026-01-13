import datetime, warnings

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# from .contoh.controllers import contoh
# from .user.controllers import user

warnings.simplefilter("ignore", DeprecationWarning)
jwt = JWTManager()

def create_app():
	#-------------- CONFIGURATION ------------------------
	app = Flask(__name__, static_url_path=None) #panggil modul flask

	app.config['CORS_HEADERS'] = 'Content-Type'
	app.config["SECRET_KEY"] = "R4h4s!AD0n6"
	app.config["JWT_SECRET_KEY"] = "R4h4s!AD0n6"
	app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=1)
	app.config['JWT_DEFAULT_REALM'] = 'Login Required'

	CORS(app, resources={r"*": {"origins": "*"}})
	jwt.init_app(app)
	#------------- END CONFIGURATION ------------------------

	# #--------------------- ERROR HANDLER ------------------------
	# # fungsi error handle Halaman Tidak Ditemukan
	# @app.errorhandler(404)
	# @cross_origin()
	# def not_found(error):
	# 	return make_response(jsonify({'error': 'Tidak Ditemukan','status_code':404}), 404)

	# #fungsi error handle Halaman internal server error
	# @app.errorhandler(500)
	# @cross_origin()
	# def not_found(error):
	# 	return make_response(jsonify({'error': 'Error Server','status_code':500}), 500)
	# #-------------------- END ERROR HANDLER ------------------------

	# def tambahLogs(logs):
	# 	f = open(app.config['LOGS'] + "/" + secure_filename(strftime("%Y-%m-%d"))+ ".txt", "a")
	# 	f.write(logs)
	# 	f.close()

	#--------------------- REGISTER BLUEPRINT ------------------------
	# app.register_blueprint(contoh, url_prefix='/contoh')
	# app.register_blueprint(user, url_prefix='/user')
	#-------------------- END REGISTER BLUEPRINT ------------------------

	print("===> Application Initialized <===")

	return app