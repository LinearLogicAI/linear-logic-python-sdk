import io
import tensorflow as tf
from typing import Dict
from linlog.data_types.task import Task
from linlog.dataset import LocalDataset
from linlog.tensorflow import utils


def create_bbox_tf_example(example: Task, img, label_mapping: Dict[str, int], normalize: bool = True):
    # Image height
    height = example.get("media_specs", {}).get("height")
    # Image width 
    width = example.get("media_specs", {}).get("width") 
    filename = str.encode(example['id']) # Filename of the image. Empty if image is not from file
    image_format = b'png' # b'jpeg' or b'png'

    def normalize_coordinate(coordinate: float, axis: str) -> float:
        if not normalize:
            return coordinate

        assert axis in ["horizontal", "vertical"], "Invalid axis"

        if axis == "horizontal":
            return coordinate / width

        return coordinate / height

    annotations = [a for a in example.get('annotations', []) if a['type'] == 'bounding-box']

    # List of normalized left x coordinates in bounding box (1 per box)
    xmins = [normalize_coordinate(a['left'], "horizontal") for a in annotations] 
    # List of normalized right x coordinates in bounding box
    xmaxs = [normalize_coordinate(a['left'] + a['width'], "horizontal") for a in annotations] 
    
    # List of normalized top y coordinates in bounding box (1 per box)
    ymins = [normalize_coordinate(a['top'], "vertical") for a in annotations]
    # List of normalized bottom y coordinates in bounding box (1 per box)
    ymaxs = [normalize_coordinate(a['top'] + a['height'], "vertical") for a in annotations] 
    
    # List of string class name of bounding box (1 per box)
    classes_text = [str.encode(a['label']) for a in annotations]
    # List of integer class id of bounding box (1 per box)
    classes = [label_mapping[a['label']] for a in annotations]

    img = img.resize((244, 244))
    byteIO = io.BytesIO()
    img.save(byteIO, format='PNG')
    encoded_image_data = byteIO.getvalue()
    #encoded_image_data = img.read() # Encoded image bytes

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': utils.int64_feature(height),
        'image/width': utils.int64_feature(width),
        'image/filename': utils.bytes_feature(filename),
        'image/source_id': utils.bytes_feature(filename),
        'image/encoded': utils.bytes_feature(encoded_image_data),
        'image/format': utils.bytes_feature(image_format),
        'image/object/bbox/xmin': utils.float_list_feature(xmins),
        'image/object/bbox/xmax': utils.float_list_feature(xmaxs),
        'image/object/bbox/ymin': utils.float_list_feature(ymins),
        'image/object/bbox/ymax': utils.float_list_feature(ymaxs),
        'image/object/class/text': utils.bytes_list_feature(classes_text),
        'image/object/class/label': utils.int64_list_feature(classes),
    }))
    return tf_example


def parse_bbox_tf_record(example):
    feature_description = {
        'image/height': tf.io.FixedLenFeature([], tf.int64),
        'image/width': tf.io.FixedLenFeature([], tf.int64),
        'image/filename': tf.io.FixedLenFeature([], tf.string),
        'image/source_id': tf.io.FixedLenFeature([], tf.string),
        'image/encoded': tf.io.VarLenFeature(dtype=tf.string),
        'image/format': tf.io.FixedLenFeature([], tf.string),
        'image/object/bbox/xmin': tf.io.VarLenFeature(dtype=tf.float32),
        'image/object/bbox/xmax': tf.io.VarLenFeature(dtype=tf.float32),
        'image/object/bbox/ymin': tf.io.VarLenFeature(dtype=tf.float32),
        'image/object/bbox/ymax': tf.io.VarLenFeature(dtype=tf.float32),
        'image/object/class/text': tf.io.VarLenFeature(dtype=tf.string),
        'image/object/class/label': tf.io.FixedLenFeature([], tf.int64),
    }
    example = tf.io.parse_single_example(example, feature_description)

    #print("encoded", example["image/encoded"][:50])
    #example["image"] = tf.io.decode_jpeg(example["image/encoded"], channels=3)
    return example

