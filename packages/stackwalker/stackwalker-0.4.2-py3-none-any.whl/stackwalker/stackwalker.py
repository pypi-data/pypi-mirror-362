"""
Core utilities for bidirectional frame inspection and debugging.

This module provides low-level utilities for inspecting Python's call stack with
support for both forward and backward navigation. It enables automatic detection
of caller context for logging, debugging, and code generation purposes.

The frame inspection utilities allow you to walk in both directions through the
call stack to identify calling functions, their line numbers, and other execution
context information. This is particularly useful for creating debugging tools
and logging systems that need to show meaningful caller information.

Features:
    - Bidirectional frame navigation (backwards to callers, forwards to callees)
    - Complete call stack collection and analysis
    - Safe frame inspection with graceful error handling
    - Function name and line number extraction utilities

Public functions:


Example:
    Basic frame inspection:

        def caller_function():          # Frame -2 (index 2 from root)
            target_function()

        def target_function():          # Frame -1 (index 1 from root)
            # Get different frames using index
            current = _get_frame(0)     # target_function
            caller = _get_frame(-1)     # caller_function
            root = _get_frame(-2)       # __main__

            # Forward navigation (from root)
            root_alt = _get_frame(1)    # __main__ (deepest caller)
            caller_alt = _get_frame(2)  # caller_function (second frame)

    Complete call stack analysis:

        def level1():
            level2()

        def level2():
            level3()

        def level3():
            frames = _collect_frame_stack()
            for i, frame in enumerate(frames):
                name = _get_frame_name(frame)
                line = _get_frame_line(frame)
                print(f"Frame {i}: {name}:{line}")

    Output:
        Frame 0: level3:45
        Frame 1: level2:42
        Frame 2: level1:39
        Frame 3: __main__:50

Frame index Reference:
    Negative index (backward navigation):
        -1: immediate caller
        -2: caller's caller
        -3: caller's caller's caller

    Positive index (forward navigation from root):
        +1: deepest caller (root of call stack)
        +2: second frame from root
        +3: third frame from root

    Zero index:
        0: current frame

Notes:
    - Frame index use collected stack for efficient bidirectional navigation
    - Functions gracefully handle missing frames by returning safe defaults
    - Primarily used by logging and debugging utilities in this package
    - Uses inspect.currentframe() which may not be available in all Python implementations
    - Forward navigation is implemented by collecting the full stack and indexing from the end
"""
import inspect
from typing import Any
from types import FrameType


def _collect_frame_stack() -> list[FrameType]:
    """Collect all frames in the current call stack.

    Returns:
        list: List of frames from current (index 0) to root caller
    """
    frames = []
    frame = inspect.currentframe()
    while frame:
        frames.append(frame)
        frame = frame.f_back
    return frames


def _get_frame(frame_index: int = -2) -> FrameType | None:
    """Get frame with bidirectional navigation using collected stack.

    Args:
        frame_index (int): index from current frame
            -  0: _collect_frame_stack
            - -1: _get_frame
            - -2: caller of _get_frame
            - -3: next caller in stack
            - +1: stacks before stackwalker
            - +2: ...
    """
    frames = _collect_frame_stack()

    if not frames:
        return None

    if frame_index == 0:
        return frames[0]  # _collect_frame_stack is the index 0

    if frame_index < 0:
        # Negative = go backwards (normal behavior)
        index = abs(frame_index)
        return frames[index] if index < len(frames) else None

    if frame_index > 0:
        # Positive = go from the end (root caller direction)
        index = len(frames) - frame_index
        return frames[index] if index >= 0 else None

    return None


def _get_frame_name(frame: FrameType) -> str:
    """Get function name from a frame object."""
    return frame.f_code.co_name if frame else "Unknown"


def _get_frame_line(frame: FrameType) -> int:
    """Get line number from a frame object."""
    return frame.f_lineno if frame else 0


def _get_module_name(frame: FrameType) -> str:
    """Get module name from a frame object.

    Args:
        frame (FrameType): Frame object to extract module name from.

    Returns:
        str: Module name or "Unknown" if not available.
    """
    return frame.f_globals.get("__name__", "Unknown") if frame else "Unknown"


