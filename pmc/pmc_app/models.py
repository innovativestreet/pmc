from django.db import models


class UserProfile(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    mobile = models.PositiveIntegerField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)


class QuestionMaster(models.Model):
    question = models.CharField(max_length=255, null=True, blank=True)
    question_gender_group = models.CharField(max_length=10, null=True, blank=True)
    question_age_group_id = models.PositiveIntegerField(null=True, blank=True)
    question_type_id = models.PositiveIntegerField(null=True, blank=True)
    question_category_id = models.PositiveIntegerField(null=True, blank=True)
    question_is_active = models.PositiveIntegerField(null=True, blank=True)


class AnswerMaster(models.Model):
    answer = models.CharField(max_length=255, null=True, blank=True)
    question_id = models.CharField(max_length=10, null=True, blank=True)
    answer_weightage = models.PositiveIntegerField(null=True, blank=True)
    answer_is_active = models.PositiveIntegerField(null=True, blank=True)


class AgeGroupMaster(models.Model):
    # Teenagers <= 17 Years
    # Young Adults >17 && <= 28 Years
    # Adults >28 && <= 48  Years
    # Middle Age >48 && <= 64  Years
    # Old Age > 64 Years
    name = models.CharField(max_length=255, null=True, blank=True)
    min_age = models.PositiveIntegerField(null=True, blank=True)
    max_age = models.PositiveIntegerField(null=True, blank=True)


class QuestionTypeMaster(models.Model):
    # Personal, Professional, Surrounding, Health, Ethics etc
    name = models.CharField(max_length=255, null=True, blank=True)


class QuestionCategoryMaster(models.Model):
    # Anxity, Depression, etc
    name = models.CharField(max_length=255, null=True, blank=True)
