
class SuccessHandler:
    def success_200(self, detail):
        return_data = {
            "detail": detail,
            "status": "200",
        }
        return return_data
    
    def success_201(self):
        return_data = {
            "detail": "Insert Success",
            "status": "201",
        }
        return return_data
    
    def success_204(self):
        return_data = {
            "detail": "Delete Success",
            "status": "204",
        }
        return return_data

