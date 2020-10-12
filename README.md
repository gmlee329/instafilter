# Instance Shadow Detection
This repo is implemented on [Detectron2](https://github.com/facebookresearch/detectron2).
The original repo is [original repo](https://github.com/stevewongv/InstanceShadowDetection).

I made flask api server and web frontend to run the model and get result via http protocol.

## How to run
**Run right now!**  
[![Run on Ainize](https://ainize.ai/static/images/run_on_ainize_button.svg)](https://ainize.web.app/redirect?git_repo=https://github.com/gmlee329/InstanceShadowDetection)

[DEMO](https://master-instance-shadow-detection-gmlee329.endpoint.ainize.ai)

**In local**  
It must need GPU so, [Nvidia-docker](https://github.com/NVIDIA/nvidia-docker) is needed.
```bash 
$ git clone https://github.com/gmlee329/InstanceShadowDetection.git
$ docker build -t isd .
$ docker run --gpus 0 -it -p <host port>:80 --name isd isd
```
Then it will run in local

If you want to check the web page,  
install ngrok and enter the command below
```bash
$ ~/ngrok http <hostport>
```
Then, you can run the model and get result via webpage. 

## <a name="CitingLISA"></a> Citation
If you use LISA, SOBA, or SOAP, please use the following BibTeX entry.
#
![instafilter](development/header_image.jpg)

[![PyVersion](https://img.shields.io/pypi/pyversions/instafilter.svg)](https://img.shields.io/pypi/pyversions/instafilter.svg)
[![PyPI](https://img.shields.io/pypi/v/instafilter.svg)](https://pypi.python.org/pypi/instafilter)

Modifiy images using Instagram-like filters in python. [Read how it works on Medium](https://medium.com/@travis.hoppe/instagram-filters-in-python-acc1ee7e67bc)!

    pip install instafilter

Example:

``` python
from instafilter import Instafilter

model = Instafilter("Lo-fi")
new_image = model("myimage.jpg")

# To save the image, use cv2
import cv2
cv2.imwrite("modified_image.jpg", new_image)
```

## Sample images

Browse samples for every filter in [`development/examples`](development/examples).

**Ludwig**
[![Example image: Ludwig](development/examples/Ludwig.jpg)](examples/Ludwig.jpg)

**Stinson**
[![Example image: Stinson](development/examples/Stinson.jpg)](examples/Stinson.jpg)

**Moon**
[![Example image: Moon](development/examples/Moon.jpg)](examples/Moon.jpg)

## Train

See the code in [`development/train_new_model`](development/train_new_model) to train a new model.

## Roadmap

+ Medium post

## Credits

+ Made with ❤️ by [Travis Hoppe](https://twitter.com/metasemantic?lang=en).

+ Header image sourced from [Will Terra](https://unsplash.com/photos/qIY9mUKT540) and modified with instafilter.
