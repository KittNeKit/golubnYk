# Social Media API

This Django REST framework-based API serves as a RESTful interface for a social media platform.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/social-media-api
```

2. Change to the project's directory:
```bash
cd social-media-api
```
3. Сopy .env_sample file with your examples of env variables to your .env
file


4. Once you're in the desired directory, run the following command to create a virtual environment:
```bash
python -m venv venv
```
5. Activate the virtual environment:

On macOS and Linux:

```bash
source venv/bin/activate
```
On Windows:
```bash
venv\Scripts\activate
```

6. Install the dependencies

```bash
pip install -r requirements.txt
```

7. Set up the database:

Run the migrations

```bash
python manage.py migrate
```


8. Start the development server
```bash
python manage.py runserver
```
9. Access the website locally at http://localhost:8000.


10. Link to the swagger documentation http://localhost:8000/api/doc/swagger/

## Features:

- Authentication: Implement a secure method of accessing API endpoints by utilizing JWT token-based authentication.


- Post management: Enable comprehensive CRUD functionality to handle posts, including their creation, retrieval. Additionally, provide the ability to filter posts based on their hashtags. Also User can see only owns posts and posts their following users




- User management: Allow users to register, modify their profile details.


- API documentation: Utilize Swagger UI to automatically generate interactive API documentation, which facilitates developers in effortlessly exploring and testing the API's endpoints.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.



