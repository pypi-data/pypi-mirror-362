#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import logging

import yaml
import requests

from xenoslib.base import SingletonWithArgs


logger = logging.getLogger(__name__)


class YamlConfig(dict):
    """A thread unsafe yaml file config utility , can work as a dict except __init__"""

    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, name, value):
        try:
            getattr(super(), name)
        except AttributeError as exc:
            if str(exc).startswith("'super' object has no attribute "):
                self[name] = value
                return
            raise exc
        raise AttributeError(f"'{__class__.__name__}' object attribute '{name}' is read-only")

    def __str__(self):
        return yaml.safe_dump(self.copy(), allow_unicode=True)

    def __repr__(self):
        return repr(str(self))

    def __init__(self, conf_path=None):
        pass

    def __new__(cls, conf_path="config.yml", *args, **kwargs):
        if not hasattr(cls, "_instances"):
            cls._instances = {}
        if cls._instances.get(conf_path) is None:
            cls._instances[conf_path] = super().__new__(cls)
            super().__setattr__(cls._instances[conf_path], "_conf_path", conf_path)
        cls._instances[conf_path]._load_conf()
        return cls._instances[conf_path]

    def _load_conf(self):
        if os.path.exists(self._conf_path):
            with open(self._conf_path, encoding="utf-8") as r:
                self.update(yaml.safe_load(r))

    def save(self):
        data = str(self)
        with open(self._conf_path, "w", encoding="utf-8") as w:
            w.write(data)
            # yaml.safe_dump(self.copy(), w, allow_unicode=True)


