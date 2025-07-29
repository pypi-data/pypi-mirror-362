import os
import glob
import math

from ..utils import create_aoi_geodataframe, format_datetime_param


class SHDownloader:
    def __init__(self, download_folder):
        try:
            from sentinelhub import SHConfig
        except ImportError:
            raise ImportError(
                "The sentinelhub package is required. Please install it with 'pip install sentinelhub' and try again."
            )
        try:
            from dotenv import load_dotenv

            load_dotenv()
        except ImportError:
            raise ImportError(
                "The python-dotenv package is required. Please install it with 'pip install python-dotenv' and try again."
            )
        self.download_folder = download_folder
        self.config = SHConfig()
        try:
            self.config.sh_client_id = os.environ["SH_CLIENT_ID"]
            self.config.sh_client_secret = os.environ["SH_CLIENT_SECRET"]
        except KeyError:
            # There is not SH_CLIENT_ID and SH_CLIENT_SECRET in the environment
            raise KeyError(
                "Please set the SH_CLIENT_ID and SH_CLIENT_SECRET environment variables."
            )
        self.mosaicking_order = None

    def compute_image_size(self, gdf):
        from sentinelhub import CRS, BBox, bbox_to_dimensions

        self.bbox = BBox(bbox=gdf.total_bounds.tolist(), crs=CRS.WGS84)
        self.bbox_size = bbox_to_dimensions(self.bbox, resolution=self.resolution)
        return self.bbox_size

    def download(self, aoi, date):
        gdf = create_aoi_geodataframe(aoi)
        self.time_interval = format_datetime_param(date)
        self.compute_image_size(gdf)
        if self.bbox_size[0] > 2500 or self.bbox_size[1] > 2500:
            return self.download_large_area(gdf)
            # raise Exception("Area too large")
        return self.download_small_area(self.bbox)

    def request_bands(self, bbox):
        from sentinelhub import (
            bbox_to_dimensions,
            SentinelHubRequest,
            MimeType,
        )

        return SentinelHubRequest(
            data_folder=self.download_folder,
            evalscript=self.script,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=self.data_collection,
                    time_interval=self.time_interval,
                    mosaicking_order=self.mosaicking_order,
                )
            ],
            responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
            bbox=self.bbox,
            size=bbox_to_dimensions(bbox, resolution=self.resolution),
            config=self.config,
        )

    def download_small_area(self, bbox):
        request_bands = self.request_bands(bbox)
        request_bands.save_data()
        downloaded_files = glob.glob(f"{self.download_folder}/*/response.tiff")
        if len(downloaded_files) == 0:
            raise Exception("No files downloaded, check your configuration and parameters")
        folder = downloaded_files[0]
        return folder

    def get_tiles(self):
        # compute number of images to download
        self.max_resolution = 2500
        return (
            math.ceil(self.bbox_size[0] / self.max_resolution),
            math.ceil(self.bbox_size[1] / self.max_resolution),
        )

    def download_large_area(self, gdf):
        tiles = self.get_tiles()
        geom = gdf.geometry.unary_union  # ???
        bbox_splitter = BBoxSplitter([geom], CRS.WGS84, tiles)
        bbox_list = bbox_splitter.get_bbox_list()
        for i, bbox in enumerate(bbox_list):
            request_bands = self.request_bands(bbox)
            request_bands.save_data()
        downloaded_files = glob.glob(f"{self.download_folder}/*/response.tiff")
        dst_path = self.download_folder + "/output.tiff"
        command = f"gdal_merge.py -o {dst_path} " + " ".join(downloaded_files)
        os.system(command)
        return dst_path
