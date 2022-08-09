from cProfile import label
from linlog.tensorflow.formatter import parse_bbox_tf_record
import tensorflow as tf
from functools import partial
import math


def get_object_detection_dataset(path: str, shuffle=True):
    img_size = (256,256)
    ignore_order = tf.data.Options()
    ignore_order.experimental_deterministic = False  # disable order, increase speed
    dataset = tf.data.TFRecordDataset(
        [path]
    )  # automatically interleaves reads from multiple files

    #dataset = dataset.with_options(
    #    ignore_order
    #)  # uses data as soon as it streams in, rather than in its original order

    def decode_fn(record_bytes):
        example = tf.io.parse_single_example(
            record_bytes,
            {
                'image/height': tf.io.FixedLenFeature([], tf.int64),
                'image/width': tf.io.FixedLenFeature([], tf.int64),
                #'image/filename': tf.io.FixedLenFeature([], tf.string),
                #'image/source_id': tf.io.FixedLenFeature([], tf.string),
                'image/encoded': tf.io.VarLenFeature(dtype=tf.string),
                #'image/format': tf.io.FixedLenFeature([], tf.string),
                'image/object/bbox/xmin': tf.io.VarLenFeature(dtype=tf.float32),
                'image/object/bbox/xmax': tf.io.VarLenFeature(dtype=tf.float32),
                'image/object/bbox/ymin': tf.io.VarLenFeature(dtype=tf.float32),
                'image/object/bbox/ymax': tf.io.VarLenFeature(dtype=tf.float32),
                'image/object/class/text': tf.io.VarLenFeature(dtype=tf.string),
                'image/object/class/label': tf.io.VarLenFeature(dtype=tf.int64),
            }
        )

        for key in ['image/object/bbox/xmin', 
                'image/object/bbox/xmax', 
                'image/object/bbox/ymin', 
                'image/object/bbox/ymax',
                'image/object/class/text',
                'image/object/class/label']:
                pass
            #example[key] = tf.sparse.to_dense(example[key])
        
        return example

    dataset = dataset.map(decode_fn)
    return dataset
