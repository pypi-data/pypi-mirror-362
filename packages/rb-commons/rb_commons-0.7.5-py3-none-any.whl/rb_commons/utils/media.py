from pydantic import ValidationError

class MediaUtils:

    @staticmethod
    def url_builder(key: str):
        try:
            from rb_commons.configs.config import configs
            DIGITALOCEAN_S3_ENDPOINT_URL = configs.DIGITALOCEAN_S3_ENDPOINT_URL
            DIGITALOCEAN_STORAGE_BUCKET_NAME = configs.DIGITALOCEAN_STORAGE_BUCKET_NAME
        except ValidationError as e:
            from rb_commons.configs.v2.config import configs
            DIGITALOCEAN_S3_ENDPOINT_URL = configs.DIGITALOCEAN_S3_ENDPOINT_URL
            DIGITALOCEAN_STORAGE_BUCKET_NAME = configs.DIGITALOCEAN_STORAGE_BUCKET_NAME

        return "{endpoint_url}/{bucket_name}/{key}" \
            .format(endpoint_url=DIGITALOCEAN_S3_ENDPOINT_URL,
                    bucket_name=DIGITALOCEAN_STORAGE_BUCKET_NAME, key=key)