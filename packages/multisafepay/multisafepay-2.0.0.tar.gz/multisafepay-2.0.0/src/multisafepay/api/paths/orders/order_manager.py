# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import json
from typing import Union

from multisafepay.api.base.abstract_manager import AbstractManager
from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.orders.order_id.capture.request.capture_request import (
    CaptureOrderRequest,
)
from multisafepay.api.paths.orders.order_id.capture.response.order_capture import (
    OrderCapture,
)
from multisafepay.api.paths.orders.order_id.refund.request.components.checkout_data import (
    CheckoutData,
)
from multisafepay.api.paths.orders.order_id.refund.request.refund_request import (
    RefundOrderRequest,
)
from multisafepay.api.paths.orders.order_id.refund.response.order_refund import (
    OrderRefund,
)
from multisafepay.api.paths.orders.order_id.update.request.update_request import (
    UpdateOrderRequest,
)
from multisafepay.api.paths.orders.request.order_request import OrderRequest
from multisafepay.api.paths.orders.response.order_response import Order
from multisafepay.api.shared.cart.shopping_cart import ShoppingCart
from multisafepay.api.shared.description import Description
from multisafepay.client.client import Client
from multisafepay.util.dict_utils import dict_empty
from multisafepay.util.message import MessageList, gen_could_not_created_msg
from multisafepay.value_object.amount import Amount
from multisafepay.value_object.currency import Currency


