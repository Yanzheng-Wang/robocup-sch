from typing import overload

import CppPackage


@overload
def buffered_condition(condition: "bool", buffer_frame: int, max_count: int = 9999)->bool:...
@overload
def buffered_condition(condition: "bool", buffer_size: str, max_count: int = 9999)->bool:...

def buffered_condition(condition: "bool", buffer: int|str, max_count: int = 9999)->bool:
    """
    Args:
        在新一轮检测周期（cycle）开始时，初始化一个新的计数任务。
    :param condition: 当前条件（如传感器/行为条件）
    :param buffer: 缓冲帧数（条件需连续成立多少帧才算成立）
    :param max_count: 计数帧数（最大检测帧数，超时阈值）
    :return: 条件是否满足
    """
    if buffer is str:
        match buffer:
            case "normal":
                buffer_frame = 6
            case "slow":
                buffer_frame = 10
            case "fast":
                buffer_frame = 1
            case _:
                raise ValueError(f"Unknown buffer size: {buffer}")
    elif isinstance(buffer, int):
        buffer_frame = buffer
    else:
        raise TypeError(f"buffer must be int or str, got {type(buffer)}")

    if CppPackage.isTimeOut(condition, buffer_frame, max_count):
        return True
    else:
        return False