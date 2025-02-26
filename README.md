[![PyPI version](https://badge.fury.io/py/proxyseller.svg)](https://badge.fury.io/py/proxyseller)
[![image](https://img.shields.io/pypi/pyversions/proxyseller.svg)](https://pypi.org/project/proxyseller/)
[![Github last commit date](https://img.shields.io/github/last-commit/makarworld/proxyseller.svg?label=Updated&logo=github&cacheSeconds=600)](https://github.com/makarworld/proxyseller/commits)
# proxyseller - Unofficial python library for working with proxy-seller.com

PyPi: https://pypi.org/project/proxyseller/

Site: https://proxy-seller.com/

Docs: https://docs.proxy-seller.com/

> pip install proxyseller

Example:
```python
from proxyseller import ProxySeller
# async version
# from proxyseller._async import ProxySeller
# from proxyseller import AsyncProxySeller



api_key = "YOUR_API_KEY"
proxyseller = ProxySeller(api_key)

print(proxyseller.balance())
```




# Main part of code was sourced from https://bitbucket.org/abuztrade/user-api-python/src/master/