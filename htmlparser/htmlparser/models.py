from django.db import models


class HtmlData(models.Model):
    h1_count = models.PositiveIntegerField()
    h2_count = models.PositiveIntegerField()
    h3_count = models.PositiveIntegerField()
    links = models.ManyToManyField('Links', related_name="links")


class Links(models.Model):
    link = models.URLField()

    def natural_key(self):
        return self.link