class RequestAdapter:
    def request(self, method, path, *args, **kwargs):
        """to-do: support stream=True"""
        url = f"{self.base_url}/{path}"
        logger.debug(url)
        response = self.session.request(method, url, *args, **kwargs)
        logger.debug(response.text)
        response.raise_for_status()
        try:
            return response.json()
        except Exception as exc:
            logger.debug(exc)
            return response

    def get(self, path, *args, **kwargs):
        return self.request("get", path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return self.request("post", path, *args, **kwargs)

    def put(self, path, *args, **kwargs):
        return self.request("put", path, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        return self.request("delete", path, *args, **kwargs)

    def patch(self, path, *args, **kwargs):
        return self.request("patch", path, *args, **kwargs)

    def head(self, path, *args, **kwargs):
        return self.request("head", path, *args, **kwargs)

    def __init__(self):
        self.session = requests.Session()


def del_to_recyclebin(filepath, on_fail_delete=False):
    """delete file to recyclebin if possible"""
    if not sys.platform == "win32":
        if on_fail_delete:
            os.remove(filepath)
            return True
        return False
    from win32com.shell import shell, shellcon

    res, _ = shell.SHFileOperation(
        (
            0,
            shellcon.FO_DELETE,
            filepath,
            None,
            shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,
            None,
            None,
        )
    )
    return res == 0


def send_notify(msg, key):
    """send a message for ifttt"""
    url = f"https://maker.ifttt.com/trigger/message/with/key/{key}"
    data = {"value1": msg}
    return requests.post(url, data=data, timeout=(30, 30))


class IFTTTLogHandler(logging.Handler):
    """
    log handler for IFTTT
    usage：
    key = 'xxxxx.xxxzx.xxxzx.xxxzx'
    iftttloghandler = IFTTTLogHandler(key, level=logging.INFO)
    logging.getLogger(__name__).addHandler(iftttloghandler)
    """

    def __init__(self, key, level=logging.CRITICAL, *args, **kwargs):
        self.key = key
        super().__init__(level=level, *args, **kwargs)

    def emit(self, record):
        try:
            send_notify(self.format(record), self.key)
        except Exception as exc:
            print(exc)


class SlackLogHandler(logging.Handler):
    """
    log handler for Slack
    usage：
    slackloghandler = SlackLogHandler(webhook_url, level=logging.INFO)
    logging.getLogger(__name__).addHandler(slackloghandler)
    """

    def __init__(self, webhook_url, level=logging.CRITICAL, *args, **kwargs):
        self.url = webhook_url
        self.headers = {"Content-type": "application/json"}
        super().__init__(level=level, *args, **kwargs)

    def emit(self, record):
        try:
            data = {"text": self.format(record)}
            requests.post(self.url, headers=self.headers, json=data, timeout=(30, 30))
        except Exception as exc:
            print(exc)


class DingTalkLogHandler(logging.Handler):
    """
    log handler for DingTalk
    usage：
    token = 'xxxxx.xxxzx.xxxzx.xxxzx'
    dingtalkloghandler = DingTalkLogHandler(token, level=logging.INFO)
    logging.getLogger(__name__).addHandler(dingtalkloghandler)
    """

    def __init__(self, token, level=logging.CRITICAL, *args, **kwargs):
        self.token = token
        super().__init__(level=level, *args, **kwargs)

    def emit(self, record):
        headers = {"Content-Type": "application/json"}
        url = "https://oapi.dingtalk.com/robot/send"
        params = {"access_token": self.token}
        msg = self.format(record)
        data = {"msgtype": "text", "text": {"content": msg}}
        try:
            response = requests.post(
                url, headers=headers, params=params, json=data, timeout=(10, 10)
            )
            print(response.json())
        except Exception as exc:
            print(exc)


class ConfigLoader(SingletonWithArgs):
    """Centralized configuration management with optional Vault integration.

    Args:
        config_file_path (str): Path to the YAML configuration file. Defaults to "config.yml".
        vault_secret_id (str, optional): Secret ID for Vault authentication.
            If provided, enables Vault functionality and imports hvac module.

    Attributes:
        cache (dict): Cache storage for frequently accessed configuration values.

    Example:
        # Without Vault (hvac not imported)
        >>> config = ConfigLoader("config.yml")

        # With Vault (hvac imported on demand)
        >>> config = ConfigLoader("config.yml", vault_secret_id="my-secret-id")
    """

    cache = {}
    vault_client = None

    def __init__(self, config_file_path="config.yml", vault_secret_id=None):
        """Initialize the ConfigLoader with a configuration file and optional Vault secret."""
        with open(config_file_path, "r") as f:
            self._raw_config = yaml.safe_load(f) or {}

        if vault_secret_id is not None:
            self.vault_secret_id = vault_secret_id
            self._check_and_renew_vault_client()

    def _init_vault_client(self):
        """Initialize and authenticate the Vault client (imports hvac on demand).

        Args:
            vault_secret_id (str): Secret ID for Vault authentication.

        Raises:
            ImportError: If hvac package is not installed.
            KeyError: If required Vault configuration is missing.
            Exception: If Vault authentication fails.
        """
        try:
            import hvac  # Lazy import
        except ImportError as e:
            raise ImportError(
                "hvac package is required for Vault integration. " "Install with: pip install hvac"
            ) from e

        try:
            vault_config = self._raw_config.get("vault", {})
            vault_url = vault_config.get("url")
            vault_space = vault_config.get("space")
            vault_role_id = vault_config.get("role_id")

            if not all([vault_url, vault_space, vault_role_id]):
                raise KeyError("Missing required Vault configuration in config.yml")

            self.vault_client = hvac.Client(url=vault_url, namespace=vault_space, timeout=45)
            self.vault_client.auth.approle.login(
                role_id=vault_role_id, secret_id=self.vault_secret_id
            )
        except Exception as e:
            self.vault_client = None
            raise Exception(f"Failed to initialize Vault client: {str(e)}")

    def _check_and_renew_vault_client(self):
        # 检查当前Token的状态，包括过期时间和可续租性
        if not self.vault_client or not self.vault_client.is_authenticated():
            # 如果当前Token无效，则重新认证
            self._init_vault_client()

    def get(self, section, key_name, use_cache=True):
        """Retrieve a configuration value.

        Args:
            section (str): The configuration section name.
            key_name (str): The key name within the section.
            use_cache (bool): Whether to use cached values. Defaults to True.

        Returns:
            The configuration value, which may come from:
            - Direct configuration value
            - Vault secret (if Vault is initialized)
            - Cache (if enabled)

        Raises:
            KeyError: If the section or key is not found.
            Exception: If Vault access is required but not available.
        """
        if section not in self._raw_config:
            raise KeyError(f"Section '{section}' not found")

        # Check for direct value first
        if key_name in self._raw_config[section]:
            return self._raw_config[section][key_name]

        # Handle Vault reference if Vault is enabled
        vault_key = f"{key_name}@vault"
        if vault_key in self._raw_config[section]:
            if self.vault_client is None:
                raise Exception(
                    f"Vault access required for {key_name} but Vault is not initialized"
                )

            cache_key = f"{section}_{key_name}"

            if use_cache and cache_key in self.cache:
                return self.cache[cache_key]
            value = self._get_value_from_vault(section, key_name)
            self.cache[cache_key] = value
            return value

        raise KeyError(f"Key '{key_name}' or '{vault_key}' not found in section '{section}'")

    def _get_value_from_vault(self, section, key_name):
        """Retrieve a secret value from Vault.

        Args:
            section (str): The configuration section name.
            key_name (str): The key name within the section.

        Returns:
            The secret value from Vault.

        Raises:
            Exception: If Vault access fails.
        """
        try:
            vault_path = self._raw_config[section]["vault_path"]
            vault_key = self._raw_config[section][f"{key_name}@vault"]
            vault_namepsace = self._raw_config[section].get("vault_namespace")
            if vault_namepsace:
                self.vault_client.adapter.namespace = vault_namepsace
            else:
                self.vault_client.adapter.namespace = self._raw_config["vault"]["space"]
            data = self.vault_client.secrets.kv.read_secret_version(
                path=vault_path, mount_point="kv", raise_on_deleted_version=True
            )
            return data["data"]["data"][vault_key]
        except Exception as e:
            raise Exception(f"Failed to fetch {key_name} from Vault: {str(e)}")

    def __getitem__(self, section):
        """Dictionary-style access to configuration sections."""
        if section not in self._raw_config:
            raise KeyError(f"Section '{section}' not found")
        return SectionProxy(self, section)

    def __getattr__(self, section):
        """Attribute-style access to configuration sections."""
        try:
            return self[section]
        except KeyError as e:
            raise AttributeError(str(e))


class SectionProxy:
    """Proxy class for configuration section access."""

    def __init__(self, config_loader, section):
        self._loader = config_loader
        self._section = section

    def __getitem__(self, key):
        """Dictionary-style access to configuration values."""
        return self._loader.get(self._section, key)

    def __getattr__(self, key):
        """Attribute-style access to configuration values."""
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(str(e))

    def __repr__(self):
        """String representation of the section's configuration."""
        return yaml.dump(self._loader._raw_config[self._section])


if __name__ == "__main__":
    config_without_vault = ConfigLoader("config.yml")
    print("Without Vault:", config_without_vault.get("jira", "url"))

    # This will only work if you provide a valid Vault secret ID
    # and hvac package is installed
    config_with_vault = ConfigLoader("config.yml", vault_secret_id=os.getenv("VAULT_SECRET_ID"))

    print("With Vault:", config_with_vault.test.test)
    print("With Vault:", config_with_vault["cis"]["cis_client_id"])
