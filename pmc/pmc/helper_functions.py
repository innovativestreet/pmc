from rest_framework.response import Response


class ValidateRequestData:
    def __init__(self, data):
        self.data = data
        self.errors = []

    def has(self, list_of_fields):
        for field in list_of_fields:
            if field not in self.data:
                self.errors.append(f'{field} is required')
                continue
            if self.data[field] == "":
                self.errors.append(f'{field} should not be blank')
                continue
            if self.data[field] is None:
                self.errors.append(f'{field} should not be null')
                continue

    def has_errors(self):
        if self.errors:
            return self.errors[0]
        return None


class ResponseHandler:
    def __init__(self, data, message, error, request_status_code):
        self.data = data
        self.message = message
        self.error = error
        self.request_status_code = request_status_code

    # without data set
    def response_handler(self):
        return Response({"result":{
            "message": self.message, "error": self.error, "status": self.request_status_code
        }})