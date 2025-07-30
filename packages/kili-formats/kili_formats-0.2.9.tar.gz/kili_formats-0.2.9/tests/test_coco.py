from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
import requests
from PIL import Image

from kili_formats.format.coco import (
    _get_coco_categories_with_mapping,
    _get_coco_geometry_from_kili_bpoly,
    convert_from_kili_to_coco_format,
)
from kili_formats.types import Job

from .helpers import coco as helpers


def test__get_coco_image_annotations():
    with TemporaryDirectory() as tmp_dir:
        job_name = "JOB_0"
        local_file_path = tmp_dir / Path("image1.jpg")
        image_width = 1920
        image_height = 1080
        Image.new("RGB", (image_width, image_height)).save(local_file_path)
        coco_annotation = convert_from_kili_to_coco_format(
            jobs={
                (job_name): {
                    "mlTask": "OBJECT_DETECTION",
                    "content": {
                        "categories": {
                            "OBJECT_A": {"name": "Object A"},
                            "OBJECT_B": {"name": "Object B"},
                        }
                    },
                    "instruction": "",
                    "isChild": False,
                    "isNew": False,
                    "isVisible": True,
                    "models": {},
                    "required": True,
                    "tools": ["semantic"],
                }
            },
            assets=[
                helpers.get_asset(
                    local_file_path,
                    with_annotation=[
                        {
                            "x": 0.0,
                            "y": 0.0,
                        },
                        {
                            "x": 0.5,
                            "y": 0.0,
                        },
                        {
                            "x": 0.0,
                            "y": 0.5,
                        },
                    ],
                )
            ],
            title="Test project",
            project_input_type="IMAGE",
            annotation_modifier=lambda x, _, _1: x,
            merged=False,
        )

        assert "Test project" in coco_annotation["info"]["description"]
        categories_by_id = {cat["id"]: cat["name"] for cat in coco_annotation["categories"]}
        assert coco_annotation["images"][0]["file_name"] == "data/image1.jpg"
        assert coco_annotation["images"][0]["width"] == 1920
        assert coco_annotation["images"][0]["height"] == 1080
        assert coco_annotation["annotations"][0]["image_id"] == 0
        assert categories_by_id[coco_annotation["annotations"][0]["category_id"]] == "OBJECT_A"
        assert coco_annotation["annotations"][0]["bbox"] == [0, 0, 960, 540]
        assert coco_annotation["annotations"][0]["segmentation"] == [
            [0.0, 0.0, 960.0, 0.0, 0.0, 540.0]
        ]
        # Area of a triangle: base * height / 2
        assert coco_annotation["annotations"][0]["area"] == 960.0 * 540.0 / 2

        good_date = True
        try:
            datetime.strptime(coco_annotation["info"]["date_created"], "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            good_date = False
        assert good_date, (
            "The date is not in the right format: " + coco_annotation["info"]["date_created"]
        )


def test__get_coco_image_annotation_area_with_self_intersecting_polygon():
    with TemporaryDirectory() as tmp_dir:
        job_name = "JOB_0"
        local_file_path = tmp_dir / Path("image1.jpg")
        image_width = 1920
        image_height = 1080
        Image.new("RGB", (image_width, image_height)).save(local_file_path)
        coco_annotation = convert_from_kili_to_coco_format(
            jobs={
                (job_name): {
                    "mlTask": "OBJECT_DETECTION",
                    "content": {
                        "categories": {
                            "OBJECT_A": {"name": "Object A"},
                            "OBJECT_B": {"name": "Object B"},
                        }
                    },
                    "instruction": "",
                    "isChild": False,
                    "isNew": False,
                    "isVisible": True,
                    "models": {},
                    "required": True,
                    "tools": ["semantic"],
                }
            },
            assets=[
                helpers.get_asset(
                    local_file_path,
                    with_annotation=[
                        {
                            "x": 0.0,
                            "y": 0.0,
                        },
                        {
                            "x": 0.5,
                            "y": 0.0,
                        },
                        {
                            "x": 0.0,
                            "y": 0.5,
                        },
                        {
                            "x": 0.5,
                            "y": 0.5,
                        },
                        {
                            "x": 0.0,
                            "y": 0.0,
                        },
                    ],
                )
            ],
            title="Test project",
            project_input_type="IMAGE",
            annotation_modifier=lambda x, _, _1: x,
            merged=False,
        )

        assert coco_annotation["annotations"][0]["bbox"] == [0, 0, 960, 540]
        assert coco_annotation["annotations"][0]["segmentation"] == [
            [0.0, 0.0, 960.0, 0.0, 0.0, 540.0, 960.0, 540.0, 0.0, 0.0]
        ]
        # Here we have a self-intersecting polygon with 2 opposites triangles, so the area is
        # the sum of the areas of the 2 triangles.
        # Area of a triangle: base * height / 2
        assert coco_annotation["annotations"][0]["area"] == (960.0 * 270.0 / 2) * 2


def test__get_coco_image_annotation_area_with_negative_polygons():
    with TemporaryDirectory() as tmp_dir:
        job_name = "JOB_0"
        local_file_path = tmp_dir / Path("image1.jpg")
        image_width = 1920
        image_height = 1080
        Image.new("RGB", (image_width, image_height)).save(local_file_path)
        coco_annotation = convert_from_kili_to_coco_format(
            jobs={
                (job_name): {
                    "mlTask": "OBJECT_DETECTION",
                    "content": {
                        "categories": {
                            "OBJECT_A": {"name": "Object A"},
                            "OBJECT_B": {"name": "Object B"},
                        }
                    },
                    "instruction": "",
                    "isChild": False,
                    "isNew": False,
                    "isVisible": True,
                    "models": {},
                    "required": True,
                    "tools": ["semantic"],
                }
            },
            assets=[
                helpers.get_asset(
                    local_file_path,
                    with_annotation=[
                        {
                            "x": 0.0,
                            "y": 0.0,
                        },
                        {
                            "x": 0.5,
                            "y": 0.0,
                        },
                        {
                            "x": 0.0,
                            "y": 0.5,
                        },
                    ],
                    negative_polygons=[
                        [
                            {
                                "x": 0.1,
                                "y": 0.1,
                            },
                            {
                                "x": 0.4,
                                "y": 0.1,
                            },
                            {
                                "x": 0.1,
                                "y": 0.4,
                            },
                        ],
                        [
                            {
                                "x": 0.0,
                                "y": 0.0,
                            },
                            {
                                "x": 0.1,
                                "y": 0.0,
                            },
                            {
                                "x": 0.0,
                                "y": 0.1,
                            },
                        ],
                    ],
                )
            ],
            title="Test project",
            project_input_type="IMAGE",
            annotation_modifier=lambda x, _, _1: x,
            merged=False,
        )

        assert coco_annotation["annotations"][0]["bbox"] == [0, 0, 960, 540]
        assert coco_annotation["annotations"][0]["segmentation"] == [
            [0.0, 0.0, 960.0, 0.0, 0.0, 540.0],
            [192.0, 108.0, 768.0, 108.0, 192.0, 432.0],
            [0.0, 0.0, 192.0, 0.0, 0.0, 108.0],
        ]
        # Here we have a positive triangle with 2 negative triangles inside, so the area is the
        # area of the positive triangle minus the area of the negative triangles.
        # Area of a triangle: base * height / 2
        assert coco_annotation["annotations"][0]["area"] == (960.0 * 540.0 / 2) - (
            576.0 * 324.0 / 2
        ) - (192.0 * 108.0 / 2)


@pytest.mark.parametrize(
    ("name", "normalized_vertices", "expected_angle", "expected_bounding_box"),
    [
        (
            "rotated bbox",
            [
                {"x": 0.29542394060228344, "y": 0.5619730837117777},
                {"x": 0.36370176857458425, "y": 0.4036476855151382},
                {"x": 0.4595066260060737, "y": 0.5342261578662051},
                {"x": 0.3912287980337728, "y": 0.6925515560628448},
            ],
            37.47617956136133,
            [698.3073956632018, 435.93950035634924, 231.7840874775929, 215.46126441579023],
        ),
        (
            "horizontal bbox",
            [
                {"x": 0.57214895419755, "y": 0.8004988292446383},
                {"x": 0.57214895419755, "y": 0.5027584456173183},
                {"x": 0.6435613050929351, "y": 0.5027584456173183},
                {"x": 0.6435613050929351, "y": 0.8004988292446383},
            ],
            0.0,
            [1098.525992059296, 542.9791212667037, 137.1117137191393, 321.55961431750563],
        ),
    ],
)
def test__get_coco_image_annotations_with_label_modifier(
    name, normalized_vertices, expected_angle, expected_bounding_box
):
    with TemporaryDirectory() as tmp_dir:
        job_name = "JOB_0"

        image_width = 1920
        image_height = 1080
        local_file_path = tmp_dir / Path("image1.jpg")
        Image.new("RGB", (image_width, image_height)).save(local_file_path)

        expected_segmentation = [
            a for p in normalized_vertices for a in [p["x"] * image_width, p["y"] * image_height]
        ]

        coco_annotation = convert_from_kili_to_coco_format(
            jobs={
                (job_name): {
                    "mlTask": "OBJECT_DETECTION",
                    "content": {
                        "categories": {
                            "OBJECT_A": {"name": "Object A"},
                            "OBJECT_B": {"name": "Object B"},
                        }
                    },
                    "instruction": "",
                    "isChild": False,
                    "isNew": False,
                    "isVisible": True,
                    "models": {},
                    "required": True,
                    "tools": ["semantic"],
                }
            },
            assets=[
                helpers.get_asset(
                    local_file_path,
                    with_annotation=normalized_vertices,
                )
            ],
            title="Test project",
            project_input_type="IMAGE",
            annotation_modifier=helpers.estimate_rotated_bb_from_kili_poly,
            merged=False,
        )

        #### DON'T DELETE - for debugging #####
        # helpers.display_kili_and_coco_bbox(
        # local_file_path, expected_segmentation, coco_annotation
        # )
        ##########

        assert "Test project" in coco_annotation["info"]["description"]
        categories_by_id = {cat["id"]: cat["name"] for cat in coco_annotation["categories"]}
        assert coco_annotation["images"][0]["file_name"] == "data/image1.jpg"
        assert coco_annotation["images"][0]["width"] == image_width
        assert coco_annotation["images"][0]["height"] == image_height
        assert coco_annotation["annotations"][0]["image_id"] == 0
        assert categories_by_id[coco_annotation["annotations"][0]["category_id"]] == "OBJECT_A"
        assert coco_annotation["annotations"][0]["bbox"] == pytest.approx(expected_bounding_box)
        assert coco_annotation["annotations"][0]["attributes"] == {"rotation": expected_angle}
        assert coco_annotation["annotations"][0]["segmentation"][0] == pytest.approx(
            expected_segmentation
        )
        # Area of a rectangle: width * height
        assert coco_annotation["annotations"][0]["area"] == round(
            expected_bounding_box[2] * expected_bounding_box[3]
        )

        good_date = True
        try:
            datetime.strptime(coco_annotation["info"]["date_created"], "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            good_date = False
        assert good_date, (
            "The date is not in the right format: " + coco_annotation["info"]["date_created"]
        )


def test__get_coco_image_annotations_without_annotation():
    with TemporaryDirectory() as tmp_dir:
        job_name = "JOB_0"
        local_file_path = tmp_dir / Path("image1.jpg")
        image_width = 1920
        image_height = 1080
        Image.new("RGB", (image_width, image_height)).save(local_file_path)
        coco_annotation = convert_from_kili_to_coco_format(
            jobs={
                (job_name): {
                    "mlTask": "OBJECT_DETECTION",
                    "content": {
                        "categories": {
                            "OBJECT_A": {"name": "Object A"},
                            "OBJECT_B": {"name": "Object B"},
                        }
                    },
                    "instruction": "",
                    "isChild": False,
                    "isNew": False,
                    "isVisible": True,
                    "models": {},
                    "required": True,
                    "tools": ["semantic"],
                }
            },
            assets=[
                helpers.get_asset(
                    local_file_path,
                    with_annotation=None,
                )
            ],
            title="Test project",
            project_input_type="IMAGE",
            annotation_modifier=lambda x, _, _1: x,
            merged=False,
        )

        assert "Test project" in coco_annotation["info"]["description"]
        assert coco_annotation["images"][0]["file_name"] == "data/image1.jpg"
        assert coco_annotation["images"][0]["width"] == 1920
        assert coco_annotation["images"][0]["height"] == 1080
        assert len(coco_annotation["annotations"]) == 0


def test_coco_video_jsoncontent():
    json_interface = {
        "jobs": {
            "JOB_0": {
                "content": {
                    "categories": {
                        "OBJECT_A": {"children": [], "color": "#472CED", "name": "A"},
                        "OBJECT_B": {"children": [], "name": "B", "color": "#5CE7B7"},
                    },
                    "input": "radio",
                },
                "instruction": "dfgdfg",
                "mlTask": "OBJECT_DETECTION",
                "required": 1,
                "tools": ["rectangle"],
                "isChild": False,
                "models": {"tracking": {}},
            }
        }
    }
    job_object_detection = {
        "JOB_0": {
            "annotations": [
                {
                    "categories": [{"confidence": 100, "name": "OBJECT_A"}],
                    "": "JOB_0",
                    "mid": "2022040515434712-7532",
                    "mlTask": "OBJECT_DETECTION",
                    "boundingPoly": [
                        {
                            "normalizedVertices": [
                                {"x": 0.16504140348233334, "y": 0.7986938935103378},
                                {"x": 0.16504140348233334, "y": 0.2605618833516984},
                                {"x": 0.8377886490672706, "y": 0.2605618833516984},
                                {"x": 0.8377886490672706, "y": 0.7986938935103378},
                            ]
                        }
                    ],
                    "type": "rectangle",
                    "children": {},
                }
            ]
        }
    }
    asset_video_no_content_and_json_content = {
        "latestLabel": {
            "jsonResponse": {
                "0": {},
                "1": job_object_detection,
                "2": job_object_detection,
                **{str(i): {} for i in range(3, 5)},
            },
            "author": {"firstname": "Jean-Pierre", "lastname": "Dupont"},
        },
        "externalId": "video2",
        "content": "",
        "jsonContent": [],
    }
    # fill asset with jsonContent frames on disk
    with TemporaryDirectory() as tmp_dir_for_frames:
        for i, filelink in enumerate(
            [
                "https://storage.googleapis.com/label-public-staging/Frame/vid2_frame/video2-img000001.jpg",
                "https://storage.googleapis.com/label-public-staging/Frame/vid2_frame/video2-img000002.jpg",
                "https://storage.googleapis.com/label-public-staging/Frame/vid2_frame/video2-img000003.jpg",
                "https://storage.googleapis.com/label-public-staging/Frame/vid2_frame/video2-img000004.jpg",
                "https://storage.googleapis.com/label-public-staging/Frame/vid2_frame/video2-img000005.jpg",
            ]
        ):
            filepath = (
                Path(tmp_dir_for_frames)
                / f"{asset_video_no_content_and_json_content['externalId']}_{i + 1}.jpg"
            )
            with open(filepath, "wb") as f:
                f.write(requests.get(filelink, timeout=20).content)
            asset_video_no_content_and_json_content["jsonContent"].append(filepath)

        labels_json = convert_from_kili_to_coco_format(
            jobs={("JOB_0"): Job(**json_interface["jobs"]["JOB_0"])},
            assets=[asset_video_no_content_and_json_content],
            title="test",
            project_input_type="VIDEO",
            annotation_modifier=lambda x, _, _1: x,
            merged=False,
        )

        assert len(labels_json["images"]) == 5
        assert len(labels_json["annotations"]) == 2  # 2 frames with annotations

        assert [img["file_name"] for img in labels_json["images"]] == [
            f"data/video2_{i + 1}.jpg" for i in range(5)
        ]

        assert labels_json["annotations"][0]["image_id"] == 2
        assert labels_json["annotations"][1]["image_id"] == 3


def test_get_coco_geometry_from_kili_bpoly():
    boundingPoly = [
        {
            "normalizedVertices": [
                {"x": 0.1, "y": 0.1},
                {"x": 0.1, "y": 0.4},
                {"x": 0.8, "y": 0.4},
                {"x": 0.8, "y": 0.1},
            ]
        }
    ]
    boundingPoly_with_90_rotation = [
        {
            "normalizedVertices": [
                {"x": 0.9, "y": 0.1},
                {"x": 0.6, "y": 0.1},
                {"x": 0.6, "y": 0.8},
                {"x": 0.9, "y": 0.8},
            ]
        }
    ]
    boundingPoly_with_180_rotation = [
        {
            "normalizedVertices": [
                {"x": 0.9, "y": 0.9},
                {"x": 0.9, "y": 0.6},
                {"x": 0.2, "y": 0.6},
                {"x": 0.2, "y": 0.9},
            ]
        }
    ]
    boundingPoly_with_270_rotation = [
        {
            "normalizedVertices": [
                {"x": 0.1, "y": 0.9},
                {"x": 0.4, "y": 0.9},
                {"x": 0.4, "y": 0.2},
                {"x": 0.1, "y": 0.2},
            ]
        }
    ]
    image_width, image_height = 1920, 1080
    area, bbox, polygons = _get_coco_geometry_from_kili_bpoly(
        boundingPoly, image_width, image_height, 0
    )
    area_90_rotation, bbox_90_rotation, polygons_90_rotation = _get_coco_geometry_from_kili_bpoly(
        boundingPoly_with_90_rotation, image_width, image_height, 90
    )
    (
        area_180_rotation,
        bbox_180_rotation,
        polygons_180_rotation,
    ) = _get_coco_geometry_from_kili_bpoly(
        boundingPoly_with_180_rotation, image_width, image_height, 180
    )
    (
        area_270_rotation,
        bbox_270_rotation,
        polygons_270_rotation,
    ) = _get_coco_geometry_from_kili_bpoly(
        boundingPoly_with_270_rotation, image_width, image_height, 270
    )
    assert bbox == [192, 108, 1344, 324]
    assert bbox_90_rotation == [192, 108, 1344, 324]
    assert bbox_180_rotation == [192, 108, 1344, 324]
    assert bbox_270_rotation == [192, 108, 1344, 324]

    assert area == bbox[2] * bbox[3]  # Area of a rectangle: width * height
    assert area_90_rotation == bbox_90_rotation[2] * bbox_90_rotation[3]
    assert area_180_rotation == bbox_180_rotation[2] * bbox_180_rotation[3]
    assert area_270_rotation == bbox_270_rotation[2] * bbox_270_rotation[3]

    assert bbox[0] == 0.1 * image_width
    assert bbox[1] == 0.1 * image_height
    assert bbox[2] == round((0.8 - 0.1) * image_width)
    assert bbox[3] == round((0.4 - 0.1) * image_height)

    assert bbox_90_rotation[0] == 0.1 * image_width
    assert bbox_90_rotation[1] == 0.1 * image_height
    assert bbox_90_rotation[2] == round((0.8 - 0.1) * image_width)
    assert bbox_90_rotation[3] == round((0.4 - 0.1) * image_height)

    assert bbox_180_rotation[0] == 0.1 * image_width
    assert bbox_180_rotation[1] == 0.1 * image_height
    assert bbox_180_rotation[2] == round((0.8 - 0.1) * image_width)
    assert bbox_180_rotation[3] == round((0.4 - 0.1) * image_height)

    assert bbox_270_rotation[0] == 0.1 * image_width
    assert bbox_270_rotation[1] == 0.1 * image_height
    assert bbox_270_rotation[2] == round((0.8 - 0.1) * image_width)
    assert bbox_270_rotation[3] == round((0.4 - 0.1) * image_height)

    assert polygons == [[192.0, 108.0, 192.0, 432.0, 1536.0, 432.0, 1536.0, 108.0]]


def test__get_kili_cat_id_to_coco_cat_id_mapping_with_split_jobs():
    jobs = {("DESSERT_JOB"): helpers.DESSERT_JOB}

    kili_cat_id_to_coco_cat_id, coco_categories = _get_coco_categories_with_mapping(
        jobs, merged=False
    )
    assert kili_cat_id_to_coco_cat_id == {"DESSERT_JOB": {"APPLE_PIE": 0, "TIRAMISU": 1}}

    assert coco_categories == [
        {"id": 0, "name": "APPLE_PIE", "supercategory": "DESSERT_JOB"},
        {"id": 1, "name": "TIRAMISU", "supercategory": "DESSERT_JOB"},
    ]


def test__get_kili_cat_id_to_coco_cat_id_mapping_with_merged_jobs():
    jobs = {("MAIN_JOB"): helpers.MAIN_JOB, ("DESSERT_JOB"): helpers.DESSERT_JOB}

    kili_cat_id_to_coco_cat_id, coco_categories = _get_coco_categories_with_mapping(
        jobs, merged=True
    )

    assert kili_cat_id_to_coco_cat_id == {
        "DESSERT_JOB": {"APPLE_PIE": 0, "TIRAMISU": 1},
        "MAIN_JOB": {"SPAGHETTIS": 3, "PIZZA": 2},
    }

    assert coco_categories == [
        {"id": 0, "name": "DESSERT_JOB/APPLE_PIE", "supercategory": "DESSERT_JOB"},
        {"id": 1, "name": "DESSERT_JOB/TIRAMISU", "supercategory": "DESSERT_JOB"},
        {"id": 2, "name": "MAIN_JOB/PIZZA", "supercategory": "MAIN_JOB"},
        {"id": 3, "name": "MAIN_JOB/SPAGHETTIS", "supercategory": "MAIN_JOB"},
    ]


def test_coco_export_with_multi_jobs():
    json_response_dessert = {
        "author": {"firstname": "Jean-Pierre", "lastname": "Dupont"},
        "DESSERT_JOB": {
            "annotations": [
                {
                    "categories": [
                        {
                            "name": "APPLE_PIE",
                            "confidence": 100,
                        }
                    ],
                    "boundingPoly": [
                        {
                            "normalizedVertices": [
                                {"x": 0.1, "y": 0.1},
                                {"x": 0.1, "y": 0.4},
                                {"x": 0.8, "y": 0.4},
                                {"x": 0.8, "y": 0.1},
                            ]
                        }
                    ],
                }
            ]
        },
    }

    json_response_main = {
        "author": {"firstname": "Jean-Pierre", "lastname": "Dupont"},
        "MAIN_JOB": {
            "annotations": [
                {
                    "categories": [
                        {
                            "name": "SPAGHETTIS",
                            "confidence": 100,
                        }
                    ],
                    "boundingPoly": [
                        {
                            "normalizedVertices": [
                                {"x": 0.1, "y": 0.1},
                                {"x": 0.1, "y": 0.4},
                                {"x": 0.8, "y": 0.4},
                                {"x": 0.8, "y": 0.1},
                            ]
                        }
                    ],
                }
            ]
        },
    }

    with TemporaryDirectory() as output_dir:
        local_file_path = Path(output_dir) / Path("image1.jpg")
        image_width = 1920
        image_height = 1080
        Image.new("RGB", (image_width, image_height)).save(local_file_path)
        assets = [
            {
                "latestLabel": {"jsonResponse": json_response_dessert},
                "externalId": "car_1",
                "jsonContent": "",
                "content": str(Path(output_dir) / Path("image1.jpg")),
            },
            {
                "latestLabel": {"jsonResponse": json_response_main},
                "externalId": "car_2",
                "jsonContent": "",
                "content": str(Path(output_dir) / Path("image1.jpg")),
            },
        ]

        labels_json = convert_from_kili_to_coco_format(
            {("MAIN_JOB"): helpers.MAIN_JOB, ("DESSERT_JOB"): helpers.DESSERT_JOB},
            assets,
            "Multi job project",
            "IMAGE",
            annotation_modifier=None,
            merged=True,
        )

        assert len(labels_json["images"]) == 2
        assert len(labels_json["annotations"]) == 2  # 2 frames with annotations
        categories_by_id = {cat["id"]: cat["name"] for cat in labels_json["categories"]}

        assert labels_json["annotations"][0]["image_id"] == 0
        assert labels_json["annotations"][1]["image_id"] == 1

        assert labels_json["categories"] == [
            {"id": 0, "name": "DESSERT_JOB/APPLE_PIE", "supercategory": "DESSERT_JOB"},
            {"id": 1, "name": "DESSERT_JOB/TIRAMISU", "supercategory": "DESSERT_JOB"},
            {"id": 2, "name": "MAIN_JOB/PIZZA", "supercategory": "MAIN_JOB"},
            {"id": 3, "name": "MAIN_JOB/SPAGHETTIS", "supercategory": "MAIN_JOB"},
        ]

        assert (
            categories_by_id[labels_json["annotations"][0]["category_id"]]
            == "DESSERT_JOB/APPLE_PIE"
        )
        assert (
            categories_by_id[labels_json["annotations"][1]["category_id"]] == "MAIN_JOB/SPAGHETTIS"
        )