class OrderManager(AbstractManager):
    """
    Manages operations related to orders, such as creating, updating, capturing, and refunding orders.
    """

    def __init__(self: "OrderManager", client: Client) -> None:
        """
        Initialize the OrderManager with a client.

        Parameters
        ----------
        client (Client): The client used to make API requests.

        """
        super().__init__(client)

    @staticmethod
    def __custom_api_response(response: ApiResponse) -> CustomApiResponse:
        """
        Create a custom API response from a given ApiResponse.

        Parameters
        ----------
        response (ApiResponse): The original API response.

        Returns
        -------
        CustomApiResponse: The custom API response with additional data or warnings.

        """
        args: dict = {
            **response.dict(),
            "data": None,
        }
        if not dict_empty(response.get_body_data()):
            try:
                args["data"] = Order.from_dict(
                    d=response.get_body_data().copy(),
                )
            except Exception:
                args["warnings"] = MessageList().add_message(
                    gen_could_not_created_msg("Order"),
                )

        return CustomApiResponse(**args)

    def get(self: "OrderManager", order_id: str) -> CustomApiResponse:
        """
        Retrieve an order by its ID.

        Parameters
        ----------
        order_id (str): The ID of the order to retrieve.

        Returns
        -------
        CustomApiResponse: The custom API response containing the order data.

        """
        encoded_order_id = self.encode_path_segment(order_id)
        endpoint = f"json/orders/{encoded_order_id}"
        context = {"order_id": order_id}
        response: ApiResponse = self.client.create_get_request(
            endpoint,
            context,
        )
        return OrderManager.__custom_api_response(response)

    def create(
        self: "OrderManager",
        request_order: OrderRequest,
    ) -> CustomApiResponse:
        """
        Create a new order.

        Parameters
        ----------
        request_order (OrderRequest): The request object containing order details.

        Returns
        -------
        CustomApiResponse: The custom API response containing the created order data.

        """
        json_data = json.dumps(request_order.to_dict())
        response: ApiResponse = self.client.create_post_request(
            "json/orders",
            request_body=json_data,
        )
        return OrderManager.__custom_api_response(response)

    def update(
        self: "OrderManager",
        order_id: str,
        update_request: UpdateOrderRequest,
    ) -> CustomApiResponse:
        """
        Update an existing order.

        Parameters
        ----------
        order_id (str): The ID of the order to update.
        update_request (UpdateOrderRequest): The request object containing updated order details.

        Returns
        -------
        CustomApiResponse: The custom API response containing the updated order data.

        """
        json_data = json.dumps(update_request.to_dict())
        encoded_order_id = self.encode_path_segment(order_id)
        response = self.client.create_patch_request(
            f"json/orders/{encoded_order_id}",
            request_body=json_data,
        )
        args: dict = {
            **response.dict(),
            "data": None,
        }
        return CustomApiResponse(**args)

    def capture(
        self: "OrderManager",
        order_id: str,
        capture_request: CaptureOrderRequest,
    ) -> CustomApiResponse:
        """
        Capture an order.

        Parameters
        ----------
        order_id (str): The ID of the order to capture.
        capture_request (CaptureOrderRequest): The request object containing capture details.

        Returns
        -------
        CustomApiResponse: The custom API response containing the capture data.

        """
        json_data = json.dumps(capture_request.to_dict())
        encoded_order_id = self.encode_path_segment(order_id)

        response = self.client.create_post_request(
            f"json/orders/{encoded_order_id}/capture",
            request_body=json_data,
        )
        args: dict = {
            **response.dict(),
            "data": None,
        }
        if not dict_empty(response.get_body_data()):
            try:
                args["data"] = OrderCapture.from_dict(
                    d=response.get_body_data().copy(),
                )
            except Exception:
                args["warnings"] = MessageList().add_message(
                    gen_could_not_created_msg("OrderCapture"),
                )

        return CustomApiResponse(**args)

    def refund(
        self: "OrderManager",
        order_id: str,
        request_refund: RefundOrderRequest,
    ) -> CustomApiResponse:
        """
        Refund an order.

        Parameters
        ----------
        order_id (str): The ID of the order to refund.
        request_refund (RefundOrderRequest): The request object containing refund details.

        Returns
        -------
        CustomApiResponse: The custom API response containing the refund data.

        """
        json_data = json.dumps(request_refund.to_dict())
        encoded_order_id = self.encode_path_segment(order_id)
        response = self.client.create_post_request(
            f"json/orders/{encoded_order_id}/refunds",
            request_body=json_data,
        )
        args: dict = {
            **response.dict(),
            "data": None,
        }
        if not dict_empty(response.get_body_data()):
            try:
                args["data"] = OrderRefund.from_dict(
                    d=response.get_body_data().copy(),
                )
            except Exception:
                args["warnings"] = MessageList().add_message(
                    gen_could_not_created_msg("OrderRefund"),
                )

        return CustomApiResponse(**args)

    def refund_by_item(
        self: "OrderManager",
        order: Order,
        merchant_item_id: Union[str, int],
        quantity: int = 0,
    ) -> CustomApiResponse:
        """
        Refund an order by item.

        Parameters
        ----------
        order (Order): The order to refund.
        merchant_item_id (str | int): The merchant item ID to refund.
        quantity Optional[int]: The quantity to refund (default is 0).

        Returns
        -------
        CustomApiResponse: The custom API response containing the refund data.

        """
        request_refund = self.create_refund_request(order)
        request_refund.checkout_data.refund_by_merchant_item_id(
            merchant_item_id,
            quantity,
        )

        # Encode the order_id before calling refund
        return self.refund(order.order_id, request_refund)

    @staticmethod
    def create_refund_request(order: Order) -> RefundOrderRequest:
        """
        Create a refund request from an order.

        Parameters
        ----------
        order (Order): The order to create a refund request from.

        Returns
        -------
        RefundOrderRequest: The refund request object.

        """
        checkout_data = CheckoutData()
        extracted_shopping_cart: ShoppingCart = order.shopping_cart
        checkout_data.generate_from_shopping_cart(extracted_shopping_cart)

        request_refund = RefundOrderRequest()
        request_refund.add_checkout_data(checkout_data)
        request_refund.add_amount(Amount(amount=order.amount))
        request_refund.add_description(
            Description(description=order.description),
        )
        request_refund.add_currency(Currency(currency=order.currency))
        return request_refund
