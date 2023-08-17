class MessagesDTO:
	CODE_ERROR= "CODE_ERROR"
	CODE_OK= "CODE_OK"
	CODE_WARNIG= "CODE_WARNIG"

	WARNING_SAME_VALUE = "WARNING_SAME_VALUE"
	WARNING_NOTMATCH_CONGINTO_DB = "WARNING_NOTMATCH_CONGINTO_DB"

	ERROR_INVALID_ID_OR_EMAIL= "ERROR_INVALID_ID_OR_EMAIL"
	ERROR_INVALID_METHOD= "ERROR_INVALID_METHOD"
	ERROR_INVALID_EMAIL= "ERROR_INVALID_EMAIL"

	ERROR_SUSCRIBER_NOT_FOUNDIN_BD= "ERROR_SUSCRIBER_NOT_FOUNDIN_BD"
	ERROR_EMAIL_NOT_FOUNDIN_BD= "ERROR_EMAIL_NOT_FOUNDIN_BD"
	ERROR_EMAIL_ALREADY_EXISTIN_BD= "ERROR_EMAIL_ALREADY_EXISTIN_BD"
	ERROR_UPDATEIN_BD= "ERROR_UPDATEIN_BD"
	
	ERROR_EMAIL_ALREADY_EXISTIN_COGNITO= "ERROR_EMAIL_ALREADY_EXISTIN_COGNITO"
	ERROR_EMAIL_NOT_FOUNDIN_COGNITO= "ERROR_EMAIL_NOT_FOUNDIN_COGNITO"
	ERROR_UPDATEIN_COGNITO= "ERROR_UPDATEIN_COGNITO"

	ERROR_USER_HAS_PAYMENTS ="ERROR_USER_HAS_PAYMENTS"
	OK_USER_FOUND= "OK_USER_FOUND"


	ERROR_WITH_CONNECTION_DB = "ERROR_WITH_CONNECTION_DB"
	def OK_USER_UPDATED_SES(newEmail, oldEmail): 
		return """TIPO DE FALLA:ERROR EN EL CORREO ELECTRONICO Buen día Se ha actualizado al correo solicitado ({}) correo anterior ({}), por favor validar que el cliente pueda acceder con sus credenciales o de aplicar un reset de contraseña en caso de no contar con el pass. Saludos""".format(newEmail,oldEmail)
	
	def OK_USER_UPDATED(newEmail, oldEmail): 
		return """TIPO DE FALLA:ERROR EN EL CORREO ELECTRONICO Buen día Se ha actualizado al correo solicitado ({}) correo anterior ({}), por favor validar que el cliente pueda acceder con sus credenciales. Saludos""".format(newEmail,oldEmail)
	
	def OK_USER_DELETED(USER, user_ses):
		if USER["dth"] == "SI" and len(user_ses) != 0 :
			return """Buen día A petición se elimina la cuenta DTH {} con correo ({}) y teléfono {} de la bd de mvshub al igual que en SES Se reasigna con nuestros compañeros de Siebel para que nos apoyen a eliminar la carpeta de Dish digital Saludos""".format(USER["id_customer"],USER["email"],USER["mobile"])
		elif USER["dth"] == 'NO' and USER["id_cliente_siebel"] == 0:
			return """TIPO DE FALLA: SE REGISTRO COMO CLIENTE DIGITAL(CLIENTE DTH) Buen día Se valida y el registro fue como cliente digital, se elimina la cuenta {} de mvshub,  favor de solicitar al cliente que se registre nuevamente con el número de teléfono que tiene ligado a su cuenta dth para realizar una correcta migración. Saludos""".format(USER["email"])
		elif USER["dth"] == 'NO' and len(user_ses)!= 0 :
			return """Buen día A petición se elimina la cuenta Digital {} con correo ({}) y teléfono {} de la bd de mvshub al igual que en SES Se reasigna con nuestros compañeros de Siebel para hacer lo propio en Siebel Saludos""".format(USER["id_customer"],USER["email"],USER["mobile"])
		else:
			return """TIPO DE FALLA: FALLA REGISTRO APP Buen día A petición se elimina la cuenta DTH {} con correo ({}) y teléfono {} de la bd de mvshub. Saludos""".format(USER["id_customer"],USER["email"],USER["mobile"])

	def getJson():
		values = {

		}
		return values
