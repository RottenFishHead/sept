from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """
    Storage for static files (CSS, JS, images)
    Collected with collectstatic -> goes into <bucket>/static/
    """
    location = "static"
    default_acl = "public-read"


class MediaStorage(S3Boto3Storage):
    """
    Storage for uploaded media files (CKEditor images, user uploads)
    Saved into <bucket>/media/
    """
    location = "media"
    file_overwrite = False  # don’t overwrite files with same name
    default_acl = "public-read"