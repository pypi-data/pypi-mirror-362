# -*- coding: utf-8 -*-
"""
"""

from functools import wraps


def register_error(error_type):
    def decorator(func):
        @wraps(func)
        def error_wrapper(self, *args, **kwargs):
            try:
                # print(type, args, kwargs)
                return func(self, *args, **kwargs)

            except Exception as e:
                class_name = self.__class__.__name__
                method_name = func.__name__

                print(f">> Exception: {class_name} -> {method_name}")
                print(e)

                self.status.method = f"{class_name}.{method_name}"
                self.status.error = True

                if hasattr(self, "status"):
                    # self.status.to_pickle()
                    self.status.to_json()
                else:
                    # self.to_pickle()
                    self.to_json()
                return None

        return error_wrapper
    return decorator
