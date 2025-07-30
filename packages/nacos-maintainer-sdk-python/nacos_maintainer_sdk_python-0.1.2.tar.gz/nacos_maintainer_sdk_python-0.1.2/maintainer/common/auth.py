from maintainer.common.constants import Constants


class Credentials(object):
	def __init__(self, access_key_id, access_key_secret, security_token=None):
		self.access_key_id = access_key_id
		self.access_key_secret = access_key_secret
		self.security_token = security_token

	def get_access_key_id(self):
		return self.access_key_id

	def get_access_key_secret(self):
		return self.access_key_secret

	def get_security_token(self):
		return self.security_token


class CredentialsProvider(object):
	def get_credentials(self):
		return


class StaticCredentialsProvider(CredentialsProvider):
	def __init__(self, access_key_id="", access_key_secret="",
			security_token=""):
		self.credentials = Credentials(access_key_id, access_key_secret,
									   security_token)

	def get_credentials(self):
		return self.credentials

	def set_access_key_id(self, access_key_id):
		self.credentials.access_key_id = access_key_id

	def set_access_key_secret(self, access_key_secret):
		self.credentials.access_key_secret = access_key_secret


class RequestResource(object):

	def __init__(self, type: str, namespace: str, group: str, resource: str):
		self.type = type
		if namespace is None or namespace == "":
			namespace = Constants.DEFAULT_NAMESPACE_ID
		self.namespace = namespace
		if group is None or group == "":
			group = "DEFAULT_GROUP"
		self.group = group
		self.resource = resource

	def get_type(self):
		return self.type

	def get_namespace(self):
		return self.namespace

	def get_group(self):
		return self.group

	def get_resource(self):
		return self.resource
