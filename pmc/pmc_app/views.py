from django.shortcuts import render
from django.http import HttpResponse, FileResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
from rest_framework import viewsets, permissions, status, views
import requests
import json
import pandas as pd

from pmc.helper_functions import ValidateRequestData, ResponseHandler
from pmc_app.models import UserProfile, QuestionMaster, AnswerMaster, QuestionCategoryMaster, \
    QuestionTypeMaster, AgeGroupMaster, AmbassadorData
from pmc_app.searializers import AmbassadorDataSerializer, UserProfileSerializer, QuestionMasterSerializer, AnswerMasterSerializer, \
    QuestionCategoryMasterSerializer, QuestionTypeMasterSerializer, AgeGroupMasterSerializer


class AmbassadorViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = AmbassadorDataSerializer
    queryset = AmbassadorData.objects.all()
    http_method_names = ['get', 'post', 'patch']

    def create(self, request, *args, **kwargs):
        try:
            request_data_validation = ValidateRequestData(request.data)
            request_data_validation.has(['name', 'email', 'mobile', 'created_by'])
            errors = request_data_validation.has_errors()
            if errors:
                response = ResponseHandler([], str(errors), True, status.HTTP_400_BAD_REQUEST)
                return response.response_handler()

            mobile = request.data.get('mobile')
            user_data = pd.DataFrame(UserProfile.objects.filter(mobile=mobile).values())
            if user_data.empty:
                response = ResponseHandler([], "User not exits, ask user to give test.", True, status.HTTP_200_OK)
                return response.response_handler()

            ambassador_data = pd.DataFrame(AmbassadorData.objects.filter(user_id=user_data['id'][0]).values())
            if not ambassador_data.empty:
                response = ResponseHandler([], "User is already mapped with ambassador.", True, status.HTTP_200_OK)
                return response.response_handler()

            obj = AmbassadorData(user_id=user_data['id'][0], created_by=request.data.get('created_by'), is_approved=0)
            obj.save()

            response = ResponseHandler([], "User mapped successfully", False, status.HTTP_200_OK)
            return response.response_handler()

        except Exception as e:
            response = ResponseHandler([], "Something went wrong", True, status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response.response_handler()

    def retrieve(self, request, *args, **kwargs):
        try:
            ambassador_id = int(kwargs["pk"])
            ambassador_data = pd.DataFrame(AmbassadorData.objects.filter(created_by=ambassador_id).values())
            if ambassador_data.empty:
                response = ResponseHandler([], "Ambassador not exits", True, status.HTTP_200_OK)
                return response.response_handler()

            result = []
            for index, ambassador in ambassador_data.iterrows():
                user_id = ambassador["user_id"]
                is_user_approved = ambassador["is_approved"]

                user_data = pd.DataFrame(UserProfile.objects.filter(id=user_id).values())
                if user_data.empty:
                    continue

                user_name = user_data["name"][0]
                user_email = user_data["email"][0]
                user_mobile = user_data["mobile"][0]

                data = {"user_name": user_name, "user_email": user_email, "user_mobile": user_mobile.formatted, "user_approved": is_user_approved}
                result.append(data)

            total_onboarded_user = len(result)
            total_earning = 100 # TODO: need logic

            response = ResponseHandler(result, None, False, status.HTTP_200_OK, total_onboarded_user, total_earning)
            return response.response_handler()
        except Exception as e:
            response = ResponseHandler([], "Something went wrong", True, status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response.response_handler()


class LoginViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        try:
            username = request.data["username"]
            password = request.data["password"]

            user_data = pd.DataFrame(UserProfile.objects.filter(username=username, password=password).values())
            if user_data.empty:
                response = ResponseHandler([], "User id or password not correct", True, status.HTTP_200_OK)
                return response.response_handler()

            result = []
            for index, user in user_data.iterrows():
                user_name = user["username"]
                user_gender = user["gender"]
                user_role = user["role"]
                user_total_coins = user["total_coins"]
                user_total_onboarded_user = user["total_onboarded_user"]

                data = {"user_name": user_name, "user_gender": user_gender}
                if user_role == 4:
                    data["user_total_coins"] = user_total_coins
                    data["user_total_onboarded_user"] = user_total_onboarded_user
                    data["user_role"] = user_role

                result.append(data)

            response = ResponseHandler(result, "User Exist", False, status.HTTP_200_OK)
            return response.response_handler()
        except Exception as e:
            response = ResponseHandler([], "Something went wrong", True, status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response.response_handler()


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def list(self, request, *args, **kwargs):
        user_data = pd.DataFrame(UserProfile.objects.values())
        if user_data.empty:
            response = ResponseHandler([], "Data not found", True, status.HTTP_200_OK)
            return response.response_handler()

        result = []
        for index, user in user_data.iterrows():
            user_name = user["username"]
            user_gender = user["gender"]
            user_role = user["role"]
            user_total_coins = user["total_coins"]
            user_total_onboarded_user = user["total_onboarded_user"]

            data = {"user_name": user_name, "user_gender": user_gender}
            if user_role == 4:
                data["user_total_coins"] = user_total_coins
                data["user_total_onboarded_user"] = user_total_onboarded_user

            result.append(data)

        response = ResponseHandler(result, "User Exist", False, status.HTTP_200_OK)
        return response.response_handler()

    def retrieve(self, request, *args, **kwargs):
        user_id = int(kwargs["pk"])
        user_data = pd.DataFrame(UserProfile.objects.filter(id=user_id).values())
        if user_data.empty:
            response = ResponseHandler([], "User not exits", True, status.HTTP_200_OK)
            return response.response_handler()

        result = []
        for index, user in user_data.iterrows():
            user_name = user["username"]
            user_gender = user["gender"]
            user_role = user["role"]
            user_total_coins = user["total_coins"]
            user_total_onboarded_user = user["total_onboarded_user"]

            data = {"user_name": user_name, "user_gender": user_gender}
            if user_role == 4:
                data["user_total_coins"] = user_total_coins
                data["user_total_onboarded_user"] = user_total_onboarded_user

            result.append(data)

        response = ResponseHandler(result, "User Exist", False, status.HTTP_200_OK)
        return response.response_handler()

    @action(methods=['POST'], detail=False)
    def update_ambassador_details(self, request):
        onboarded_by = request.data["onboarded_by"]
        onboarded_data = request.data["onboarded_data"]

        for user in onboarded_data:
            try:
                obj = UserProfile.objects.get(mobile=user["user_mobile"], role=2)
                obj.created_by = onboarded_by
                obj.save()
            except Exception as e:
                pass

        response = ResponseHandler([], "User Successfully Updated", False, status.HTTP_200_OK)
        return response.response_handler()

    def create(self, request, *args, **kwargs):
        try:
            request_data_validation = ValidateRequestData(request.data)
            request_data_validation.has(['email', 'mobile'])
            errors = request_data_validation.has_errors()
            if errors:
                response = ResponseHandler([], str(errors), True, status.HTTP_400_BAD_REQUEST)
                return response.response_handler()

            email = request.data.get('email')
            mobile = request.data.get('mobile')

            user_data = pd.DataFrame(UserProfile.objects.filter(mobile=mobile).values())
            if not user_data.empty:
                response = ResponseHandler([], "User already exits", True, status.HTTP_200_OK)
                return response.response_handler()

            user_creation_resp = super(UserProfileViewSet, self).create(request)

            if user_creation_resp.status_code not in [200, 201]:
                response = ResponseHandler([], "User not created", True, status.HTTP_500_INTERNAL_SERVER_ERROR)
                return response.response_handler()

            response = ResponseHandler([], "User Successfully Created", False, status.HTTP_200_OK)
            return response.response_handler()

        except Exception as e:
            response = ResponseHandler([], "Something went wrong", True, status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response.response_handler()

    def update(self, request, *args, **kwargs):
        try:
            user_update_resp = super(UserProfileViewSet, self).update(request, partial=True)
            if user_update_resp.status_code not in [200, 201]:
                response = ResponseHandler([], "Update Failed", True, status.HTTP_500_INTERNAL_SERVER_ERROR)
                return response.response_handler()

            response = ResponseHandler([], "Updated Successfully", False, status.HTTP_200_OK)
            return response.response_handler()
        except Exception as e:
            response = ResponseHandler([], "Something went wrong", True, status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response.response_handler()


class QuestionCategoryMasterViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = QuestionCategoryMasterSerializer
    queryset = QuestionCategoryMaster.objects.all()
    http_method_names = ['get', 'post', 'patch']


class QuestionTypeMasterViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = QuestionTypeMasterSerializer
    queryset = QuestionTypeMaster.objects.all()
    http_method_names = ['get', 'post', 'patch']


class AgeGroupMasterViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = AgeGroupMasterSerializer
    queryset = AgeGroupMaster.objects.all()
    http_method_names = ['get', 'post', 'patch']


class AnswerMasterViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = AnswerMasterSerializer
    queryset = AnswerMaster.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def destroy(self, request, *args, **kwargs):
        try:
            records = AnswerMaster.objects.filter(question_id=kwargs['pk']).delete()
            if records[0] > 0:
                response = ResponseHandler([], "Records Deleted", False, status.HTTP_200_OK)
                return response.response_handler()
            response = ResponseHandler([], "Records Not Found", False, status.HTTP_200_OK)
            return response.response_handler()
        except Exception as e:
            response = ResponseHandler([], "Something went wrong", True, status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response.response_handler()


class QuestionMasterViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = QuestionMasterSerializer
    queryset = QuestionMaster.objects.all()
    http_method_names = ['get', 'post', 'patch']

    def create(self, request, *args, **kwargs):
        try:
            request_data_validation = ValidateRequestData(request.data)
            request_data_validation.has(['question', 'answer_1', 'weight_1'])
            errors = request_data_validation.has_errors()
            if errors:
                response = ResponseHandler([], str(errors), True, status.HTTP_400_BAD_REQUEST)
                return response.response_handler()

            request.data['question_is_active'] = request.data.get('question_is_active', 1)
            request.data['question_gender_group_id'] = request.data.get('question_gender_group_id', 1)
            request.data['question_age_group_id'] = request.data.get('question_age_group_id', 1)
            request.data['question_type_id'] = request.data.get('question_type_id', 1)
            request.data['question_category_id'] = request.data.get('question_category_id', 1)

            question_creation_resp = super(QuestionMasterViewSet, self).create(request)

            if question_creation_resp.status_code not in [200, 201]:
                response = ResponseHandler([], "Question not created", True, status.HTTP_500_INTERNAL_SERVER_ERROR)
                return response.response_handler()

            question_id = question_creation_resp.data["id"]
            for i in [1, 2, 3, 4, 5]:
                answer_key = "answer_" + str(i)
                weight_key = "weight_" + str(i)
                answer = request.data.get(answer_key, None)
                weight = request.data.get(weight_key, 1)
                if answer is not None:
                    answer_request = {
                        "question_id": question_id,
                        "answer": answer,
                        "answer_weightage": weight
                    }

                    header = {'Content-Type': 'application/json'}
                    qes_ans_resp = requests.post(url=f"{settings.API_BASE_URL}/api/v1/question_answer_mapping/",
                                                 data=json.dumps(answer_request), headers=header)

                    if qes_ans_resp.status_code not in [200, 201]:
                        response = ResponseHandler([], "Question's answer not mapped", True,
                                                   status.HTTP_500_INTERNAL_SERVER_ERROR)
                        return response.response_handler()

            response = ResponseHandler([], "Question Created Successfully", False, status.HTTP_200_OK)
            return response.response_handler()

        except Exception as e:
            response = ResponseHandler([], "Something went wrong", True, status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response.response_handler()

    def update(self, request, *args, **kwargs):
        """
        In QuestionMaster Table: partial update will be perform
        In AnswerMaster Table: remove existing record for question id and create new record
        """
        try:
            question_creation_resp = super(QuestionMasterViewSet, self).update(request, partial=True)

            if question_creation_resp.status_code not in [200, 201]:
                response = ResponseHandler([], "Update Failed", True, status.HTTP_500_INTERNAL_SERVER_ERROR)
                return response.response_handler()

            question_id = question_creation_resp.data["id"]
            header = {'Content-Type': 'application/json'}
            delete_exiting_data = requests.delete(
                url=f"{settings.API_BASE_URL}/api/v1/question_answer_mapping/{question_id}/",
                headers=header)
            if delete_exiting_data.status_code not in [200, 201]:
                response = ResponseHandler([], "Deletion failed for existing records", True, status.HTTP_500_INTERNAL_SERVER_ERROR)
                return response.response_handler()

            for i in [1, 2, 3, 4, 5]:
                answer_key = "answer_" + str(i)
                weight_key = "weight_" + str(i)
                answer = request.data.get(answer_key, None)
                weight = request.data.get(weight_key, 1)
                if answer is not None:
                    answer_request = {
                        "question_id": question_id,
                        "answer": answer,
                        "answer_weightage": weight
                    }

                    qes_ans_resp = requests.post(url=f"{settings.API_BASE_URL}/api/v1/question_answer_mapping/",
                                                 data=json.dumps(answer_request), headers=header)

                    if qes_ans_resp.status_code not in [200, 201]:
                        response = ResponseHandler([], "Question's answer not mapped", True,
                                                   status.HTTP_500_INTERNAL_SERVER_ERROR)
                        return response.response_handler()

            response = ResponseHandler([], "Question Updated Successfully", False, status.HTTP_200_OK)
            return response.response_handler()

        except Exception as e:
            response = ResponseHandler([], "Something went wrong", True, status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response.response_handler()
