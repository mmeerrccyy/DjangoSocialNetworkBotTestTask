import random

import requests
from enum import StrEnum

from data_generators import generate_email, generate_password, generate_username, generate_random_text
from config_loader import Config

CONFIG_FILE_PATH = "./config.yml"
loaded_config = Config(CONFIG_FILE_PATH)


class APIKeys(StrEnum):
    REGISTER_API = f"{loaded_config.api}users/register"
    POST_API = f"{loaded_config.api}posts/"
    LIKE_API = f"{loaded_config.api}like/"


class RequestTypes(StrEnum):
    REGISTER_USER_TYPE = "REGISTER"
    CREATE_POST_TYPE = "CREATE_POST"
    GET_POSTS_TYPE = "GET_POSTS"
    LIKE_TYPE = "LIKE"


users_keys = []
posts = []


def register_request(username, email, password):
    response = requests.post(
        APIKeys.REGISTER_API,
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )
    return response.json()


def create_post_request(text, access_key):
    response = requests.post(
        APIKeys.POST_API,
        {"text": text},
        headers={
            "Authorization": f"Bearer {access_key}"
        }
    )
    return response.json()


def get_posts_request():
    return requests.get(APIKeys.POST_API).json()


def like_post(post_id, access_key):
    response = requests.get(
        f"{APIKeys.LIKE_API}?post_id={post_id}",
        headers={"Authorization": f"Bearer {access_key}"}
    )
    return response.json()


def request_generator(request_type, max_number_of_requests=None):
    if request_type == RequestTypes.GET_POSTS_TYPE:
        for post in get_posts_request():
            posts.append(post["id"])
        return

    for _ in range(random.randint(1, max_number_of_requests)):
        match request_type:
            case RequestTypes.REGISTER_USER_TYPE:
                generated_username = generate_username()
                generated_email = generate_email(generated_username)
                generated_password = generate_password()
                response = register_request(generated_username, generated_email, generated_password)
                users_keys.append(response["access_token"])
            case RequestTypes.CREATE_POST_TYPE:
                for user_token in users_keys:
                    generated_text = generate_random_text()
                    create_post_request(generated_text, user_token)
            case RequestTypes.LIKE_TYPE:
                for user_token in users_keys:
                    random_post = random.choice(posts)
                    like_post(random_post, user_token)


if __name__ == "__main__":
    request_generator(RequestTypes.REGISTER_USER_TYPE, loaded_config.max_users)
    request_generator(RequestTypes.CREATE_POST_TYPE, loaded_config.max_posts)
    request_generator(RequestTypes.GET_POSTS_TYPE)
    request_generator(RequestTypes.LIKE_TYPE, loaded_config.max_likes_per_user)
