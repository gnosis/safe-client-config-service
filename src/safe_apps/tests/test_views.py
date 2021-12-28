from typing import Any, Dict, List

from django.urls import reverse
from rest_framework.test import APITestCase

from ..models import SafeApp
from .factories import ClientFactory, ProviderFactory, SafeAppFactory


class EmptySafeAppsListViewTests(APITestCase):
    def test_empty_set(self) -> None:
        url = reverse("v1:safe-apps:list")

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


class JsonPayloadFormatViewTests(APITestCase):
    def test_json_payload_format(self) -> None:
        safe_app = SafeAppFactory.create()

        json_response = [
            {
                "id": safe_app.app_id,
                "url": safe_app.url,
                "name": safe_app.name,
                "iconUrl": safe_app.icon_url,
                "description": safe_app.description,
                "chainIds": safe_app.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
                    "value": [],
                },
            }
        ]
        url = reverse("v1:safe-apps:list")

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_response)


class FilterSafeAppListViewTests(APITestCase):
    def test_all_safes_returned(self) -> None:
        (safe_app_1, safe_app_2, safe_app_3) = SafeAppFactory.create_batch(3)
        json_response = [
            {
                "id": safe_app_1.app_id,
                "url": safe_app_1.url,
                "name": safe_app_1.name,
                "iconUrl": safe_app_1.icon_url,
                "description": safe_app_1.description,
                "chainIds": safe_app_1.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
                    "value": [],
                },
            },
            {
                "id": safe_app_2.app_id,
                "url": safe_app_2.url,
                "name": safe_app_2.name,
                "iconUrl": safe_app_2.icon_url,
                "description": safe_app_2.description,
                "chainIds": safe_app_2.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
                    "value": [],
                },
            },
            {
                "id": safe_app_3.app_id,
                "url": safe_app_3.url,
                "name": safe_app_3.name,
                "iconUrl": safe_app_3.icon_url,
                "description": safe_app_3.description,
                "chainIds": safe_app_3.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
                    "value": [],
                },
            },
        ]
        url = reverse("v1:safe-apps:list")

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_response)

    def test_all_apps_returned_on_empty_chain_id_value(self) -> None:
        (safe_app_1, safe_app_2, safe_app_3) = SafeAppFactory.create_batch(3)
        json_response = [
            {
                "id": safe_app_1.app_id,
                "url": safe_app_1.url,
                "name": safe_app_1.name,
                "iconUrl": safe_app_1.icon_url,
                "description": safe_app_1.description,
                "chainIds": safe_app_1.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
                    "value": [],
                },
            },
            {
                "id": safe_app_2.app_id,
                "url": safe_app_2.url,
                "name": safe_app_2.name,
                "iconUrl": safe_app_2.icon_url,
                "description": safe_app_2.description,
                "chainIds": safe_app_2.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
                    "value": [],
                },
            },
            {
                "id": safe_app_3.app_id,
                "url": safe_app_3.url,
                "name": safe_app_3.name,
                "iconUrl": safe_app_3.icon_url,
                "description": safe_app_3.description,
                "chainIds": safe_app_3.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
                    "value": [],
                },
            },
        ]
        url = reverse("v1:safe-apps:list") + f'{"?chainId="}'

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_response)

    def test_apps_returned_on_filtered_chain_id(self) -> None:
        SafeAppFactory.create_batch(3, chain_ids=[10])
        (safe_app_4, safe_app_5) = SafeAppFactory.create_batch(2, chain_ids=[1])

        json_response = [
            {
                "id": safe_app_4.app_id,
                "url": safe_app_4.url,
                "name": safe_app_4.name,
                "iconUrl": safe_app_4.icon_url,
                "description": safe_app_4.description,
                "chainIds": safe_app_4.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
                    "value": [],
                },
            },
            {
                "id": safe_app_5.app_id,
                "url": safe_app_5.url,
                "name": safe_app_5.name,
                "iconUrl": safe_app_5.icon_url,
                "description": safe_app_5.description,
                "chainIds": safe_app_5.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
                    "value": [],
                },
            },
        ]
        url = reverse("v1:safe-apps:list") + f'{"?chainId=1"}'

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_response)

    def test_apps_returned_on_unexisting_chain(self) -> None:
        SafeAppFactory.create_batch(3, chain_ids=[12])
        json_response: List[Dict[str, Any]] = []
        url = reverse("v1:safe-apps:list") + f'{"?chainId=10"}'

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_response)

    def test_apps_returned_on_same_chainid_key_pair(self) -> None:
        safe_app_1 = SafeAppFactory.create(chain_ids=[1])
        SafeAppFactory.create(chain_ids=[2])
        json_response = [
            {
                "id": safe_app_1.app_id,
                "url": safe_app_1.url,
                "name": safe_app_1.name,
                "iconUrl": safe_app_1.icon_url,
                "description": safe_app_1.description,
                "chainIds": safe_app_1.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
                    "value": [],
                },
            }
        ]
        url = reverse("v1:safe-apps:list") + f'{"?chainId=2&chainId=1"}'

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_response)

    def test_apps_returned_on_non_existent_client_url(self) -> None:
        safe_app = SafeAppFactory.create()
        url = reverse("v1:safe-apps:list") + f'{"?client_url=non_existent_host"}'

        response = self.client.get(path=url, data=None, format="json")

        json_response = [
            {
                "id": safe_app.app_id,
                "url": safe_app.url,
                "name": safe_app.name,
                "iconUrl": safe_app.icon_url,
                "description": safe_app.description,
                "chainIds": safe_app.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
                    "value": [],
                },
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_response)

    def test_apps_returned_on_empty_client_url(self) -> None:
        safe_app = SafeAppFactory.create()
        url = reverse("v1:safe-apps:list") + f'{"?client_url="}'

        response = self.client.get(path=url, data=None, format="json")

        json_response = [
            {
                "id": safe_app.app_id,
                "url": safe_app.url,
                "name": safe_app.name,
                "iconUrl": safe_app.icon_url,
                "description": safe_app.description,
                "chainIds": safe_app.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
                    "value": [],
                },
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_response)

    def test_apps_returned_on_same_client_url_key_pair(self) -> None:
        client_1 = ClientFactory.create(url="safe.com")
        client_2 = ClientFactory.create(url="pump.com")
        safe_app_1 = SafeAppFactory.create(exclusive_clients=(client_1,))
        SafeAppFactory.create(exclusive_clients=(client_2,))
        json_response = [
            {
                "id": safe_app_1.app_id,
                "url": safe_app_1.url,
                "name": safe_app_1.name,
                "iconUrl": safe_app_1.icon_url,
                "description": safe_app_1.description,
                "chainIds": safe_app_1.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.DOMAIN_ALLOWLIST,
                    "value": [client_1.url],
                },
            }
        ]
        url = (
            reverse("v1:safe-apps:list")
            + f'{"?client_url=pump.com&client_url=safe.com"}'
        )

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_response)

    def test_apps_returned_on_filtered_client_url(self) -> None:
        client = ClientFactory.create(url="safe.com")
        client_2 = ClientFactory.create(url="pump.com")
        safe_app_1 = SafeAppFactory.create(exclusive_clients=(client,))
        safe_app_2 = SafeAppFactory.create()
        safe_app_3 = SafeAppFactory.create(exclusive_clients=(client, client_2,))
        SafeAppFactory.create(exclusive_clients=(client_2,))

        # For some reason, it puts an app with no restrictions to the end of the array. For now we will ignore this until we add a meaningful ordering to the API.
        json_response = [
            {
                "id": safe_app_1.app_id,
                "url": safe_app_1.url,
                "name": safe_app_1.name,
                "iconUrl": safe_app_1.icon_url,
                "description": safe_app_1.description,
                "chainIds": safe_app_1.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": 'DOMAIN_ALLOWLIST',
                    "value": ["safe.com"],
                },
            },
            {
                "id": safe_app_3.app_id,
                "url": safe_app_3.url,
                "name": safe_app_3.name,
                "iconUrl": safe_app_3.icon_url,
                "description": safe_app_3.description,
                "chainIds": safe_app_3.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": 'DOMAIN_ALLOWLIST',
                    "value": ["safe.com", "pump.com"],
                },
            },
            {
                "id": safe_app_2.app_id,
                "url": safe_app_2.url,
                "name": safe_app_2.name,
                "iconUrl": safe_app_2.icon_url,
                "description": safe_app_2.description,
                "chainIds": safe_app_2.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": 'NO_RESTRICTIONS',
                    "value": [],
                },
            },
        ]
        url = reverse("v1:safe-apps:list") + f'{"?client_url=safe.com"}'

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_response)


