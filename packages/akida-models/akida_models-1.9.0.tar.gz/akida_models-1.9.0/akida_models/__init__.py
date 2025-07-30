"""
Imports models.
"""

from .version import __version__

from .dvs import (convtiny_dvs, convtiny_gesture_pretrained, convtiny_handy_samsung_pretrained)
from .imagenet import (mobilenet_imagenet, mobilenet_imagenet_pretrained, akidanet_imagenet,
                       akidanet_imagenet_pretrained, akidanet_faceidentification_pretrained,
                       akidanet_plantvillage_pretrained, akidanet_vww_pretrained,
                       akidanet_edge_imagenet, akidanet_edge_imagenet_pretrained,
                       akidanet_faceidentification_edge_pretrained, akidanet18_imagenet,
                       akidanet18_imagenet_pretrained)
from .kws import ds_cnn_kws, ds_cnn_kws_pretrained
from .modelnet40 import pointnet_plus_modelnet40, pointnet_plus_modelnet40_pretrained
from .utk_face import vgg_utk_face, vgg_utk_face_pretrained
from .detection import yolo_base, yolo_widerface_pretrained, yolo_voc_pretrained
from .centernet import centernet_base, centernet_voc_pretrained
from .mnist import gxnor_mnist, gxnor_mnist_pretrained
from .portrait128 import akida_unet_portrait128, akida_unet_portrait128_pretrained
from .tenn_spatiotemporal import (tenn_spatiotemporal_dvs128, tenn_spatiotemporal_dvs128_pretrained,
                                  tenn_spatiotemporal_eye, tenn_spatiotemporal_eye_pretrained,
                                  tenn_spatiotemporal_jester, tenn_spatiotemporal_jester_pretrained)

from .utils import fetch_file
from .model_io import load_model
