import collections
import matplotlib.pyplot as plt
from PIL import Image
import requests
import sys
import torch

import preprocess
import postprocess


# Arguments
image_path = sys.argv[1]
model_url = "https://yolo-model-opendatahub-model.apps.trustyai.dzzt.p1.openshiftapps.com/v2/models/yolo-model" # put ODH model url here

# Preprocess
print("Preprocessing")
im = Image.open(image_path)

max_dim = max(im.size)
im = im.resize((int(im.size[0] * 640/max_dim), int(im.size[1] * 640/max_dim)))
torch_im = torch.tensor(preprocess.get_as_numpy(im))
request_body = preprocess.to_kserve(im)

# Send to model
print("Sending to model")
response = requests.post(model_url+"/infer", json=request_body).json()


# Process response to PyTorch tensors
print("Postprocessing")
pred_dict, proto_dict = response["outputs"]
pred = torch.tensor(pred_dict['data']).reshape(pred_dict['shape'])
proto = torch.tensor(proto_dict['data']).reshape(proto_dict['shape'])

# Set up mask generator
args = {"conf":.25, "iou":.45, "agnostic_nms": False, "max_det":1000}
segPredictor = postprocess.SegmentationPredictor(overrides=args)

# Put class names into mask generator
ModelSubstitute = collections.namedtuple("ModelSubstitute", ["names"])
segPredictor.model = ModelSubstitute(names=postprocess.names)
segPredictor.batch = [["."]]

# generate masks
results = segPredictor.postprocess([pred, proto], torch_im, torch_im)

# Visualize
print("Visualizing")
plt.imshow(results[0].plot())
plt.axis("off")
plt.savefig("seg.png")
plt.show()