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
Labels module
"""

from ..hfpipeline import HFPipeline


class Labels(HFPipeline):
    """
    Applies a text classifier to text. Supports zero shot and standard text classification models
    """

    def __init__(self, path=None, quantize=False, gpu=True, model=None, dynamic=True, **kwargs):
        super().__init__(
            "zero-shot-classification" if dynamic else "text-classification", path, quantize, gpu, model, **kwargs
        )

        self.dynamic = dynamic

    def __call__(self, text, labels=None, multilabel=False, flatten=None, workers=0, **kwargs):
        """
        Applies a text classifier to text. Returns a list of (id, score) sorted by highest score,
        where id is the index in labels. For zero shot classification, a list of labels is required.
        For text classification models, a list of labels is optional, otherwise all trained labels are returned.

        This method supports text as a string or a list. If the input is a string, the return
        type is a 1D list of (id, score). If text is a list, a 2D list of (id, score) is
        returned with a row per string.

        Args:
            text: text|list
            labels: list of labels
            multilabel: labels are independent if True, scores are normalized to sum to 1 per text item if False, raw scores returned if None
            flatten: flatten output to a list of labels if present. Accepts a boolean or float value to only keep scores greater than that number.
            workers: number of concurrent workers to use for processing data, defaults to None
            kwargs: additional keyword args

        Returns:
            list of (id, score) or list of labels depending on flatten parameter
        """

        if self.dynamic:
            results = self.pipeline(text, labels, multi_label=multilabel, truncation=True, num_workers=workers)
        else:
            function = (
                "none" if multilabel is None else "sigmoid" if multilabel or len(self.labels()) == 1 else "softmax"
            )

            results = self.pipeline(text, top_k=None, function_to_apply=function, num_workers=workers, **kwargs)

        if isinstance(text, str):
            results = [results]

        outputs = self.outputs(results, labels, flatten)
        return outputs[0] if isinstance(text, str) else outputs

    def labels(self):
        """
        Returns a list of all text classification model labels sorted in index order.

        Returns:
            list of labels
        """

        return list(self.pipeline.model.config.id2label.values())

    def outputs(self, results, labels, flatten):
        """
        Processes pipeline results and builds outputs.

        Args:
            results: pipeline results
            labels: list of labels
            flatten: flatten output to a list of labels if present. Accepts a boolean or float value to only keep scores greater than that number.

        Returns:
            list of outputs
        """

        outputs = []
        threshold = 0.0 if isinstance(flatten, bool) else flatten

        for result in results:
            if self.dynamic:
                if flatten:
                    result = [label for x, label in enumerate(result["labels"]) if result["scores"][x] >= threshold]
                    outputs.append(result[:1] if isinstance(flatten, bool) else result)
                else:
                    outputs.append(
                        [(labels.index(label), result["scores"][x]) for x, label in enumerate(result["labels"])]
                    )
            else:
                if flatten:
                    result = [
                        x["label"] for x in result if x["score"] >= threshold and (not labels or x["label"] in labels)
                    ]
                    outputs.append(result[:1] if isinstance(flatten, bool) else result)
                else:
                    outputs.append(self.limit(result, labels))

        return outputs

    def limit(self, result, labels):
        """
        Filter result using labels. If labels is None, original result is returned.

        Args:
            result: results array sorted by score descending
            labels: list of labels or None

        Returns:
            filtered results
        """

        config = self.pipeline.model.config

        result = [(config.label2id.get(x["label"], 0), x["score"]) for x in result]

        if labels:
            matches = []
            for label in labels:
                if label.isdigit():
                    label = int(label)
                    keys = list(config.id2label.keys())
                else:
                    label = label.lower()
                    keys = [x.lower() for x in config.label2id.keys()]

                if label in keys:
                    matches.append(keys.index(label))

            return [(label, score) for label, score in result if label in matches]

        return result
