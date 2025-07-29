from .execption import HuiBiaoException


class FolderResourceAlreadyExistException(HuiBiaoException):
    def __init__(self, path: str):
        super().__init__(f"Folder resource already exist: {path}!")
