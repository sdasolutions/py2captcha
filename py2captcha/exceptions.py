"""Exception definitions"""


class TwoCaptchaException(Exception):
    def __init__(self, error_code, information, *args):
        super(TwoCaptchaException, self).__init__("{}".format(error_code))
        self.error_code = error_code
        self.information = information
