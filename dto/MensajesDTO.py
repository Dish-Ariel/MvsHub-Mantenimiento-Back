class MessagesDTO:
	CODE_ERROR= "CODE_ERROR"
	CODE_OK= "CODE_OK"
	CODE_WARNIG= "CODE_WARNIG"

	WARNING_SAME_VALUE = "WARNING_SAME_VALUE"
	WARNING_NOTMATCH_CONGINTO_DB = "WARNING_NOTMATCH_CONGINTO_DB"

	ERROR_INVALID_ID_OR_EMAIL= "ERROR_INVALID_ID_OR_EMAIL"
	ERROR_INVALID_METHOD= "ERROR_INVALID_METHOD"
	ERROR_INVALID_EMAIL= "ERROR_INVALID_EMAIL"
	ERROR_INVALID_DATE= "ERROR_INVALID_DATE"

	ERROR_SUSCRIBER_NOT_FOUNDIN_BD= "ERROR_SUSCRIBER_NOT_FOUNDIN_BD"
	ERROR_SUSCRIBER_NOT_FOUNDIN_SBL= "ERROR_SUSCRIBER_NOT_FOUNDIN_SBL"
	ERROR_SUSCRIBER_NOT_READYTO_DISABLE= "ERROR_SUSCRIBER_NOT_READYTO_DISABLE"
	ERROR_SUSCRIBER_ALREADY_DISABLE_AMAZON= "ERROR_SUSCRIBER_ALREADY_DISABLE_AMAZON"
	ERROR_EMAIL_NOT_FOUNDIN_BD= "ERROR_EMAIL_NOT_FOUNDIN_BD"
	ERROR_EMAIL_ALREADY_EXISTIN_BD= "ERROR_EMAIL_ALREADY_EXISTIN_BD"
	ERROR_UPDATEIN_BD= "ERROR_UPDATEIN_BD"
	
	ERROR_EMAIL_ALREADY_EXISTIN_COGNITO= "ERROR_EMAIL_ALREADY_EXISTIN_COGNITO"
	ERROR_EMAIL_NOT_FOUNDIN_COGNITO= "ERROR_EMAIL_NOT_FOUNDIN_COGNITO"
	ERROR_USERNAME_NOT_FOUNDIN_COGNITO= "ERROR_USERNAME_NOT_FOUNDIN_COGNITO"
	ERROR_USERNAME_DISABLED_COGNITO= "ERROR_USERNAME_DISABLED_COGNITO"
	ERROR_UPDATEIN_COGNITO= "ERROR_UPDATEIN_COGNITO"
	ERROR_USER_HAS_PAYMENTS ="ERROR_USER_HAS_PAYMENTS"
	
	ERROR_WITH_CONNECTION_DB = "ERROR_WITH_CONNECTION_DB"

	OK_USERS_FOUND= "OK_USERS_FOUND"
	OK_USER_DISABLED= "OK_USER_DISABLED"
	OK_SUSCRIBER_SERVICES_DISABLED= "OK_SUSCRIBER_SERVICES_DISABLED"

	def OK_USER_UPDATED_SES(newEmail, oldEmail): 
		return """TIPO DE FALLA:ERROR EN EL CORREO ELECTRONICO Buen día Se ha actualizado al correo solicitado ({}) correo anterior ({}), por favor validar que el cliente pueda acceder con sus credenciales o de aplicar un reset de contraseña en caso de no contar con el pass. Saludos""".format(newEmail,oldEmail)
	
	def OK_USER_UPDATED(newEmail, oldEmail): 
		return """TIPO DE FALLA:ERROR EN EL CORREO ELECTRONICO Buen día Se ha actualizado al correo solicitado ({}) correo anterior ({}), por favor validar que el cliente pueda acceder con sus credenciales. Saludos""".format(newEmail,oldEmail)
	
	def OK_USER_DELETED(USER, user_ses):
		
		if USER["dth"] == "SI" and len(user_ses) == 0 :
			return """TIPO DE FALLA: FALLA REGISTRO APP Buen día A petición se elimina la cuenta DTH {} con estatus ({}), correo ({}) y teléfono {} de la bd de mvshub. Saludos""".format(USER["id_customer"],USER['status'],USER["email"],USER["mobile"])
		elif USER["dth"] == "SI" and len(user_ses) != 0:
			return """Buen día A petición se elimina la cuenta Vinculada {} con status ({}), correo ({}) y teléfono {} de la bd de mvshub al igual que en SES Se reasigna con nuestros compañeros de Siebel para que nos apoyen a eliminar la carpeta de Dish digital Saludos""".format(USER["id_customer"],USER["email"],USER["mobile"])
		elif USER["dth"] == "NO" and len(user_ses) == 0:
			return """TIPO DE FALLA : FALLA REGISTRO APP Buen día A petición se elimina la cuenta Lead {} con correo ({}) y teléfono {} de la bd de mvshub. Saludos""".format(USER["id_customer"],USER['status'],USER["email"],USER["mobile"])
		elif USER["dth"] == "NO" and len(user_ses) != 0 and USER["id_cliente_siebel"] == 0:
			return """TIPO DE FALLA : FALLA REGISTRO APP Buen día A petición se elimina la cuenta Lead {} con status({}), correo ({}) y teléfono {} de la bd de mvshub al igual que en SES  Saludos""".format(USER["id_customer"],USER['status'],USER["email"],USER["mobile"])
		elif USER["dth"] == "NO" and len(user_ses) != 0  and USER["id_cliente_siebel"] != 0:
			return """Buen día A petición se elimina la cuenta Lead {} con status ({}), correo ({}) y teléfono {} de la bd de mvshub al igual que en SES Se reasigna con nuestros compañeros de Siebel para hacer lo propio en Siebel Saludos""".format(USER["id_customer"],USER['status'],USER["email"],USER["mobile"])
		else:
			return "SE ELIMINO USUARIO CON ESTATUS NO CONSIDERADO"
	def getJson():
		values = {

		}
		return values