class ProviderInfoTests(APITestCase):
    def test_provider_returned_in_response(self) -> None:
        provider = ProviderFactory.create()
        safe_app = SafeAppFactory.create(provider=provider)

        json_response = [
            {
                "id": safe_app.app_id,
                "url": safe_app.url,
                "name": safe_app.name,
                "iconUrl": safe_app.icon_url,
                "description": safe_app.description,
                "chainIds": safe_app.chain_ids,
                "provider": {"name": provider.name, "url": provider.url},
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
                    "value": [],
                },
            }
        ]
        url = reverse("v1:safe-apps:list")

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_response)

    def test_provider_not_returned_in_response(self) -> None:
        safe_app = SafeAppFactory.create()

        json_response = [
            {
                "id": safe_app.app_id,
                "url": safe_app.url,
                "name": safe_app.name,
                "iconUrl": safe_app.icon_url,
                "description": safe_app.description,
                "chainIds": safe_app.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
                    "value": [],
                },
            }
        ]
        url = reverse("v1:safe-apps:list")

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_response)


class CacheSafeAppTests(APITestCase):
    def test_should_cache_response(self) -> None:
        safe_app_1 = SafeAppFactory.create()

        json_response = [
            {
                "id": safe_app_1.app_id,
                "url": safe_app_1.url,
                "name": safe_app_1.name,
                "iconUrl": safe_app_1.icon_url,
                "description": safe_app_1.description,
                "chainIds": safe_app_1.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
                    "value": [],
                },
            }
        ]
        url = reverse("v1:safe-apps:list")

        response = self.client.get(path=url, data=None, format="json")

        cache_control = response.headers.get("Cache-Control")

        self.assertEqual(response.status_code, 200)
        # Cache-Control should be 10 minutes (60 * 10)
        self.assertEqual(cache_control, "max-age=600")
        self.assertEqual(response.json(), json_response)


