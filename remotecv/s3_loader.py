# Simple implementation of thumbor-communities s3_storage


from remotecv.utils import logger
from bucket import Bucket

import os

def load_sync(path):
	"""
	Loads image from S3 Bucket
	:param string path: full path containing bucket
	"""
	bucket = path.lstrip('/').split('/')
	key = '/'.join(path.split('/'))[1:]
	logging.warn('[PATCH_BUCKET_KEY]', path, bucket, key)
	region = os.environ.get('AWS_REGION', 'us-east-1')

	bucket_loader = Bucket(bucket, region)

	return bucket_loader.get(key)