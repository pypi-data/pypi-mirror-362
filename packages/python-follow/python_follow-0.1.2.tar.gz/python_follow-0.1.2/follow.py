import functools
import inspect
import sys
import threading
import time
from dataclasses import dataclass
from typing import Callable, Union


@dataclass
class FollowConfig:
    follow_threads: bool = True
    follow_for_loops: bool = True
    follow_while_loops: bool = True
    follow_variable_set: bool = True
    follow_function_calls: bool = False
    follow_return: bool = False
    follow_prints: bool = False


def apply_config(line: str, config: FollowConfig) -> bool:
    line = line.strip()
    if not config.follow_for_loops and line.startswith('for '):
        return False
    if not config.follow_while_loops and line.startswith('while '):
        return False
    if not config.follow_variable_set and '=' in line:
        return False
    if not config.follow_prints and line.startswith('print'):
        return False
    return True


def follow(
        config: Union[FollowConfig, None] = None,
        follower: Callable = print,
):
    if config is None:
        config = FollowConfig()

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            source_lines, starting_line = inspect.getsourcelines(func)
            source_map = {
                starting_line + i: line.strip('\n').strip()
                for i, line in enumerate(source_lines)
            }

            prev_time = [time.time()]
            prev_line = [None]

            def tracer(frame, event, _):
                if frame.f_code.co_name != func.__name__:
                    return tracer

                if event == 'line':
                    now = time.time()
                    line = source_map.get(frame.f_lineno, 'Unknown').strip()
                    local_vars = dict(frame.f_locals)

                    if not apply_config(line, config):
                        return tracer

                    if prev_line[0] is not None:
                        elapsed = (now - prev_time[0]) * 1000  # noqa

                        data = {
                            'function': func.__name__,
                            'instruction': prev_line[0],
                            'execution_time': elapsed,
                            'local_vars': [
                                {'var': var, 'val': val, 'type': type(val).__name__}
                                for var, val in local_vars.items()
                            ],
                        }  # noqa
                        follower(data)

                    prev_time[0] = now
                    prev_line[0] = line  # noqa

                return tracer

            sys.settrace(tracer)

            if config.follow_threads:
                wrap_thread_targets()

            try:
                result = func(*args, **kwargs)

                if prev_line[0] is not None:
                    elapsed = (time.time() - prev_time[0]) * 1000

                    data = {
                        'function': func.__name__,
                        'instruction': prev_line[0],
                        'execution_time': elapsed,
                        'local_vars': [],
                    }
                    follower(data)

            finally:
                sys.settrace(None)

            return result

        def wrap_thread_targets():
            original_init = threading.Thread.__init__

            def new_init(thread_self, *args, **kwargs):
                target = kwargs.get('target')
                if not target and len(args) >= 1:
                    # target can also be positional
                    target = args[0]

                    # Rewrap positional target
                    args = (decorator(target),) + args[1:]
                elif callable(target):
                    kwargs['target'] = decorator(target)

                original_init(thread_self, *args, **kwargs)

            threading.Thread.__init__ = new_init
        return wrapper
    return decorator