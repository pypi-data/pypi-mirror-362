from __future__ import annotations

import json
import re
from pathlib import Path

from .errors import (
    ManifestValidationError,
)


def validate_manifest(manifest_path):
    manifest_file = Path(manifest_path).open("r", encoding="utf-8", errors="ignore")  # noqa: SIM115
    manifest_file_content = manifest_file.read()
    json_manifest = json.loads(manifest_file_content, strict=False)
    json_manifest_dict = dict(json_manifest)

    for index1, investigation in json_manifest_dict["investigations"]:
        if investigation["name"] == "" or None:
            msg = f"Investigation {index1} has no name"
            raise ManifestValidationError(msg)
        if bool(re.search(r"\s", investigation["name"])) is True:
            msg = f"{investigation['name']} has spaces and is not a valid name for an investigation"
            raise ManifestValidationError(msg)
        if investigation["owner"] == "" or None:
            msg = f"Investigation {index1} has no valid owner"
            raise ManifestValidationError(msg)
        if investigation["owner"] not in investigation["members"]:
            msg = "Investigation owner not in members"
            raise ManifestValidationError(msg)
        for child_study_id in investigation["children"]:
            for index2, study in json_manifest_dict["studies"]:
                if (
                    str(child_study_id) == str(study["id"])
                    and study["owner"] != investigation["owner"]
                ):
                    msg = f"No match between study {index2} and investigation {index1} owner"
                    raise ManifestValidationError(msg)

    for index1, study in json_manifest_dict["studies"]:
        if study["name"] == "" or None:
            msg = f"Study {index1} has no name"
            raise ManifestValidationError(msg)
        if study["owner"] == "" or None:
            msg = f"Study {index1} has no valid owner"
            raise ManifestValidationError(msg)
        for index2, investigation in json_manifest_dict["investigations"]:
            if (
                study["id"]
                not in json_manifest_dict["investigations"][index2]["children"]
            ):
                msg = f"Study {index1} not in valid investigation"
                raise ManifestValidationError(msg)
            if investigation["id"] not in study["parents"]:
                msg = f"Study {index1} does not have valid parents"
                raise ManifestValidationError(msg)
        for child_assay_id in study["children"]:
            for index3, assay in json_manifest_dict["assays"]:
                if (
                    str(child_assay_id) == str(assay["id"])
                    and assay["owner"] != study["owner"]
                ):
                    msg = f"No match between assay {index3} and study {index1} owner"
                    raise ManifestValidationError(msg)

    for index1, assay in json_manifest_dict["assays"]:
        if assay["name"] == "" or None:
            msg = f"Assay {index1} has no name"
            raise ManifestValidationError(msg)
        if assay["owner"] == "" or None:
            msg = f"Assay {index1} has no valid owner"
            raise ManifestValidationError(msg)
        for index2, study in json_manifest_dict["studies"]:
            if assay["id"] not in json_manifest_dict["studies"][index2]["children"]:
                msg = f"Assay {index1} not in valid study"
                raise ManifestValidationError(msg)
            if study["id"] not in assay["parents"]:
                msg = f"Assay {index1} does not have valid parents"
                raise ManifestValidationError(msg)
