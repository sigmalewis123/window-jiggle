import win32gui
import win32con
import time
import random

def window_callback(hwnd, windows):
    if win32gui.IsWindowVisible(hwnd):
        # Store both the window handle and its original position
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        if right - left >= 50 and bottom - top >= 50:  # Only store non-tiny windows
            windows.append((hwnd, (left, top, right, bottom)))
    return True

def jiggle_windows():
    try:
        # Get all visible windows and their original positions
        windows = []
        win32gui.EnumWindows(window_callback, windows)
        
        while True:
            # Move each window slightly
            for hwnd, original_pos in windows:
                try:
                    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                    width = right - left
                    height = bottom - top
                    
                    # Move window left or right by 5 pixels
                    offset = 5 if random.random() < 0.5 else -5
                    win32gui.SetWindowPos(hwnd, 
                                        win32con.HWND_TOP,
                                        left + offset, 
                                        top,
                                        width,
                                        height,
                                        win32con.SWP_NOSIZE)
                except:
                    continue
                    
            # Small delay before next movement
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nRestoring windows to original positions...")
        # Restore all windows to their original positions
        for hwnd, (left, top, right, bottom) in windows:
            try:
                win32gui.SetWindowPos(hwnd, 
                                    win32con.HWND_TOP,
                                    left, 
                                    top,
                                    right - left,
                                    bottom - top,
                                    win32con.SWP_NOSIZE)
            except:
                continue
        print("Window jiggling stopped!")

if __name__ == "__main__":
    print("Window jiggling started! Press Ctrl+C to stop.")
    jiggle_windows()
