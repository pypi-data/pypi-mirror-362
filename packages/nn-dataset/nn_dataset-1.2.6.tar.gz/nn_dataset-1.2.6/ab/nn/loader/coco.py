from ab.nn.loader.coco_ import Detection, Segmentation, Caption

def loader(transform_fn, task):
    if task == 'obj-detection':
        f = Detection
    elif task == 'img-segmentation':
        f = Segmentation
    elif task == 'img-captioning':
        f = Caption
    else:
        raise Exception(f"The task '{task}' is not implemented for COCO dataset.")

    return f.loader(transform_fn, task)
