from django.db import models


class Resume(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    professional_summary = models.TextField(blank=True)

    company = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=100, blank=True)
    experience_describtion = models.TextField(blank=True)

    college = models.CharField(max_length=150, blank=True)
    degree = models.CharField(max_length=100, blank=True)
    passing_year = models.CharField(max_length=20, blank=True)

    skill1 = models.CharField(max_length=100, blank=True)
    skill2 = models.CharField(max_length=100, blank=True)
    skill3 = models.CharField(max_length=100, blank=True)
    skill4 = models.CharField(max_length=100, blank=True)

    project_name = models.CharField(max_length=150, blank=True)
    project_description = models.TextField(blank=True)

    template = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
