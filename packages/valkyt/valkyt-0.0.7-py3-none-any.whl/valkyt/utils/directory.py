import os


class Dir:

    @staticmethod
    def create_dir(paths: str, create: bool = True) -> str:
        try: 
            if create: os.makedirs(paths)
        except Exception as err: ...
        finally: return paths
        ...

    @staticmethod
    def basedir(path: str) -> str:
        return os.path.dirname(path)
        ...