from django.db import models


class Calendar_API(models.Model):
    Name = models.CharField(blank=False, max_length=50)
    Description = models.TextField(blank=True)
    Date = models.DateField(blank=False)
    Time = models.TimeField(blank=True, null=True)

    tag_choices = [
        ("Work", "Work"),
        ("Fun", "Fun"),
    ]
    Tag = models.CharField(blank=True, max_length=5, choices=tag_choices)

    def __str__(self):
        return self.Name
