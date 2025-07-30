from typing import Union, List, Set

from time import sleep
from traceback import format_exception
from os.path import abspath, expanduser, join, exists
import logging
from datetime import date, datetime, time, timedelta
from dateutil import parser

import pandas as pd

import earthaccess

import colored_logging as cl

import numpy as np

import rasters as rt
from rasters import Raster

from .constants import *
from .exceptions import *
from .login import login
from .HLS_connection import HLSConnection
from .get_CMR_granule_ID import get_CMR_granule_ID
from .HLS2_sentinel_granule import HLS2SentinelGranule
from .HLS2_landsat_granule import HLS2LandsatGranule
from .HLS_CMR_query import HLS_CMR_query
from .timer import Timer
from .daterange import date_range

logger = logging.getLogger(__name__)

class HLS2CMRConnection(HLSConnection):
    URL = CMR_SEARCH_URL

    def __init__(
            self,
            working_directory: str = None,
            download_directory: str = None,
            target_resolution: int = None,
            retries: int = DEFAULT_RETRIES,
            wait_seconds: float = DEFAULT_WAIT_SECONDS):
        if target_resolution is None:
            target_resolution = self.DEFAULT_TARGET_RESOLUTION

        if working_directory is None:
            working_directory = abspath(".")

        working_directory = expanduser(working_directory)
        logger.debug(f"HLS 2.0 working directory: {cl.dir(working_directory)}")

        if download_directory is None:
            download_directory = join(working_directory, DOWNLOAD_DIRECTORY)

        logger.debug(f"HLS 2.0 download directory: {cl.dir(download_directory)}")

        self.auth = login()

        super(HLS2CMRConnection, self).__init__(
            working_directory=working_directory,
            download_directory=download_directory,
            target_resolution=target_resolution
        )

        self.retries = retries
        self.wait_seconds = wait_seconds

        self._listing = pd.DataFrame([], columns=["date_UTC", "tile", "sentinel", "landsat"])
        self._granules = pd.DataFrame([], columns=["ID", "sensor", "tile", "date_UTC", "granule"])

    def date_directory(self, date_UTC: Union[date, str]) -> str:
        if isinstance(date_UTC, str):
            date_UTC = parser.parse(date_UTC).date()

        directory = join(self.download_directory, f"{date_UTC:%Y.%m.%d}")

        return directory

    def sentinel_directory(self, granule: earthaccess.search.DataGranule, date_UTC: Union[date, str]) -> str:
        date_directory = self.date_directory(date_UTC=date_UTC)
        granule_directory = join(date_directory, get_CMR_granule_ID(granule))

        return granule_directory

    def landsat_directory(self, granule: earthaccess.search.DataGranule, tile: str, date_UTC: Union[date, str]) -> str:
        if self.check_unavailable_date("Landsat", tile, date_UTC):
            raise HLSLandsatNotAvailable(f"Landsat is not available at tile {cl.place(tile)} on {cl.time(date_UTC)}")

        date_directory = self.date_directory(date_UTC=date_UTC)
        granule_directory = join(date_directory, get_CMR_granule_ID(granule))

        return granule_directory

    def sentinel(self, tile: str, date_UTC: Union[date, str]) -> HLS2SentinelGranule:
        if isinstance(date_UTC, str):
            date_UTC = parser.parse(date_UTC).date()

        logger.info(f"searching for Sentinel tile {cl.name(tile)} on {cl.time(date_UTC)}")
        granule: earthaccess.search.DataGranule
        granule = self.sentinel_granule(tile=tile, date_UTC=date_UTC)
        directory = self.sentinel_directory(granule, date_UTC=date_UTC)

        # TODO: login dude
        logger.info(f"retrieving Sentinel tile {cl.name(tile)} on {cl.time(date_UTC)}: {directory}")
        file_paths = earthaccess.download(granule, abspath(expanduser(directory)))
        for download_file_path in file_paths:
            if isinstance(download_file_path, Exception):
                raise HLSDownloadFailed("Error when downloading HLS2 files") from download_file_path

        hls_granule = HLS2SentinelGranule(directory)

        return hls_granule

    def landsat(self, tile: str, date_UTC: Union[date, str]) -> HLS2LandsatGranule:
        if isinstance(date_UTC, str):
            date_UTC = parser.parse(date_UTC).date()

        logger.info(f"searching for Landsat tile {cl.name(tile)} on {cl.time(date_UTC)}")
        granule: earthaccess.search.DataGranule
        granule = self.landsat_granule(tile=tile, date_UTC=date_UTC)
        directory = self.landsat_directory(granule, tile=tile, date_UTC=date_UTC)

        logger.info(f"retrieving Landsat tile {cl.name(tile)} on {cl.time(date_UTC)}: {directory}")
        file_paths = earthaccess.download(granule, abspath(expanduser(directory)))
        for download_file_path in file_paths:
            if isinstance(download_file_path, Exception):
                raise HLSDownloadFailed("Error when downloading HLS2 files") from download_file_path

        hls_granule = HLS2LandsatGranule(directory)

        return hls_granule

    def NDVI(
            self,
            tile: str,
            date_UTC: Union[date, str],
            **kwargs) -> Raster:
        """
        Retrieve the NDVI (Normalized Difference Vegetation Index) raster for a given HLS tile and date.
    
        This method attempts to retrieve the NDVI data for the specified tile and date
        from both Sentinel-2 (S30) and Landsat-8/9 (L30) HLS products. If both are available,
        it computes the mean NDVI. If only one is available, it uses that. If neither is
        available, it raises an exception.
    
        The returned NDVI raster is resampled to the target resolution if necessary.
    
        Parameters
        ----------
        tile : str
            The HLS tile identifier (e.g., '10SEG'). May include sub-tile info, but only the first 5 characters are used for data retrieval.
        date_UTC : Union[date, str]
            The UTC date for which to retrieve the NDVI. Can be a `date` object or an ISO-format string.
        **kwargs
            Additional keyword arguments (currently unused).
    
        Returns
        -------
        Raster
            The NDVI raster for the specified tile and date, resampled to the target resolution.
    
        Raises
        ------
        HLSNotAvailable
            If neither Sentinel nor Landsat data is available for the given tile and date.
        HLSSentinelMissing, HLSLandsatMissing
            If the granule is missing on the remote server.
        HLSBandNotAcquired
            If the NDVI band is not available in the granule.
    
        Notes
        -----
        - If both Sentinel and Landsat data are available, the mean NDVI is computed.
        - The raster is resampled to the target resolution using "average" (if >30m) or "cubic" (if <30m).
        """
    
        # Save the original tile and its geometry for later use
        target_tile = tile
        target_geometry = self.grid(target_tile)
    
        # Use only the first 5 characters of the tile for data retrieval
        tile = tile[:5]
        geometry = self.grid(tile)
    
        # Attempt to retrieve Sentinel granule for the tile and date
        try:
            sentinel = self.sentinel(tile=tile, date_UTC=date_UTC)
        except HLSSentinelNotAvailable:
            sentinel = None
        except HLSSentinelMissing as e:
            raise e
    
        # Attempt to retrieve Landsat granule for the tile and date
        try:
            landsat = self.landsat(tile=tile, date_UTC=date_UTC)
        except HLSLandsatNotAvailable:
            landsat = None
        except HLSLandsatMissing as e:
            raise e
    
        # Handle cases where neither, one, or both granules are available
        if sentinel is None and landsat is None:
            # No data available from either source
            raise HLSNotAvailable(f"HLS2 is not available at {tile} on {date_UTC}")
        elif sentinel is not None and landsat is None:
            # Only Sentinel data is available
            try:
                NDVI = sentinel.NDVI
            except HLSBandNotAcquired:
                raise HLSNotAvailable(f"HLS2 S30 is not available at {tile} on {date_UTC}")
        elif sentinel is None and landsat is not None:
            # Only Landsat data is available
            try:
                NDVI = landsat.NDVI
            except HLSBandNotAcquired:
                raise HLSNotAvailable(f"HLS2 L30 is not available at {tile} on {date_UTC}")
        else:
            # Both Sentinel and Landsat data are available; compute mean NDVI
            NDVI = rt.Raster(
                np.nanmean(np.dstack([sentinel.NDVI, landsat.NDVI]), axis=2),
                geometry=sentinel.geometry
            )
    
        # Resample the raster to the target resolution if needed
        if self.target_resolution > 30:
            # Downsample using average resampling
            NDVI = NDVI.to_geometry(geometry, resampling="average")
        elif self.target_resolution < 30:
            # Upsample using cubic resampling
            NDVI = NDVI.to_geometry(geometry, resampling="cubic")

        return NDVI

    def albedo(
            self,
            tile: str,
            date_UTC: Union[date, str],
            **kwargs) -> Raster:
        """
        Retrieve the surface albedo raster for a given HLS tile and date.
    
        This method attempts to retrieve the albedo data for the specified tile and date
        from both Sentinel-2 (S30) and Landsat-8/9 (L30) HLS products. If both are available,
        it computes the mean albedo. If only one is available, it uses that. If neither is
        available, it raises an exception.
    
        The returned albedo raster is resampled to the target resolution if necessary.
    
        Parameters
        ----------
        tile : str
            The HLS tile identifier (e.g., '10SEG'). May include sub-tile info, but only the first 5 characters are used for data retrieval.
        date_UTC : Union[date, str]
            The UTC date for which to retrieve the albedo. Can be a `date` object or an ISO-format string.
        **kwargs
            Additional keyword arguments (currently unused).
    
        Returns
        -------
        Raster
            The surface albedo raster for the specified tile and date, resampled to the target resolution.
    
        Raises
        ------
        HLSNotAvailable
            If neither Sentinel nor Landsat data is available for the given tile and date.
        HLSSentinelMissing, HLSLandsatMissing
            If the granule is missing on the remote server.
        HLSBandNotAcquired
            If the albedo band is not available in the granule.
    
        Notes
        -----
        - If both Sentinel and Landsat data are available, the mean albedo is computed.
        - The raster is resampled to the target resolution using "average" (if >30m) or "cubic" (if <30m).
        """
    
        # Save the original tile and its geometry for later use
        target_tile = tile
        target_geometry = self.grid(target_tile)
    
        # Use only the first 5 characters of the tile for data retrieval
        tile = tile[:5]
        geometry = self.grid(tile)
    
        # Attempt to retrieve Sentinel granule for the tile and date
        try:
            sentinel = self.sentinel(tile=tile, date_UTC=date_UTC)
        except HLSSentinelNotAvailable:
            sentinel = None
        except HLSSentinelMissing as e:
            raise e
    
        # Attempt to retrieve Landsat granule for the tile and date
        try:
            landsat = self.landsat(tile=tile, date_UTC=date_UTC)
        except HLSLandsatNotAvailable:
            landsat = None
        except HLSLandsatMissing as e:
            raise e
    
        # Handle cases where neither, one, or both granules are available
        if sentinel is None and landsat is None:
            # No data available from either source
            raise HLSNotAvailable(f"HLS2 is not available at {tile} on {date_UTC}")
        elif sentinel is not None and landsat is None:
            # Only Sentinel data is available
            try:
                albedo = sentinel.albedo
            except HLSBandNotAcquired:
                raise HLSNotAvailable(f"HLS2 S30 is not available at {tile} on {date_UTC}")
        elif sentinel is None and landsat is not None:
            # Only Landsat data is available
            try:
                albedo = landsat.albedo
            except HLSBandNotAcquired:
                raise HLSNotAvailable(f"HLS2 L30 is not available at {tile} on {date_UTC}")
        else:
            # Both Sentinel and Landsat data are available; compute mean albedo
            albedo = rt.Raster(
                np.nanmean(np.dstack([sentinel.albedo, landsat.albedo]), axis=2),
                geometry=sentinel.geometry
            )
    
        # Resample the raster to the target resolution if needed
        if self.target_resolution > 30:
            # Downsample using average resampling
            albedo = albedo.to_geometry(geometry, resampling="average")
        elif self.target_resolution < 30:
            # Upsample using cubic resampling
            albedo = albedo.to_geometry(geometry, resampling="cubic")

        return albedo

    def search(
            self,
            tile: str = None,
            start_UTC: Union[date, datetime, str] = None,
            end_UTC: Union[date, datetime, str] = None,
            collections: List[str] = None,
            IDs: List[str] = None,
            page_size: int = PAGE_SIZE):
        if isinstance(start_UTC, str):
            start_UTC = parser.parse(start_UTC)

            if start_UTC.time() == time(0, 0, 0):
                start_UTC = start_UTC.date()

        if end_UTC is None:
            end_UTC = start_UTC

        if isinstance(end_UTC, str):
            end_UTC = parser.parse(end_UTC)

            if end_UTC.time() == time(0, 0, 0):
                end_UTC = end_UTC.date()

        if isinstance(start_UTC, datetime):
            start_UTC = datetime.combine(start_UTC, time(0, 0, 0))

        if isinstance(end_UTC, datetime):
            end_UTC = datetime.combine(end_UTC, time(23, 59, 59))

        if collections is None:
            collections = COLLECTIONS

        if IDs is None:
            ID_message = ""
        else:
            ID_message = f" with IDs: {', '.join(IDs)}"

        logger.info(f"searching {', '.join(collections)} at {tile} from {start_UTC} to {end_UTC}{ID_message}")

        attempt_count = 0

        while attempt_count < self.retries:
            attempt_count += 1

            try:
                granules = HLS_CMR_query(
                    tile=tile,
                    start_date=start_UTC,
                    end_date=end_UTC,
                    page_size=page_size
                )
                break
            except Exception as e:
                logger.warning(f"HLS connection attempt {attempt_count} failed")
                logger.warning(format_exception(e))

                if attempt_count < self.retries:
                    sleep(self.wait_seconds)
                    logger.warning(f"re-trying HLS server:")
                    continue
                else:
                    raise HLSServerUnreachable(f"HLS server un-reachable:")

        self._granules = pd.concat([self._granules, granules]).drop_duplicates(subset=["ID", "date_UTC"])
        logger.info(f"Currently storing {cl.val(len(self._granules))} DataGranules for HLS2")

        return granules

    def dates_listed(self, tile: str) -> Set[date]:
        return set(
            self._listing[self._listing.tile == tile].date_UTC.apply(lambda date_UTC: parser.parse(date_UTC).date()))

    def listing(
            self,
            tile: str,
            start_UTC: Union[date, str],
            end_UTC: Union[date, str] = None,
            page_size: int = PAGE_SIZE) -> (pd.DataFrame, pd.DataFrame):
        SENTINEL_REPEAT_DAYS = 5
        LANDSAT_REPEAT_DAYS = 16
        GIVEUP_DAYS = 10

        tile = tile[:5]

        timer = Timer()

        if isinstance(start_UTC, str):
            start_UTC = parser.parse(start_UTC).date()

        if end_UTC is None:
            end_UTC = start_UTC

        if isinstance(end_UTC, str):
            end_UTC = parser.parse(end_UTC).date()

        if set(date_range(start_UTC, end_UTC)) <= self.dates_listed(tile):
            listing_subset = self._listing[self._listing.tile == tile]
            listing_subset = listing_subset[listing_subset.date_UTC.apply(
                lambda date_UTC: parser.parse(str(date_UTC)).date() >= start_UTC and parser.parse(
                    str(date_UTC)).date() <= end_UTC)]
            listing_subset = listing_subset.sort_values(by="date_UTC")

            return listing_subset

        logger.info(
            f"started listing available HLS2 granules at tile {cl.place(tile)} from {cl.time(start_UTC)} to {cl.time(end_UTC)}")

        giveup_date = datetime.utcnow().date() - timedelta(days=GIVEUP_DAYS)
        search_start = start_UTC - timedelta(days=max(SENTINEL_REPEAT_DAYS, LANDSAT_REPEAT_DAYS))
        search_end = end_UTC

        granules = self.search(
            tile=tile,
            start_UTC=search_start,
            end_UTC=search_end,
            page_size=page_size
        )

        sentinel_granules = granules[granules.sensor == "S30"][
            ["date_UTC", "tile", "granule"]].rename(columns={"granule": "sentinel"})
        landsat_granules = granules[granules.sensor == "L30"][
            ["date_UTC", "tile", "granule"]].rename(columns={"granule": "landsat"})

        sentinel_dates = set(sentinel_granules.date_UTC)
        landsat_dates = set(landsat_granules.date_UTC)

        dates = pd.DataFrame({
            "date_UTC": [
                (start_UTC + timedelta(days=day_offset)).strftime("%Y-%m-%d")
                for day_offset
                in range((end_UTC - start_UTC).days + 1)
            ],
            "tile": tile,
        })

        hls_granules = pd.merge(landsat_granules, sentinel_granules, how="outer")
        listing = pd.merge(dates, hls_granules, how="left")
        date_list = list(listing.date_UTC)

        listing["sentinel_available"] = listing.sentinel.apply(lambda sentinel: not pd.isna(sentinel))

        sentinel_dates_expected = set()

        for d in date_list:
            if d in sentinel_dates:
                sentinel_dates_expected.add(d)

            if (parser.parse(d).date() - timedelta(days=SENTINEL_REPEAT_DAYS)).strftime(
                    "%Y-%m-%d") in sentinel_dates_expected:
                sentinel_dates_expected.add(d)

        listing["sentinel_expected"] = listing.date_UTC.apply(lambda date_UTC: date_UTC in sentinel_dates_expected)

        listing["sentinel_missing"] = listing.apply(
            lambda row: not row.sentinel_available and row.sentinel_expected and parser.parse(
                str(row.date_UTC)) >= parser.parse(str(giveup_date)),
            axis=1
        )

        listing["sentinel"] = listing.apply(lambda row: "missing" if row.sentinel_missing else row.sentinel, axis=1)

        # Populate landsat with None where it's missing
        listing["landsat_available"] = listing.landsat.apply(lambda landsat: not pd.isna(landsat))

        landsat_dates_expected = set()

        for d in date_list:
            if d in landsat_dates:
                landsat_dates_expected.add(d)

            if (parser.parse(d).date() - timedelta(days=LANDSAT_REPEAT_DAYS)).strftime(
                    "%Y-%m-%d") in landsat_dates_expected:
                landsat_dates_expected.add(d)

        # listing["landsat_expected"] = listing.apply(lambda row: parser.parse(str(row.date_UTC)).date().strftime("%Y-%m-%d") in landsat_dates_expected, axis=1)
        listing["landsat_expected"] = listing.date_UTC.apply(
            lambda date_UTC: parser.parse(str(date_UTC)).date().strftime("%Y-%m-%d") in landsat_dates_expected)

        listing["landsat_missing"] = listing.apply(
            lambda row: not row.landsat_available and row.landsat_expected and parser.parse(
                str(row.date_UTC)) >= parser.parse(str(giveup_date)),
            axis=1
        )

        listing["landsat"] = listing.apply(lambda row: "missing" if row.landsat_missing else row.landsat, axis=1)
        listing = listing[["date_UTC", "tile", "sentinel", "landsat"]]

        logger.info(
            f"finished listing available HLS2 granules at tile {cl.place(tile)} from {cl.time(start_UTC)} to {cl.time(end_UTC)} ({timer})")

        self._listing = pd.concat([self._listing, listing]).drop_duplicates(subset=["date_UTC", "tile"])

        return listing

    def sentinel_granule(self, tile: str, date_UTC: Union[date, str]) -> earthaccess.search.DataGranule:
        if isinstance(date_UTC, str):
            date_UTC = parser.parse(date_UTC).date()

        listing = self.listing(tile=tile, start_UTC=date_UTC, end_UTC=date_UTC)
        granule = listing.iloc[-1].sentinel

        if isinstance(granule, float) and np.isnan(granule):
            self.mark_date_unavailable("Sentinel", tile, date_UTC)
            raise HLSSentinelNotAvailable(f"Sentinel is not available at tile {cl.place(tile)} on {cl.time(date_UTC)}")
        elif granule == "missing":
            raise HLSSentinelMissing(
                f"Sentinel is missing on remote server at tile {cl.place(tile)} on {cl.time(date_UTC)}")
        else:
            return granule

    def landsat_granule(self, tile: str, date_UTC: Union[date, str]) -> earthaccess.search.DataGranule:
        if isinstance(date_UTC, str):
            date_UTC = parser.parse(date_UTC).date()

        listing = self.listing(tile=tile, start_UTC=date_UTC, end_UTC=date_UTC)
        granule = listing.iloc[-1].landsat

        if isinstance(granule, float) and np.isnan(granule):
            self.mark_date_unavailable("Landsat", tile, date_UTC)
            error_string = f"Landsat is not available at tile {cl.place(tile)} on {cl.time(date_UTC)}"
            most_recent_listing = listing[listing.landsat.apply(
                lambda landsat: not (landsat == "missing" or (isinstance(granule, float) and np.isnan(granule))))]

            if len(most_recent_listing) > 0:
                most_recent = most_recent_listing.iloc[-1].landsat
                error_string += f" most recent granule: {cl.val(most_recent)}"

            raise HLSLandsatNotAvailable(error_string)
        elif granule == "missing":
            raise HLSLandsatMissing(
                f"Landsat is missing on remote server at tile {cl.place(tile)} on {cl.time(date_UTC)}")
        else:
            return granule
