import boto3
import src.config as config
import os
import mimetypes
import tempfile
from src.utils.file_utils import get_temporary_filename

class AWSClient(object):
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AWSClient, cls).__new__(cls)
            cls.instance._session = boto3.Session(region_name="ap-southeast-1", aws_access_key_id=config.AWS_ACCESS_KEY_ID, aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)
        return cls.instance

  
    def upload_to_s3(self, local_file, s3_key):
        try:            
            if not os.path.exists(local_file):
                raise FileNotFoundError(local_file)
            content_type = mimetypes.MimeTypes().guess_type(local_file)[0]
            bucket_name = config.S3_BUCKET
            s3 = self._session.client('s3')
            extra_args = {}
            if content_type is not None:
                extra_args['ContentType'] = content_type
            extra_args['ACL'] = 'public-read'
            s3.upload_file(local_file, bucket_name, s3_key, ExtraArgs=extra_args)
            print(f"{local_file} uploaded to {bucket_name}/{s3_key}")
            return True
        except Exception:
            print("AWS credentials not available.")
            return False
    
    def get_s3_public_url(self, key):
        return f"https://{config.S3_BUCKET}.s3.amazonaws.com/{key}"
    
    def download_from_s3(self, key, filename=None):
        bucket = config.S3_BUCKET
        print("download_from_s3")
        suffix = key.split('.')[-1]
        if filename is None:
            if len(key.split('.')) == 1:
                filename = get_temporary_filename('')
            else:
                filename = get_temporary_filename(suffix='.' + suffix)
        s3 = self._session.client('s3')
        s3.download_file(bucket, key, filename)
        print("Downloaded to: {0}".format(filename))
        return filename

    