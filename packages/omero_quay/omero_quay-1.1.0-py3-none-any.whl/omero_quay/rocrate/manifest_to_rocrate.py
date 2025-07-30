from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from jinja2 import Environment, PackageLoader
from rocrate_validator import models, services

from ..core.interface import Interface

try:
    from .vignette_generator import VignetteGenerator
except ImportError:
    VignetteGenerator = None

log = logging.getLogger(__name__)

SRC_DIR = Path(__file__).parent.parent.resolve()


jinja_env = Environment(
    loader=PackageLoader("omero_quay"),
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)

templates = SRC_DIR / "templates"
icons = SRC_DIR / "icons"

rocrate_template_path = templates / "ro-crate-metadata.json.j2"
html_template_path = templates / "html_rocrate_main_page_template.j2"
index_template_path = templates / "ro-crate-preview.html.j2"


investigation_icon_path = icons / "investigation.svg"
study_icon_path = icons / "study.svg"
assay_icon_path = icons / "assay.svg"


class RocrateGenerator(Interface):
    """
    Generate RO-Crate metadata and preview for each investigation in the manifest
    """

    def __init__(self, conf, manifest):
        super().__init__(conf, manifest, scheme="file", host=os.uname().nodename)
        self.rocrate_output = None
        self.rocrate_filename = None
        self.html_output = None
        self.pipeline()

    def pipeline(self):
        self.render_rocrate_json_file()
        enriched_rocrate_output = self.rocrate_output
        # enriched_rocrate_output = self.create_vignettes_from_manifest(
        # self.rocrate_output
        # )
        self.render_rocrate_html_file(enriched_rocrate_output)

    def render_rocrate_json_file(self):
        rocrate_file_name = "ro-crate-metadata.json"
        self.rocrate_filename = rocrate_file_name
        template = jinja_env.get_template("ro-crate-metadata.json.j2")
        self.rocrate_output = template.render(
            filename=self.rocrate_filename,
            manifest=self.manifest,
            investigation=self.manifest.investigations[0],
        )

    def create_vignettes_from_manifest(self, json_content):
        json_string = json.loads(json_content, strict=False)
        json_dict = dict(json_string)
        for investigation_item in self.manifest.investigations:
            for rocrate_item in json_dict["@graph"]:
                if rocrate_item["@id"] == investigation_item.id:
                    rocrate_item["thumbnailUrl"] = investigation_icon_path
        for study_item in self.manifest.studies:
            for rocrate_item in json_dict["@graph"]:
                if rocrate_item["@id"] == study_item.id:
                    rocrate_item["thumbnailUrl"] = study_icon_path
        for assay_item in self.manifest.assays:
            for rocrate_item in json_dict["@graph"]:
                if rocrate_item["@id"] == assay_item.id:
                    rocrate_item["thumbnailUrl"] = assay_icon_path
        for item in self.manifest.images:
            # print("IMAGE_ITEM: " + str(item))
            item_path = item.importlink.srce_url
            item_vignette_generator = VignetteGenerator(item_path)
            item_vignette_generator.save_image_as_gif()
            for rocrate_item in json_dict["@graph"]:
                if rocrate_item["@id"] == item.id:
                    rocrate_item["thumbnailUrl"] = item_vignette_generator.vignette_path
        return json.dumps(json_dict, indent=2)

    def dump_json_file(self):
        json_content = self.rocrate_output
        with Path(self.rocrate_filename).open("w", encoding="utf-8") as fh:
            fh.write(json_content)
        fh.close()

    def render_rocrate_html_file(self, json_content):
        json_string = json.loads(json_content, strict=False)
        json_dict = dict(json_string)
        template = jinja_env.get_template("ro-crate-preview.html.j2")
        self.html_output = template.render(input=json_dict)

    def dump_html_file(self):
        html_file_name = "rocrate_index_preview.html"
        html_content = self.html_output
        with Path(html_file_name).open("w", encoding="utf-8") as fh:
            fh.write(html_content)
        fh.close()

    def validate_rocrate_file(self):
        # Create an instance of `ValidationSettings` class to configure the validation
        settings = services.ValidationSettings(
            # Set the path to the RO-Crate root directory
            rocrate_uri=str(self.rocrate_filename),
            # Set the identifier of the RO-Crate profile to use for validation.
            # If not set, the system will attempt to automatically determine the appropriate validation profile.
            profile_identifier="ro-crate-1.1",
            # Set the requirement level for the validation
            requirement_severity=models.Severity.REQUIRED,
        )

        # Call the validation service with the settings
        result = services.validate(settings)

        # Check if the validation was successful
        if not result.has_issues():
            log.info("RO-Crate is valid!")
            return True
        log.info("RO-Crate is invalid!")
        # Explore the issues
        for issue in result.get_issues():
            # Every issue object has a reference to the check that failed, the severity of the issue, and a message describing the issue.
            log.info(
                f'Detected issue of severity {issue.severity.name} with check "{issue.check.identifier}": {issue.message}'
            )
        return False
