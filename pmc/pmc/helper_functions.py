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
    def __init__(self, data, message, error, request_status_code, total_onboarded_user=None, total_earning=None):
        self.data = data
        self.message = message
        self.error = error
        self.request_status_code = request_status_code
        self.total_onboarded_user = total_onboarded_user
        self.total_earning = total_earning


    def response_handler(self):
        final_result = {}
        if self.data is not None and len(self.data) > 0:
            final_result["data"] = self.data

        if self.message is not None:
            final_result["message"] = self.message

        if self.error is not None:
            final_result["error"] = self.error

        if self.request_status_code is not None:
            final_result["status"] = self.request_status_code

        if self.total_onboarded_user is not None:
            final_result["total_onboarded_user"] = self.total_onboarded_user

        if self.total_earning is not None:
            final_result["total_earning"] = self.total_earning

        return Response(final_result)