# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import base64
import hashlib
import hmac
import json
import time

from multisafepay.exception.invalid_argument import InvalidArgumentException


class Webhook:
    """
    A class to represent a webhook.

    """

    @staticmethod
    def validate(
        request: str,
        auth: str,
        api_key: str,
        validation_time_in_seconds: int = 600,
    ) -> bool:
        """
        Validates the webhook request by checking the HMAC signature and timestamp.

        Parameters
        ----------
        request (str): The raw JSON request string.
        auth (str): The base64 encoded authentication header.
        api_key (str): The API key used to generate the HMAC signature.
        validation_time_in_seconds (int):
            The time in seconds within which the request is considered valid.

        Returns
        -------
        bool: True if the request is valid, False otherwise.

        Raises
        ------
        InvalidArgumentException:
            If the request is not a string or if the validation_time_in_seconds is negative.

        """
        if not isinstance(request, str):
            raise InvalidArgumentException(
                "Request can only be a string or TransactionResponse with raw data",
            )

        try:
            transaction_json = json.loads(request)
            transaction_compact_json = json.dumps(
                transaction_json,
                separators=(",", ":"),
            )
        except json.JSONDecodeError as e:
            raise InvalidArgumentException(
                "Request must be a valid JSON string",
            ) from e

        if validation_time_in_seconds < 0:
            raise InvalidArgumentException(
                "Argument validation_time_in_seconds must be equal or greater than 0",
            )

        auth_header_decoded = base64.b64decode(auth).decode()
        timestamp, sha512hex_payload = auth_header_decoded.split(":")

        if (
            validation_time_in_seconds > 0
            and int(timestamp) + validation_time_in_seconds < time.time()
        ):
            return False

        payload = f"{timestamp}:{transaction_compact_json}"

        hash_ = hmac.new(
            api_key.strip().encode(),
            payload.encode(),
            hashlib.sha512,
        ).hexdigest()
        return hash_ == sha512hex_payload
