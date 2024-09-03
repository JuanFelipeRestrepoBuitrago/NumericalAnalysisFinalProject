# Numerical Analysis Final Project

## Content Table
- [Developers](#developers)
- [Introduction](#introduction)
- [Project Structure](#project-structure)
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
├── .env.example # Environment variables example. \
├── README.md # Folder or Service README. \
├── Dockerfile # File to build the docker image. \
└── requirements.txt # Python dependencies. \

## Setup Instructions

1. **Environment Setup**: Make sure you have python 3.8 or higher installed. The python version used was the 3.9.13.
2. **Directory Navigation**: navigate to the BACKEND directory `cd BACKEND`.
3. **Virtual Environment Setup (Optional)**: setup a python venv if desired `python -m  venv .venv` and activate it `.venv\Scripts\activate` in Windows or `source .venv\bin\activate` in Linux or Mac.
4. **Dependencies Installation**: Execute `pip install -r requirements.txt` to install the needed dependencies. 
5. **Environment Variables**: Configure the environment variables as in the `.env.example` file.
6. **Execution**: Execute `uvicorn app.app:app --reload --port 8000` to initialize the API in the 8000 port. 

## Docker Image

### Image Build

You can access the api's image docker hub [piper04](https://hub.docker.com/r/piper04/upnpc) user or build your own image following the next steps:

1. **Navigate to the Backend Directory**: navigate to the BACKEND directory `cd BACKEND`.
2. **Build an image**: Create or build the image of the backend API with your docker hub user `docker build -t "$USER/$PROJECT_NAME:$API_NAME.v$API_VERSION" . --no-cache --network host` or without it `docker build -t "$PROJECT_NAME:$API_NAME.v$API_VERSION" . --no-cache --network host`.
3. **Push the image (Optional)**: Push the docker image you just created to docker hub, is optional. `sudo docker push "$USER/$PROJECT_NAME:$API_NAME.v$API_VERSION"`.

### Image Usage

## Endpoints

The API provides several endpoint to apply or use different numerical methods for different purposes. The available endpoints are: 

- `POST /`: .
- `GET /`: Verifies if the API is Up.

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
