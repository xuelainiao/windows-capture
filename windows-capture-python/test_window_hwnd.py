#!/usr/bin/env python3
"""
测试window_hwnd参数的示例脚本

这个脚本演示了如何使用window_hwnd参数来捕获特定窗口
"""

import ctypes
import time
from windows_capture import WindowsCapture, Frame, InternalCaptureControl


def find_window_by_title(title):
    """
    通过窗口标题获取窗口句柄(HWND)
    
    参数:
        title: 窗口标题的部分或完整匹配
    
    返回:
        窗口句柄(HWND)或None
    """
    user32 = ctypes.windll.user32
    
    def enum_windows_proc(hwnd, lParam):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buffer = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buffer, length + 1)
            if title.lower() in buffer.value.lower():
                found_windows.append(hwnd)
        return True
    
    found_windows = []
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    user32.EnumWindows(WNDENUMPROC(enum_windows_proc), 0)
    
    return found_windows[0] if found_windows else None


def test_window_capture():
    """测试使用window_hwnd参数捕获窗口"""
    
    # 查找一个窗口，这里以"记事本"为例
    hwnd = find_window_by_title("记事本")
    
    if hwnd is None:
        print("未找到记事本窗口，请确保记事本已打开")
        print("尝试查找其他窗口...")
        
        # 尝试查找其他常见窗口
        common_titles = ["Chrome", "Edge", "文件资源管理器", "此电脑", "计算器"]
        for title in common_titles:
            hwnd = find_window_by_title(title)
            if hwnd:
                print(f"找到窗口: {title}, HWND: {hwnd}")
                break
    
    if hwnd is None:
        print("未找到合适的窗口进行测试")
        print("请手动打开一个窗口（如记事本、浏览器等）并重新运行脚本")
        return
    
    print(f"使用窗口句柄: {hwnd} 进行捕获")
    
    # 创建捕获实例，使用window_hwnd参数
    capture = WindowsCapture(
        cursor_capture=True,
        draw_border=True,
        window_hwnd=hwnd,  # 使用窗口句柄
    )
    
    frame_count = 0
    max_frames = 5
    
    @capture.event
    def on_frame_arrived(frame: Frame, capture_control: InternalCaptureControl):
        nonlocal frame_count
        frame_count += 1
        
        print(f"收到第 {frame_count} 帧")
        print(f"帧尺寸: {frame.width}x{frame.height}")
        
        # 保存前几张截图
        if frame_count <= max_frames:
            filename = f"window_capture_{frame_count}.png"
            frame.save_as_image(filename)
            print(f"已保存截图: {filename}")
        
        # 捕获足够的帧后停止
        if frame_count >= max_frames:
            capture_control.stop()
    
    @capture.event
    def on_closed():
        print("捕获会话已关闭")
    
    print("开始捕获窗口...")
    try:
        capture.start()
        print("捕获完成")
    except Exception as e:
        print(f"捕获失败: {e}")


def test_monitor_vs_window():
    """测试monitor_index和window_hwnd的互斥性"""
    
    print("\n=== 测试参数验证 ===")
    
    # 测试1: 同时指定window_hwnd和monitor_index
    try:
        capture = WindowsCapture(
            window_hwnd=12345,
            monitor_index=0
        )
        print("错误: 应该抛出异常但没有")
    except ValueError as e:
        print(f"✓ 正确检测到冲突参数: {e}")
    
    # 测试2: 同时指定window_hwnd和window_name
    try:
        capture = WindowsCapture(
            window_hwnd=12345,
            window_name="测试窗口"
        )
        print("错误: 应该抛出异常但没有")
    except ValueError as e:
        print(f"✓ 正确检测到冲突参数: {e}")
    
    # 测试3: 只指定window_hwnd
    try:
        capture = WindowsCapture(
            window_hwnd=12345
        )
        print("✓ 只指定window_hwnd参数有效")
    except Exception as e:
        print(f"✗ 意外错误: {e}")


if __name__ == "__main__":
    print("=== Windows Capture Window HWND 测试 ===")
    
    # 测试参数验证
    test_monitor_vs_window()
    
    # 测试实际捕获
    print("\n=== 开始实际捕获测试 ===")
    test_window_capture()
    
    print("\n=== 测试完成 ===")