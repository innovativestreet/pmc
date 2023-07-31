from django.shortcuts import render
from django.http import HttpResponse, FileResponse, JsonResponse
from django.conf import settings
from rest_framework import viewsets, permissions, status, views
import requests
import json

from pmc_app.models import UserProfile, QuestionMaster, AnswerMaster, QuestionCategoryMaster, \
    QuestionTypeMaster, AgeGroupMaster
from pmc_app.searializers import UserProfileSerializer, QuestionMasterSerializer, AnswerMasterSerializer, \
    QuestionCategoryMasterSerializer, QuestionTypeMasterSerializer, AgeGroupMasterSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    http_method_names = ['get', 'post', 'patch']


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
            question = request.data.get('question', None)
            if question is None:
                return JsonResponse({"msg": "Question is mandatory", "error": True},
                                    status=status.HTTP_400_BAD_REQUEST)

            question_creation_resp = super(QuestionMasterViewSet, self).create(request)

            if question_creation_resp.status_code not in [200, 201]:
                return JsonResponse({"msg": "Question not created", "error": True},
                                    status=status.is_success())

            question_id = question_creation_resp.data["id"]
            for i in [1, 2, 3, 4, 5]:
                answer_key = "answer_" + str(i)
                weight_key = "weight_" + str(i)
                answer = request.data.get(answer_key, None)
                weight = request.data.get(weight_key, None)
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
                        return JsonResponse({"msg": "Question not created", "error": True},
                                                status=status.is_success())

            return JsonResponse({"msg": "Question Created Successfully", "error": False},
                                status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"msg": "Something went wrong", "error": True},
                                status=status.is_success())

