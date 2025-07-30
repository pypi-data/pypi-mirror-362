"""
TablestoreStore 使用示例

这个示例展示了如何使用基于阿里云 Tablestore 的 LangGraph checkpoint store。
"""

import asyncio
from tablestore import OTSClient

from tablestore_store import TablestoreStore, GetOp, PutOp, DeleteOp, SearchOp


def create_tablestore_client():
    """创建 Tablestore 客户端"""
    # 请替换为您的实际配置
    endpoint = "https://your-instance.cn-hangzhou.ots.aliyuncs.com"
    access_key_id = "your-access-key-id"
    access_key_secret = "your-access-key-secret"
    instance_name = "your-instance-name"
    
    client = OTSClient(endpoint, access_key_id, access_key_secret, instance_name)
    return client


def basic_usage_example():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 创建客户端和存储
    client = create_tablestore_client()
    store = TablestoreStore(client, table_name="test_store")
    
    # 基本的 get/put/delete 操作
    namespace = ("user", "123")
    key = "profile"
    value = {"name": "Alice", "age": 30, "city": "Shanghai"}
    
    # 存储数据
    store.mset([(namespace, key, value)])
    print(f"存储数据: {namespace}/{key} = {value}")
    
    # 获取数据
    result = store.mget([(namespace, key)])
    print(f"获取数据: {result[0]}")
    
    # 删除数据
    store.mdelete([(namespace, key)])
    print("数据已删除")
    
    # 验证删除
    result = store.mget([(namespace, key)])
    print(f"删除后获取: {result[0]}")


def batch_operations_example():
    """批量操作示例"""
    print("\n=== 批量操作示例 ===")
    
    client = create_tablestore_client()
    store = TablestoreStore(client, table_name="test_store")
    
    # 准备批量操作
    operations = [
        PutOp(("user", "001"), "profile", {"name": "Alice", "age": 25}),
        PutOp(("user", "002"), "profile", {"name": "Bob", "age": 30}),
        PutOp(("user", "003"), "profile", {"name": "Charlie", "age": 35}),
        PutOp(("user", "001"), "settings", {"theme": "dark", "language": "zh"}),
        PutOp(("user", "002"), "settings", {"theme": "light", "language": "en"}),
    ]
    
    # 执行批量操作
    results = store.batch(operations)
    print(f"批量存储完成，结果: {results}")
    
    # 批量获取
    get_operations = [
        GetOp(("user", "001"), "profile"),
        GetOp(("user", "002"), "profile"),
        GetOp(("user", "003"), "profile"),
        GetOp(("user", "001"), "settings"),
        GetOp(("user", "002"), "settings"),
    ]
    
    results = store.batch(get_operations)
    print("批量获取结果:")
    for i, result in enumerate(results):
        op = get_operations[i]
        print(f"  {op.namespace}/{op.key}: {result}")


def search_operations_example():
    """搜索操作示例"""
    print("\n=== 搜索操作示例 ===")
    
    client = create_tablestore_client()
    store = TablestoreStore(client, table_name="test_store")
    
    # 先存储一些测试数据
    test_data = [
        PutOp(("products", "electronics"), "laptop", {"brand": "Apple", "price": 1299, "category": "electronics"}),
        PutOp(("products", "electronics"), "phone", {"brand": "Samsung", "price": 899, "category": "electronics"}),
        PutOp(("products", "books"), "novel", {"title": "1984", "author": "Orwell", "category": "books"}),
        PutOp(("products", "books"), "textbook", {"title": "Python Guide", "author": "Smith", "category": "books"}),
    ]
    
    store.batch(test_data)
    print("测试数据已存储")
    
    # 搜索所有产品
    search_op = SearchOp(("products",), limit=10)
    results = store.batch([search_op])
    print(f"搜索所有产品: {results[0]}")
    
    # 搜索电子产品
    search_op = SearchOp(("products", "electronics"), limit=10)
    results = store.batch([search_op])
    print(f"搜索电子产品: {results[0]}")
    
    # 搜索书籍
    search_op = SearchOp(("products", "books"), limit=10)
    results = store.batch([search_op])
    print(f"搜索书籍: {results[0]}")


async def async_operations_example():
    """异步操作示例"""
    print("\n=== 异步操作示例 ===")
    
    client = create_tablestore_client()
    store = TablestoreStore(client, table_name="test_store")
    
    # 异步批量操作
    operations = [
        PutOp(("async", "test1"), "data", {"value": 1, "timestamp": "2024-01-01"}),
        PutOp(("async", "test2"), "data", {"value": 2, "timestamp": "2024-01-02"}),
        PutOp(("async", "test3"), "data", {"value": 3, "timestamp": "2024-01-03"}),
    ]
    
    # 异步执行
    results = await store.abatch(operations)
    print(f"异步批量存储完成: {results}")
    
    # 异步获取
    get_operations = [
        GetOp(("async", "test1"), "data"),
        GetOp(("async", "test2"), "data"),
        GetOp(("async", "test3"), "data"),
    ]
    
    results = await store.abatch(get_operations)
    print("异步批量获取结果:")
    for i, result in enumerate(results):
        op = get_operations[i]
        print(f"  {op.namespace}/{op.key}: {result}")


def yield_keys_example():
    """遍历键的示例"""
    print("\n=== 遍历键示例 ===")
    
    client = create_tablestore_client()
    store = TablestoreStore(client, table_name="test_store")
    
    # 遍历所有用户相关的键
    print("用户相关的键:")
    for namespace, key in store.yield_keys(("user",)):
        print(f"  {namespace}/{key}")
    
    # 遍历所有产品相关的键
    print("产品相关的键:")
    for namespace, key in store.yield_keys(("products",)):
        print(f"  {namespace}/{key}")
    
    # 遍历所有键
    print("所有键:")
    for namespace, key in store.yield_keys(()):
        print(f"  {namespace}/{key}")


def cleanup_example():
    """清理示例"""
    print("\n=== 清理示例 ===")
    
    client = create_tablestore_client()
    store = TablestoreStore(client, table_name="test_store")
    
    # 收集所有需要删除的键
    keys_to_delete = []
    for namespace, key in store.yield_keys(()):
        keys_to_delete.append((namespace, key))
    
    if keys_to_delete:
        print(f"准备删除 {len(keys_to_delete)} 个键")
        
        # 批量删除
        delete_ops = [DeleteOp(namespace, key) for namespace, key in keys_to_delete]
        results = store.batch(delete_ops)
        print(f"删除完成: {results}")
    else:
        print("没有需要删除的键")


if __name__ == "__main__":
    try:
        # 基本使用示例
        basic_usage_example()
        
        # 批量操作示例
        batch_operations_example()
        
        # 搜索操作示例
        search_operations_example()
        
        # 异步操作示例
        asyncio.run(async_operations_example())
        
        # 遍历键示例
        yield_keys_example()
        
        # 清理示例
        cleanup_example()
        
    except Exception as e:
        print(f"运行示例时出错: {e}")
        print("请确保:")
        print("1. 已正确配置阿里云 Tablestore 连接信息")
        print("2. 已安装必要的依赖包: pip install ots2 orjson")
        print("3. 具有相应的访问权限")