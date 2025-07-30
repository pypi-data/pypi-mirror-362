import json
from typing import Dict

from huibiao_framework.resource.file_operator import SingleFileOperator


class JsonFileOperator(SingleFileOperator[Dict]):
    @classmethod
    def file_suffix(cls) -> str:
        return "json"

    @SingleFileOperator.ignore_if_path_not_exists
    def load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            self.set_data(json.load(f))

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.get_data(), f, ensure_ascii=False, indent=2)
