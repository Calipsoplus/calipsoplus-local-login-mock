import logging

from django.contrib.auth import authenticate, login, logout

from rest_framework import status
from rest_framework.decorators import api_view

from login.models import MockUser
from settings.utils.request import JSONResponse

@api_view(['POST'])
def login_user(request):
    """
    Checks if a username and password combination matches with application records.

    Request arguments:
    username -- the name of the user to check
    password -- the password of the user

    Responses:
    HTTP 200 OK -- The user exists and the password matches
    HTTP 400 Bad Request -- Missing arguments or exception during processing
    HTTP 401 Unauthorized -- Any other case
    """
    logout(request)
    try:
        username = request.data['username']
        password = request.data['password']
    except Exception as e:
        return JSONResponse(
            "Expected 'username' and 'password'",
            status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JSONResponse('Login OK', status=status.HTTP_200_OK)
    else:
        return JSONResponse('Unable to authenticate', status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def check_umbrella_linked_account(request):
    """
    Checks if an account exists for a certain EAA hash (Umbrella).

    Request arguments:
    eea_hash -- the hash returned by the Umbrella SSO system

    Responses:
    HTTP 200 OK -- An account exists with this hash, the account name is returned
    HTTP 404 Not Found -- No account has been found with this hash
    HTTP 400 Bad Request -- Missing arguments or error during processing
    """

    logger.info('Attempting to check for linked Umbrella account')
    try:
        eaa_hash = request.data['eaa_hash']
        logger.debug('Got EAA Hash')
    except Exception as e:
        logger.error(e)
        return JSONResponse(
            "Expected 'eaa_hash'",
            status=status.HTTP_400_BAD_REQUEST)
    
    linked_account = MockUser.objects.filter(eaa_hash__icontains=eaa_hash)
    if linked_account.exists():
        logger.info('Found linked Umbrella account')
        return JSONResponse(data={
            'login': linked_account.first().login
        }, status=status.HTTP_200_OK)
    else:
        logger.info('Could not found linked account for provided hash')
        return JSONResponse('Could not found linked account for provided EAA Hash',
            status=status.HTTP_404_NOT_FOUND)


