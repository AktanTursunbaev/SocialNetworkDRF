import requests
from faker import Faker
import config

fake = Faker(use_weighting=False)
user_authentication_details = []
post_ids = []


def signup_user():
    username = fake.first_name().lower()
    password = fake.bothify(text="?#?#?#?#")
    response = requests.post(
        "http://127.0.0.1:8000/user/signup/",
        data={"username": username, "password": password},
    )
    response.raise_for_status()
    print(f"User {username} created")
    return {"username": username, "password": password}


def authenticate_user(username, password):
    response = requests.post(
        "http://127.0.0.1:8000/token/",
        data={"username": username, "password": password},
    )
    response.raise_for_status()
    print(f"User {username} authenticated")
    return response.json()


def create_post(access_token):
    title = fake.word().capitalize()
    content = fake.paragraph()
    response = requests.post(
        "http://127.0.0.1:8000/post/create/",
        data={"title": title, "content": content},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    print(f"Post {title} created")
    return response.json()


def update_access_token(user):
    refresh_token = user["refresh"]
    response = requests.post(
        "http://127.0.0.1:8000/token/refresh/", data={"refresh": refresh_token}
    )
    response.raise_for_status()
    print(f"User {user['username']} refreshed access token")
    user["access"] = response.json()["access"]


def like_post(post_id, user):
    access_token = user["access"]
    response = requests.post(
        f"http://127.0.0.1:8000/post/like/{post_id}/",
        data={"is_liked": True},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    print(f"User {user['username']} liked Post{post_id}")


def main():
    for _ in range(config.NUMBER_OF_USERS):
        credentials = signup_user()
        user_details = {
            "username": credentials["username"],
            "password": credentials["password"],
        }
        token_values = authenticate_user(
            user_details["username"],
            user_details["password"],
        )
        user_details["refresh"] = token_values["refresh"]
        user_details["access"] = token_values["access"]
        user_authentication_details.append(user_details)
        for _ in range(fake.random_int(min=0, max=config.MAX_NUMBER_OF_POSTS_PER_USER)):
            post_details = create_post(user_details["access"])
            post_ids.append(post_details["id"])

    for user in user_authentication_details:
        update_access_token(user)
        maximum_likes = (
            len(post_ids)
            if len(post_ids) < config.MAX_NUMBER_OF_LIKES_PER_USER
            else config.MAX_NUMBER_OF_LIKES_PER_USER
        )
        selected_post_ids = fake.random_elements(
            elements=post_ids,
            length=fake.random_int(min=0, max=maximum_likes),
            unique=True,
        )
        for post_id in selected_post_ids:
            like_post(post_id, user)


if __name__ == "__main__":
    main()
