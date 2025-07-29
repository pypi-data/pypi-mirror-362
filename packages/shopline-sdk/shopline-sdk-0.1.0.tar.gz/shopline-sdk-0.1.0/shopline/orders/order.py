#!/usr/bin/python3
# @Time    : 2025-06-17
# @Author  : Kevin Kong (kfx2007@163.com)

from shopline.comm import Comm
from shopline.comm import API_URL
from shopline.comm.exceptions import ShoplineAPIException
import logging

class Order(Comm):
    
    def get_orders(self, updated_after=None, updated_before=None,created_after=None, created_before=None, order_ids=[], per_page=50, page=1, sort_by="asc", previous_id=None):
        """
        Get the list of orders.
        :param updated_after: Filter orders updated after this date.
        :param updated_before: Filter orders updated before this date.
        :param created_after: Filter orders created after this date.
        :param created_before: Filter orders created before this date.
        :param order_ids: List of specific order IDs to retrieve.
        :param per_page: Number of orders per page.
        :param page: Page number to retrieve.
        :param sort_by: Field to sort the orders by.
        :param previous_id: ID of the last order from the previous page, used for pagination
        
        :return: List of orders.
        """
        
        url = f"{API_URL}/orders"
        params = {
            "updated_after": updated_after,
            "updated_before": updated_before,
            "created_after": created_after,
            "created_before": created_before,
            "order_ids": order_ids,
            "per_page": per_page,
            "page": page,
            "sort_by": sort_by,
            "previous_id": previous_id
        }
        response = self.get(url, params=params)
        if response.status_code != 200:
            raise ShoplineAPIException(f"Failed to fetch orders: {response.status_code} - {response.text}")
        return response.json() if response.status_code == 200 else None
    
    def get_order(self, order_id):
        """
        Get a specific order by its ID.
        
        :param order_id: The ID of the order to retrieve.
        :return: The order details.
        """
        url = f"{API_URL}/orders/{order_id}"
        response = self.get(url)
        if response.status_code != 200:
            raise ShoplineAPIException(f"Failed to fetch order {order_id}: {response.status_code} - {response.text}")
        return response.json() if response.status_code == 200 else None
    
    def update_order(self, order_id, data):
        """
        Update an order with the given data.
        
        :param order_id: The ID of the order to update.
        :param data: The data to update the order with.
        :return: The updated order details.
        """
        url = f"{API_URL}/orders/{order_id}"
        response = self.patch(url, json=data)
        if response.status_code != 200:
            raise ShoplineAPIException(f"Failed to update order {order_id}: {response.status_code} - {response.text}")
        return response.json() if response.status_code == 200 else None
    
    def update_delivery_status(self, order_id, status):
        """
        Update the delivery status of an order.
        
        https://open-api.docs.shoplineapp.com/docs/update-order-delivery-status
        
        pending 備貨中
        shipping 發貨中
        shipped 已發貨
        arrived 已到達
        
        :param order_id: The ID of the order to update.
        :param status: The new delivery status to set.
        :return: The updated order details.
        """
        url = f"{API_URL}/orders/{order_id}/order_delivery_status"
        data = {"status": status}
        response = self.patch(url, json=data)
        if response.status_code != 200:
            raise ShoplineAPIException(f"Failed to update delivery status for order {order_id}: {response.status_code} - {response.text}")
        return response.json() if response.status_code == 200 else None