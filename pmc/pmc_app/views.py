from django.shortcuts import render
from django.http import HttpResponse, FileResponse, JsonResponse
from django.conf import settings
from rest_framework import viewsets, permissions, status, views
import requests
import json

from pmc.helper_functions import ValidateRequestData, ResponseHandler
from pmc_app.models import UserProfile, QuestionMaster, AnswerMaster, QuestionCategoryMaster, \
    QuestionTypeMaster, AgeGroupMaster
from pmc_app.searializers import UserProfileSerializer, QuestionMasterSerializer, AnswerMasterSerializer, \
    QuestionCategoryMasterSerializer, QuestionTypeMasterSerializer, AgeGroupMasterSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    http_method_names = ['get', 'post', 'patch']

    def create(self, request, *args, **kwargs):
        try:
            request_data_validation = ValidateRequestData(request.data)
            request_data_validation.has(['email', 'mobile'])
            errors = request_data_validation.has_errors()
            if errors:
                response = ResponseHandler([], str(errors), True, status.HTTP_400_BAD_REQUEST)
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
    http_method_names = ['get', 'post', 'patch']


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


