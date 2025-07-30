from . import serial

def set_gimbal_speed(pitch: float, yaw: float) -> None:
    """
    设置云台的速度。
    Args:
        pitch (float): 云台俯仰速度，范围[-450, 450] (°/s) 
        yaw (float):   云台偏航速度，范围[-450, 450] (°/s)
    Returns:
        None
    """
    serial.write_serial(f"gimbal speed p {pitch} y {yaw};")

def move_gimbal(pitch: float | None, yaw: float | None, vpitch: float | None, vyaw: float | None) -> None:
    """
    控制云台移动。
    Args:
        pitch (float):  云台俯仰角度，范围[-55, 55] (°)
        yaw (float):    云台偏航角度，范围[-55, 55] (°)
        vpitch (float): 云台俯仰速度，范围[0, 540] (°/s)
        vyaw (float):   云台偏航速度，范围[0, 540] (°/s)
    Raises:
        ValueError: 如果所有角度和速度参数都为 None 或 参数不在范围内。
    """

    if pitch and not (-55 <= pitch <= 55) or \
       yaw and not (-55 <= yaw <= 55) or \
       vpitch and not (0 <= vpitch <= 540) or \
       vyaw and not (0 <= vyaw <= 540):
        raise ValueError("参数不在范围内。")

    all_none = False
    command = "gimbal move "

    if pitch:
        all_none = True
        command += f"p {pitch} "
    if yaw:
        all_none = True
        command += f"y {yaw} "
    if vpitch:
        all_none = True
        command += f"vp {vpitch} "
    if vyaw:
        all_none = True
        command += f"vy {vyaw} "
    if all_none:
        raise ValueError("At least one of pitch, yaw, vpitch, or vyaw must be provided.")

    command += ";"
    serial.write_serial(command)

def move_gimbal_absolute(pitch: float | None, yaw: float | None, vpitch: int, vyaw: int) -> None:
    """
    控制云台绝对移动。
    Args:
        pitch (float):  云台俯仰角度，范围[-25, 30] (°)
        yaw (float):    云台偏航角度，范围[-250, 250] (°)
        vpitch (int):   云台俯仰速度，范围[0, 540] (°/s)
        vyaw (int):     云台偏航速度，范围[0, 540] (°/s)
    Raises:
        ValueError: 如果所有角度和速度参数都为 None 或 参数不在范围内。
    """

    if pitch and not (-25 <= pitch <= 30) or \
       yaw and not (-250 <= yaw <= 250) or \
       vpitch and not (0 <= vpitch <= 540) or \
       vyaw and not (0 <= vyaw <= 540):
        raise ValueError("参数不在范围内。")

    all_none = False
    command = "gimbal moveto "

    if pitch:
        all_none = True
        command += f"p {pitch} "
    if yaw:
        all_none = True
        command += f"y {yaw} "
    if vpitch:
        all_none = True
        command += f"vp {vpitch} "
    if vyaw:
        all_none = True
        command += f"vy {vyaw} "
    if all_none:
        raise ValueError("At least one of pitch, yaw, vpitch, or vyaw must be provided.")

    command += ";"
    serial.write_serial(command)    

def set_gimbal_suspend() -> None:
    """
    挂起云台。
    """
    serial.write_serial("gimbal suspend;")

def set_gimbal_resume() -> None:
    """
    恢复云台。
    """
    serial.write_serial("gimbal resume;")

def set_gimbal_recenter() -> None:
    """
    云台会中。
    """
    serial.write_serial("gimbal recenter;")
