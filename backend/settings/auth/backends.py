from django.conf import settings
import hashlib
import logging

from django.contrib.auth.models import User

from login.models import MockUser

class MockDatabaseAuthBackend:
    """
    Basic authentication backend to authenticate users against a database 
    representing an existing user database in the facility.

    This implements two methods required by Django: authenticate and get_user.
    For more info and more advance implementations, 
    check https://docs.djangoproject.com/en/2.1/topics/auth/customizing/
    """
    logger = logging.getLogger(__name__)

    def authenticate(self, request, username=None, password=None):
        """
        Given a username/password combination, attempt to find it and, 
        if successful, return the associated Django User object.
        """
        self.logger.info('Attempting to authenticate via external database')
        try:
            if None in (username, password):
                self.logger.warning('Tried to authenticate user with missing fields, rejecting')
                return None

            # Fetch user from DB
            self.logger.debug('Authenticating %s', username)
            try:
                mock_user = MockUser.objects.get(login=username)
            except MockUser.DoesNotExist:
                self.logger.info('%s not found in database', username)
                return None

            # Check match
            if password == mock_user.password:
                self.logger.info('Authenticated %s', username)
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist as dne:
                    self.logger.info('Creating %s user in django database, as it is not yet present', username)
                    # User will have unusable password in Django's own model, 
                    # authentication is handled through the external db
                    user = User.objects.create_user(username,'')
                    user.save()
                return user
            return None

        except Exception as e:
            self.logger.error(e)
            raise e

    def get_user(self, user_id):
        """
        Retrieve the user's entry in the User model if it exists
        :param user_id:
        :return:
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
