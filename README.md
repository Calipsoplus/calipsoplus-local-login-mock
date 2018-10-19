# CalipsoPlus Local Login Mock

This is a mock implementation of an external authentication system implementing the local authentication REST API required for the CalipsoPlus portal.

**IMPORTANT:** This is only intended to be a demonstration system, not to be used for actual production.

## Local deployment
The following are instructions to deploy the application in a traditional manner:
### Installation
The only previous requirements for installing this application is an existing Python 3.6+ installation with the corresponding pip package.

To install the application, execute the following commands in the terminal:
```bash
git clone git@git.cells.es:mis/calipsoplus-local-login-mock.git -b master calipsologin
cd calipsologin
python3 -m venv env
env/bin/pip install -r backend/requirements.txt
```

### Initializing the model
If this is the first time you run the application, you will need to run the database migrations beforehand to initialize the application model:

```bash
source env/bin/activate
cd backend
python manage.py migrate
```

In addition to that, if you wish to initialize the model with some test users, you may use the JSON fixture provided to that effect:

```bash
python manage.py loaddata users.json
```

This application uses a SQLite3 file-based database, so no special configuration is required.


### Running the application
To run the application in a local environment, simply run the development server (remember to have the virtual environment activated):
```bash
python manage.py runserver
```
This will start a development server in your machine, listening in the port 8000 by default.


## Docker deployment
For your convenience, a Dockerfile is provided to enable launching the application in a container, with a test set of users ready for your use.

If this is your first time deploying the application or you have made changes in the code, you may need to build the image:
```bash
docker build -t calipso_login_mock .
```

After that, you can just run it in the console:
```bash
docker run -p 8000:8000 -it calipso_login_mock
```
Or, if you prefer to run it detached as a daemon:
```bash
docker run -p 8000:8000 -d calipso_login_mock
```

This will get the application running in the port 8000. You may also attach a bash terminal to the container to perform any needed configuration adjustments:

```bash
docker exec -it {container} /bin/bash
```
This will be useful if you need to set a superuser for the application (see next section).

## Adding users
### Through a JSON fixture
You may add new users loading the data from a fixture file, as seen in the *Initializing the model* section.

```bash
python manage.py loaddata users.json
```

### Through the administration site
You can also add users through the administration site, accessible at the (APPLICATION_URL)/admin endpoint.

If this is the first time you run the application, you will have to create a superuser in the application so you can access the administration site. You may do so with the following command:

```bash
python manage.py createsuperuser
```

The MockUser model contains three fields: "username", "password", and "eea_hash" (used to link with an Umbrella SSO account). 

Please note that to simplify operation the password is stored unhashed, this will obviously not be the case in an actual production environment.

## API
This application provides a basic implementation of the REST API required for the CalipsoPlus Portal. Unless specified, all methods will use JSON as request and response format. 

The following endpoints are provided:

### Login (POST)
Authenticate a username/password combination. This mock implementation only contains a test user, 'calipsoplus', authenticated by a password of the same name.

#### Arguments
* **username**: String. The name of the account we attempt to authenticate.
* **password**: String. The password of the account, unhashed.

#### Responses
* **HTTP 200 OK**: The username/password combination exists, the authentication has succeeded.
* **HTTP 401 Unauthorized**: The username/password does not exist, the authentication has not succeeded.
* **HTTP 400 Bad Request**: Missing arguments or an error has occurred during processing.


### Login/Umbrella (POST)
Check that an account exists linked to the provided EAA hash (Umbrella) and returns the local username if found.

#### Arguments
* **eaa_hash**: String. Hash returned by the Umbrella SSO system.

#### Responses
* **HTTP 200 OK**: An account exists with the provided EAA hash, the local username is returned.
* **HTTP 404 Not Found**: An account does not exist with the provided EAA hash.
* **HTTP 400 Bad Request**: Missing arguments or an error has occurred during processing.



