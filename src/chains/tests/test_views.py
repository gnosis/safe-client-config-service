from django.urls import reverse
from rest_framework.test import APITestCase

from .factories import ChainFactory


class EmptyChainsListViewTests(APITestCase):
    def test_empty_chains(self):
        url = reverse("v1:chains:list")
        json_response = {"count": 0, "next": None, "previous": None, "results": []}

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, json_response)


class ChainJsonPayloadFormatViewTests(APITestCase):
    def test_json_payload_format(self):
        chain = ChainFactory.create()
        json_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "chainId": str(chain.id),
                    "chainName": chain.name,
                    "rpcUrl": chain.rpc_url,
                    "blockExplorerUrl": chain.block_explorer_url,
                    "nativeCurrency": {
                        "name": chain.currency_name,
                        "symbol": chain.currency_symbol,
                        "decimals": chain.currency_decimals,
                    },
                    "transactionService": chain.transaction_service_url,
                    "theme": {
                        "textColor": chain.theme_text_color,
                        "backgroundColor": chain.theme_background_color,
                    },
                }
            ],
        }
        url = reverse("v1:chains:list")

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_response)


class ChainPaginationViewTests(APITestCase):
    def test_pagination_next_page(self):
        ChainFactory.create_batch(11)
        url = reverse("v1:chains:list")

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        # number of items should be equal to the number of total items
        self.assertEqual(response.data["count"], 11)
        self.assertEqual(
            response.data["next"],
            "http://testserver/api/v1/chains/?limit=10&offset=10",
        )
        self.assertEqual(response.data["previous"], None)
        # returned items should be equal to max_limit
        self.assertEqual(len(response.data["results"]), 10)

    def test_request_more_than_max_limit_should_return_max_limit(self):
        ChainFactory.create_batch(11)
        # requesting limit > max_limit
        url = reverse("v1:chains:list") + f'{"?limit=11"}'

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        # number of items should be equal to the number of total items
        self.assertEqual(response.data["count"], 11)
        self.assertEqual(
            response.data["next"],
            "http://testserver/api/v1/chains/?limit=10&offset=10",
        )
        self.assertEqual(response.data["previous"], None)
        # returned items should still be equal to max_limit
        self.assertEqual(len(response.data["results"]), 10)

    def test_offset_greater_than_count(self):
        ChainFactory.create_batch(11)
        # requesting offset of number of chains
        url = reverse("v1:chains:list") + f'{"?offset=11"}'

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 11)
        self.assertEqual(response.data["next"], None)
        self.assertEqual(
            response.data["previous"],
            "http://testserver/api/v1/chains/?limit=10&offset=1",
        )
        # returned items should still be zero
        self.assertEqual(len(response.data["results"]), 0)


class ChainDetailViewTests(APITestCase):
    def test_json_payload_format(self):
        chain = ChainFactory.create(id=1)
        url = reverse("v1:chains:detail", args=[1])
        json_response = {
            "chainId": str(chain.id),
            "chainName": chain.name,
            "rpcUrl": chain.rpc_url,
            "blockExplorerUrl": chain.block_explorer_url,
            "nativeCurrency": {
                "name": chain.currency_name,
                "symbol": chain.currency_symbol,
                "decimals": chain.currency_decimals,
            },
            "transactionService": chain.transaction_service_url,
            "theme": {
                "textColor": chain.theme_text_color,
                "backgroundColor": chain.theme_background_color,
            },
        }

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_response)

    def test_no_match(self):
        ChainFactory.create(id=1)
        url = reverse("v1:chains:detail", args=[2])

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 404)

    def test_match(self):
        chain = ChainFactory.create(id=1)
        url = reverse("v1:chains:detail", args=[1])
        json_response = {
            "chain_id": str(chain.id),
            "chain_name": chain.name,
            "rpc_url": chain.rpc_url,
            "block_explorer_url": chain.block_explorer_url,
            "native_currency": {
                "name": chain.currency_name,
                "symbol": chain.currency_symbol,
                "decimals": chain.currency_decimals,
            },
            "transaction_service": chain.transaction_service_url,
            "theme": {
                "text_color": chain.theme_text_color,
                "background_color": chain.theme_background_color,
            },
        }

        response = self.client.get(path=url, data=None, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, json_response)
