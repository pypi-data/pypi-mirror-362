#!/usr/bin/env python3
"""
K线数据验证工具
用于检查和修复K线数据格式问题
"""

def validate_kline_data(data, verbose=True):
    """
    验证K线数据格式

    Args:
        data: K线数据列表
        verbose: 是否显示详细信息

    Returns:
        bool: 数据是否有效
    """
    if not isinstance(data, list):
        if verbose:
            print("❌ 数据必须是列表格式")
        return False

    if len(data) == 0:
        if verbose:
            print("✅ 空数据列表（有效）")
        return True

    errors = []

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            errors.append(f"第 {i+1} 项不是字典格式")
            continue

        # 检查必需字段
        required_fields = ['timestamp', 'open', 'high', 'low', 'close']
        missing_fields = [field for field in required_fields if field not in item]
        if missing_fields:
            errors.append(f"第 {i+1} 项缺少字段: {missing_fields}")
            continue

        # 检查数据类型
        try:
            timestamp = float(item['timestamp'])
            open_price = float(item['open'])
            high_price = float(item['high'])
            low_price = float(item['low'])
            close_price = float(item['close'])

            if 'volume' in item:
                volume = float(item['volume'])
                if volume < 0:
                    errors.append(f"第 {i+1} 项成交量不能为负数: {volume}")

        except (ValueError, TypeError) as e:
            errors.append(f"第 {i+1} 项数据类型错误: {e}")
            continue

        # 检查价格关系
        if not (high_price >= low_price):
            errors.append(f"第 {i+1} 项: 最高价 ({high_price}) 必须 >= 最低价 ({low_price})")

        if not (low_price <= open_price <= high_price):
            errors.append(f"第 {i+1} 项: 开盘价 ({open_price}) 必须在 [{low_price}, {high_price}] 范围内")

        if not (low_price <= close_price <= high_price):
            errors.append(f"第 {i+1} 项: 收盘价 ({close_price}) 必须在 [{low_price}, {high_price}] 范围内")

        # 检查时间戳
        if timestamp <= 0:
            errors.append(f"第 {i+1} 项: 时间戳必须为正数")

    if verbose:
        if errors:
            print(f"❌ 发现 {len(errors)} 个错误:")
            for error in errors:
                print(f"   - {error}")
        else:
            print(f"✅ 数据验证通过，共 {len(data)} 条记录")

    return len(errors) == 0

def fix_kline_data(data):
    """
    修复K线数据格式问题

    Args:
        data: 原始K线数据列表

    Returns:
        list: 修复后的数据列表
    """
    if not isinstance(data, list):
        return []

    fixed_data = []

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            continue

        # 检查必需字段
        required_fields = ['timestamp', 'open', 'high', 'low', 'close']
        if not all(field in item for field in required_fields):
            continue

        try:
            # 转换数据类型
            timestamp = float(item['timestamp'])
            open_price = float(item['open'])
            high_price = float(item['high'])
            low_price = float(item['low'])
            close_price = float(item['close'])

            # 修复价格关系
            # 确保 high >= low
            if high_price < low_price:
                high_price, low_price = low_price, high_price

            # 确保 open 和 close 在 [low, high] 范围内
            open_price = max(low_price, min(high_price, open_price))
            close_price = max(low_price, min(high_price, close_price))

            # 重新调整 high 和 low 以确保包含 open 和 close
            high_price = max(high_price, open_price, close_price)
            low_price = min(low_price, open_price, close_price)

            # 处理成交量
            volume = 0
            if 'volume' in item:
                try:
                    volume = max(0, float(item['volume']))
                except (ValueError, TypeError):
                    volume = 0

            fixed_item = {
                'timestamp': int(timestamp),
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close_price, 2),
                'volume': int(volume)
            }

            fixed_data.append(fixed_item)

        except (ValueError, TypeError):
            # 跳过无法修复的数据
            continue

    return fixed_data

def generate_sample_data(count=10):
    """生成示例数据"""
    import random
    import time

    data = []
    base_time = int(time.time() * 1000)
    base_price = 100.0

    for i in range(count):
        timestamp = base_time + i * 86400 * 1000

        # 价格变化
        change = random.uniform(-2, 2)
        base_price += change

        # 生成开盘价和收盘价
        open_price = base_price + random.uniform(-1, 1)
        close_price = base_price + random.uniform(-1, 1)

        # 生成高低价（确保覆盖开盘和收盘价）
        high_price = max(open_price, close_price) + random.uniform(0, 1)
        low_price = min(open_price, close_price) - random.uniform(0, 1)

        data.append({
            'timestamp': timestamp,
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2),
            'volume': random.randint(1000, 10000)
        })

        base_price = close_price

    return data

if __name__ == "__main__":
    print("🔍 K线数据验证工具")
    print("=" * 50)

    # 测试1: 生成并验证示例数据
    print("\n📊 测试1: 生成示例数据")
    sample_data = generate_sample_data(5)
    print(f"生成了 {len(sample_data)} 条示例数据")
    validate_kline_data(sample_data)

    # 测试2: 测试错误数据
    print("\n📊 测试2: 测试错误数据")
    bad_data = [
        {
            'timestamp': 1640995200000,
            'open': 100,
            'high': 95,  # 错误：高价 < 低价
            'low': 105,
            'close': 103,
            'volume': 1000
        },
        {
            'timestamp': 1641081600000,
            'open': 110,  # 错误：开盘价超出高低价范围
            'high': 108,
            'low': 101,
            'close': 106,
            'volume': 1200
        }
    ]

    print("原始错误数据:")
    validate_kline_data(bad_data)

    # 测试3: 修复错误数据
    print("\n📊 测试3: 修复错误数据")
    fixed_data = fix_kline_data(bad_data)
    print("修复后的数据:")
    validate_kline_data(fixed_data)

    print("\n修复前后对比:")
    for i, (original, fixed) in enumerate(zip(bad_data, fixed_data)):
        print(f"第 {i+1} 条数据:")
        print(f"  原始: O={original['open']}, H={original['high']}, L={original['low']}, C={original['close']}")
        print(f"  修复: O={fixed['open']}, H={fixed['high']}, L={fixed['low']}, C={fixed['close']}")

    print("\n✅ 验证工具测试完成")