"""2Captcha API tasks"""


class BaseTask(object):
    """Base task"""

    def serialize(self, **params):
        """Serialize params"""
        return "".join(["&{0}={1}".format(k, v) for k, v in params.items()])


class GoogleReCaptchav2Task(BaseTask):
    """Google Recaptcha v2"""
    TASK_ID = 'userrecaptcha'
    params = "&method=&googlekey={0}&pageurl={1}"

    def __init__(self, googlekey, pageurl):
        self.googlekey = googlekey
        self.pageurl = pageurl

    def serialize(self):
        """Serialize params"""
        params = {
            'method': self.TASK_ID,
            'googlekey': self.googlekey,
            'pageurl': self.pageurl
        }
        return super(GoogleReCaptchav2Task, self).serialize(**params)
