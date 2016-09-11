# Simple implementation of thumbor-communities s3_storage


from remotecv.utils import logger
from bucket import Bucket

import urllib2
import os


def load_sync(path):
	"""
	Loads image from S3 Bucket
	:param string path: full path containing bucket
	"""
	path = urllib2.unquote(path)
	bucket = path.lstrip('/').split('/')
	key = '/'.join(path.split('/'))[1:]
	logger.warn('[PATCH_BUCKET_KEY]: '+ str(type(path))
	region = os.environ.get('AWS_REGION', 'us-east-1')

	bucket_loader = Bucket(bucket, region)

	return bucket_loader.get(key)