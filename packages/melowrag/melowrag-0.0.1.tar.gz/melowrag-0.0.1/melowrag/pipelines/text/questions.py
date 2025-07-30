# Copyright 2025 The MelowRAG Author @erfanzar (Erfan Zare Chavoshi).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Questions module
"""

from ..hfpipeline import HFPipeline


class Questions(HFPipeline):
    """
    Runs extractive QA for a series of questions and contexts.
    """

    def __init__(self, path=None, quantize=False, gpu=True, model=None, **kwargs):
        super().__init__("question-answering", path, quantize, gpu, model, **kwargs)

    def __call__(self, questions, contexts, workers=0):
        """
        Runs a extractive question-answering model against each question-context pair, finding the best answers.

        Args:
            questions: list of questions
            contexts: list of contexts to pull answers from
            workers: number of concurrent workers to use for processing data, defaults to None

        Returns:
            list of answers
        """

        answers = []

        for x, question in enumerate(questions):
            if question and contexts[x]:
                result = self.pipeline(question=question, context=contexts[x], num_workers=workers)

                answer, score = result["answer"], result["score"]

                if score < 0.05:
                    answer = None

                answers.append(answer)
            else:
                answers.append(None)

        return answers
