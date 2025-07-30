from typing import Any, Dict, Optional
import asyncio
import time
import logging
from fastmcp import FastMCP
import os
import dotenv
from .booking_system import BookingSystem, ValidationError

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

dotenv.load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("CUHKSZ-BOOKING")

# 全局变量
_booking_instance: Optional[BookingSystem] = None
_last_login_time: float = 0
_global_cache: Dict[str, Dict] = {}
LOGIN_TIMEOUT = 15 * 60  # 15分钟，单位秒

def _get_booking_instance() -> BookingSystem:
    """获取Booking实例，如果需要则重新登录"""
    global _booking_instance, _last_login_time
    
    current_time = time.time()
    
    # 检查是否需要重新登录
    if (_booking_instance is None or 
        current_time - _last_login_time > LOGIN_TIMEOUT):
        
        if _booking_instance is None:
            logger.info("Booking instance not found, creating a new one.")
        else:
            logger.info(f"Login session timed out ({LOGIN_TIMEOUT}s). Performing relogin.")
        
        username = os.getenv("BOOKING_USERNAME")
        password = os.getenv("BOOKING_PASSWORD")
        
        if not username or not password:
            logger.error("BOOKING_USERNAME and BOOKING_PASSWORD must be set in environment variables.")
            raise ValueError("BOOKING_USERNAME and BOOKING_PASSWORD must be set in environment variables")
        
        try:
            _booking_instance = BookingSystem(username, password)
            _last_login_time = current_time
            logger.info(f"Booking login successful at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}")
        except ValidationError as e:
            logger.error(f"Failed to login to Booking system: {e}")
            raise RuntimeError(f"Failed to login to Booking system: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during Booking login: {e}")
            raise RuntimeError(f"Unexpected error during Booking login: {e}")
    
    return _booking_instance

def _get_cached_or_fetch(cache_key: str, fetch_func, ttl: int = 300) -> str:
    """从缓存获取数据或重新获取"""
    global _global_cache
    
    current_time = time.time()
    
    # 检查缓存是否存在且未过期
    if (cache_key in _global_cache and 
        current_time - _global_cache[cache_key]['timestamp'] < ttl):
        logger.info(f"Cache HIT for key: '{cache_key}'")
        return _global_cache[cache_key]['data']
    
    logger.info(f"Cache MISS for key: '{cache_key}'. Fetching new data.")
    # 缓存不存在或已过期，重新获取数据
    try:
        data = fetch_func()
        _global_cache[cache_key] = {
            'data': data,
            'timestamp': current_time
        }
        logger.info(f"Successfully fetched and cached data for key: '{cache_key}'")
        return data
    except Exception as e:
        logger.error(f"Error fetching data for key '{cache_key}': {e}", exc_info=True)
        return f"Error: {str(e)}"

def _format_field_info(field_info: dict) -> str:
    """格式化场地信息"""
    if not field_info:
        return "未找到场地信息"
    
    places_str = "\n".join([f"  - {name} (ID: {pid})" for pid, name in field_info['places'].items()])
    bookings_str = "\n".join([f"  - {booking}" for booking in field_info['book_info']])
    
    return f"""场地信息:
场地名称: {field_info['field_name']}
场地ID: {field_info['field_id']}

可用场所:
{places_str}

当前预订 ({len(field_info['book_info'])} 个):
{bookings_str if bookings_str else "  无预订"}"""

def _format_available_places(available_places: list, field_info: dict, start_time: str, end_time: str) -> str:
    """格式化可用场地信息"""
    if not available_places:
        return f"时间段 {start_time} 到 {end_time} 内没有可用场地"
    
    places_str = "\n".join([f"  - {field_info['places'][pid]} (ID: {pid})" for pid in available_places])
    
    return f"""时间段 {start_time} 到 {end_time} 的可用场地:

{places_str}

共 {len(available_places)} 个场地可用"""

@mcp.tool()
async def booking_get_field_info(field: str, start_time: str, end_time: str) -> str:
    """获取场地信息和预订情况
    
    Args:
        field: 场地类型 (如 'badminton')
        start_time: 开始时间 (格式: YYYY-MM-DD HH:MM)
        end_time: 结束时间 (格式: YYYY-MM-DD HH:MM)
    """
    logger.info(f"Tool 'booking_get_field_info' called with params: field={field}, start_time={start_time}, end_time={end_time}")
    cache_key = f"field_info_{field}_{start_time}_{end_time}"
    
    def fetch_field_info():
        booking = _get_booking_instance()
        field_info = booking.get_field_info(field, start_time, end_time)
        return _format_field_info(field_info)
    
    return await asyncio.get_event_loop().run_in_executor(
        None, lambda: _get_cached_or_fetch(cache_key, fetch_field_info, ttl=600)  # 10分钟缓存
    )

