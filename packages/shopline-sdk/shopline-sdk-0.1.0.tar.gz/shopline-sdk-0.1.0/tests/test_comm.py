#!/usr/bin/python3
# @Time    : 2025-06-16
# @Author  : Kevin Kong (kfx2007@163.com)

import unittest
from shopline.api import ShoplineAPI


class TestComm(unittest.TestCase):
    def setUp(self):
        self.shopline = ShoplineAPI(
            "d5c95e06004cbe28a76f306e36ba307d26e2b414ddfae067f137b152193e211b",
            "1b63264ea446d59f08a26db543ea4686b5056ef194c25076deb2ef2652b3db0d",
            "684291be1dc1b00060d52b9e",
        )
        self.redirect_uri = "https://192.168.195.11:9015/shopline/oauth/callback"

    def test_get_oauth_url(self):
        scope = "customers orders products"
        url = self.shopline.comm.get_oauth_url(self.redirect_uri, scope)
        print("++++++url+++++++")
        print(url)

    def test_get_access_token(self):
        code = "71726d184a0bcbbecea8eb09c73e6cbc42d97e4182ffb263fad5ff32669a1f85"
        token = self.shopline.comm.get_access_token(code, self.redirect_uri)
        print("++++++token+++++++")
        print(token)
        """
        {'access_token': 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJmODBkMzEzNmYzZGNlNGVhZTljMDE3NGZkYzhhNjVlNyIsImRhdGEiOnsibWVyY2hhbnRfaWQiOiI2ODQyOTFiZTFkYzFiMDAwNjBkNTJiOWUiLCJhcHBsaWNhdGlvbl9pZCI6IjY4NDI5MzAzMmJkYTMwMDAwYWFhMWZhZCJ9LCJpc3MiOiJodHRwczovL2RldmVsb3BlcnMuc2hvcGxpbmVhcHAuY29tIiwiYXVkIjpbXSwic3ViIjoiNjg0MjkxYmUxZGMxYjAwMDYwZDUyYjllIn0.UGqWBCq61iVP31R2IMol6ukE8VOUwwW8WLBpqshehu4', 'token_type': 'Bearer', 'expires_in': 15778476, 'refresh_token': 'efdee02ee191de5e52d3f10d82af96ef7e42ac6e536b15a9f6dc700be984b186', 'scope': 'addon_products', 'created_at': 1750141238, 'resource_owner_id': '684291be1dc1b00060d52b9e'}
        """


if __name__ == "__main__":
    unittest.main()
