from typing import List

from bluer_options.timer import Timer
from bluer_options import string
from bluer_options import host
from bluer_objects.metadata import post_to_object, get_from_object
from bluer_objects import storage
from bluer_objects.storage.policies import DownloadPolicy
from bluer_algo.image_classifier.dataset.dataset import ImageClassifierDataset
from bluer_algo.image_classifier.model.predictor import ImageClassifierPredictor
from bluer_sbc.imager.camera import instance as camera

from bluer_ugv.swallow.session.classical.keyboard import ClassicalKeyboard
from bluer_ugv.swallow.session.classical.leds import ClassicalLeds
from bluer_ugv.swallow.session.classical.setpoint import ClassicalSetPoint
from bluer_ugv.swallow.session.classical.mode import OperationMode
from bluer_ugv import env
from bluer_ugv.logger import logger


class ClassicalCamera:
    def __init__(
        self,
        keyboard: ClassicalKeyboard,
        leds: ClassicalLeds,
        setpoint: ClassicalSetPoint,
        object_name: str,
    ):
        self.prediction_timer = Timer(
            period=env.BLUER_UGV_CAMERA_PREDICTION_PERIOD,
            name="{}.prediction".format(self.__class__.__name__),
        )
        self.training_timer = Timer(
            period=env.BLUER_UGV_CAMERA_TRAINING_PERIOD,
            name="{}.training".format(self.__class__.__name__),
        )

        self.keyboard = keyboard
        self.leds = leds
        self.setpoint = setpoint

        self.object_name = object_name

        self.dict_of_classes = {
            0: "no_action",
            1: "left",
            2: "right",
        }

        self.dataset = ImageClassifierDataset(
            dict_of_classes=self.dict_of_classes,
            object_name=self.object_name,
        )

        self.predictor = None

        logger.info(
            "{}: prediction=1/{}, train=1/{}".format(
                self.__class__.__name__,
                string.pretty_duration(env.BLUER_UGV_CAMERA_PREDICTION_PERIOD),
                string.pretty_duration(env.BLUER_UGV_CAMERA_TRAINING_PERIOD),
            )
        )

    def initialize(self) -> bool:
        if not camera.open(log=True):
            return False

        if not storage.download(
            env.BLUER_UGV_SWALLOW_MODEL,
            policy=DownloadPolicy.DOESNT_EXIST,
        ):
            return False

        success, self.predictor = ImageClassifierPredictor.load(
            object_name=env.BLUER_UGV_SWALLOW_MODEL,
        )
        return success

    def cleanup(self):
        camera.close(log=True)

        self.dataset.save(
            metadata={
                "source": host.get_name(),
            },
            log=True,
        )

        dataset_list: List[str] = get_from_object(
            object_name=env.BLUER_UGV_SWALLOW_DATASET_LIST,
            key="dataset-list",
            default=[],
            download=True,
        )
        dataset_list.append(self.object_name)
        if not post_to_object(
            object_name=env.BLUER_UGV_SWALLOW_DATASET_LIST,
            key="dataset-list",
            value=dataset_list,
            upload=True,
            verbose=True,
        ):
            logger.error("failed to add object to dataset list.")

    def update(self) -> bool:
        if self.setpoint.speed <= 0:
            return True

        if self.keyboard.mode == OperationMode.PREDICTION:
            return self.update_prediction()

        if self.keyboard.mode == OperationMode.TRAINING:
            return self.update_training()

        return True

    def update_prediction(self) -> bool:
        if not self.prediction_timer.tick():
            return True

        self.leds.leds["red"]["state"] = not self.leds.leds["red"]["state"]

        success, image = camera.capture(
            close_after=False,
            open_before=False,
            log=True,
        )
        if not success:
            return success

        success, metadata = self.predictor.predict(
            image=image,
        )
        if not success:
            return success

        predicted_class = metadata["predicted_class"]
        if predicted_class == 1:
            self.setpoint.put(
                what="steering",
                value=env.BLUER_UGV_SWALLOW_STEERING_SETPOINT,
                log=True,
            )
        elif predicted_class == 2:
            self.setpoint.put(
                what="steering",
                value=-env.BLUER_UGV_SWALLOW_STEERING_SETPOINT,
                log=True,
            )

        return True

    def update_training(self) -> bool:
        if not (self.training_timer.tick() or self.keyboard.last_key != ""):
            return True

        self.leds.leds["red"]["state"] = not self.leds.leds["red"]["state"]

        filename = "{}.png".format(
            string.pretty_date(
                as_filename=True,
                unique=True,
            )
        )

        success, _ = camera.capture(
            close_after=False,
            open_before=False,
            object_name=self.object_name,
            filename=filename,
            log=True,
        )
        if not success:
            return success

        logger.info(f"self.keyboard.last_key: {self.keyboard.last_key}")

        if not self.dataset.add(
            filename=filename,
            class_index=(
                0
                if self.keyboard.last_key == ""
                else 1 if self.keyboard.last_key == "a" else 2
            ),
            log=True,
        ):
            return False

        self.training_timer.reset()

        return True
