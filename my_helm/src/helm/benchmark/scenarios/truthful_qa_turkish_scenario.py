from typing import Dict, List

from helm.common.hierarchical_logger import hlog
from .scenario import Scenario, Instance, Reference, TRAIN_SPLIT, TEST_SPLIT, CORRECT_TAG, Input, Output
from datasets import load_dataset

class TruthfulQATScenario(Scenario):
    name = "truthful_qat"
    description = "Truthful QA Turkish"
    tags = ["knowledge", "harms", "multiple_choice"]

    def __init__(self):
        super().__init__()


    def process_split(self, data, split: str) -> List[Instance]:
        instances: List[Instance] = []
        hlog(f"Reading data for {split}")
        for sample in data:
                # Example: ["What color is the sky?", "red", "blue", "green", "B"]
                dd = {0:'A', 1:'B', 2:'C', 3:'D'}
                question, choices, labels = sample['question'], sample['mc1_targets']['choices'], sample['mc1_targets']['labels']

                refs = []
                for c, l in zip(choices,labels):
                    if l == 1:
                        refs.append(Reference(Output(text=c), tags=[CORRECT_TAG]))
                    else:
                        refs.append(Reference(Output(text=c),tags=[]))
                instance = Instance(
                    input=Input(text=question),
                    references=refs,
                    split=split,
                )
                instances.append(instance)
        return instances

    def get_instances(self, output_path: str) -> List[Instance]:
        # Download the raw data
        dataset = load_dataset("mukayese/truthful_qa-tr", token="***REMOVED***")

        # Read all the instances
        instances: List[Instance] = []
        splits: Dict[str, str] = {
            "validation": TEST_SPLIT,
        }        
        for split in splits:
            split_data = dataset[split]
            instances.extend(self.process_split(split_data, splits[split]))

        return instances
