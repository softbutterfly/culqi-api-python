import os
import unittest
from copy import deepcopy
from uuid import uuid4

import pytest
from dotenv import load_dotenv

from culqi import __version__
from culqi.client import Culqi
from culqi.resources import Subscription

from .data import Data


class SubscriptionTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        load_dotenv()
        self.version = __version__
        self.public_key = os.environ.get("API_PUBLIC_KEY")
        self.private_key = os.environ.get("API_PRIVATE_KEY")
        self.culqi = Culqi(self.public_key, self.private_key)
        self.subscription = Subscription(client=self.culqi)

        self.metadata = {"order_id": "0001"}

    @property
    def subscription_data(self):
        # pylint-x: disable=no-member
        email = f"richard{uuid4().hex[:4]}@piedpiper.com"

        token_data = deepcopy(Data.CARD["successful"]["visa"])
        token_data["email"] = email
        token = self.culqi.token.create(data=token_data)

        customer_data = deepcopy(Data.CUSTOMER)
        customer_data["email"] = email
        customer = self.culqi.customer.create(data=customer_data)

        card_data = {
            "token_id": token["data"]["id"],
            "customer_id": customer["data"]["id"],
        }
        card = self.culqi.card.create(data=card_data)

        plan_data = deepcopy(Data.PLAN)
        plan_data["name"] = f"plan-{uuid4().hex[:4]}"
        plan = self.culqi.plan.create(data=plan_data)

        return {
            "card_id": card["data"]["id"],
            "plan_id": plan["data"]["id"],
        }

    def test_url(self):
        # pylint: disable=protected-access
        id_ = "sample_id"

        assert self.subscription._get_url() == "https://api.culqi.com/v2/subscriptions"
        assert (
            self.subscription._get_url(id_)
            == f"https://api.culqi.com/v2/subscriptions/{id_}"
        )

    @pytest.mark.vcr()
    def test_subscription_create(self):
        subscription = self.subscription.create(data=self.subscription_data)
        assert subscription["data"]["object"] == "subscription"

    @pytest.mark.vcr()
    def test_subscription_retrieve(self):
        created_subscription = self.subscription.create(data=self.subscription_data)
        retrieved_subscription = self.subscription.read(
            created_subscription["data"]["id"]
        )
        assert (
            created_subscription["data"]["id"] == retrieved_subscription["data"]["id"]
        )

    @pytest.mark.vcr()
    def test_subscription_list(self):
        retrieved_subscription_list = self.subscription.list(
            headers={
                "Accept-Encoding": "identity",
            },
        )
        assert "items" in retrieved_subscription_list["data"]

    @pytest.mark.vcr()
    def test_subscription_update(self):
        created_subscription = self.subscription.create(data=self.subscription_data)

        metadata = {"metadata": self.metadata}
        updated_subscription = self.subscription.update(
            id_=created_subscription["data"]["id"], data=metadata
        )

        assert created_subscription["data"]["id"] == created_subscription["data"]["id"]
        assert updated_subscription["data"]["metadata"] == self.metadata

    @pytest.mark.vcr()
    def test_subscription_delete(self):
        created_subscription = self.subscription.create(data=self.subscription_data)
        deleted_subscription = self.subscription.delete(
            id_=created_subscription["data"]["id"]
        )

        assert deleted_subscription["data"]["deleted"]
        assert deleted_subscription["data"]["id"] == created_subscription["data"]["id"]
        assert deleted_subscription["status"] == 200


if __name__ == "__main__":
    unittest.main()
