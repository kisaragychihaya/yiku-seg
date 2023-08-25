from torch import nn
from ultralytics.models import  RTDETR
import sys

class HG_backbone(nn.Module):
    def __init__(self, *args, **kwargs):
        pretrained =bool(kwargs.get("pretrained",True))
        arch =str(kwargs.get("arch","s"))[0]
        for key in list(kwargs.keys()):
            kwargs.__delitem__(key)
        super().__init__(*args, **kwargs)
        m=RTDETR(f"rtdetr-{arch}.yaml")
        if pretrained:
            m.load(f"./model_data/rtdetr-{arch}.pt")
        self.__model = m.model.model
        self.__dict__.update(**{"l":{"feature_ch":2048,"low_ch":512},
                                "x":{"feature_ch":2048,"low_ch":512}
                                }[arch])

    def forward(self, x):
        for i, n in enumerate(self.__model):
            x = n(x)
            if x.shape[1] == 2048:# Get the featuremap
                break
            if i == 3:
                low = x # low feature

        return low, x

def hgnetv2l(pretrained=True, **kwargs):
    return HG_backbone(pretrained=pretrained,arch="l")

def hgnetv2x(pretrained=True, **kwargs):
    return HG_backbone(pretrained=pretrained,arch="x")