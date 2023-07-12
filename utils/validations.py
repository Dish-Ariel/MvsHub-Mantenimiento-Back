class SuscriberValidator:
    def whatIsIdUser(id):
        if "@" in id and id.count('@') == 1:
            return "email"
        if id.find("@") == -1 and len(id)<=9:
            return "id"
        else:
            return "error"
        
    def checkIfIsEmail(email):
        if "@" in email and email.count('@') == 1:
            return True
        else:
            return False