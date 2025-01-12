# proxyseller - Unofficial python library for working with proxy-seller.com

Site: https://proxy-seller.com/

Docs: https://docs.proxy-seller.com/

> pip install proxyseller

Example:
```python
from proxyseller import ProxySeller

api_key = "YOUR_API_KEY"
proxyseller = ProxySeller(api_key)

print(proxyseller.balance())
```

Methods:
```python
proxyseller.setPaymentId(id)
proxyseller.getPaymentId()
proxyseller.setGenerateAuth(yn)
proxyseller.getGenerateAuth()
proxyseller.authList()
proxyseller.authActive(id, active)
proxyseller.balance()
proxyseller.balanceAdd(summ, paymentId)
proxyseller.balancePaymentsList()
proxyseller.referenceList(type)
proxyseller.orderCalc(data)
proxyseller.orderCalcIpv4(countryId, periodId, quantity, authorization, customTargetName, coupon)
proxyseller.orderCalcIsp(countryId, periodId, quantity, authorization, customTargetName, coupon)
proxyseller.orderCalcMix(countryId, periodId, quantity, authorization, customTargetName, coupon)
proxyseller.orderCalcIpv6(countryId, periodId, quantity, authorization, customTargetName, protocol, coupon)
proxyseller.orderCalcMobile(countryId, periodId, quantity, authorization, operatorId, rotationId, coupon)
proxyseller.orderCalcResident(tarifId, coupon)
proxyseller.orderMakeIpv4(countryId, periodId, quantity, authorization, customTargetName, coupon)
proxyseller.orderMakeIsp(countryId, periodId, quantity, authorization, customTargetName, coupon)
proxyseller.orderMakeMix(countryId, periodId, quantity, authorization, customTargetName, coupon)
proxyseller.orderMakeIpv6(countryId, periodId, quantity, authorization, customTargetName, protocol, coupon)
proxyseller.orderMakeMobile(countryId, periodId, quantity, authorization, operatorId, rotationId, coupon)
proxyseller.orderMakeResident(tarifId, coupon)
proxyseller.orderMake(countryId, periodId, quantity, authorization, customTargetName, coupon)
proxyseller.prolongCalc(type, ids, periodId, coupon)
proxyseller.prolongMake(type, ids, periodId, coupon)
proxyseller.proxyList(type)
proxyseller.proxyDownload(type, ext, proto, listId)
proxyseller.proxyCommentSet(ids, comment)
proxyseller.proxyCheck(proxy)
proxyseller.ping()
proxyseller.residentPackage()
proxyseller.residentGeo()
proxyseller.residentList()
proxyseller.residentListRename(id, title)
proxyseller.residentListDelete(id)
proxyseller.residentSubUserCreate(is_link_date, rotation, traffic_limit, expired_at)
proxyseller.residentSubUserUpdate(is_link_date, rotation, traffic_limit, expired_at, is_active, package_key)
proxyseller.residentSubUserPackages()
proxyseller.residentSubUserDelete(package_key)
proxyseller.residentSubUserLists(package_key, list_id)
proxyseller.residentSubUserListAdd(title, whitelist, geo, export, rotation, package_key)
proxyseller.residentSubUserListRename(id, title, package_key)
proxyseller.residentSubUserListRotation(id, rotation, package_key)
proxyseller.residentSubUserListDelete(id, package_key)
proxyseller.residentSubUserListTools(package_key)
```

# Main part of code was sourced from https://bitbucket.org/abuztrade/user-api-python/src/master/