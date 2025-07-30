from __future__ import annotations

from pathlib import Path

import aicsimageio
import ffmpeg
import imageio
import numpy as np
import skimage
from aicsimageio import AICSImage

dtype_map = {
    "uint8": np.uint8,
    "uint16": np.uint16,
    "uint32": np.uint32,
}


class VignetteGenerator:
    def __init__(self, image_path):
        self.image_path = image_path
        self.vignette_numpy_array = self.vignette_pipeline()
        self.vignette_path = str(self.set_current_vignette_name_stub()) + ".gif"

    def make_fused_channels(self, aics_image):
        """
        For cosmic rays correction, use this. Otherwise, too saturated:

            retransposed_transposed_aics_image_numpy_array = (
                retransposed_transposed_aics_image_numpy_array
                * (
                    256
                    / (
                        1
                        + np.quantile(
                            retransposed_transposed_aics_image_numpy_array, 0.99
                        )  # for cosmic rays
                        - np.quantile(retransposed_transposed_aics_image_numpy_array, 0.01)
                    )
                )
            ).astype(np.uint8)
        """
        transposed_aics_image = aicsimageio.transforms.transpose_to_dims(
            aics_image, "TCZYX", "CTZYX"
        )
        bit_depth = aics_image.dtype
        max_value_original_depth = np.iinfo(bit_depth).max
        max_value_8_bit = 255

        new_C_squashed_image = np.sum(transposed_aics_image, axis=0)
        # new_C_squashed_image = skimage.color.gray2rgb(new_C_squashed_image, channel_axis=0)
        new_C_squashed_image = np.expand_dims(new_C_squashed_image, 0)

        retransposed_transposed_aics_image = aicsimageio.transforms.transpose_to_dims(
            new_C_squashed_image, "CTZYX", "TCZYX"
        )

        return (
            retransposed_transposed_aics_image
            * (max_value_8_bit / max_value_original_depth)
        ).astype(np.uint8)

    def make_Z_project(self, aics_image, method_name="max"):
        transposed_aics_image = aicsimageio.transforms.transpose_to_dims(
            aics_image, "TCZYX", "ZCTYX"
        )
        # digit_type = dtype_map[bit_depth]

        if method_name == "max":
            z_projected_channel_transposed_image = np.max(transposed_aics_image, axis=0)
        elif method_name == "min":
            z_projected_channel_transposed_image = np.min(transposed_aics_image, axis=0)
        elif method_name == "sum":
            z_projected_channel_transposed_image = np.sum(transposed_aics_image, axis=0)
        elif method_name == "average":
            z_projected_channel_transposed_image = np.mean(
                transposed_aics_image, axis=0
            )
        elif method_name == "median":
            z_projected_channel_transposed_image = np.median(
                transposed_aics_image, axis=0
            )
        elif method_name == "sd":
            z_projected_channel_transposed_image = np.std(transposed_aics_image, axis=0)
        else:
            msg = "invalid value for argument `method_name`"
            raise ValueError(msg)

        z_projected_channel_transposed_image = np.expand_dims(
            z_projected_channel_transposed_image, 0
        )
        return aicsimageio.transforms.transpose_to_dims(
            z_projected_channel_transposed_image, "ZCTYX", "TCZYX"
        )

    def resize_image(self, aics_image, new_width, new_height):
        number_of_timeframes = aics_image.shape[0]
        number_of_channels = aics_image.shape[1]
        z_depth_by_channel = aics_image.shape[2]
        return skimage.transform.resize(
            aics_image,
            (
                number_of_timeframes,
                number_of_channels,
                z_depth_by_channel,
                new_height,
                new_width,
            ),
            order=1,
            mode="reflect",
            cval=0,
            clip=True,
            preserve_range=True,
            anti_aliasing=None,
            anti_aliasing_sigma=None,
        )

    def vignette_pipeline(self):
        image_file_path = self.image_path
        aics_image = AICSImage(image_file_path)
        z_project_method_name = "max"
        thumbnail_height = 256
        thumbnail_width = 256

        aics_image_numpy_array = aics_image.data
        array_image_1 = self.make_Z_project(
            aics_image_numpy_array, z_project_method_name
        )
        array_image_2 = self.make_fused_channels(array_image_1)
        return self.resize_image(array_image_2, thumbnail_height, thumbnail_width)

    def set_vignettes_path(self):
        image_directory = Path(self.image_path).parents[0]
        vignettes_directory = str(image_directory) + "/vignettes"
        Path(vignettes_directory).mkdir(parents=True, exist_ok=True)
        return vignettes_directory

    def set_current_vignette_name_stub(self):
        vignettes_path = self.set_vignettes_path()
        image_name = Path(self.image_path).parts[-1]
        return str(vignettes_path) + "/" + str(image_name) + "_vignette"

    def save_image_as_gif(self):
        # print("Array: "+str(numpy_array))
        # vignette_stub = self.set_current_vignette_name_stub()
        vignette_path = str(self.vignette_path)
        numpy_array = self.vignette_numpy_array
        np_squeezed = np.squeeze(numpy_array, axis=(1, 2))
        imageio.mimwrite(vignette_path, np_squeezed, loop=0)

    def save_image_as_mp4_ffmpeg(
        self, framerate=60, vcodec="libx264"
    ):  # https://github.com/kkroening/ffmpeg-python/issues/246
        vignette_stub = self.set_current_vignette_name_stub()
        numpy_array = self.vignette_numpy_array
        number, height, width, channels = numpy_array.shape
        process = (
            ffmpeg.input(
                "pipe:",
                format="rawvideo",
                pix_fmt="rgb24",
                s=f"{width}x{height}",
            )
            .output(vignette_stub, pix_fmt="yuv420p", vcodec=vcodec, r=framerate)
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )
        for frame in numpy_array:
            process.stdin.write(frame.astype(np.uint8).tobytes())
        process.stdin.close()
        # process.wait()
