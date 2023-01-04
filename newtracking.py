import cv2
import time
import random
import numpy as np
import onnxruntime as ort
# from PIL import Image
# from pathlib import Path
from urllib.parse import urlparse
from os.path import splitext, basename

def get_file_name(picture_page):
    disassembled = urlparse(picture_page)
    filename, file_ext = splitext(basename(disassembled.path))
    return filename, file_ext


def write_to_txt(boxes,file_name):
    with open(file_name,'w') as wf:
        for box in boxes:
            text = str(box[0])+' '+str(box[1])+' '+str(box[2])+' '+str(box[3])+' '+str(box[4])+' \n'
            wf.write(text)


def letterbox(im, new_shape=(512,512), color=(114, 114, 114), auto=True, scaleup=True, stride=32):
        # Resize and pad image while meeting stride-multiple constraints
        shape = im.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:  # only scale down, do not scale up (for better val mAP)
            r = min(r, 1.0)

        # Compute padding
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

        if auto:  # minimum rectangle
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
        return im, r, (dw, dh)


def load_model(w):
    cuda = False
    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if cuda else ['CPUExecutionProvider']
    session = ort.InferenceSession(w, providers=providers)
    return session

def predict(image_file_name,session):
    names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
            'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
            'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
            'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
            'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
            'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
            'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
            'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
            'hair drier', 'toothbrush']

    check_labels = [15,16]

    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    img = cv2.imread(image_file_name)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    image = img.copy()
    image, ratio, dwdh = letterbox(image, (512,512), auto=False)
    image = image.transpose((2, 0, 1))
    image = np.expand_dims(image, 0)
    image = np.ascontiguousarray(image)

    im = image.astype(np.float32)
    im /= 255

    outname = [i.name for i in session.get_outputs()]

    inname = [i.name for i in session.get_inputs()]

    inp = {inname[0]:im}
    # while True:
    st = time.time()
    outputs = session.run(outname, inp)[0]

    ori_images = [img.copy()]
    boxes = []

    for i,(batch_id,x0,y0,x1,y1,cls_id,score) in enumerate(outputs):
        if cls_id in check_labels:       
            image = ori_images[int(batch_id)]

            box = np.array([x0,y0,x1,y1])
            box -= np.array(dwdh*2)
            box /= ratio
            box = box.round().astype(np.int32).tolist()

            colors = colors or [random.randint(0, 255) for _ in range(3)]
            cls_id = int(cls_id)
            score = round(float(score),3)
            text = str(names[cls_id])+': '+str(score)
            tl = 3 or round(0.002 * (image.shape[0] + image.shape[1]) / 2) + 1

            cv2.rectangle(image,box[:2],box[2:],colors[cls_id],thickness=tl,lineType=cv2.LINE_AA)
            tf = max(tl - 1, 1)
            t_size = cv2.getTextSize(text, 0, fontScale=tl / 3, thickness=tf)[0]
            c2 = box[0] + t_size[0], box[1] - t_size[1] - 3
            cv2.rectangle(image, box[:2], c2, colors[cls_id], -1, cv2.LINE_AA)
            cv2.putText(image,text,(box[0], box[1] - 2), 0, tl / 3, [225, 255, 255],thickness=3, lineType=cv2.LINE_AA)
            boxes.append([cls_id,box[0],box[1],box[2],box[3]])
            
    return image,boxes

if __name__ == "__main__":
    session = load_model('D:\Dog_Cat_Streamlit_Web_App\streamlit\yolov7-tiny.onnx') #Load model
    image,boxes = predict('cat_dog.jpg',session) #Predict

    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB) #Change cvt Color to original image
    cv2.imwrite('cat_dog_pre.jpg',image) #Save image
    print(boxes)
