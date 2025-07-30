# Copyright (C) 2022-2025 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

import httpx

from common.vault.vault_exception import VaultClientError
from common.vault.vault_exception import VaultClientException


class VaultClient:
    def __init__(self, vault_service: str, vault_crt: str | None, vault_token: str):
        self.vault_service = vault_service
        self.vault_crt = vault_crt
        self.vault_headers = {'X-Vault-Token': vault_token}

    """Get config based on service namespace"""

    def get_from_vault(self, srv_namespace: str) -> dict:
        # fetch Vault stored configurations
        verify = self.vault_crt if self.vault_crt is not None else False
        vault_gotten = httpx.get(self.vault_service, verify=verify, headers=self.vault_headers)
        if vault_gotten.status_code != 200:
            raise VaultClientException(VaultClientError.CONNECT_ERROR)

        # check Vault response
        vault_gotten_json = vault_gotten.json()
        if 'data' not in vault_gotten_json:
            raise VaultClientException(VaultClientError.RESPONSE_ERROR)

        # -grant access to service "srv_namespace"
        # default return all configurations-
        # since we might use the vault to directly
        # handle the service return. for now I will just return ALL
        vault_data: dict = vault_gotten_json['data']
        # granted = ConfigCenterPolicy.get_granted(srv_namespace)
        # config_return = {}
        # for k, v in vault_data.items():
        #     validate = lambda key, section: section in key
        #     is_granted = any([validate(k, section) for section in granted])
        #     if is_granted:
        #         config_return[k] = v
        # return config_return if granted else vault_data
        return vault_data
