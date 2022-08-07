
class ErrorHandler:
    def error_400(self):
        return_data = {
            "detail": "Check Parameters.",
            "status": "400",
        }
        return return_data

    def error_405(self):
        return_data = {
            "detail": "Method Not Allowed.",
            "status": "405",
        }
        return return_data
    
    def error_500(self, detail_ex=None):
        return_data = {
            "detail": "Internal Server Error. {}".format(detail_ex),
            "status": "500",
        }
        return return_data
