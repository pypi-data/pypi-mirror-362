import logging

from maintainer.common.auth import StaticCredentialsProvider
from maintainer.common.nacos_exception import NacosException, INVALID_PARAM


class AIMaintainerClientConfig:
    def __init__(self, server_addresses=None,  namespace_id='', context_path='', access_key=None,
                 secret_key=None, username=None, password=None, app_name='', app_key='', log_dir='', log_level=None,
                 log_rotation_backup_count=None, app_conn_labels=None, credentials_provider=None):
        self.server_list = []
        try:
            if server_addresses is not None and server_addresses.strip() != "":
                for server_address in server_addresses.strip().split(','):
                    self.server_list.append(server_address.strip())
        except Exception:
            raise NacosException(INVALID_PARAM, "server_addresses is invalid")

        self.namespace_id = namespace_id
        self.credentials_provider = credentials_provider if credentials_provider else StaticCredentialsProvider(access_key, secret_key)
        self.username = username  # the username for nacos auth
        self.password = password  # the password for nacos auth
        self.app_name = app_name
        self.app_key = app_key
        self.disable_use_config_cache = False
        self.log_dir = log_dir
        self.log_level = logging.INFO if log_level is None else log_level  # the log level for nacos client, default value is logging.INFO: log_level
        self.log_rotation_backup_count = 7 if log_rotation_backup_count is None else log_rotation_backup_count
        self.timeout_ms = 10 * 1000  # timeout for requesting Nacos server, default value is 10000ms
        self.app_conn_labels = app_conn_labels
