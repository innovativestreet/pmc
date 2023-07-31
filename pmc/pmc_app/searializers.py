from rest_framework import serializers
from pmc_app.models import *


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class QuestionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionMaster
        fields = "__all__"


class AnswerMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerMaster
        fields = "__all__"


class AgeGroupMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroupMaster
        fields = "__all__"


class QuestionTypeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTypeMaster
        fields = "__all__"


class QuestionCategoryMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategoryMaster
        fields = "__all__"
