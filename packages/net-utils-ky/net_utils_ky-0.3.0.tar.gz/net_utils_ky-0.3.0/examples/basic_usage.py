#!/usr/bin/env python3
"""
基本使用示例
"""

from net_utils_ky import NetworkUtils, AsyncNetworkUtils
import asyncio


def sync_example():
    """同步使用示例"""
    print("=== 同步使用示例 ===")
    
    # 创建网络工具实例
    net_utils = NetworkUtils()
    
    try:
        # 检查网络连接
        if net_utils.is_connected():
            print("✅ 网络连接正常")
        else:
            print("❌ 网络连接失败")
            return
        
        # 检查DNS解析
        if net_utils.dns_works():
            print("✅ DNS解析正常")
        else:
            print("❌ DNS解析失败")
        
        # 测试延迟
        latency = net_utils.get_latency()
        if latency:
            print(f"✅ 网络延迟: {latency:.2f}ms")
        else:
            print("❌ 无法测试延迟")
        
        # 发送HTTP请求
        try:
            response = net_utils.get("https://httpbin.org/get")
            print(f"✅ HTTP请求成功，状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ HTTP请求失败: {e}")
        
        # 扫描端口
        open_ports = net_utils.scan_ports("localhost", [80, 443, 8080])
        if open_ports:
            print(f"✅ 开放的端口: {open_ports}")
        else:
            print("❌ 没有发现开放的端口")
    
    finally:
        net_utils.close()


async def async_example():
    """异步使用示例"""
    print("\n=== 异步使用示例 ===")
    
    async with AsyncNetworkUtils() as async_utils:
        # 检查网络连接
        if await async_utils.is_connected():
            print("✅ 异步网络连接正常")
        else:
            print("❌ 异步网络连接失败")
            return
        
        # 发送异步HTTP请求
        try:
            response = await async_utils.get("https://httpbin.org/get")
            print(f"✅ 异步HTTP请求成功，状态码: {response.status}")
        except Exception as e:
            print(f"❌ 异步HTTP请求失败: {e}")
        
        # 并发请求
        urls = [
            "https://httpbin.org/get",
            "https://httpbin.org/status/200",
            "https://httpbin.org/status/404"
        ]
        
        try:
            responses = await async_utils.get_all(urls)
            print(f"✅ 并发请求完成，响应数量: {len(responses)}")
            
            for i, response in enumerate(responses):
                if hasattr(response, 'status'):
                    print(f"  URL {i+1}: 状态码 {response.status}")
                else:
                    print(f"  URL {i+1}: 请求失败")
        except Exception as e:
            print(f"❌ 并发请求失败: {e}")


def main():
    """主函数"""
    print("🚀 Net Utils KY - 基本使用示例")
    print("=" * 50)
    
    # 运行同步示例
    sync_example()
    
    # 运行异步示例
    asyncio.run(async_example())
    
    print("\n✅ 示例运行完成")


if __name__ == "__main__":
    main() 