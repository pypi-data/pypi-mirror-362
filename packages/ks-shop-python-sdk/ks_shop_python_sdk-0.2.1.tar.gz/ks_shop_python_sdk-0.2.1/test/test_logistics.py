import sys
from pathlib import Path
# 将项目根目录添加到 sys.path
root_dir = Path(__file__).parent.parent  # 根据文件位置调整层级
sys.path.insert(0, str(root_dir))

from ks_shop_api.logistics.request import OpenAddressDistrictListRequest
from ks_shop_api.logistics.schema import OpenAddressDistrictListSchema
from ks_shop_api.schema import baseAppInfoSchema

access_token = 'ChFvYXV0aC5hY2Nlc3NUb2tlbhJwWA_KH-gyF_nmIXRUTx1twiEPU77X0C8arRO7vajLBy49kJf4klaDJrGjNQ_pcuZzckWVnLjBzUSGfJ05qnw6kmkIL5mk89QTljvVXWE1XwQsPwF6exVOnLVMLQXBWqQyp_eq0YBoAAmiFO-Zr4_waRoS8dsD42CUQrG4hOifcpo8vBuxIiAUT41gUyRKH80T9mK-yd4hf9b3eBzg9YxZubCN06JUsigFMAE'
base_app_info = baseAppInfoSchema()
base_app_info.app_key = "ks653021946718290428"
base_app_info.secret = "ft9b-ITeSl4qooSGxrdTMQ"
base_app_info.sign_secret = "dc90166e66aa4a4a5921bf0e2941a4fe"
print(base_app_info)
ks_obj = OpenAddressDistrictListRequest(**base_app_info.model_dump())
ks_schema = OpenAddressDistrictListSchema()
ks_schema.districtVersion = "2021"  # Example value, can be set as needed
print(ks_schema)
print(ks_schema.model_dump())

res = ks_obj.getResponse(access_token, params=ks_schema)
print(res)
