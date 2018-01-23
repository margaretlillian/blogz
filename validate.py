import re

class FormValidator:
    def __init__(self, usr_input):
        self.usr_input = usr_input

    @staticmethod
    def is_bad_username(username):
        error = ''
        if not re.match(r"^[a-zA-Z0-9_-]*$", username):
            error += "No special characters except for '_' and '-'. "
        if len(username) < 3 or len(username) > 20:
            if username == '':
                error += "Please enter a username. "
            else:
                error += "Usernames must be between 3 and 20 characters. "
        else:
            return ''
        return error
            
    @staticmethod
    def is_invalid_email(email):
        error = ''
        if not re.match(r"^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$", email):
            error += "That is not a valid email. "
        if len(email) > 30:
            error += "Emails must be shorter than 30 characters. "
        if email == '':
            error += "Please enter an email address. "
        else: 
            return ''
        return error
            
    @staticmethod
    def is_invalid_password(pw):
        if not re.match(r"(?=^.{8,100}$)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&amp;*()_+}{&quot;:;'?/&gt;.&lt;,])(?!.*\s).*$", pw):
            return "Passwords must be at least 8 characters, and have a lowercase letter, uppercase letter, digit, and special character."
        else:
            return ''
    @staticmethod
    def does_not_match(pw1, pw2):
        if pw1 != pw2:
            return "Passwords do not match"
        else:
            return ''
            
    def __str__(self):
        return self.usr_input