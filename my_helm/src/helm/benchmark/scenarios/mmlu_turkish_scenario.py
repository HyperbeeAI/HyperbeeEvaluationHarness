from typing import Dict, List

from helm.common.hierarchical_logger import hlog
from .scenario import Scenario, Instance, Reference, TRAIN_SPLIT, TEST_SPLIT, CORRECT_TAG, Input, Output
from datasets import load_dataset
import os
class MMLUTScenario(Scenario):
    name = "mmlut"
    description = "Massive Multitask Language Understanding Turkish"
    tags = ["knowledge", "multiple_choice"]

    def __init__(self, subject: str):
        super().__init__()
        self.subject: str = subject


    def process_split(self, data, split: str) -> List[Instance]:
        instances: List[Instance] = []
        hlog(f"Reading data for {split}")
        for sample in data:
                # Example: ["What color is the sky?", "red", "blue", "green", "B"]
                dd = {0:'A', 1:'B', 2:'C', 3:'D'}
                question, answers, correct_choice = sample['question'], sample['choices'], dd[sample['answer']]
                answers_dict = dict(zip(["A", "B", "C", "D"], answers))
                correct_answer: str = answers_dict[correct_choice]

                def answer_to_reference(answer: str) -> Reference:
                    return Reference(Output(text=answer), tags=[CORRECT_TAG] if answer == correct_answer else [])

                instance = Instance(
                    input=Input(text=question),
                    references=list(map(answer_to_reference, answers)),
                    split=split,
                )
                instances.append(instance)
        return instances

    def get_instances(self, output_path: str) -> List[Instance]:
        # Download the raw data
        dataset = load_dataset("HyperbeeAI/mmlu_turkish", self.subject, token=os.getenv("HF_TOKEN"))

        # Read all the instances
        instances: List[Instance] = []
        splits: Dict[str, str] = {
            "dev": TRAIN_SPLIT,
            "test": TEST_SPLIT,
        }        
        for split in splits:
            split_data = dataset[split]
            instances.extend(self.process_split(split_data, splits[split]))

        return instances
