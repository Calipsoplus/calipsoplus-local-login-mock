from django.db import models

class MockUser(models.Model):
    """Object representing a user in the authentication system of the local facility."""
    login = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    eea_hash = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.login)
