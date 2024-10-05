# Numerical Analysis Final Project

## Content Table
- [Developers](#developers)
- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Pre-requisites](#pre-requisites)
- [Setup Instructions](#setup-instructions)
- [Contribution](#contribution)
- [License](#license)
- [Contact](#contact)

## Developers

- Juan Felipe Restrepo Buitrago (Main)
- Kevin Quiroz González 

## Introduction

This is the backend section of this project. It's an API which handles the functions or methods to give the retrieved data to the frontend.

## Project Structure

. \
├── app \
│   ├── auth \
│   │   ├── __init__.py # Authentication initialization. \
│   │   └── auth.py # Authentication handling file. \
│   ├── config \
│   │   ├── __init__.py # Configuration initialization. \
│   │   ├── database.py # Database handling file. \
│   │   ├── env.py # Environment variables handling file. \
│   │   └── limiter.py # Rate limiter handling file. \
│   ├── domain \
│   │   ├── __init__.py # Domain initialization. \
│   │   ├── gaussian_elimination.py # Gaussian Elimination method. \
│   │   ├── lu_factorization.py # LU Factorization method. \
│   │   └── methods.py # Numerical methods handling file. \
│   ├── models \
│   │   ├── __init__.py # Models initialization. \
│   │   ├── db_models.py # Database models file. \
│   │   └── models.py # Routes models file. \
│   ├── routes \
│   │   ├── linear_equation_systems \
│   │   │   ├── __init__.py # Linear Equation Systems initialization. \
│   │   │   └── routes.py # Linear Equation Systems routes file. \
│   │   ├── methods \
│   │   │   ├── __init__.py # Methods initialization. \
│   │   │   └── routes.py # Methods routes file. \
│   │   ├── __init__.py # Routes initialization. \
│   │   └── routes.py # Routes file. \
│   ├── tests \
│   │   ├── domain \
│   │   │   ├── linear_equation_systems \
│   │   │   │   ├── gaussian_elimination \
│   │   │   │   │   ├── __init__.py # Gaussian Elimination initialization. \
│   │   │   │   │   └── test.py # Gaussian Elimination test file. \
│   │   │   │   ├── lu_factorization \
│   │   │   │   │   ├── __init__.py # LU Factorization initialization. \
│   │   │   │   │   └── test.py # LU Factorization test file. \
│   │   │   │   └── __init__.py # Linear Equation Systems initialization. \
│   │   │   ├── methods \
│   │   │   │   ├── __init__.py # Methods initialization. \
│   │   │   │   └── test.py # Methods test file. \
│   │   │   └── __init__.py # Domain initialization. \
│   │   ├── routes \
│   │   │   ├── linear_equation_systems \
│   │   │   │   ├── __init__.py # Linear Equation Systems initialization. \
│   │   │   │   └── test.py # Linear Equation Systems test file. \
│   │   │   ├── methods \
│   │   │   │   ├── __init__.py # Methods initialization. \
│   │   │   │   └── test.py # Methods test file. \
│   │   │   ├── __init__.py # Routes initialization. \
│   │   │   └── test.py # Routes test file. \
│   │   ├── utils \
│   │   │   ├── __init__.py # Utils initialization. \
│   │   │   └── test.py # Utils test file. \
│   │   └── __init__.py # Tests initialization. \
│   ├── utils \
│   │   ├── __init__.py # Utils initialization. \
│   │   ├── crud.py # CRUD handling file. \
│   │   └── utils.py # Utils handling file. \
│   ├── __init__.py # API initialization. \
│   └── app.py # API routes and methods. \
├── .env.example # Environment variables example. \
├── README.md # Folder or Service README. \
├── Dockerfile # File to build the docker image. \
├── .dockerignore # Files to ignore when building the docker image. \
└── requirements.txt # Python dependencies. \

## Pre-requisites

- Python 3.8 or higher.
- Pip.
- Virtual Environment (Optional).
- Docker (Optional).
- MYSQL Database with the sql script provided in the [SQL Script File](../DEPLOY/db/db.sql).

## Setup Instructions

1. **Environment Setup**: Make sure you have python 3.8 or higher installed. The python version used was the 3.9.13.
2. **Directory Navigation**: navigate to the BACKEND directory `cd BACKEND`.
3. **Virtual Environment Setup (Optional)**: setup a python venv if desired `python -m  venv .venv` and activate it `.venv\Scripts\activate` in Windows or `source .venv\bin\activate` in Linux or Mac.
4. **Dependencies Installation**: Execute `pip install -r requirements.txt` to install the needed dependencies. 
5. **Environment Variables**: Configure the environment variables as in the `.env.example` file.
6. **Execution**: Execute `uvicorn app.app:app --reload --port 8000` to initialize the API in the 8000 port. 

## Docker Image

### Image Build

The access is private, so you need to ask for the access to the docker image in the ghcr.io registry. `ghcr.io/juanfeliperestrepobuitrago/numericalanalysisfinalproject/methods_solver_backend_api:latest`.

1. **Navigate to the Backend Directory**: navigate to the BACKEND directory `cd BACKEND`.
2. **Build an image**: Create or build the image of the backend API with your docker hub user `docker build -t "$USER/$PROJECT_NAME:$API_NAME.v$API_VERSION" . --no-cache --network host` or without it `docker build -t "$PROJECT_NAME:$API_NAME.v$API_VERSION" . --no-cache --network host`.
3. **Push the image (Optional)**: Push the docker image you just created to docker hub, is optional. `sudo docker push "$USER/$PROJECT_NAME:$API_NAME.v$API_VERSION"`.

### Image Usage

#### Docker Image

For using the docker image, you can run the following command:

```bash
docker run -d -p 8000:8000 --env-file .env ${USER}/methods_solver_backend_api:${TAG}
```

#### Docker Compose

For using the docker image with docker compose, you can run the following command for the docker-compose file in the DEPLOY directory [docker-compose.yml](../DEPLOY/docker-compose.yml):

```yaml
dokcer-compose up -d
```

## Endpoints

The API provides several endpoint to apply or use different numerical methods for different purposes. The available endpoints are: 

- `POST /`: .
- `GET /`: Verifies if the API is Up.
- `POST /api/${API_VERSION}/${API_NAME}/login`: Login endpoint.
- `GET /api/${API_VERSION}/${API_NAME}/protected`: Test login endpoint.
- `POST /api/${API_VERSION}/${API_NAME}/methods/bisection/`: Bisection method endpoint.
- `POST /api/${API_VERSION}/${API_NAME}/methods/false_rule/`: False Rule method endpoint.
- `POST /api/${API_VERSION}/${API_NAME}/methods/fixed_point/`: Fixed Point method endpoint.
- `POST /api/${API_VERSION}/${API_NAME}/methods/newton_raphson/`: Newton Raphson method endpoint.
- `POST /api/${API_VERSION}/${API_NAME}/methods/secant/`: Secant method endpoint.
- `POST /api/${API_VERSION}/${API_NAME}/methods/first_modified_newton_method/`: First Modified Newton method endpoint for multiple roots.
- `POST /api/${API_VERSION}/${API_NAME}/linear_equations_system/gauss_elimination/`: Gaussian Elimination method endpoint.
- `POST /api/${API_VERSION}/${API_NAME}/linear_equations_system/lu_factorization/`: LU Factorization method endpoint.

## Contribution

For contributing to this project, follow the instructions below:

1. **Fork the repository**: Make a fork of the repository and clone your fork on your local machine.
2. **Create a new branch**: Create a new branch with a name which gives an idea of the addition or correction to the project. 
3. **Make your changes**: Make your code changes and test them. 
4. **Make a pull request**: Finally, make a pull request to the original repository. 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, feel free to reach out to:
- Juan Felipe Restrepo Buitrago: [jfrestrepb@eafit.edu.co](jfrestrepb@eafit.edu.co)
- Kevin Quiroz González: [kquirozg@eafit.edu.co](mailto:kquirozg@eafit.edu.co)
