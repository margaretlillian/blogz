import re

class FormValidator:
    def __init__(self, usr_input):
        self.usr_input = usr_input

    @staticmethod
    def is_bad_username(username):
        error = ''
        if not re.match(r"^[a-zA-Z0-9_-]*$", username):
            error += "No special characters except for '_' and '-'. *"
        if len(username) < 3 or len(username) > 20:
            if username == '':
                error += "Please enter a username. *"
            else:
                error += "Usernames must be between 3 and 20 characters."
        return error.split("*")
            
    @staticmethod
    def is_invalid_email(email):
        error = ''
        if not re.match(r"^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$", email):
            error += "That is not a valid email. *"
        if len(email) > 30:
            error += "Emails must be shorter than 30 characters. *"
        if email == '':
            error += "Please enter an email address."
        return error.split("*")
            
    @staticmethod
    def is_invalid_password(pw):
        error = ''
        if not re.match(r"(?=.*?[A-Z]).*$", pw):
            error += "Passwords must have at least one capital letter. *"
        if not re.match(r"(?=.*[a-z])", pw):
            error += "Passwords must have at least one lowercase letter. *"
        if not re.match(r"(?=.*[!@#$%^&amp;*()_+}{&quot;:;'?/&gt;.&lt;,])", pw):
            error += "Passwords must have at least one special character. *"
        if not re.match(r"(?=.*\d)", pw):
            error += "Passwords must have at least one number. *"
        if not re.match(r"(?=^.{8,100}$)", pw):
            error += "Passwords must be at least 8 characters long. "
        return error.split("*")
    @staticmethod
    def does_not_match(pw1, pw2):
        if pw1 != pw2:
            return ["Passwords do not match."]
        else:
            return ''
            
    def __str__(self):
        return self.usr_input