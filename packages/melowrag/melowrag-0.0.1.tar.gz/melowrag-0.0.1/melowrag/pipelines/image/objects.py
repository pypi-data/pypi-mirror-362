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

try:
    from PIL import Image

    PIL = True
except ImportError:
    PIL = False

from ..hfpipeline import HFPipeline


class Objects(HFPipeline):
    """
    Applies object detection models to images. Supports both object detection models and image classification models.
    """

    def __init__(self, path=None, quantize=False, gpu=True, model=None, classification=False, threshold=0.9, **kwargs):
        if not PIL:
            raise ImportError('Objects pipeline is not available - install "pipeline" extra to enable')

        super().__init__(
            "image-classification" if classification else "object-detection", path, quantize, gpu, model, **kwargs
        )

        self.classification = classification
        self.threshold = threshold

    def __call__(self, images, flatten=False, workers=0):
        """
        Applies object detection/image classification models to images. Returns a list of (label, score).

        This method supports a single image or a list of images. If the input is an image, the return
        type is a 1D list of (label, score). If text is a list, a 2D list of (label, score) is
        returned with a row per image.

        Args:
            images: image|list
            flatten: flatten output to a list of objects
            workers: number of concurrent workers to use for processing data, defaults to None

        Returns:
            list of (label, score)
        """

        values = [images] if not isinstance(images, list) else images

        values = [Image.open(image) if isinstance(image, str) else image for image in values]

        results = (
            self.pipeline(values, num_workers=workers)
            if self.classification
            else self.pipeline(values, threshold=self.threshold, num_workers=workers)
        )

        outputs = []
        for result in results:
            result = [(x["label"], x["score"]) for x in result if x["score"] > self.threshold]

            result = sorted(result, key=lambda x: x[1], reverse=True)

            unique = set()
            elements = []
            for label, score in result:
                if label not in unique:
                    elements.append(label if flatten else (label, score))
                    unique.add(label)

            outputs.append(elements)

        return outputs[0] if not isinstance(images, list) else outputs
