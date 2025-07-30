from datasets import load_dataset

from minieval.datatypes import Instance, LMOutput, Task, TaskConfig
from minieval.extract import qa


class ARC(Task):
    hf_path = "ai2_arc"

    def __init__(self, dataset_name):
        if type(self) is ARC:
            raise TypeError("ARC is an abstract class. Please use a child!")

        self.dataset_name = dataset_name
        self._requests = None

    @property
    def requests(self):
        if self._requests is None:
            requests = []
            for subset in ["train", "validation", "test"]:
                dataset = load_dataset(path=self.hf_path, split=subset, name=self.dataset_name)
                requests += list(map(self._process_instance, dataset))
            self._requests = requests
        return self._requests

    def _process_instance(self, doc):
        if doc["answerKey"].isdigit():
            doc["answerKey"] = chr(ord("A") + int(doc["answerKey"]) - 1)

        gold_idx = ["A", "B", "C", "D", "E"].index(doc["answerKey"])
        choices = doc["choices"]["text"]

        return Instance(
            question=doc["question"],
            gold_completion=choices[gold_idx],
            choices=choices,
            solution=gold_idx,
            metadata={"id": doc["id"]},
        )

    @classmethod
    def extract_answer(cls, generation: LMOutput) -> int:
        answer = qa.extract_mcqa_answer(
            generation.text, answer_regexes=["\\(?([A-D])\\)?"]  # both "(A)" and "A"
        )
        if answer in ["A", "B", "C", "D"]:
            return ["A", "B", "C", "D"].index(answer)
        return None


class ARCChallenge(ARC):
    def __init__(self, config: TaskConfig):
        self.config = config
        super().__init__(dataset_name="ARC-Challenge")


class ARCEasy(ARC):
    def __init__(self, config: TaskConfig):
        self.config = config
        super().__init__(dataset_name="ARC-Easy")
