"""Exception definitions"""


class TwoCaptchaException(Exception):
    def __init__(self, msg, *args):
        super(TwoCaptchaException, self).__init__("{}".format(msg))
        self.msg = msg


class TwoCaptchaTimeoutException(Exception):
    def __init__(self, msg, *args):
        super(TwoCaptchaException, self).__init__("{}".format(msg))
        self.msg = msg


class TwoCaptchaTaskErrorException(Exception):
    def __init__(self, msg, *args):
        super(TwoCaptchaException, self).__init__("{}".format(msg))
        self.msg = msg
