import os
import glob
import json
import math
import random
import shutil


def export(
    dataset_path: str,
    output_path: str,
    split_ratio=[.7, .2, .1],
    shuffle_seed=0
):

    assert math.fsum(split_ratio) == 1.0, \
        "Sum of split ratios must be equal to 1"

    os.makedirs(output_path, exist_ok=True)
    os.makedirs(os.path.join(output_path, 'annotations'), exist_ok=True)
    os.makedirs(os.path.join(output_path, 'images'), exist_ok=True)

    tasks_fp = sorted(glob.glob(
        os.path.join(dataset_path, 'tasks') + os.path.sep + '*.json'
    ))
    images_fp = sorted(glob.glob(
        os.path.join(dataset_path, 'images') + os.path.sep + '*.jpg'
    ))

    random.Random(shuffle_seed).shuffle(tasks_fp)
    random.Random(shuffle_seed).shuffle(images_fp)

    task_count = len(tasks_fp)
    ann_train_split = tasks_fp[:math.ceil(task_count * split_ratio[0])]
    ann_test_split = tasks_fp[
        math.ceil(task_count * split_ratio[0]):
        math.ceil(task_count * (split_ratio[0] + split_ratio[1]))
    ]
    ann_val_split = tasks_fp[
        math.ceil(task_count * (split_ratio[0] + split_ratio[1])):
    ]

    img_train_split = images_fp[:math.ceil(task_count * split_ratio[0])]
    img_test_split = images_fp[
        math.ceil(task_count * split_ratio[0]):
        math.ceil(task_count * (split_ratio[0] + split_ratio[1]))
    ]
    img_val_split = images_fp[
        math.ceil(task_count * (split_ratio[0] + split_ratio[1])):
    ]

    print("img_train_split", dataset_path)
    write_images_to_folder(
        img_train_split, os.path.join(output_path, 'images', 'train')
    )
    write_images_to_folder(
        img_test_split, os.path.join(output_path, 'images', 'test')
    )
    write_images_to_folder(
        img_val_split, os.path.join(output_path, 'images', 'val')
    )

    write_annotations_to_folder(
        ann_train_split, os.path.join(output_path, 'labels', 'train')
    )
    write_annotations_to_folder(
        ann_test_split, os.path.join(output_path, 'labels', 'test')
    )
    write_annotations_to_folder(
        ann_val_split, os.path.join(output_path, 'labels', 'val')
    )


def write_images_to_folder(image_files, fp):
    os.makedirs(fp, exist_ok=True)

    for image_fp in image_files:
        img_id = image_fp.split(os.sep)[-1]
        shutil.copyfile(image_fp, os.path.join(fp, img_id))


def write_annotations_to_folder(task_files, fp):
    os.makedirs(fp, exist_ok=True)

    for task_fp in task_files:
        # fetch ID in-place
        task_id = task_fp.split(os.sep)[-1].replace('.json', '')

        with open(task_fp, 'r') as f:
            task_data = json.load(f)
            media_specs = task_data['media_specs']
            print_buffer = []

            for ann in task_data['annotations']:
                if ann['annotation_type'] == 'bounding-box':
                    b_center_x = ann['left'] + (ann['width'] / 2)
                    b_center_y = ann['top'] + (ann['height'] / 2)
                    b_width = ann['width']
                    b_height = ann['height']

                    b_center_x /= media_specs['width']
                    b_center_y /= media_specs['height']
                    b_width /= media_specs['width']
                    b_height /= media_specs['height']

                    if (
                        b_center_x < 0 or
                        b_center_y < 0 or
                        b_width < 0 or
                        b_height < 0
                    ) or (
                        b_center_x > 1 or
                        b_center_y > 1 or
                        b_width > 1 or
                        b_height > 1
                    ):
                        continue

                    # Write the bbox details to the file
                    print_buffer \
                        .append("0 {:.3f} {:.3f} {:.3f} {:.3f}"
                        .format(b_center_x, b_center_y, b_width, b_height))

                elif ann['annotation_type'] == 'polygon':
                    path = ann['segments'][0]['path']
                    coords = ' '.join([
                        f"{v['x'] / media_specs['width']} " +
                        f"{v['y'] / media_specs['height']}"
                        for v in path
                    ])
                    print_buffer.append("0 " + coords)

            save_file_name = os.path.join(fp, task_id + '.txt')
            print("\n".join(print_buffer), file=open(save_file_name, "w"))
