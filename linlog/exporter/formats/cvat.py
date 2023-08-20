import datetime
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import List
from linlog.schemas import (
    ImageTask,
    Label,
    Annotation,
    BoundingBoxAnnotation,
    PolygonAnnotation
)


def export(tasks: List[ImageTask], output_path: Path) -> ET.ElementTree:
    labels: List[Label] = []
    root = ET.Element("annotations")
    _add_subelement_text(root, "version", "1.1")
    create_meta(root, tasks, labels)
    create_images(root, tasks, labels)

    output_file_path = (output_path / "output-cvat").with_suffix(".xml")
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write(output_file_path, encoding="utf-8")
    return tree, output_file_path


def create_meta(
    root: ET.Element,
    tasks: List[ImageTask],
    task_labels: List[Label]
):
    meta = ET.SubElement(root, "meta")
    task = ET.SubElement(meta, "task")
    _add_subelement_text(task, "size", str(len(tasks)))
    _add_subelement_text(task, "mode", "annotation")
    _add_subelement_text(task, "overlapp", str(0))
    _add_subelement_text(task, "bugtracker", str(None))
    _add_subelement_text(task, "flipped", str(False))
    _add_subelement_text(
        meta, "dumped", str(datetime.datetime.now(tz=datetime.timezone.utc))
    )
    _add_subelement_text(
        task, "created", str(datetime.datetime.now(tz=datetime.timezone.utc))
    )
    _add_subelement_text(
        task, "updated", str(datetime.datetime.now(tz=datetime.timezone.utc))
    )

    labels = ET.SubElement(task, "labels")

    for row in task_labels:
        label = ET.SubElement(labels, "label")
        _add_subelement_text(label, "name", str(row.name))
        attributes = ET.SubElement(label, "attributes")

        for attribute in row.attributes if row.attributes else []:
            _add_subelement_text(attributes, 'name', str(attribute.name))
            _add_subelement_text(
                attributes,
                'input_type',
                attribute.attribute_type
            )
            _add_subelement_text(attributes, 'default_value', '')


def create_images(
    root: ET.Element,
    tasks: List[ImageTask],
    task_labels: List[Label]
):
    for idx, task in enumerate(tasks, 1):
        image = ET.SubElement(root, "image")
        image.attrib["id"] = str(idx)
        image.attrib["name"] = task.filename if task.filename else \
            task.attachment,
        image.attrib["width"] = str(task.media_specs.width)
        image.attrib["height"] = str(task.media_specs.height)

        for z_order, task_annotation in enumerate(task.annotations, 1):
            annotation = create_annotation(image, task_annotation, z_order)

            for attribute in task_annotation.attributes.keys():
                _add_subelement_text(
                    annotation,
                    'attribute',
                    str(task_annotation.attributes[attribute])
                )


def create_annotation(task: ET.Element, annotation: Annotation, z_order: int):
    if annotation.annotation_type == "bounding-box":
        box_annotation: BoundingBoxAnnotation = annotation
        box = ET.SubElement(
            task,
            "box",
            label=str(box_annotation.label),
            xtl=str(box_annotation.left),
            ytl=str(box_annotation.top),
            xbr=str(box_annotation.left + box_annotation.width),
            ybr=str(box_annotation.top + box_annotation.height),
            z_order=str(z_order),
            occluded="0"
        )
        return box
    elif annotation.annotation_type == "polygon":
        polygon_annotation: PolygonAnnotation = annotation

        points = []
        for v in polygon_annotation.segments[0].path:
            points.append(f"{v.x},{v.y}")
        points = ';'.join(points)

        polygon = ET.SubElement(
            task,
            'polygon',
            label=str(polygon_annotation.label),
            points=points,
            z_order=str(z_order),
            occluded="0"
        )
        return polygon
    else:
        print(f"[warning] skipping {annotation.annotation_type}")


def _add_subelement_text(parent: ET.Element, name: str, value: str):
    assert type(value) is str, 'value must be of type string'
    element = ET.SubElement(parent, name)
    element.text = value
    return element
