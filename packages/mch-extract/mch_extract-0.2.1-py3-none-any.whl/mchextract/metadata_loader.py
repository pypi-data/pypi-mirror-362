import itertools
from collections import defaultdict
from concurrent.futures import Future, ThreadPoolExecutor

import polars as pl

from mchextract.consts import DATA_SOURCES, DataSource, MetaFiles
from mchextract.downloader import CachedDownloader
from mchextract.models import DataAvailability, MeteoData, Parameter, Station


class MetaDataLoader:
    """Loads MeteoSwiss metadata from CSV files and creates structured data models."""

    def __init__(self, downloader: CachedDownloader):
        self._downloader = downloader
        self._executor = ThreadPoolExecutor()

    def _load_file(
        self, data_source: DataSource, key: MetaFiles
    ) -> Future[tuple[MetaFiles, DataSource, bytes]]:
        def wrapper() -> tuple[MetaFiles, DataSource, bytes]:
            return (
                key,
                data_source,
                self._downloader.download(
                    data_source.data_url, data_source.meta_files[key]
                ),
            )

        return self._executor.submit(wrapper)

    def _load_parameters(
        self, files: list[tuple[DataSource, bytes]]
    ) -> dict[str, Parameter]:
        """Load parameter definitions from CSV files from all data sources."""
        parameters = {}

        for _, file in files:
            df = pl.read_csv(
                file,
                separator=";",
                encoding="windows-1252",
                schema_overrides={
                    "parameter_decimals": pl.Int32,
                },
            )

            for row in df.iter_rows(named=True):
                parameter = Parameter(
                    shortname=row["parameter_shortname"],
                    description_de=row["parameter_description_de"].strip('"'),
                    description_fr=row["parameter_description_fr"].strip('"'),
                    description_it=row["parameter_description_it"].strip('"'),
                    description_en=row["parameter_description_en"].strip('"'),
                    group_de=row["parameter_group_de"],
                    group_fr=row["parameter_group_fr"],
                    group_it=row["parameter_group_it"],
                    group_en=row["parameter_group_en"],
                    granularity=row["parameter_granularity"],
                    decimals=row["parameter_decimals"],
                    datatype=row["parameter_datatype"],
                    unit=row["parameter_unit"],
                )
                parameters[parameter.shortname] = parameter

        return parameters

    def _load_data_inventory(
        self, files: list[tuple[DataSource, bytes]]
    ) -> dict[str, list[DataAvailability]]:
        """Load data availability information from CSV files, grouped by station."""
        inventory: dict[str, list[DataAvailability]] = {}

        for _, file in files:
            df = pl.read_csv(
                file,
                separator=";",
                encoding="windows-1252",
                schema_overrides={
                    "meas_cat_nr": pl.Int32,
                },
            ).with_columns(
                [
                    pl.col("data_since").str.strptime(
                        pl.Datetime, "%d.%m.%Y %H:%M", strict=False
                    ),
                    pl.col("data_till").str.strptime(
                        pl.Datetime, "%d.%m.%Y %H:%M", strict=False
                    ),
                ]
            )

            for row in df.iter_rows(named=True):
                station_abbr = row["station_abbr"]

                availability = DataAvailability(
                    parameter_shortname=row["parameter_shortname"],
                    meas_cat_nr=row["meas_cat_nr"],
                    data_since=row["data_since"],
                    data_till=row["data_till"],
                    owner=row["owner"],
                )

                if station_abbr not in inventory:
                    inventory[station_abbr] = []
                inventory[station_abbr].append(availability)

        return inventory

    def _load_stations(
        self,
        files: list[tuple[DataSource, bytes]],
        data_inventory: dict[str, list[DataAvailability]],
    ) -> dict[str, Station]:
        """Load station metadata from CSV files and join with data inventory."""
        stations = {}

        for data_source, file in files:
            df = pl.read_csv(
                file,
                separator=";",
                encoding="windows-1252",
                schema_overrides={
                    "station_height_masl": pl.Float64,
                    "station_height_barometer_masl": pl.Float64,
                    "station_coordinates_lv95_east": pl.Float64,
                    "station_coordinates_lv95_north": pl.Float64,
                    "station_coordinates_wgs84_lat": pl.Float64,
                    "station_coordinates_wgs84_lon": pl.Float64,
                },
            ).with_columns(
                [
                    pl.col("station_data_since").str.strptime(
                        pl.Datetime, "%d.%m.%Y %H:%M", strict=False
                    ),
                ]
            )

            for row in df.iter_rows(named=True):
                station_abbr = row["station_abbr"]

                station = Station(
                    abbr=station_abbr,
                    name=row["station_name"],
                    canton=row["station_canton"],
                    wigos_id=row["station_wigos_id"],
                    type_de=row["station_type_de"],
                    type_fr=row["station_type_fr"],
                    type_it=row["station_type_it"],
                    type_en=row["station_type_en"],
                    dataowner=row["station_dataowner"],
                    data_since=row["station_data_since"],
                    height_masl=row["station_height_masl"],
                    height_barometer_masl=row["station_height_barometer_masl"],
                    coordinates_lv95_east=row["station_coordinates_lv95_east"],
                    coordinates_lv95_north=row["station_coordinates_lv95_north"],
                    coordinates_wgs84_lat=row["station_coordinates_wgs84_lat"],
                    coordinates_wgs84_lon=row["station_coordinates_wgs84_lon"],
                    exposition_de=row["station_exposition_de"],
                    exposition_fr=row["station_exposition_fr"],
                    exposition_it=row["station_exposition_it"],
                    exposition_en=row["station_exposition_en"],
                    url_de=row["station_url_de"],
                    url_fr=row["station_url_fr"],
                    url_it=row["station_url_it"],
                    url_en=row["station_url_en"],
                    # Join with data inventory
                    available_parameters=data_inventory.get(station_abbr, []),
                    # Track which data source this station belongs to
                    data_source=data_source.name,
                )

                stations[station_abbr] = station

        return stations

    def load_all(self) -> MeteoData:
        """Load all metadata and return structured MeteoData object."""

        # Use futures to load files concurrently
        futures: list[Future[tuple[MetaFiles, DataSource, bytes]]] = []
        for data_source, key in itertools.product(DATA_SOURCES, MetaFiles):
            future = self._load_file(data_source, key)
            futures.append(future)

        # Wait for all futures to complete and collect results
        results = [future.result() for future in futures]
        metadata: dict[MetaFiles, list[tuple[DataSource, bytes]]] = defaultdict(list)

        for key, data_source, content in results:
            metadata[key].append((data_source, content))

        parameters = self._load_parameters(metadata[MetaFiles.PARAMETERS])
        data_inventory = self._load_data_inventory(metadata[MetaFiles.DATA_INVENTORY])
        stations = self._load_stations(metadata[MetaFiles.STATIONS], data_inventory)

        return MeteoData(stations=stations, parameters=parameters)
