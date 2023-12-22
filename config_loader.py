import yaml


class Config:
    def __init__(self, config_file=None):
        if config_file is None:
            config_file = "config.yml"
        with open(config_file, "r") as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)
        self.max_users = self.config.get("numbers_of_users", 5)
        self.max_posts = self.config.get("numbers_of_posts", 5)
        self.max_likes_per_user = self.config.get("numbers_of_likes_per_user", 5)
        self.api = self.config.get("api_host", "https://localhost:8000/api/")
