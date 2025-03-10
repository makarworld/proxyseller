import json
from typing import Any, Dict, List, Literal, Optional, Union

from curl_cffi import requests

# Powered by GPT4 - muhaha | rewrited by @abuztrade
# Source: https://bitbucket.org/proxy-seller/user-api-python/src/master/
# Full copy of __init__.py but async
class ProxySeller:
    URL = "https://proxy-seller.com/personal/api/v1/"

    def __init__(self, api_key: str, generate_auth: Literal["N", "Y"] = "N", payment_id: int = 1):
        """
        API key placed in https://proxy-seller.com/personal/api/.

        Args:
            api_key (str): The API key.

        Raises:
            Exception: If an error occurs during the configuration process.
        """

        self.base_uri = self.URL + api_key + "/"
        self.session = requests.AsyncSession()
        self.generate_auth = generate_auth
        self.payment_id = payment_id

    def set_payment_id(self, id: int):
        self.payment_id = id

    def get_payment_id(self) -> int:
        return self.payment_id

    def set_generate_auth(self, yn: Literal["Y", "N"]):
        if yn == "Y":
            self.generate_auth = "Y"
        else:
            self.generate_auth = "N"

    def get_generate_auth(self) -> str:
        return self.generate_auth

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
        
        if options.get("params"):
            # clear None values
            options["params"] = {k: v for k, v in options["params"].items() if v is not None}
        
        if options.get("json"):
            # clear None values
            options["json"] = {k: v for k, v in options["json"].items() if v is not None}

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


    async def proxy_list(
        self, 
        type:     Literal["ipv4", "ipv6", "mobile", "isp", "mix", "null"] = None,
        latest:   bool = None,
        order_id: str  = None,
        country:  str  = None,
        ends:     bool = None
    ):
        """
        Retrieve the list of proxies.
        https://docs.proxy-seller.com/proxy-seller/actions-with-proxies/retrieve-active-proxy

        Args:
            type (str): The type of the proxy - ipv4, ipv6, mobile, isp, mix, or null.
            latest (bool): Y/N - Return proxy from last order 
            orderId (str): Return a proxy from a specific order
            country (str): Alpha3 country name (FRA or USA or ...) 
            ends (bool): Y - List of ending proxies
                        

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
        params = dict(
            latest = "NY"[latest] if isinstance(latest, bool) else latest,
            order_id = order_id,
            country = country,
            ends = "NY"[ends] if isinstance(ends, bool) else ends
        )

        if type is None:
            return await self.request("GET", "proxy/list", params = params)
        return await self.request("GET", "proxy/list/" + str(type), params = params)


    async def proxy_download(
        self,
        type:        Literal["ipv4", "ipv6", "mobile", "isp", "mix", "resident"],
        ext:         Literal["txt", "csv", Literal[r"%login%:%password%@%ip%:%port%"]] = None,
        proto:       Literal["https", "socks5"] = None,
        listId:      int = None,
        package_key: str = None,
        country:     str = None,
        ends:        Union[bool, Literal["N", "Y"]] = None
    ):
        """
        ### Export a proxy of a certain type in txt or csv format.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/actions-with-proxies/export-ips-in-txt-csv-custom

        Args:
            type (str): The type of the proxy - ipv4 | ipv6 | mobile | isp | mix | resident.
            ext (str): Specifies the format in which the proxy list will be downloaded. | %login%:%password%@%ip%:%port% - Custom format
            proto (str): https | socks5 | None
            listId (int): only for resident, if not set - will return ip from all sheets
            package_key (str): Proxy list package_key (only for subresident) 
            country (str): Alpha3 country name (FRA or USA or ...) 
            ends (bool, str): True / Y - List of ending proxies
                    
        Returns:
            str: An example of the returned value is shown below.
                'login:password@127.0.0.1:80;
                 login2:password2@127.0.0.1:81;'
        """
        params = dict(
            ext = ext,
            proto = proto,
            listId = listId,
            package_key = package_key,
            country = country,
            ends = "NY"[ends] if isinstance(ends, bool) else ends
        )
        
        return await self.request(
            "GET",
            "proxy/download/" + type,
            params = params
        )

    async def proxy_replace(
        self,
        ids: Union[int, List[int]],
        comment: str = None,
        type: str = None
    ):
        """
        ### Automate IP replacement requests.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/actions-with-proxies/ip-replacement  

        Args:
            ids (Union[int, List[int]]): A single ID or an array of IDs in '[ ]', separated by commas.
            comment (str): Optional comment to include with the request.
            type (str): Type of replacement - NOT_WORK, INCORRECT_LOCATION, CANT_CHANGE_NETWORK, LOW_SPEED, CUSTOM.
                        
        Returns:
            dict: Response containing the status and data of the replacement request.
        """
        # Prepare the request body
        data = {
            "ids": ids if isinstance(ids, list) else [ids],
            "comment": comment,
            "type": type
        }
        
        return await self.request(
            "POST",
            "proxy/replace",
            json=data
        )

    async def proxy_comment_set(
        self,
        ids: Union[int, List[int]],
        comment: str
    ):
        """
        ### Add a comment to a specific proxy in the system.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/actions-with-proxies/comment-on-ip  

        Args:
            ids (Union[int, List[int]]): A single ID or an array of IDs in '[ ]', separated by commas.
            comment (str): The comment you want to add.
                        
        Returns:
            dict: Response containing the status and data of the comment request.
        """
        # Prepare the request body
        data = {
            "ids": ids if isinstance(ids, list) else [ids],
            "comment": comment
        }
        
        return await self.request(
            "POST",
            "proxy/comment/set",
            json=data
        )

    async def prolong_calc(
        self,
        type: str,
        ids: Union[int, List[int]],
        coupon: str = None,
        period_id: str = None
    ):
        """
        ### Calculate the cost for extending IP addresses.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/actions-with-proxies/extend-proxies  

        Args:
            type (str): The proxy type you want to extend - ipv4 | ipv6 | mobile | isp | mix | mix_isp.
            ids (Union[int, List[int]]): A single ID or an array of IDs in '[ ]', separated by commas.
            coupon (str): Optional coupon code to apply.
            period_id (str): ID of the period selected in the /reference/list/{type} request.
           
        Returns:
            dict: Response containing the status and data of the calculation request.
        """
        # Prepare the request parameters
        params = {
            "ids": ids if isinstance(ids, list) else [ids],
            "coupon": coupon,
            "periodId": period_id,
            "paymentId": self.payment_id
        }
        
        return await self.request(
            "GET",
            f"prolong/calc/{type}",
            params=params
        )

    async def prolong_make(
        self,
        type: str,
        ids: Union[int, List[int]],
        coupon: str = None,
        period_id: str = None
    ):
        """
        ### Create a renewal order for IP addresses.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/actions-with-proxies/extend-proxies#create-a-renewal-order  

        Args:
            type (str): The proxy type you want to prolong - ipv4 | ipv6 | mobile | isp | mix | mix_isp.
            ids (Union[int, List[int]]): A single ID or an array of IDs in '[ ]', separated by commas.
            coupon (str): Optional coupon code to apply.
            period_id (str): ID of the period selected in the /reference/list/{type} request.
            
        Returns:
            dict: Response containing the status and data of the renewal order request.
        """
        # Prepare the request parameters
        params = {
            "ids": ids if isinstance(ids, list) else [ids],
            "coupon": coupon,
            "periodId": period_id,
            "paymentId": self.payment_id
        }
        
        return await self.request(
            "GET",
            f"prolong/make/{type}",
            params=params
        )

    async def auth_list(self):
        """
        ### Retrieve a list of created authorizations for orders.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/actions-with-proxies/authorizations/list-of-authorizations

        Returns:
            dict: Response containing the status and data of the authorization list request.
        """
        return await self.request(
            "GET",
            "auth/list"
        )


    async def auth_add(
        self,
        order_number: str,
        login: str = None,
        password: str = None,
        ip: str = None
    ):
        """
        ### Create authorization for a specific order.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/actions-with-proxies/authorizations/create-authorization

        Args:
            order_number (str): The order number (NOT order_id).
            login (str): Login for authorization (required for login:password).
            password (str): Password for authorization (required for login:password).
            ip (str): IP address for IP authorization (required for IP authorization).
                        
        Returns:
            dict: Response containing the status and data of the authorization request.
        """
        # Determine the endpoint based on the provided parameters
        if ip:
            # IP authorization
            data = {
                "orderNumber": order_number,
                "generateAuth": self.generate_auth,
                "ip": ip
            }
            endpoint = "auth/add/ip"
        else:
            # Login:password authorization
            data = {
                "orderNumber": order_number,
                "generateAuth": self.generate_auth,
                "login": login,
                "password": password
            }
            endpoint = "auth/add"
        
        return await self.request(
            "POST",
            endpoint,
            json=data
        )
    
    async def auth_change(
        self,
        auth_id: str,
        active: bool = None,
        login: str = None,
        password: str = None,
        ip: str = None
    ):
        """
        ### Modify authentication data for accessing the proxy server.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/actions-with-proxies/authorizations/change-authorization

        Args:
            auth_id (str): Authorization ID (required).
            active (bool): Activate or deactivate authorization.
            login (str): Set a new username.
            password (str): Set a new password.
            ip (str): Set new IP address.
                        
        Returns:
            dict: Response containing the status and data of the change authorization request.
        """
        # Prepare the request body
        data = {
            "id": auth_id,
            "active": active,
            "login": login,
            "password": password,
            "ip": ip
        }

        return await self.request(
            "POST",
            "auth/change",
            json=data
        )

    async def auth_delete(self, auth_id: str):
        """
        ### Delete authorization for a specific order.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/actions-with-proxies/authorizations/delete-authorization  

        Args:
            auth_id (str): Authorization ID (required).
                        
        Returns:
            dict: Response containing the status and data of the delete authorization request.
        """
        # Prepare the request body
        data = {
            "id": auth_id
        }
        
        return await self.request(
            "DELETE",
            "auth/delete",
            json=data
        )

    async def reference_list(self, proxy_type: Optional[Literal["ipv4", "ipv6", "mobile", "isp", "resident", "mix", "mix_isp"]] = None):
        """
        ### Retrieve complete information about proxy orders.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/order-actions/complete-information  

        Args:
            proxy_type (Optional[Literal]): The proxy type you want to retrieve - ipv4 | ipv6 | mobile | isp | resident | mix | mix_isp.
                        
        Returns:
            dict: Response containing the status and data of the reference list request.
        """
        endpoint = "reference/list"
        if proxy_type:
            endpoint += f"/{proxy_type}"
        
        return await self.request(
            "GET",
            endpoint
        )


    async def order_calc_ipv4_isp_mix(
        self,
        country_id: int,
        period_id: str,
        quantity: int,
        coupon: Optional[str] = None,
        payment_id: Optional[int] = None,
        authorization: Optional[str] = None,
        custom_target_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        ### Calculate the price of an order for IPv4/ISP/MIX/MIX ISP proxies.
        
        Args:
            country_id (int): ID of the country selected in the /reference/list/{type} request.
            period_id (str): ID of the period selected in the /reference/list/{type} request.
            quantity (int): The number of proxies you want to order.
            coupon (Optional[str]): The coupon code, if available.
            payment_id (Optional[int]): IDs of the payment system. '1' for balance, '43' for the card added to your account.
            authorization (Optional[str]): The method of authorization. Leave blank if you want to use username and password.
            custom_target_name (Optional[str]): If you want to add a custom goal.
                        
        Returns:
            dict: Response containing the status and data of the order calculation request.
        """
        data = {
            "countryId": country_id,
            "periodId": period_id,
            "quantity": quantity,
            "coupon": coupon,
            "paymentId": payment_id,
            "authorization": authorization,
            "customTargetName": custom_target_name
        }
        
        return await self.request(
            "POST",
            "order/calc",
            json=data
        )

    async def order_calc_ipv6(
        self,
        country_id: int,
        period_id: str,
        quantity: int,
        coupon: Optional[str] = None,
        payment_id: Optional[int] = None,
        authorization: Optional[str] = None,
        custom_target_name: Optional[str] = None,
        protocol: Optional[Literal["HTTPS", "SOCKS5"]] = None
    ) -> Dict[str, Any]:
        """
        ### Calculate the price of an order for IPv6 proxies.
        
        Args:
            country_id (int): ID of the country selected in the /reference/list/{type} request.
            period_id (str): ID of the period selected in the /reference/list/{type} request.
            quantity (int): The number of proxies you want to order.
            coupon (Optional[str]): The coupon code, if available.
            payment_id (Optional[int]): IDs of the payment system. '1' for balance, '43' for the card added to your account.
            authorization (Optional[str]): The method of authorization. Leave blank if you want to use username and password.
            custom_target_name (Optional[str]): If you want to add a custom goal.
            protocol (Optional[Literal]): Protocol type - HTTPS or SOCKS5.
                        
        Returns:
            dict: Response containing the status and data of the order calculation request.
        """
        data = {
            "countryId": country_id,
            "periodId": period_id,
            "quantity": quantity,
            "coupon": coupon,
            "paymentId": payment_id,
            "authorization": authorization,
            "customTargetName": custom_target_name,
            "protocol": protocol
        }
        
        return await self.request(
            "POST",
            "order/calc",
            json=data
        )

    async def order_calc_mobile(
        self,
        country_id: int,
        period_id: str,
        quantity: int,
        coupon: Optional[str] = None,
        payment_id: Optional[int] = None,
        authorization: Optional[str] = None,
        custom_target_name: Optional[str] = None,
        mobile_service_type: Optional[Literal["shared", "dedicated"]] = None,
        operator_id: Optional[str] = None,
        rotation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        ### Calculate the price of an order for Mobile proxies.
        
        Args:
            country_id (int): ID of the country selected in the /reference/list/{type} request.
            period_id (str): ID of the period selected in the /reference/list/{type} request.
            quantity (int): The number of proxies you want to order.
            coupon (Optional[str]): The coupon code, if available.
            payment_id (Optional[int]): IDs of the payment system. '1' for balance, '43' for the card added to your account.
            authorization (Optional[str]): The method of authorization. Leave blank if you want to use username and password.
            custom_target_name (Optional[str]): If you want to add a custom goal.
            mobile_service_type (Optional[Literal]): Service type for mobile - shared or dedicated.
            operator_id (Optional[str]): ID of the operator selected in the /reference/list/{type} request.
            rotation_id (Optional[int]): ID of the rotation selected in the /reference/list/{type} request.
                        
        Returns:
            dict: Response containing the status and data of the order calculation request.
        """
        data = {
            "countryId": country_id,
            "periodId": period_id,
            "quantity": quantity,
            "coupon": coupon,
            "paymentId": payment_id,
            "authorization": authorization,
            "customTargetName": custom_target_name,
            "mobileServiceType": mobile_service_type,
            "operatorId": operator_id,
            "rotationId": rotation_id
        }
        
        return await self.request(
            "POST",
            "order/calc",
            json=data
        )

    async def order_calc_resident(
        self,
        tarif_id: int,
        coupon: Optional[str] = None,
        payment_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        ### Calculate the price of an order for Resident proxies.
        
        Args:
            coupon (Optional[str]): The coupon code, if available.
            payment_id (Optional[int]): IDs of the payment system. '1' for balance, '43' for the card added to your account.
            tarif_id (int): ID of the tarif selected in the /reference/list/{type} request.
                        
        Returns:
            dict: Response containing the status and data of the order calculation request.
        """
        data = {
            "coupon": coupon,
            "paymentId": payment_id,
            "tarifId": tarif_id
        }
        
        return await self.request(
            "POST",
            "order/calc",
            json=data
        )

    async def order_make_ipv4_isp_mix(
        self,
        country_id: int,
        period_id: str,
        quantity: int,
        coupon: Optional[str] = None,
        payment_id: Optional[int] = None,
        authorization: Optional[str] = None,
        custom_target_name: Optional[str] = None,
        generate_auth: Optional[str] = "N"
    ) -> Dict[str, Any]:
        """
        ### Place an order for IPv4/ISP/MIX/MIX ISP proxies.
        
        Args:
            country_id (int): ID of the country selected in the /reference/list/{type} request.
            period_id (str): ID of the period selected in the /reference/list/{type} request.
            quantity (int): The number of proxies you want to order.
            coupon (Optional[str]): The coupon code, if available.
            payment_id (Optional[int]): IDs of the payment system. '1' for balance, '43' for the card added to your account.
            authorization (Optional[str]): The method of authorization. Leave blank if you want to use username and password.
            custom_target_name (Optional[str]): If you want to add a custom goal.
            generate_auth (Optional[str]): Create custom authorization - Y/N (N - default).
                        
        Returns:
            dict: Response containing the status and data of the order placement request.
        """
        data = {
            "countryId": country_id,
            "periodId": period_id,
            "quantity": quantity,
            "coupon": coupon,
            "paymentId": payment_id,
            "authorization": authorization,
            "customTargetName": custom_target_name,
            "generateAuth": generate_auth
        }
        
        return await self.request(
            "POST",
            "order/make",
            json=data
        )

    async def order_make_ipv6(
        self,
        country_id: int,
        period_id: str,
        quantity: int,
        coupon: Optional[str] = None,
        payment_id: Optional[int] = None,
        authorization: Optional[str] = None,
        custom_target_name: Optional[str] = None,
        protocol: Optional[Literal["HTTPS", "SOCKS5"]] = None
    ) -> Dict[str, Any]:
        """
        ### Place an order for IPv6 proxies.
        
        Args:
            country_id (int): ID of the country selected in the /reference/list/{type} request.
            period_id (str): ID of the period selected in the /reference/list/{type} request.
            quantity (int): The number of proxies you want to order.
            coupon (Optional[str]): The coupon code, if available.
            payment_id (Optional[int]): IDs of the payment system. '1' for balance, '43' for the card added to your account.
            authorization (Optional[str]): The method of authorization. Leave blank if you want to use username and password.
            custom_target_name (Optional[str]): If you want to add a custom goal.
            protocol (Optional[Literal]): Protocol type - HTTPS or SOCKS5.
                        
        Returns:
            dict: Response containing the status and data of the order placement request.
        """
        data = {
            "countryId": country_id,
            "periodId": period_id,
            "quantity": quantity,
            "coupon": coupon,
            "paymentId": payment_id,
            "authorization": authorization,
            "customTargetName": custom_target_name,
            "protocol": protocol
        }
        
        return await self.request(
            "POST",
            "order/make",
            json=data
        )


    async def order_make_mobile(
        self,
        country_id: int,
        period_id: str,
        quantity: int,
        coupon: Optional[str] = None,
        payment_id: Optional[int] = None,
        authorization: Optional[str] = None,
        custom_target_name: Optional[str] = None,
        mobile_service_type: Optional[Literal["shared", "dedicated"]] = None,
        operator_id: Optional[str] = None,
        rotation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        ### Calculate the price of an order for Mobile proxies.
        
        Args:
            country_id (int): ID of the country selected in the /reference/list/{type} request.
            period_id (str): ID of the period selected in the /reference/list/{type} request.
            quantity (int): The number of proxies you want to order.
            coupon (Optional[str]): The coupon code, if available.
            payment_id (Optional[int]): IDs of the payment system. '1' for balance, '43' for the card added to your account.
            authorization (Optional[str]): The method of authorization. Leave blank if you want to use username and password.
            custom_target_name (Optional[str]): If you want to add a custom goal.
            mobile_service_type (Optional[Literal]): Service type for mobile - shared or dedicated.
            operator_id (Optional[str]): ID of the operator selected in the /reference/list/{type} request.
            rotation_id (Optional[int]): ID of the rotation selected in the /reference/list/{type} request.
                        
        Returns:
            dict: Response containing the status and data of the order calculation request.
        """
        data = {
            "countryId": country_id,
            "periodId": period_id,
            "quantity": quantity,
            "coupon": coupon,
            "paymentId": payment_id,
            "authorization": authorization,
            "customTargetName": custom_target_name,
            "mobileServiceType": mobile_service_type,
            "operatorId": operator_id,
            "rotationId": rotation_id
        }
        
        return await self.request(
            "POST",
            "order/make",
            json=data
        )

    async def order_make_resident(
        self,
        tarif_id: int,
        coupon: Optional[str] = None,
        payment_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        ### Calculate the price of an order for Resident proxies.
        
        Args:
            coupon (Optional[str]): The coupon code, if available.
            payment_id (Optional[int]): IDs of the payment system. '1' for balance, '43' for the card added to your account.
            tarif_id (int): ID of the tarif selected in the /reference/list/{type} request.
                        
        Returns:
            dict: Response containing the status and data of the order calculation request.
        """
        data = {
            "coupon": coupon,
            "paymentId": payment_id,
            "tarifId": tarif_id
        }
        
        return await self.request(
            "POST",
            "order/make",
            json=data
        )

    async def get_balance(self):
        """
        ### Retrieve the available balance of your personal account.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/balance

        Returns:
            dict: The response containing the balance information.
        """
        return await self.request(
            "GET",
            "balance/get"
        )

    async def replenish_balance(self, summ: float, payment_id: int):
        """
        ### Replenish your balance.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/balance#replenish-balance

        Args:
            summ (float): The amount you want to replenish.
            payment_id (int): The ID of the payment method you selected.

        Returns:
            dict: The response containing the status and URL for payment.
        """
        body = {
            "summ": summ,
            "paymentId": payment_id
        }
        
        return await self.request(
            "POST",
            "balance/add",
            json=body
        )

    async def get_payment_systems(self):
        """
        ### Show available payment systems for replenishing your balance.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/balance#payment-systems

        Returns:
            dict: The response containing the list of available payment systems.
        """
        return await self.request(
            "GET",
            "balance/payments/list"
        )

    async def get_residential_package(self):
        """
        ### Retrieve information about your residential proxy package.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/get-package-information  

        Returns:
            dict: The response containing package information.
        """
        return await self.request(
            "GET",
            "resident/package"
        )

    async def get_residential_geo(self, filename: str = None) -> str:
        """
        ### Retrieve all available residential proxy locations to zip file.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/get-all-locations  

        Returns:
            str: The response containing raw zip file with all available GEO information.
        """
        response = await self.request(
            "GET",
            "resident/geo"
        )

        if filename:
            if not filename.endswith(".zip"):
                filename += ".zip"

            with open(filename, "wb") as f:
                f.write(response)
        
        return response
    
    async def get_existing_ip_list(self):
        """
        ### Retrieve all created IP lists in your residential proxy package.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/get-existing-ip-list  

        Returns:
            dict: The response containing all created IP lists.
        """
        return await self.request(
            "GET",
            "resident/lists"
        )

    async def create_residential_list(self, title: str, whitelist: str = None, geo: dict = None, export: dict = None, rotation: int = -1):
        """
        ### Create a new residential proxy list.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/create-list  

        Args:
            title (str): Name of the list you are creating.
            whitelist (str): IPs for authorization. Leave blank if you want to authorize with login credentials.
            geo (dict): GEO data to add to your list (country, region, city, ISP).
            export (dict): Specifies the number of IPs in your list and the export type (port numbers and file format).
            rotation (int): '-1' for no rotation (Sticky), '0' for rotation per request, '1' to '3600' for time-based rotation in seconds.

        Returns:
            dict: The response containing the status and details of the created list.
        """
        body = {
            "title": title,
            "whitelist": whitelist,
            "geo": geo,
            "export": export,
            "rotation": rotation
        }
        
        return await self.request(
            "POST",
            "resident/list/add",
            json=body
        )

    async def rename_residential_list(self, list_id: int, title: str):
        """
        ### Rename an existing residential proxy list.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/rename-list  

        Args:
            list_id (int): ID of the list to be renamed.
            title (str): The new name for the list.

        Returns:
            dict: The response containing the status and details of the renamed list.
        """
        body = {
            "id": list_id,
            "title": title
        }
        
        return await self.request(
            "POST",
            "resident/list/rename",
            json=body
        )

    async def change_rotation_settings(self, list_id: int, rotation: int):
        """
        ### Change the rotation settings for an existing residential proxy list.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/change-rotation-settings  

        Args:
            list_id (int): ID of the list.
            rotation (int): The new rotation value to set. '-1' for no rotation (Sticky), '0' for rotation per request, '1' to '3600' for time-based rotation in seconds.

        Returns:
            dict: The response containing the status and details of the updated list.
        """
        body = {
            "id": list_id,
            "rotation": rotation
        }
        
        return await self.request(
            "POST",
            "resident/list/rotation",
            json=body
        )

    async def delete_residential_list(self, list_id: int):
        """
        ### Remove an existing residential proxy list from the package.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/delete-list  

        Args:
            list_id (int): ID of the list to be deleted.

        Returns:
            dict: The response containing the status of the deletion.
        """
        body = {
            "id": list_id
        }
        
        return await self.request(
            "DELETE",
            "resident/list/delete",
            json=body
        )

    async def create_subuser_package(self, is_link_date: bool, rotation: int, traffic_limit: str, expired_at: str):
        """
        ### Create a subuser package from your current active tariff with traffic.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/subaccounts-subusers/create-subuser-package  

        Args:
            is_link_date (bool): If 'true', the expiration date will be linked to the main package.
            rotation (int): Specifies the type of rotation: '-1' = No rotation (Sticky), '0' = Rotation per request, '1' to '3600' = Rotation by time in seconds.
            traffic_limit (str): The amount of bytes allocated for the subuser package.
            expired_at (str): The expiration date for the subuser package.

        Returns:
            dict: The response containing the status and details of the created subuser package.
        """
        body = {
            "is_link_date": is_link_date,
            "rotation": rotation,
            "traffic_limit": traffic_limit,
            "expired_at": expired_at
        }
        
        return await self.request(
            "POST",
            "residentsubuser/create",
            json=body
        )

    async def update_subuser_package(self, is_link_date: bool, rotation: int, traffic_limit: str, expired_at: str, is_active: bool, package_key: str):
        """
        ### Update the subuser's package.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/subaccounts-subusers/update-package  

        Args:
            is_link_date (bool): If 'true', the update date will be linked to the main package.
            rotation (int): Specifies the rotation type: '-1' = No rotation (Sticky), '0' = Rotation per request, '1' to '3600' = Rotation by time in seconds.
            traffic_limit (str): Specifies the amount of bytes allocated for the subpackage.
            expired_at (str): Expiration date of the subpackage.
            is_active (bool): Set the status of the subpackage: 'true' for active, 'false' for inactive.
            package_key (str): Key of your active package.

        Returns:
            dict: The response containing the status and details of the updated subuser package.
        """
        body = {
            "is_link_date": is_link_date,
            "rotation": rotation,
            "traffic_limit": traffic_limit,
            "expired_at": expired_at,
            "is_active": is_active,
            "package_key": package_key
        }
        
        return await self.request(
            "POST",
            "residentsubuser/update",
            json=body
        )

    async def get_subuser_packages(self):
        """
        ### Retrieve information about the subuser's package, including remaining traffic and expiration date.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/subaccounts-subusers/get-package-information  

        Returns:
            dict: The response containing the status and details of the subuser's package.
        """
        return await self.request(
            "GET",
            "residentsubuser/packages"
        )

    async def delete_subuser_package(self, package_key: str):
        """
        ### Remove a subuser's package.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/subaccounts-subusers/delete-subusers-package  

        Args:
            package_key (str): Subpackage key from "Get subuser package information" request.

        Returns:
            dict: The response containing the status of the deletion.
        """
        body = {
            "package_key": package_key
        }
        
        return await self.request(
            "DELETE",
            "residentsubuser/delete",
            json=body
        )

    async def retrieve_existing_ip_lists(self, package_key: str, list_id: int = None):
        """
        ### Retrieve all created lists in the subuser's package.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/subaccounts-subusers/retrieve-existing-ip-lists  

        Args:
            package_key (str): The key of the subuser's package from which you want to view the proxy list.
            list_id (int, optional): The ID of the list you want to view.

        Returns:
            dict: The response containing the status and details of the existing IP lists.
        """
        params = {
            "package_key": package_key,
            "listId": list_id
        }
        
        return await self.request(
            "GET",
            "residentsubuser/lists",
            params=params
        )

    async def create_ip_list(self, title: str, whitelist: str = None, geo: dict = None, export: dict = None, rotation: int = -1, package_key: str = None):
        """
        ### Create an IP list in the subuser's package.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/subaccounts-subusers/create-ip-list  

        Args:
            title (str): Name of the list you are creating.
            whitelist (str, optional): IPs for authorization. Leave blank if you want to authorize with login credentials.
            geo (dict, optional): GEO data to add to your list (country, region, city, ISP).
            export (dict, optional): Specifies the number of IPs in your list and the export type (port numbers and file format).
            rotation (int, optional): '-1' for no rotation (Sticky), '0' for rotation per request, '1' to '3600' for time-based rotation in seconds.
            package_key (str, optional): Key of a subuser's package where you want to add the list of IPs.

        Returns:
            dict: The response containing the status and details of the created IP list.
        """
        body = {
            "title": title,
            "whitelist": whitelist,
            "geo": geo,
            "export": export,
            "rotation": rotation,
            "package_key": package_key
        }
        
        return await self.request(
            "POST",
            "residentsubuser/list/add",
            json=body
        )

    async def rename_created_list(self, list_id: int, title: str, package_key: str):
        """
        ### Rename an existing list in a subuser's package.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/subaccounts-subusers/rename-created-list  

        Args:
            list_id (int): ID of the list to be renamed.
            title (str): The new name for the list.
            package_key (str): The key of the subuser's package where the list of IPs will be renamed.

        Returns:
            dict: The response containing the status and details of the renamed list.
        """
        body = {
            "id": list_id,
            "title": title,
            "package_key": package_key
        }
        
        return await self.request(
            "POST",
            "residentsubuser/list/rename",
            json=body
        )

    async def change_rotation(self, list_id: int, rotation: int, package_key: str):
        """
        ### Change the rotation of a created list in a subuser's package.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/subaccounts-subusers/change-rotation  

        Args:
            list_id (int): ID of the created list.
            rotation (int): The new rotation value to set. "-1" for no rotation (Sticky), "0" for rotation per request, "1" to "3600" for time-based rotation in seconds.
            package_key (str): Key of the subuser's package where you want to change rotation.

        Returns:
            dict: The response containing the status and details of the updated list.
        """
        body = {
            "id": list_id,
            "rotation": rotation,
            "package_key": package_key
        }
        
        return await self.request(
            "POST",
            "residentsubuser/list/rotation",
            json=body
        )

    async def delete_list(self, list_id: int, package_key: str):
        """
        ### Remove a created list from a subuser's package.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/subaccounts-subusers/delete-list  

        Args:
            list_id (int): ID of the created list.
            package_key (str): The key of the subuser's package from which you want to remove the list.

        Returns:
            dict: The response containing the status of the deletion.
        """
        body = {
            "id": list_id,
            "package_key": package_key
        }
        
        return await self.request(
            "DELETE",
            "residentsubuser/list/delete",
            json=body
        )


    async def subuser_create_special_list(self, package_key: str):
        """
        ### Create a special list in a subuser's package.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/subaccounts-subusers/create-a-special-list-for-api-tool  

        Args:
            package_key (str): The key of the subuser's package where you want to create the special list.

        Returns:
            dict: The response containing the status and details of the created special list.
        """
        body = {
            "package_key": package_key
        }
        
        return await self.request(
            "PUT",
            "residentsubuser/list/tools",
            json=body
        )

    async def create_special_list(self):
        """
        ### Create a special list of residential proxies.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/api-tool/create-a-special-list

        Returns:
            dict: A response containing the status and data of the created list.
                Example response:
                {
                    "status": "success",
                    "data": {
                        "id": 561,
                        "login": "api3c8aa1d4",
                        "password": "AZT62Dx3"
                    },
                    "errors": []
                }
        """
        return await self.request(
            "PUT",
            "resident/list/tools"
        )

    async def get_all_isp_codes(self):
        """
        ### Retrieve a list of all available ISP codes.
        
        Docs: https://docs.proxy-seller.com/proxy-seller/residential-proxy/api-tool/get-all-isp-codes

        Returns:
            list: A list of dictionaries containing ISP information.
                Example response:
                [
                    {
                        "isp": "001 IT Complex",
                        "code": 23
                    },
                    {
                        "isp": "01 System Srl",
                        "code": 24
                    },
                    {
                        "isp": "01 Telecom Ltd",
                        "code": 25
                    },
                    ...
                ]
        """
        return await self.request(
            "GET",
            "resident/geo/isp"
        )
