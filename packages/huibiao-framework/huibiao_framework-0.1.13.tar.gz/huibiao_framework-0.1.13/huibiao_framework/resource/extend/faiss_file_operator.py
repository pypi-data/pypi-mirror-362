import faiss

from huibiao_framework.resource.file_operator import SingleFileOperator


class FaissIndexFileOperator(SingleFileOperator[faiss.Index]):
    @classmethod
    def file_suffix(cls) -> str:
        return "index"

    @SingleFileOperator.ignore_if_path_not_exists
    def load(self):
        self.set_data(faiss.read_index(self.path))

    def save(self):
        faiss.write_index(self.data, self.path)