@mcp.tool()
async def booking_get_available_places(field: str, query_start_time: str, query_end_time: str, 
                                     check_start_time: str, check_end_time: str) -> str:
    """查询指定时间段的可用场地
    
    Args:
        field: 场地类型 (如 'badminton')
        query_start_time: 查询数据的开始时间 (格式: YYYY-MM-DD HH:MM)
        query_end_time: 查询数据的结束时间 (格式: YYYY-MM-DD HH:MM)
        check_start_time: 检查可用性的开始时间 (格式: YYYY-MM-DD HH:MM)
        check_end_time: 检查可用性的结束时间 (格式: YYYY-MM-DD HH:MM)
    """
    logger.info(f"Tool 'booking_get_available_places' called with params: field={field}, query_time={query_start_time}-{query_end_time}, check_time={check_start_time}-{check_end_time}")
    cache_key = f"available_{field}_{query_start_time}_{query_end_time}_{check_start_time}_{check_end_time}"
    
    def fetch_available_places():
        booking = _get_booking_instance()
        field_info = booking.get_field_info(field, query_start_time, query_end_time)
        if not field_info:
            return f"Error: 场地类型 '{field}' 不存在"
        
        available_places = booking.get_available_places(field_info, check_start_time, check_end_time)
        return _format_available_places(available_places, field_info, check_start_time, check_end_time)
    
    return await asyncio.get_event_loop().run_in_executor(
        None, lambda: _get_cached_or_fetch(cache_key, fetch_available_places, ttl=300)  # 5分钟缓存
    )

@mcp.tool()
async def booking_book(field_id: str, place_id: str, start_time: str, end_time: str, 
                      telephone: str, reason: str, details: str) -> str:
    """预订场地
    
    Args:
        field_id: 场地ID (如 '1097')
        place_id: 场所ID
        start_time: 开始时间 (格式: YYYY-MM-DD HH:MM)
        end_time: 结束时间 (格式: YYYY-MM-DD HH:MM)
        telephone: 联系电话
        reason: 预订原因
        details: 详细说明
    """
    logger.info(f"Tool 'booking_book' called with params: field_id={field_id}, place_id={place_id}, time={start_time}-{end_time}")
    
    def perform_booking():
        booking = _get_booking_instance()
        try:
            success = booking.book(field_id, place_id, start_time, end_time, telephone, reason, details)
            if success:
                return f"""预订成功！

场地ID: {field_id}
场所ID: {place_id}
时间: {start_time} 到 {end_time}
联系电话: {telephone}
预订原因: {reason}
详细说明: {details}

请按时到场并遵守场馆规定。"""
            else:
                return "预订失败：未知错误"
        except Exception as e:
            return f"预订失败：{str(e)}"
    
    # 预订操作不使用缓存，每次都执行
    return await asyncio.get_event_loop().run_in_executor(None, perform_booking)

# @mcp.tool()
# async def booking_clear_cache() -> str:
#     """清除缓存"""
#     logger.info("Tool 'booking_clear_cache' called.")
#     global _global_cache
#     _global_cache.clear()
#     logger.info("Global cache has been cleared.")
#     return "Cache cleared successfully"

# @mcp.tool()
# async def booking_force_relogin() -> str:
#     """强制重新登录"""
#     logger.info("Tool 'booking_force_relogin' called.")
#     global _booking_instance, _last_login_time
#     _booking_instance = None
#     _last_login_time = 0
    
#     try:
#         _get_booking_instance()
#         return "Force relogin successful"
#     except Exception as e:
#         logger.error("Force relogin failed.", exc_info=True)
#         return f"Force relogin failed: {str(e)}"

# 交互式测试函数
def test():
    async def _test():
        print("请先设置环境变量 BOOKING_USERNAME 和 BOOKING_PASSWORD")
        # print("1. 查询场地信息\n2. 查询可用场地\n3. 预订场地\n4. 清除缓存\n5. 强制重新登录")
        print("1. 查询场地信息\n2. 查询可用场地\n3. 预订场地")
        choice = input("请选择功能编号: ")
        
        if choice == "1":
            field = input("请输入场地类型（如 badminton）: ")
            start_time = input("请输入开始时间（如 2024-01-01 08:00）: ")
            end_time = input("请输入结束时间（如 2024-01-01 22:00）: ")
            result = await booking_get_field_info(field, start_time, end_time)
            print("\n场地信息查询结果:\n", result)
        elif choice == "2":
            field = input("请输入场地类型（如 badminton）: ")
            query_start = input("请输入查询开始时间（如 2024-01-01 08:00）: ")
            query_end = input("请输入查询结束时间（如 2024-01-01 22:00）: ")
            check_start = input("请输入检查开始时间（如 2024-01-01 14:00）: ")
            check_end = input("请输入检查结束时间（如 2024-01-01 15:00）: ")
            result = await booking_get_available_places(field, query_start, query_end, check_start, check_end)
            print("\n可用场地查询结果:\n", result)
        elif choice == "3":
            field_id = input("请输入场地ID（如 1097）: ")
            place_id = input("请输入场所ID: ")
            start_time = input("请输入开始时间（如 2024-01-01 14:00）: ")
            end_time = input("请输入结束时间（如 2024-01-01 15:00）: ")
            telephone = input("请输入联系电话: ")
            reason = input("请输入预订原因: ")
            details = input("请输入详细说明: ")
            result = await booking_book(field_id, place_id, start_time, end_time, telephone, reason, details)
            print("\n预订结果:\n", result)
        # elif choice == "4":
        #     result = await booking_clear_cache()
        #     print(result)
        # elif choice == "5":
        #     result = await booking_force_relogin()
        #     print(result)
        else:
            print("无效选择")
    
    asyncio.run(_test())

if __name__ == "__main__":
    test()
