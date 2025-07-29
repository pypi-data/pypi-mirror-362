import gc
from pathlib import Path
from types import MappingProxyType
from typing import Any

from huggingface_hub import hf_hub_download
from pyspark import keyword_only

from scaledp.models.detectors.BaseDetector import BaseDetector
from scaledp.params import HasBatchSize, HasDevice
from scaledp.schemas.Box import Box
from scaledp.schemas.DetectorOutput import DetectorOutput

from ...enums import Device


class YoloDetector(BaseDetector, HasDevice, HasBatchSize):
    _model = None

    defaultParams = MappingProxyType(
        {
            "inputCol": "image",
            "outputCol": "boxes",
            "keepInputData": False,
            "scaleFactor": 1.0,
            "scoreThreshold": 0.5,
            "device": Device.CPU,
            "batchSize": 2,
            "partitionMap": False,
            "numPartitions": 0,
            "pageCol": "page",
            "pathCol": "path",
            "propagateError": False,
        },
    )

    @keyword_only
    def __init__(self, **kwargs: Any) -> None:
        super(YoloDetector, self).__init__()
        self._setDefault(**self.defaultParams)
        self._set(**kwargs)
        self.get_model({k.name: v for k, v in self.extractParamMap().items()})

    @classmethod
    def get_model(cls, params):
        if cls._model:
            return cls._model
        from ultralytics import YOLO

        model = params["model"]
        if not Path(model).is_file():
            model = hf_hub_download(repo_id=model, filename="best.pt")

        detector = YOLO(model)
        device = "cpu" if int(params["device"]) == Device.CPU.value else "cuda"

        cls._model = detector.to(device)
        return cls._model

    @classmethod
    def call_detector(cls, images, params):
        import torch

        detector = cls.get_model(params)

        results = detector(
            [image[0] for image in images],
            conf=params["scoreThreshold"],
            save_conf=True,
        )

        results_final = []
        for res, (_image, image_path) in zip(results, images):
            boxes = []
            for box in res.boxes:
                boxes.append(Box.from_bbox(box.xyxy[0]))
            results_final.append(
                DetectorOutput(path=image_path, type="yolo", bboxes=boxes),
            )

        gc.collect()
        if int(params["device"]) == Device.CUDA.value:
            torch.cuda.empty_cache()

        return results_final
