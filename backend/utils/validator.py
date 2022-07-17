import re


class Validator:
    global connection

    def __init__(self):
        self._errors = []

    """
    regular
    """

    def required(self, params):
        if len([x for x in params if x is None]) > 0:
            self._errors.append("Information is incomplete")

    def is_letter_number_only(self, str):
        if re.match("^[A-Za-z0-9]*$", str):
            return True
        return False

    """
    User
    """

    def check_username(self, input, letterNumberOnly=False):
        if letterNumberOnly == True and self.is_letter_number_only(input) == False:
            self._errors.append("username has illegal characters")
            return

        if input is None or len(input) < 6 or len(input) > 30:
            self._errors.append("username format is wrong")

    def check_nickname(self, input, letterNumberOnly=False):
        if letterNumberOnly == True and self.is_letter_number_only(input) == False:
            self._errors.append("nickname has illegal characters")
            return

        if input is None or len(input) < 6 or len(input) > 30:
            self._errors.append("nickname format is wrong")

    def check_password(self, input, letterNumberOnly=False):
        if letterNumberOnly == True and self.is_letter_number_only(input) == False:
            self._errors.append("Password has illegal characters")
            return

        if input is None or len(input) < 6 or len(input) > 30:
            self._errors.append("Password format is wrong")


    def get_errors(self):
        return self._errors