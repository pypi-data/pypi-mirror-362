<p align="center">
    <img src="https://raw.githubusercontent.com/MultiSafepay/MultiSafepay-logos/master/MultiSafepay-logo-color.svg" width="400px" position="center">
</p>

# MultiSafepay Python SDK
[![Code Quality](https://img.shields.io/github/actions/workflow/status/multisafepay/python-sdk/code-quality.yaml?style=for-the-badge)](https://github.com/MultiSafepay/python-sdk/actions/workflows/code-quality.yaml)
[![Codecov](https://img.shields.io/codecov/c/github/multisafepay/python-sdk?style=for-the-badge)](https://app.codecov.io/gh/MultiSafepay/python-sdk)
[![License](https://img.shields.io/github/license/multisafepay/python-sdk?style=for-the-badge)](https://github.com/MultiSafepay/python-sdk/blob/master/LICENSE)
[![Latest stable version](https://img.shields.io/github/v/release/multisafepay/python-sdk?style=for-the-badge)](https://pypi.org/project/multisafepay/)
[![Python versions](https://img.shields.io/pypi/pyversions/multisafepay?style=for-the-badge)](https://pypi.org/project/multisafepay/)

Easily integrate MultiSafepay's payment solutions into your Python applications with this official API client.
This SDK provides convenient access to the MultiSafepay REST API, supports all core payment features, and is designed for seamless integration into any Python-based backend.

## About MultiSafepay

MultiSafepay is a Dutch payment services provider, which takes care of contracts, processing transactions, and
collecting payment for a range of local and international payment methods. Start selling online today and manage all
your transactions in one place!

## Installation

Here's how to use pip to put the MultiSafepay library into your Python.

```bash
pip install multisafepay
```

## Getting started

### Initialize the client

```python
from multisafepay.sdk import Sdk

multisafepay_sdk: Sdk = Sdk(api_key='<api_key>', is_production=True)
```

## Examples

Go to the folder `examples` to see how to use the SDK.

## Code quality checks

### Linting

```bash
make lint
```

## Testing

```bash
make test
```

## Support

Create an issue on this repository or email <a href="mailto:integration@multisafepay.com">
integration@multisafepay.com</a>

## Contributors

If you create a pull request to suggest an improvement, we'll send you some MultiSafepay swag as a thank you!

## License

[Open Software License (OSL 3.0)](https://github.com/MultiSafepay/php-sdk/blob/master/LICENSE.md)

## Want to be part of the team?

Are you a developer interested in working at MultiSafepay? Check out
our [job openings](https://www.multisafepay.com/careers/#jobopenings) and feel free to get in touch!