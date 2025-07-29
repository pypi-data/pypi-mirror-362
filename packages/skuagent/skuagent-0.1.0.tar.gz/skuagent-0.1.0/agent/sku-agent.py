from typing import Any
from mcp.server.fastmcp import FastMCP
import pymysql
from dbutils.pooled_db import PooledDB
import json

mcp = FastMCP("sku-agent")


# pool = PooledDB(
#     creator=pymysql,  # 使用的数据库模块
#     maxconnections=5,  # 最大连接数
#     mincached=2,       # 初始化时，至少创建的空连接数
#     maxcached=5,       # 连接池中最多缓存的连接数
#     blocking=True,     # 连接池中如果没有可用连接后，是否阻塞等待
#     host='121.121.32.2',
#     port=3306,
#     user='root',
#     password='123456',
#     database='pp',
#     charset='utf8mb4',
#     cursorclass=pymysql.cursors.DictCursor
# )

# def get_connection():
#     return pool.connection()

@mcp.tool(description="根据设备名称、设备厂家、设备型号查询对应设备")
async def get_sku(name:str,manufacture:str,model:str)->str:
    """根据设备名称、设备厂家、设备型号查询对应设备
    Args:
        name:设备名称
        manufacture:设备厂家
        model:设备型号
    """
    # with get_connection() as connection:
    #     with connection.cursor() as cursor:
            # sql = "SELECT name,phone_number,location_city FROM wk_official_website_resume WHERE name =%s AND phone_number = %s AND location_city = %s"
            # cursor.execute(sql, (name,manufacture,model))
            # result = cursor.fetchone()
            # return str(result) if result else "未找到匹配的设备"
            # employee_string = '{"first_name": "Michael", "last_name": "Rodgers", "department": "Marketing"}'
            # json_object = json.loads(employee_string)
            # return json_object
    employee_string = '{"first_name": "Michael", "last_name": "Rodgers", "department": "Marketing"}'
    json_object = json.loads(employee_string)
    return json_object


if __name__ == "__main__":
    # 初始化并运行服务器
    mcp.run(transport='streamable-http')