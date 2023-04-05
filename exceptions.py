from service.models import engine


class Exceptions:
    __slots__ = []

    @staticmethod
    def get_exception(e):
        exception = f"Cannot get it because {e}"
        try:
            engine.connect().close()
            return exception
        finally:
            return exception

    @staticmethod
    def delete_exception(e):
        exception = f"Position was not deleted because {e}"
        try:
            engine.connect().close()
            return exception
        finally:
            return exception

    @staticmethod
    def patch_exception(e):
        exception = f"Wasn't patched because {e}"
        try:
            engine.connect().close()
            return exception
        finally:
            return exception

    @staticmethod
    def post_exception(e):
        exception = f"Wasn't posted because {e}"
        try:
            engine.connect().close()
            return exception
        finally:
            return exception

