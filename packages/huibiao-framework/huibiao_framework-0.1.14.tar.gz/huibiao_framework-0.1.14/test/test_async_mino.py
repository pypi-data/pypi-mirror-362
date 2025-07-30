from huibiao_framework.resource import TaskResource
from huibiao_framework.resource.extend import FaissIndexFileOperator, JsonFileOperator
from huibiao_framework.resource.file_operator import BatchFileOperator
from huibiao_framework.task import TaskResourceSyncMinio
from huibiao_framework.task.task import HuibiaoTask
from pathlib import Path

class MyTaskResource(TaskResource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title_faiss_index: FaissIndexFileOperator = self.genSingleFileOperator("title_faiss.index", FaissIndexFileOperator, 0.2)
        self.pdf_parse_json: JsonFileOperator = self.genSingleFileOperator("pdf_parse.json", JsonFileOperator, 0.4)
        self.page_json: BatchFileOperator = self.genBatchFileOperator("page_json", JsonFileOperator, 0.2)
        self.test_json: JsonFileOperator = self.genSingleFileOperator("test.json", JsonFileOperator, 0.2)


class MyTask(HuibiaoTask[MyTaskResource]):

    TASK_TYPE = "file_parse"

    def __init__(self, task_id: str):
        super().__init__(task_type=self.TASK_TYPE, project_id=task_id, task_resource_cls=MyTaskResource)

    async def pipeline(self):
        # ..... 更多步骤
        pass


    @HuibiaoTask.StepAnnotation("步骤一", output="page_json")
    async def step1(self):
        self.task_resource.page_json.append({"page_num": 2, "text": "hello world"})
        print(self.task_resource.page_json[0].data)



if __name__ == "__main__":
    task_id = "task001"
    my_task = MyTask(task_id)
    sync_mino: TaskResourceSyncMinio = my_task.genSyncMinioClient()
    sync_mino
    filepath = sync_mino._task_resource.resource_dict["pdf_parse.json"].path()
    batchpath = sync_mino._task_resource.resource_dict["page_json"].folder
    base_dir = sync_mino._task_resource.task_dir
    print(Path(filepath).relative_to(Path(base_dir)))
    print(filepath.replace(base_dir, ""))
    print(Path(batchpath).relative_to(Path(base_dir)))
    print(batchpath.replace(base_dir, ""))



