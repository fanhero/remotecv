# Simple botocore Bucket loader implmentation


import botocore.session

class Bucket(object):
	"""
	Handles AWS S3 API
	"""

	_bucket = None
	_region = None
	_cache = dict()

	def __init__(self, bucket, region):
		"""
		Constructor
		:param string bucket: Bucket name
		:param string region: AWS Region
		:return: The initialized Bucket
		"""
		self._bucket = bucket
		self._region = region
	
		session = None or botocore.session.get_session()
		self._client = session.create_client('s3', region_name=self._region)

	def get(self, key):
		"""
		Returns objects matching key from bucket
		:param string key: Key to retrieve the file
		"""
		s3_object = self._client.get_object(Bucket=self._bucket, Key=key)
		return s3_object['Body'].read()