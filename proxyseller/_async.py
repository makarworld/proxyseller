import json
from typing import Literal

from curl_cffi import requests

# Powered by GPT4 - muhaha
class ProxySeller:
    URL = "https://proxy-seller.com/personal/api/v1/"
    paymentId = 1
    generateAuth = "N"

    def __init__(self, api_key: str):
        """
        API key placed in https://proxy-seller.com/personal/api/.

        Args:
            api_key (str): The API key.

        Raises:
            Exception: If an error occurs during the configuration process.
        """

        self.base_uri = self.URL + api_key + "/"
        self.session = requests.AsyncSession()

    def setPaymentId(self, id: int):
        self.paymentId = id

    def getPaymentId(self) -> int:
        return self.paymentId

    def setGenerateAuth(self, yn: Literal["Y", "N"]):
        if yn == "Y":
            self.generateAuth = "Y"
        else:
            self.generateAuth = "N"

    def getGenerateAuth(self) -> str:
        return self.generateAuth

    async def request(self, method: str, uri: str, **options) -> str:
        """
        Send a request to the server.

        Args:
            method (str): The HTTP method to use for the request.
            uri (str): The URI to send the request to.
            options (dict): Additional options for the request.

        Returns:
            mixed: The response from the server.

        Raises:
            Exception: If an error occurs during the request.
        """
        if options is None:
            options = {}

        response = await self.session.request(method, self.base_uri + uri, **options)
        try:
            data = json.loads(response.text)
            if "status" in data and data["status"] == "success":  # Normal response
                return data["data"]
            elif "errors" in data:  # Normal error response
                raise ValueError(data["errors"][0]["message"])
            else:  # raw data
                return str(response.content)
        except json.decoder.JSONDecodeError:
            return response.content

    async def authList(self) -> list:
        """
        Get auths

        Returns:
            array list auths
        """
        return await self.request("GET", "auth/list")

    async def authActive(self, id: int, active: Literal["Y", "N"]) -> list:
        """
        Set auth active state

        Args:
            id (int): auth id
            active (str): active state (Y/N)

        Returns:
            array list auths
        """
        return await self.request("POST", "auth/active", json={"id": id, "active": active})

    async def balance(self) -> float:
        """
        Retrieve the balance statistic.

        Returns:
            float: The balance statistic.
        """
        return await self.request("GET", "balance/get")["summ"]

    async def balanceAdd(self, summ: float = 5, paymentId: int = 29) -> str:
        """
        Replenish the balance.

        Args:
            summ (float): The amount to add to the balance.
            payment_id (int): The identifier for the payment method.

        Returns:
            str: A link to the payment page. An example is shown below.
                'https://proxy-seller.com/personal/pay/?ORDER_ID=123456789&PAYMENT_ID=987654321&HASH=343bd596fb97c04bfb76557710837d34'
        """
        return await self.request(
            "POST", "balance/add", json={"summ": summ, "paymentId": paymentId}
        )["url"]

    async def balancePaymentsList(self) -> list:
        """
        Retrieve a list of payment systems for balance replenishing.

        Returns:
            list: An example of the returned value is shown below.
                [
                    {
                        'id': '29',
                        'name': 'PayPal'
                    },
                    {
                        'id': '37',
                        'name': 'Visa / MasterCard'
                    }
                ]
        """
        return await self.request("GET", "balance/payments/list")["items"]

    async def referenceList(
        self, type: Literal["ipv4", "ipv6", "mobile", "isp", "mix", "null"] = None
    ) -> dict:
        """
        Retrieve necessary guides for creating an order.
        This includes:
        - Countries, operators and rotation periods (mobile only)
        - Proxy periods
        - Purposes and services (only for ipv4, ipv6, isp, mix)
        - Allowed quantities (only for mix proxy)

        Args:
            type (str): The type of the proxy - ipv4, ipv6, mobile, isp, mix, or null.

        Returns:
            dict: The guide information for creating an order.
        """
        return await self.request("GET", "reference/list/" + str(type))

    def prepare(self, **kwargs) -> dict:
        allLocals = dict(kwargs)
        return allLocals

    async def orderCalc(self, data: dict) -> dict:
        """
        Calculate the order.

        Args:
            json (dict): Free format dictionary to send into endpoint.

        Returns:
            dict: The response from the endpoint.
        """
        return await self.request("POST", "order/calc", json=data)

    async def orderCalcIpv4(
        self,
        countryId: int,
        periodId: int,
        quantity: int,
        authorization: str,
        customTargetName: str,
        coupon: str = "OXSYUO_885446",
    ):
        """
        Calculate the preliminary order for IPv4.
        Preliminary order calculation.
        An error in the warning must be corrected before placing an order.

        Args:
            country_id (int): The identifier for the country.
            period_id (int): The identifier for the period.
            quantity (int): The quantity of items.
            authorization (str): IP address.
            coupon (str): The coupon code.
            custom_target_name (str): The custom name for the target.

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'warning': 'Insufficient funds. Total $2. Not enough $33.10',
                    'balance': 2,
                    'total': 35.1,
                    'quantity': 5,
                    'currency': 'USD',
                    'discount': 0.22,
                    'price': 7.02
                }
        """
        return await self.orderCalc(
            self.prepare(
                paymentId=self.paymentId,
                generateAuth=self.generateAuth,
                countryId=countryId,
                periodId=periodId,
                quantity=quantity,
                authorization=authorization,
                coupon=coupon,
                customTargetName=customTargetName,
            )
        )

    async def orderCalcIsp(
        self,
        countryId: int,
        periodId,
        quantity,
        authorization,
        customTargetName,
        coupon: str = "OXSYUO_885446",
    ):
        """
        Calculate the preliminary order for ISP.
        Preliminary order calculation.
        An error in the warning must be corrected before placing an order.

        Args:
            country_id (int): The identifier for the country.
            period_id (int): The identifier for the period.
            quantity (int): The quantity of items.
            authorization (str): IP address.
            coupon (str): The coupon code.
            custom_target_name (str): The custom name for the target.

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'warning': 'Insufficient funds. Total $2. Not enough $33.10',
                    'balance': 2,
                    'total': 35.1,
                    'quantity': 5,
                    'currency': 'USD',
                    'discount': 0.22,
                    'price': 7.02
                }
        """
        return await self.orderCalc(
            self.prepare(
                paymentId=self.paymentId,
                generateAuth=self.generateAuth,
                countryId=countryId,
                periodId=periodId,
                quantity=quantity,
                authorization=authorization,
                coupon=coupon,
                customTargetName=customTargetName,
            )
        )

    async def orderCalcMix(
        self,
        countryId: int,
        periodId: int,
        quantity: int,
        authorization: str,
        customTargetName: str,
        coupon: str = "OXSYUO_885446",
    ):
        """
        Calculate the preliminary order for MIX.
        Preliminary order calculation.
        An error in the warning must be corrected before placing an order.

        Args:
            country_id (int): The identifier for the country.
            period_id (int): The identifier for the period.
            quantity (int): The quantity of items.
            authorization (str): IP address.
            coupon (str): The coupon code.
            custom_target_name (str): The custom name for the target.

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'warning': 'Insufficient funds. Total $2. Not enough $33.10',
                    'balance': 2,
                    'total': 35.1,
                    'quantity': 5,
                    'currency': 'USD',
                    'discount': 0.22,
                    'price': 7.02
                }
        """
        return await self.orderCalc(
            self.prepare(
                paymentId=self.paymentId,
                generateAuth=self.generateAuth,
                countryId=countryId,
                periodId=periodId,
                quantity=quantity,
                authorization=authorization,
                coupon=coupon,
                customTargetName=customTargetName,
            )
        )

    async def orderCalcIpv6(
        self,
        countryId: int,
        periodId: int,
        quantity: int,
        authorization: str,
        customTargetName: str,
        protocol: Literal["HTTPS", "SOCKS5"],
        coupon: str = "OXSYUO_885446",
    ):
        """
        Calculate the preliminary order for IPv6.
        Preliminary order calculation.
        An error in the warning must be corrected before placing an order.

        Args:
            country_id (int): The identifier for the country.
            period_id (int): The identifier for the period.
            quantity (int): The quantity of items.
            authorization (str): IP address.
            coupon (str): The coupon code.
            custom_target_name (str): The custom name for the target.
            protocol (str): The protocol HTTPS or SOCKS5.

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'warning': 'Insufficient funds. Total $2. Not enough $33.10',
                    'balance': 2,
                    'total': 35.1,
                    'quantity': 5,
                    'currency': 'USD',
                    'discount': 0.22,
                    'price': 7.02
                }
        """
        return await self.orderCalc(
            self.prepare(
                paymentId=self.paymentId,
                generateAuth=self.generateAuth,
                countryId=countryId,
                periodId=periodId,
                quantity=quantity,
                authorization=authorization,
                coupon=coupon,
                customTargetName=customTargetName,
                protocol=protocol,
            )
        )

    async def orderCalcMobile(
        self,
        countryId: int,
        periodId: int,
        quantity: int,
        authorization: str,
        operatorId: int,
        rotationId: int,
        coupon: str = "OXSYUO_885446",
    ):
        """
        Calculate the preliminary order for Mobile.
        Preliminary order calculation.
        An error in the warning must be corrected before placing an order.

        Args:
            country_id (int): The identifier for the country.
            period_id (int): The identifier for the period.
            quantity (int): The quantity of items.
            authorization (str): IP address.
            coupon (str): The coupon code.
            operatorId (int): The identifier for the operator.
            rotationId (int): The identifier for the rotation.

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'warning': 'Insufficient funds. Total $2. Not enough $33.10',
                    'balance': 2,
                    'total': 35.1,
                    'quantity': 5,
                    'currency': 'USD',
                    'discount': 0.22,
                    'price': 7.02
                }
        """
        return await self.orderCalc(
            self.prepare(
                paymentId=self.paymentId,
                generateAuth=self.generateAuth,
                countryId=countryId,
                periodId=periodId,
                quantity=quantity,
                authorization=authorization,
                coupon=coupon,
                operatorId=operatorId,
                rotationId=rotationId,
            )
        )

    async def orderCalcResident(self, tarifId: int, coupon: str = "OXSYUO_885446"):
        """
        Calculate the preliminary order for Resident.
        Preliminary order calculation.
        An error in the warning must be corrected before placing an order.

        Args:
            tarifId (int): The identifier for the tarif.
            coupon (str): The coupon code.

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'orderId': 1000000,
                    'total': 35.1,
                    'balance': 10.19
                }
        """
        return await self.orderCalc(
            self.prepare(paymentId=self.paymentId, tarifId=tarifId, coupon=coupon)
        )

    async def orderMakeIpv4(
        self,
        countryId: int,
        periodId: int,
        quantity: int,
        authorization: str,
        customTargetName: str,
        coupon: str = "OXSYUO_885446",
    ):
        """
        Create an order for IPv4.

        Attention! Calling this method will deduct funds from your balance!
        The parameters are identical to the /order/calc method. Practice there before calling the /order/make method.

        Args:
            country_id (int): The identifier for the country.
            period_id (int): The identifier for the period.
            quantity (int): The quantity of items.
            authorization (str): The authorization token.
            coupon (str): The coupon code.
            custom_target_name (str): The custom name for the target.

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'orderId': 1000000,
                    'total': 35.1,
                    'balance': 10.19
                }
        """
        return await self.orderMake(
            self.prepare(
                paymentId=self.paymentId,
                generateAuth=self.generateAuth,
                countryId=countryId,
                periodId=periodId,
                quantity=quantity,
                authorization=authorization,
                coupon=coupon,
                customTargetName=customTargetName,
            )
        )

    async def orderMakeIsp(
        self,
        countryId: int,
        periodId: int,
        quantity: int,
        authorization: str,
        customTargetName: str,
        coupon: str = "OXSYUO_885446",
    ):
        """
        Create an order for ISP.

        Attention! Calling this method will deduct funds from your balance!
        The parameters are identical to the /order/calc method. Practice there before calling the /order/make method.

        Args:
            country_id (int): The identifier for the country.
            period_id (int): The identifier for the period.
            quantity (int): The quantity of items.
            authorization (str): The authorization token.
            coupon (str): The coupon code.
            custom_target_name (str): The custom name for the target.

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'orderId': 1000000,
                    'total': 35.1,
                    'balance': 10.19
                }
        """
        return await self.orderMake(
            self.prepare(
                paymentId=self.paymentId,
                generateAuth=self.generateAuth,
                countryId=countryId,
                periodId=periodId,
                quantity=quantity,
                authorization=authorization,
                coupon=coupon,
                customTargetName=customTargetName,
            )
        )

    async def orderMakeMix(
        self,
        countryId: int,
        periodId: int,
        quantity: int,
        authorization: str,
        customTargetName: str,
        coupon: str = "OXSYUO_885446",
    ):
        """
        Create an order for MIX.

        Attention! Calling this method will deduct funds from your balance!
        The parameters are identical to the /order/calc method. Practice there before calling the /order/make method.

        Args:
            country_id (int): The identifier for the country.
            period_id (int): The identifier for the period.
            quantity (int): The quantity of items.
            authorization (str): The authorization token.
            coupon (str): The coupon code.
            custom_target_name (str): The custom name for the target.

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'orderId': 1000000,
                    'total': 35.1,
                    'balance': 10.19
                }
        """
        return await self.orderMake(
            self.prepare(
                paymentId=self.paymentId,
                generateAuth=self.generateAuth,
                countryId=countryId,
                periodId=periodId,
                quantity=quantity,
                authorization=authorization,
                coupon=coupon,
                customTargetName=customTargetName,
            )
        )

    async def orderMakeIpv6(
        self,
        countryId: int,
        periodId: int,
        quantity: int,
        authorization: str,
        customTargetName: str,
        protocol: Literal["HTTPS", "SOCKS5"],
        coupon: str = "OXSYUO_885446",
    ):
        """
        Create an order for IPv6.

        Attention! Calling this method will deduct funds from your balance!
        The parameters are identical to the /order/calc method. Practice there before calling the /order/make method.

        Args:
            country_id (int): The identifier for the country.
            period_id (int): The identifier for the period.
            quantity (int): The quantity of items.
            authorization (str): The authorization token.
            coupon (str): The coupon code.
            custom_target_name (str): The custom name for the target.
            protocol (str): The protocol HTTPS or SOCKS5.

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'orderId': 1000000,
                    'total': 35.1,
                    'balance': 10.19
                }
        """
        return await self.orderMake(
            self.prepare(
                paymentId=self.paymentId,
                generateAuth=self.generateAuth,
                countryId=countryId,
                periodId=periodId,
                quantity=quantity,
                authorization=authorization,
                coupon=coupon,
                customTargetName=customTargetName,
                protocol=protocol,
            )
        )

    async def orderMakeMobile(
        self,
        countryId: int,
        periodId: int,
        quantity: int,
        authorization: str,
        operatorId: int,
        rotationId: int,
        coupon: str = "OXSYUO_885446",
    ):
        """
        Create an order for Mobile.

        Attention! Calling this method will deduct funds from your balance!
        The parameters are identical to the /order/calc method. Practice there before calling the /order/make method.

        Args:
            country_id (int): The identifier for the country.
            period_id (int): The identifier for the period.
            quantity (int): The quantity of items.
            authorization (str): The authorization token.
            coupon (str): The coupon code.
            operatorId (int): The identifier for the operator.
            rotationId (int): The identifier for the rotation.

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'orderId': 1000000,
                    'total': 35.1,
                    'balance': 10.19
                }
        """
        return await self.orderMake(
            self.prepare(
                paymentId=self.paymentId,
                generateAuth=self.generateAuth,
                countryId=countryId,
                periodId=periodId,
                quantity=quantity,
                authorization=authorization,
                coupon=coupon,
                operatorId=operatorId,
                rotationId=rotationId,
            )
        )

    async def orderMakeResident(self, tarifId: int, coupon: str = "OXSYUO_885446"):
        """
        Create an order for Resident.

        Attention! Calling this method will deduct funds from your balance!
        The parameters are identical to the /order/calc method. Practice there before calling the /order/make method.

        Args:
            tarifId (int): The identifier for the tarif.
            coupon (str): The coupon code.

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'orderId': 1000000,
                    'total': 35.1,
                    'balance': 10.19
                }
        """
        return await self.orderMake(
            self.prepare(paymentId=self.paymentId, tarifId=tarifId, coupon=coupon)
        )

    async def orderMake(self, data: dict):
        """
        Create an order.

        Args:
            json (dict): Free format dictionary to send into endpoint.

        Returns:
            dict: The response from the endpoint.
        """
        return await self.request("POST", "order/make", json=data)

    async def prolongCalc(
        self,
        type: Literal["ipv4", "ipv6", "mobile", "isp", "mix"],
        ids: list,
        periodId: int,
        coupon: str = "OXSYUO_885446",
    ):
        """
        Calculate the renewal.

        Args:
            type (str): The type of the order - ipv4, ipv6, mobile, isp, or mix.
            ids (list): A list of identifiers proxy.
            period_id (str): The identifier for the period.
            coupon (str): The coupon code.

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'warning': 'Insufficient funds. Total $2. Not enough $33.10',
                    'balance': 2,
                    'total': 35.1,
                    'quantity': 5,
                    'currency': 'USD',
                    'discount': 0.22,
                    'price': 7.02,
                    'items': [],
                    'orders': 1
                }
        """
        return await self.request(
            "POST",
            "prolong/calc/" + type,
            json={"ids": ids, "periodId": periodId, "coupon": coupon},
        )

    async def prolongMake(
        self,
        type: Literal["ipv4", "ipv6", "mobile", "isp", "mix"],
        ids: list,
        periodId: int,
        coupon: str = "OXSYUO_885446",
    ):
        """
        Create a renewal order.

        Attention! Calling this method will deduct $ from your balance!
        The parameters are identical to the /prolong/calc method. Practice there before calling the /prolong/make method.

        Args:
            type (str): The type of the order - ipv4, ipv6, mobile, isp, or mix.
            ids (list): A list of identifiers proxy.
            period_id (str): The identifier for the period.
            coupon (str): The coupon code.

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'orderId': 1000000,
                    'total': 35.1,
                    'balance': 10.19
                }
        """
        return await self.request(
            "POST",
            "prolong/make/" + type,
            json={"ids": ids, "periodId": periodId, "coupon": coupon},
        )

    async def proxyList(
        self, type: Literal["ipv4", "ipv6", "mobile", "isp", "mix", "null"] = None
    ):
        """
        Retrieve the list of proxies.

        Args:
            type (str): The type of the proxy - ipv4, ipv6, mobile, isp, mix, or null.

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'id': 9876543,
                    'order_id': 123456,
                    'basket_id': 9123456,
                    'ip': '127.0.0.2',
                    'ip_only': '127.0.0.2',
                    'protocol': 'HTTP',
                    'port_socks': 50101,
                    'port_http': 50100,
                    'login': 'login',
                    'password': 'password',
                    'auth_ip': '',
                    'rotation': '',
                    'link_reboot': '#',
                    'country': 'France',
                    'country_alpha3': 'FRA',
                    'status': 'Active',
                    'status_type': 'ACTIVE',
                    'can_prolong': 1,
                    'date_start': '26.06.2023',
                    'date_end': '26.07.2023',
                    'comment': '',
                    'auto_renew': 'Y',
                    'auto_renew_period': ''
                }
        """
        if type is None:
            return await self.request("GET", "proxy/list")
        return await self.request("GET", "proxy/list/" + str(type))

    async def proxyDownload(
        self,
        type: Literal["ipv4", "ipv6", "mobile", "isp", "mix", "resident"],
        ext: Literal["txt", "csv", None] = None,
        proto: Literal["https", "socks5", None] = None,
        listId: int = None,
    ):
        """
        Export a proxy of a certain type in txt or csv format.

        Args:
            type (str): The type of the proxy - ipv4 | ipv6 | mobile | isp | mix | resident.
            ext (str): txt | csv | None
            proto (str): https | socks5 | None
            listId (int): only for resident, if not set - will return ip from all sheets
        Returns:
            str: An example of the returned value is shown below.
                'login:password@127.0.0.2:50100'
        """
        return await self.request(
            "GET",
            "proxy/download/" + type,
            params={"ext": ext, "proto": proto, "listId": listId},
        )

    async def proxyCommentSet(self, ids: list, comment: str = None):
        """
        Set a comment for a proxy.

        Args:
            ids (list): Any id, regardless of the type of proxy.
            comment (str): The comment to set.

        Returns:
            int: The number of proxies updated.
        """
        return await self.request(
            "POST", "proxy/comment/set", json={"ids": ids, "comment": comment}
        )["updated"]

    async def proxyCheck(self, proxy: str):
        """
        Check a single proxy.

        Args:
            proxy (str): Available values - user:password@127.0.0.1:8080, user@127.0.0.1:8080, 127.0.0.1:8080.

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'ip': '127.0.0.1',
                    'port': 8080,
                    'user': 'user',
                    'password': 'password',
                    'valid': True,
                    'protocol': 'HTTP',
                    'time': 1234
                }
        """
        return await self.request("GET", "tools/proxy/check", params={"proxy": proxy})

    async def ping(self):
        """
        Check the availability of the service.

        Returns:
            float: A Unix timestamp representing the current time.
        """
        return await self.request("GET", "system/ping")["pong"]

    async def residentPackage(self):
        """
        Package Information
        Remaining traffic, end date

        Returns:
            dict: An example of the returned value is shown below.
                {
                    'is_active': true,
                    'rotation': 60,
                    'tarif_id': 2,
                    'traffic_limit': 7516192768,
                    'traffic_usage': 10,
                    'expired_at': "d.m.Y H:i:s",
                    'auto_renew': false
                }
        """
        return await self.request("GET", "resident/package")

    async def residentGeo(self):
        """
        Database geo locations (zip ~300Kb, unzip ~3Mb)

        Returns:
            binary
        """
        return await self.request("GET", "resident/geo")

    async def residentList(self):
        """
        List of existing ip list in a package
        You can download the list via endpoint /proxy/download/resident?listId=123

        Returns:
            array
        """
        return await self.request("GET", "resident/lists")

    async def residentListRename(self, id: int, title: str):
        """
        Rename list in user package

        Args:
            id (int): List ID
            title (str): Title list

        Returns:
            int: The number of proxies updated.
        """
        return await self.request(
            "POST", "resident/list/rename", json={"id": id, "title": title}
        )

    async def residentListDelete(self, id: int):
        """
        Remove list from user package

        Args:
            id (int): List ID

        Returns:
            array: Updated list model
        """
        return await self.request("DELETE", "resident/list/delete", json={"id": id})

    async def residentSubUserCreate(
        self, is_link_date: bool, rotation: int, traffic_limit: int, expired_at: str
    ):
        """
        Create subuser package

        Args:
            is_link_date (bool): "If 'true', the expiration date will be linked to the main package.
            rotation (int): Specifies the type of rotation: '-1' = No rotation (Sticky), '0' = Rotation per request, '1' to '3600' = Rotation by time in seconds.
            traffic_limit (int): The amount of bytes allocated for the subuser package.
            expired_at (str): The expiration date for the subuser package.

        Returns:
            created subuser package info
        """
        return await self.request(
            "POST",
            "residentsubuser/create",
            json={
                "is_link_date": is_link_date,
                "rotation": rotation,
                "traffic_limit": traffic_limit,
                "expired_at": expired_at,
            },
        )

    async def residentSubUserUpdate(
        self,
        package_key: str,
        is_link_date: bool = None,
        rotation: int = None,
        traffic_limit: int = None,
        expired_at: str = None,
        is_active: bool = None,
    ):
        """
        Update subuser package

        Args:
            is_link_date (bool): If 'true', the update date will be linked to the main package.
            rotation (int): Specifies the rotation type: '-1' = No rotation (Sticky),
                            '0' = Rotation per request, '1' to '3600' = Rotation by time in seconds.
            traffic_limit (int): Specifies the amount of bytes allocated for the subpackage.
            expired_at (str): Expiration date of the subpackage in the format 'd.m.Y'.
            is_active (bool): Set the status of the subpackage: 'true' for active, 'false' for inactive.
            package_key (str): Key of your active package.

        Returns:
            Updated subuser package info
        """
        params = {
            "package_key": package_key,
            "is_link_date": is_link_date,
            "rotation": rotation,
            "traffic_limit": traffic_limit,
            "expired_at": expired_at,
            "is_active": is_active,
        }
        params = {k: v for k, v in params.items() if v is not None}


        return await self.request(
            "POST",
            "residentsubuser/update",
            json=params,
        )

    async def residentSubUserPackages(self):
        """
        Get package information

        Returns:
            Package information including remaining traffic and expiration date.
        """
        return await self.request("GET", "residentsubuser/packages")

    async def residentSubUserDelete(self, package_key: str):
        """
        Delete subuser's package

        Args:
            package_key (str): Subpackage key from "Get subuser package information" request.

        Returns:
            Response indicating the result of the deletion.
        """
        return await self.request(
            "DELETE", "residentsubuser/delete", json={"package_key": package_key}
        )

    async def residentSubUserLists(self, package_key: str, list_id: int = None):
        """
        Retrieve existing IP lists

        Args:
            package_key (str): The key of the subuser's package from which you want to view the proxy list.
            list_id (int, optional): The ID of the list you want to view. If not provided, retrieves all lists.

        Returns:
            List of existing IP lists or specific list information.
        """
        params = {"package_key": package_key}
        if list_id is not None:
            params["listId"] = list_id

        return await self.request("GET", "residentsubuser/lists", params=params)

    async def residentSubUserListAdd(
        self,
        title: str,
        whitelist: str,
        geo: dict,
        export: dict,
        rotation: int,
        package_key: str,
    ):
        """
        Create IP list in the subuser's package

        Args:
            title (str): Name of the list you are creating.
            whitelist (str): IPs for authorization. Leave blank if you want to authorize with login credentials.
            geo (dict): GEO data to add to your list (country, region, city, ISP).
            export (dict): Specify the number of IPs in your list and the export type (ports and file format).
            rotation (int): '-1' for no rotation (Sticky), '0' for rotation per request,
                            '1' to '3600' for time-based rotation in seconds.
            package_key (str): Key of a subuser's package where you want to add the list of IPs.

        Returns:
            Response indicating the result of the creation.
        """
        return await self.request(
            "POST",
            "residentsubuser/list/add",
            json={
                "title": title,
                "whitelist": whitelist,
                "geo": geo,
                "export": export,
                "rotation": rotation,
                "package_key": package_key,
            },
        )

    async def residentSubUserListRename(self, id: int, title: str, package_key: str):
        """
        Rename created list in the subuser's package

        Args:
            id (int): ID of the list to be renamed.
            title (str): The new name for the list.
            package_key (str): The key of the subuser's package where the list of IPs will be renamed.

        Returns:
            Response indicating the result of the renaming.
        """
        return await self.request(
            "POST",
            "residentsubuser/list/rename",
            json={"id": id, "title": title, "package_key": package_key},
        )

    async def residentSubUserListRotation(self, id: int, rotation: int, package_key: str):
        """
        Change rotation of a created list in the subuser's package

        Args:
            id (int): ID of the created list.
            rotation (int): The new rotation value to set:
                            "-1" for no rotation (Sticky),
                            "0" for rotation per request,
                            "1" to "3600" for time-based rotation in seconds.
            package_key (str): Key of the subuser's package where you want to change rotation.

        Returns:
            Response indicating the result of the rotation change.
        """
        return await self.request(
            "POST",
            "residentsubuser/list/rotation",
            json={"id": id, "rotation": rotation, "package_key": package_key},
        )

    async def residentSubUserListDelete(self, id: int, package_key: str):
        """
        Delete a created list from the subuser's package

        Args:
            id (int): ID of the created list.
            package_key (str): The key of the subuser's package from which you want to remove the list.

        Returns:
            Response indicating the result of the deletion.
        """
        return await self.request(
            "DELETE",
            "residentsubuser/list/delete",
            json={"id": id, "package_key": package_key},
        )

    async def residentSubUserListTools(self, package_key: str):
        """
        Create a special list in the subuser's package

        Args:
            package_key (str): The key of the subuser's package where you want to create the special list.

        Returns:
            Response indicating the result of the creation.
        """
        return await self.request(
            "PUT", "residentsubuser/list/tools", json={"package_key": package_key}
        )
