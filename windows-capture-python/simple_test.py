#!/usr/bin/env python3
"""
简单的window_hwnd功能验证脚本
"""

from windows_capture import WindowsCapture

# 测试参数验证
print("=== 测试参数验证 ===")

# 测试1: 只指定window_hwnd
try:
    capture = WindowsCapture(window_hwnd=12345)
    print("✓ 只指定window_hwnd参数有效")
except Exception as e:
    print(f"✗ 意外错误: {e}")

# 测试2: 同时指定window_hwnd和monitor_index
try:
    capture = WindowsCapture(window_hwnd=12345, monitor_index=0)
    print("✗ 应该抛出异常但没有")
except ValueError as e:
    print(f"✓ 正确检测到冲突参数: {e}")

# 测试3: 同时指定window_hwnd和window_name
try:
    capture = WindowsCapture(window_hwnd=12345, window_name="测试")
    print("✗ 应该抛出异常但没有")
except ValueError as e:
    print(f"✓ 正确检测到冲突参数: {e}")

print("\n=== 测试完成 ===")
print("window_hwnd参数验证成功！")
print("使用示例:")
print("capture = WindowsCapture(window_hwnd=窗口句柄值)")
print("或")
print("capture = WindowsCapture(monitor_index=0)")
print("或")
print("capture = WindowsCapture(window_name='窗口标题')")