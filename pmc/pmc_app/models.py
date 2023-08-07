from django.db import models

class UserRoles(models.Model):
    # 1 -> admin, 2 -> patient, 3 -> doctor
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = 'user_roles'
        indexes = [
            models.Index(fields=['id'])
        ]


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    mobile = models.PositiveIntegerField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    role = models.PositiveIntegerField(default=1)
    address = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'user_profile'
        indexes = [
            models.Index(fields=['id'])
        ]

class UserScoreQuestionCatMapping(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField()
    user_score = models.PositiveIntegerField()
    question_type_id = models.PositiveIntegerField()
    question_cat_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        db_table = 'user_score_question_type_cat_mapping'
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['user_id']),
            models.Index(fields=['question_type_id']),
            models.Index(fields=['question_cat_id']),
        ]

class QuestionMaster(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=500, null=True, blank=True)
    question_gender_group_id = models.PositiveIntegerField(default=0)
    question_age_group_id = models.PositiveIntegerField(default=0)
    question_type_id = models.PositiveIntegerField(default=0)
    question_category_id = models.PositiveIntegerField(default=0)
    question_is_active = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        db_table = 'question_master'
        indexes = [
            models.Index(fields=['id'])
        ]


class AnswerMaster(models.Model):
    id = models.AutoField(primary_key=True)
    answer = models.CharField(max_length=500, null=True, blank=True)
    question_id = models.CharField(max_length=10, null=True, blank=True)
    answer_weightage = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        db_table = 'answer_master'
        indexes = [
            models.Index(fields=['id'])
        ]

class AgeGroupMaster(models.Model):
    # Neutral = 0
    # Teenagers < 20 Years
    # Young Adults >=20 && <= 28 Years
    # Adults >28 && <= 48  Years
    # Middle Age >48 && <= 64  Years
    # Old Age > 64 Years
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    value = models.PositiveIntegerField(null=True, blank=True)
    min_age = models.PositiveIntegerField(null=True, blank=True)
    max_age = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        db_table = 'age_group_master'
        indexes = [
            models.Index(fields=['id'])
        ]


class QuestionTypeMaster(models.Model):
    # Neutral (0), Personal (1), Professional (2), Surrounding (3), Health (4), Ethics (5)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    value = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        db_table = 'question_type_master'
        indexes = [
            models.Index(fields=['id'])
        ]


class QuestionCategoryMaster(models.Model):
    # Neutral (0), Anxity (1), Depression (2)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    value = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        db_table = 'question_category_master'
        indexes = [
            models.Index(fields=['id'])
        ]


class VideoMaster(models.Model):
    id = models.AutoField(primary_key=True)
    video_link = models.CharField(max_length=500, null=True, blank=True)

    # 0 means > general video irrespective of any score
    score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        db_table = 'video_master'
        indexes = [
            models.Index(fields=['id'])
        ]


# class ReportMaster(models.Model):
