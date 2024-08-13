from django.db import models

class Key(models.Model):
    name = models.CharField(max_length=50)
    uid = models.CharField(max_length=150)
    secret = models.CharField(max_length=150)
    token = models.CharField(max_length=150, null=True, blank=True)
    valid_until = models.BigIntegerField(null=True, blank=True)
    expire_date = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.uid

    class Meta:
        ordering = ['name']

class Piscine(models.Model):
    month = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    sort_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.month} {self.year}"

    def user_count(self):
        return self.user_set.count()

    class Meta:
        ordering = ['-sort_order']

class User(models.Model):
    user_id = models.PositiveIntegerField(unique=True)
    login = models.CharField(max_length=16, null=True, blank=True)
    evaluation_points = models.IntegerField()
    location = models.CharField(max_length=16, null=True, blank=True)
    wallet = models.PositiveIntegerField()
    updated_at = models.CharField(max_length=64, null=True, blank=True)
    image = models.URLField(max_length=255, null=True, blank=True)
    active = models.BooleanField()
    profile_url = models.URLField(max_length=255, null=True, blank=True)
    favorite_users = models.ManyToManyField('self', symmetrical=False, related_name='favorited_by', blank=True)
    piscine = models.ForeignKey(Piscine, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.login

    class Meta:
        ordering = ['-user_id']

class Project(models.Model):
    name        = models.CharField(max_length=128, null=True, blank=True)
    slug        = models.CharField(max_length=128, null=True, blank=True)
    project_id  = models.IntegerField()
    status      = models.CharField(max_length=64, null=True, blank=True)
    validated   = models.BooleanField()
    final_mark  = models.IntegerField()
    marked_at   = models.CharField(max_length=64, null=True, blank=True)
    cursus_id   = models.PositiveIntegerField()
    user        = models.ForeignKey(User, on_delete=models.CASCADE)  # Many-to-One relation

    def __str__(self):
        return f"{self.name} - {self.user.login}"

    class Meta:
        ordering = ['-marked_at']

class CursusProject(models.Model):
    project_id          = models.IntegerField()
    name                = models.CharField(max_length=128, null=True, blank=True)
    slug                = models.CharField(max_length=128, null=True, blank=True)
    difficulty          = models.IntegerField()
    estimate_time       = models.CharField(max_length=128, null=True, blank=True)
    is_subscriptable    = models.BooleanField()
    project_url         = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['difficulty']

class Cursus(models.Model):
    name            = models.CharField(max_length=255, null=True, blank=True)
    level           = models.FloatField()
    begin_at        = models.CharField(max_length=64, null=True, blank=True)
    blackholed_at   = models.CharField(max_length=255, null=True, blank=True)
    cursus_id       = models.PositiveIntegerField(null=True)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)  # Many-to-One relation

    def __str__(self):
        return f"login: {self.user.login} - cursus: {self.cursus_id} - level: {self.level}"

    class Meta:
        ordering = ['-cursus_id']


class ClusterLocation(models.Model):
    host        = models.CharField(max_length=32, primary_key=True)
    begin_at    = models.CharField(max_length=64, null=True, blank=True)
    profile_url = models.URLField(max_length=255, null=True, blank=True)
    image       = models.URLField(max_length=255, null=True, blank=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"host: {self.host}"

    class Meta:
        ordering = ['host']


class UsefulLink(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=1024)
    creator = models.CharField(max_length=100, blank=True, null=True)
    link_creator = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

