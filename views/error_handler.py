
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
