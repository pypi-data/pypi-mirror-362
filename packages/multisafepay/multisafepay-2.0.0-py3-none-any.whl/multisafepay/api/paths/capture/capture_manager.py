# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import json

from multisafepay.api.base.abstract_manager import AbstractManager
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.capture.request.capture_request import (
    CaptureRequest,
)
from multisafepay.api.paths.capture.response.capture import CancelReservation
from multisafepay.client.client import Client
from multisafepay.util.dict_utils import dict_empty
from multisafepay.util.message import MessageList, gen_could_not_created_msg


class CaptureManager(AbstractManager):
    """
    A class to manage capture operations.
    """

    def __init__(self: "CaptureManager", client: Client) -> None:
        """
        Initialize the CaptureManager with a client.

        Parameters
        ----------
        client (Client): The client used to make API requests.

        """
        super().__init__(client)

    def capture_reservation_cancel(
        self: "CaptureManager",
        order_id: str,
        capture_request: CaptureRequest,
    ) -> CustomApiResponse:
        """
        Cancel a capture reservation.

        This method sends a PATCH request to cancel a capture reservation for a given order ID
        and capture request. It returns a CustomApiResponse containing a CancelReservation object.

        Parameters
        ----------
        order_id (str): The ID of the order to cancel the capture reservation for.
        capture_request (CaptureRequest): The capture request data.

        Returns
        -------
        CustomApiResponse[CancelReservation]: The response containing the CancelReservation object.

        """
        json_data = json.dumps(capture_request.dict())
        encoded_order_id = self.encode_path_segment(order_id)
        response = self.client.create_patch_request(
            f"json/capture/{encoded_order_id}",
            request_body=json_data,
        )
        args: dict = {
            **response.dict(),
            "data": None,
        }
        if not dict_empty(response.get_body_data()):
            try:
                args["data"] = CancelReservation(
                    **response.get_body_data().copy(),
                )
            except Exception as e:
                args["warnings"] = (
                    MessageList()
                    .add_message(str(e))
                    .add_message(gen_could_not_created_msg("Capture"))
                    .get_messages()
                )

        return CustomApiResponse(**args)
