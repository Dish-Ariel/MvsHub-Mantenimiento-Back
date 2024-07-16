class ResponseDTO:

	def __init__(self):
		self.code = "CODE_ERROR"
		self.description = ""
		self.data = {}

	@property
	def code(self):
		return self.__code
	
	@code.setter
	def code(self, code):
		self.__code = code
	
	@property
	def description(self):
		return self.__description
	
	@description.setter
	def description(self, description):
		self.__description = description
			
	@property
	def data(self):
		return self.__data
	
	@data.setter
	def data(self, data):
		self.__data = data
		
		
	def getJSON(self):
		return {
			"code" : str(self.__code),
            "description" : str(self.__description),
	        "data" : str(self.__data)
        }

