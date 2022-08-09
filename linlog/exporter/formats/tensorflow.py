import os
import tensorflow as tf
from linlog.dataset import LocalDataset
from linlog.tensorflow.formatter import create_bbox_tf_example


def handle_tf_export(ds_path, dataset):
    output_path = "dataset.tfrecord"

    writer = tf.io.TFRecordWriter(ds_path + os.sep + output_path)

    for example, img in dataset:
        tf_example = create_bbox_tf_example(example, img, dataset.label_mapping)
        writer.write(tf_example.SerializeToString())

    writer.close()