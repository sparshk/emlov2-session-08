import torch
import torch.nn.functional as F
import torchvision.transforms as T

from ts.torch_handler.vision_handler import VisionHandler
from ts.utils.util import map_class_to_label


class ImageClassifier(VisionHandler):
    """
    ImageClassifier handler class. This handler takes an image
    and returns the name of object in that image.
    """

    topk = 5
    # These are the standard Imagenet dimensions
    # and statistics
    image_processing = T.Compose(
            [
                T.Resize(224),
                T.ToTensor(),
                T.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
            ]
        )

    def set_max_result_classes(self, topk):
        self.topk = topk

    def get_max_result_classes(self):
        return self.topk

    def postprocess(self, data):
        ps = F.softmax(data, dim=-1)
        probs, classes = torch.topk(ps, self.topk, dim=1)
        probs = probs.tolist()
        classes = classes.tolist()
        return map_class_to_label(probs, self.mapping, classes)


# torch-model-archiver --model-name cifar_basic --version 1.0 --serialized-file new_trace_file/model.script.pt --handler src/torch_handler/cifar_handler.py --extra-files src/torch_handler/cifar_classes/index_to_name.json