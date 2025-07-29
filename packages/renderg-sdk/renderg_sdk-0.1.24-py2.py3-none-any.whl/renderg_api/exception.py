
class RenderGAPIError(Exception):

    def __init__(self, err_code, err_msg, request_url):
        self.err_code = err_code
        self.err_msg = err_msg
        self.request_url = request_url

    def __str__(self):
        return 'Error code: {}, Error message: {}, URL: {}'.format(
            self.err_code,
            self.err_msg,
            self.request_url
        )