def _find_frame_by_name(name: str, module_name: str, offset: int = 0) -> FrameType | None:
    """Find a frame by its function name.

    NOTE: method names in stack are not unique, so this will return the first match.

    Args:
        name (str): Function name to search for in the call stack.
        offset (int): If frame is found, return the frame at this offset from the found frame.

    Returns:
        FrameType: Frame object if found, None otherwise.
    """
    if not name:
        raise ValueError("Function name must be provided")
    if not module_name:
        raise ValueError("Module name must be provided")

    frames = _collect_frame_stack()
    for frame in frames:
        # print(_get_frame_name(frame), _get_module_name(frame))
        if _get_frame_name(frame) == name and _get_module_name(frame) == module_name:
            index = frames.index(frame) + offset
            return frames[index] if 0 <= index < len(frames) else None
    return None


def get_frame_by_name(caller_name: str, module_name: str, offset: int = 1) -> dict[str, Any]:
    """Get frame information by function name and module name.

    Args:
        name (str): Function name to search for.
        module_name (str): Module name where the function is defined.
        offset (int): Offset from the found frame to return.

    Returns:
        dict: Frame information including frame object, caller name, line number, and module name.
    """
    frame = _find_frame_by_name(caller_name, module_name, offset)
    if not frame:
        return {
            "frame": None,
            "caller_name": "Unknown",
            "caller_line": 0,
            "module_name": "Unknown"
        }
    return {
        "frame": frame,
        "caller_name": _get_frame_name(frame),
        "caller_line": _get_frame_line(frame),
        "module_name": _get_module_name(frame)
    }


def get_frame_by_index(index: int = -4) -> dict[str, Any]:
    """Get frame name and line number from a frame object.

    If index is None, returns frame info of caller of this method.

    Args:
        index (int): index of frame stack or None

    Returns:
        tuple: (function name, line number)
    """
    frame = _get_frame(index)

    if not frame:
        return {
            "frame": None,
            "caller_name": "Unknown",
            "caller_line": 0,
            "module_name": "Unknown"
        }

    return {
        "frame": frame,
        "caller_name": _get_frame_name(frame),
        "caller_line": _get_frame_line(frame),
        "module_name": _get_module_name(frame)
    }


def get_frame_list() -> list[dict[str, Any]]:
    """Get a list of frame information for the current call stack.

    Returns:
        list: List of dictionaries containing frame info for each frame in the stack.
    """
    frames = _collect_frame_stack()
    frame_list = []
    for frame in frames:
        frame_info = {
            "frame": frame,
            "caller_name": _get_frame_name(frame),
            "caller_line": _get_frame_line(frame),
            "module_name": _get_module_name(frame)
        }
        frame_list.append(frame_info)
    return frame_list


def get_frame_name_list() -> list[tuple[str, str]]:
    """Get a list of function names from the current call stack.

    Returns:
        list: List of function names for each frame in the stack.
    """
    return [(_get_module_name(frame), _get_frame_name(frame)) for frame in _collect_frame_stack()]


if __name__ == "__main__":
    def test1(index):
        """Building frames for testing"""
        test2(index)

    def test2(index):
        """Building frames for testing"""
        __frame = _get_frame(index)
        if not __frame:
            print(f"No frame found for index: {index}")
            return
        __frame_name = _get_frame_name(__frame)
        __frame_line = _get_frame_line(__frame)
        __module_name = _get_module_name(__frame)
        print(
            f"index: {index}, Name: {__module_name}.{__frame_name}, Line: {__frame_line}")

    def test3():
        """Testing frame retrieval by name"""
        for __frame in get_frame_name_list():
            print(f"Frame found: {__frame}")
        __frame3 = get_frame_by_name("test3", "__main__")
        print(f"Frame by name: {__frame3}")

    # Test different indexes
    # print("=== Frame Navigation Test ===")
    # test1(0)   # Index: 0, Name: __main__._collect_frame_stack, Line: 96
    # test1(-1)  # Index: -1, Name: __main__._get_frame, Line: 121
    # test1(-2)  # Index: -2, Name: __main__.test2, Line: 27
    # test1(-3)  # Index: -3, Name: __main__.test1, Line: 266
    # test1(1)   # Index: 1, Name: __main__.<module>, Line: 284
    # test1(2)   # Index: 2, Name: __main__.test1, Line: 266

    # Test frame retrieval by name
    # print("\n=== Frame Retrieval by Name Test ===")
    # test3()