class SafeAppsVisibilityTests(APITestCase):
    def test_visible_safe_app_is_shown(self) -> None:
        visible_safe_app = SafeAppFactory.create(visible=True)
        json_response = [
            {
                "id": visible_safe_app.app_id,
                "url": visible_safe_app.url,
                "name": visible_safe_app.name,
                "iconUrl": visible_safe_app.icon_url,
                "description": visible_safe_app.description,
                "chainIds": visible_safe_app.chain_ids,
                "provider": None,
                "accessControl": {
                    "type": SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
                    "value": [],
                },
            }
        ]
        url = reverse("v1:safe-apps:list")

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_response)

    def test_not_visible_safe_app_is_not_shown(self) -> None:
        SafeAppFactory.create(visible=False)
        json_response: List[Dict[str, Any]] = []
        url = reverse("v1:safe-apps:list")

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_response)


class ClientTests(APITestCase):
    def test_client_with_no_exclusive_apps(self) -> None:
        SafeAppFactory.create()
        ClientFactory()
        url = reverse("v1:safe-apps:list")

        response = self.client.get(path=url, data=None, format="json")

        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json_response[0]["accessControl"]["type"],
            SafeApp.AccessControlPolicy.NO_RESTRICTIONS,
        )
        self.assertEqual(json_response[0]["accessControl"]["value"], [])

    def test_client_with_exclusive_apps(self) -> None:
        client_1 = ClientFactory()
        SafeAppFactory.create(exclusive_clients=(client_1,))
        url = reverse("v1:safe-apps:list")

        response = self.client.get(path=url, data=None, format="json")

        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json_response[0]["accessControl"]["type"],
            SafeApp.AccessControlPolicy.DOMAIN_ALLOWLIST,
        )
        self.assertEqual(json_response[0]["accessControl"]["value"], [client_1.url])
