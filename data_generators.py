import secrets
import string


def generate_username(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def generate_email(username, domain="example.com"):
    return f"{username}@{domain}"


def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))


def generate_random_text(length=50):
    characters = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    return ''.join(secrets.choice(characters) for _ in range(length))
