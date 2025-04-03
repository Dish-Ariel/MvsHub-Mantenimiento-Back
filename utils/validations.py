import datetime

class SuscriberValidator:
    def whatIsIdUser(id):
        if(id == "" or id == None):
            return "error"
        
        if "@" in id and id.count('@') == 1:
            return "email"
        
        if id.find("@") == -1:
            if(id.startswith("5") and len(id) >=9):
                return "idCustomer"
            else:
                return "siebel"
        
    def checkIfIsEmail(email):
        if(" " in email):
            return False
        
        if "@" in email and email.count('@') == 1:
            return True
        else:
            return False
        
    def checkIfIsDate(date_text):
        try:
            date = datetime.date.fromisoformat(date_text)
            return date
        except ValueError:
            return False