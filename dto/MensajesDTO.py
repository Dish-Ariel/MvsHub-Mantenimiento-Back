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

	OK_USER_FOUND= "OK_USER_FOUND"
	OK_USER_DELETED= "OK_USER_DELETED"

	def OK_USER_UPDATED_SES(newEmail, oldEmail): 
		return """TIPO DE FALLA:ERROR EN EL CORREO ELECTRONICO Buen día Se ha actualizado al correo solicitado ({}) correo anterior ({}), por favor validar que el cliente pueda acceder con sus credenciales o de aplicar un reset de contraseña en caso de no contar con el pass. Saludos""".format(newEmail,oldEmail)
	
	def OK_USER_UPDATED(newEmail, oldEmail): 
		return """TIPO DE FALLA:ERROR EN EL CORREO ELECTRONICO Buen día Se ha actualizado al correo solicitado ({}) correo anterior ({}), por favor validar que el cliente pueda acceder con sus credenciales. Saludos""".format(newEmail,oldEmail)
	
	def getJson():
		values = {

		}
		return values
