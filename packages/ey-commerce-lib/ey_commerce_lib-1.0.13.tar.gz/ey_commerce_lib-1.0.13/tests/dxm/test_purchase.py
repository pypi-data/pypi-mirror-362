import pytest

from ey_commerce_lib.dxm.constant.order import ORDER_SEARCH_APPROVAL_BASE_FORM, \
    ORDER_SEARCH_PENDING_PROCESSING_BASE_FORM, ORDER_SEARCH_SELF_WAREHOUSE_BASE_FORM, \
    ORDER_SEARCH_OUT_OF_STOCK_BASE_FORM
from ey_commerce_lib.dxm.main import DxmClient
from ey_commerce_lib.dxm.schemas.warehouse import WarehouseProductQuery
from ey_commerce_lib.dxm.utils.mark import get_custom_mark_content_list_by_data_custom_mark, \
    generate_add_or_update_user_comment_data_by_content_list
from ey_commerce_lib.four_seller.main import FourSellerClient
from ey_commerce_lib.four_seller.schemas.query.order import FourSellerOrderQueryModel
from ey_commerce_lib.takesend.main import TakeSendClient


async def login_success(user_token: str):
    print(f'user_token: {user_token}')
    pass


@pytest.mark.asyncio
async def test_auto_login_4seller():
    # user_token = await auto_login_4seller(user_name="sky@eeyoung.com", password="ey010203@@")
    # print(user_token)
    async with FourSellerClient(
            user_name="xxxxx",
            password="xxxxxx",
            login_success_call_back=login_success,
            user_token="xxxxxx") as four_seller_client:
        await four_seller_client.list_history_order(FourSellerOrderQueryModel())


cookies = {
    'dxm_i': 'MTAyNzg5NiFhVDB4TURJM09EazIhZjc5ZTMxMjZmN2Q3NTk5OGZlMDg4YjQzNzNlNzlmOWY',
    'dxm_t': 'MTcxNDk2NDU4MiFkRDB4TnpFME9UWTBOVGd5IWIzZWRjYTc3YTdjYWE0MmIxMWYwNjFhOTlmMDgxZjY5',
    'dxm_c': 'TWVOMVpiclYhWXoxTlpVNHhXbUp5VmchNmM5MmM5ODc1MDBkODVjOWJmOTFlMzdhNGJiNWI3Njk',
    'dxm_w': 'ZDc3NWVhOTdkOTEyNGE4ZmRkODBmYzc2YmFlOGVjZjEhZHoxa056YzFaV0U1TjJRNU1USTBZVGhtWkdRNE1HWmpOelppWVdVNFpXTm1NUSFmZWZiZGZiMTEwMzhlN2M4M2MzYjZmYjAxYTcxMjViMw',
    'dxm_s': 'aMHO7LWKAQe6NzFrV3O4cceXkBriLGNmwondOR7INWs',
    'MYJ_MKTG_fapsc5t4tc': 'JTdCJTdE',
    'MYJ_fapsc5t4tc': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJkMGRlYzNkYi00MTNlLTQyZjktOWIxNC0xYzBhZTY4MTk4ZmIlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIxMDI3ODk2JTIyJTJDJTIycGFyZW50SWQlMjIlM0ElMjIyNTg2MzQlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzMxMDU5MDc1MjU0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczMTA1OTA3NTQyNCUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTE2JTdE',
    'MYJ_fapsc5t4tc': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJkMGRlYzNkYi00MTNlLTQyZjktOWIxNC0xYzBhZTY4MTk4ZmIlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIxMDI3ODk2JTIyJTJDJTIycGFyZW50SWQlMjIlM0ElMjIyNTg2MzQlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzMxMDU5MDc1MTEwJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczMTA1OTA3NTk5NiUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTE2JTdE',
    '_dxm_ad_client_id': '7AEFA0B78CE1B35075D391C5226612CED',
    'Hm_lvt_f8001a3f3d9bf5923f780580eb550c0b': '1731459796,1731547149,1731590878,1731893161',
    'HMACCOUNT': 'F266E8F609D8D8B1',
    'MYJ_fapsc5t4tc': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJkMGRlYzNkYi00MTNlLTQyZjktOWIxNC0xYzBhZTY4MTk4ZmIlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIxMDI3ODk2JTIyJTJDJTIycGFyZW50SWQlMjIlM0ElMjIyNTg2MzQlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzMxOTAxNDMzMTk3JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRJZCUyMiUzQTExNiU3RA==',
    'Hm_lpvt_f8001a3f3d9bf5923f780580eb550c0b': '1731901433',
    'JSESSIONID': 'CD9C8372185D453012E5EEFBA64E2C9C',
}

headers = {
    'accept': 'text/html, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.dianxiaomi.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.dianxiaomi.com/sys/index.htm?go=m420',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}


@pytest.mark.asyncio
async def test_dxm_api():
    async with (DxmClient(headers=headers, cookies=cookies) as dxm_client):
        data = await dxm_client.list_order_count()
        for item in data:
            print(item)


@pytest.mark.asyncio
async def test_warehouse():
    async with (DxmClient(headers=headers, cookies=cookies) as dxm_client):
        print(await dxm_client.page_warehouse_product(WarehouseProductQuery()))

@pytest.mark.asyncio
async def test_tasksend_api():
    async with (TakeSendClient(username="", password="") as tasksend_client):
        await tasksend_client.login()