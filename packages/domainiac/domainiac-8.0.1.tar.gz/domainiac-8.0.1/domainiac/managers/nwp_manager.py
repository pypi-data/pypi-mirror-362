import datamazing.pandas as pdz
import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree

from ..modeling.nwp import Coordinate, Neighborhood, NWPParameter, NWPProvider


class NWPManager:
    """
    Contains all logic concerning NWP data.
    This includes:
    - Getting NWP data
    - Getting average NWP data
    - Finding closest NWP coordinates
    """

    NWP_INTERPOLATION_METHODS = {
        # Wind and temperature are estimates
        # of the instantaneous value at time t.
        # We use linear interpolation.
        NWPParameter.WIND: ("linear", "instantanous"),
        NWPParameter.TEMPERATURE: ("linear", "instantanous"),
        # solar is an estimate of the average value
        # in the interval [t-1, t].
        # We use PCHIP interpolation to ensure
        # a smooth shape and non-negative values
        # (https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.PchipInterpolator.html)
        NWPParameter.SOLAR: ("pchip", "interval_average"),
    }

    NWP_RESOLUTIONS = {
        (NWPProvider.ECMWF, NWPParameter.WIND): pd.Timedelta("PT3H"),
        (NWPProvider.ECMWF, NWPParameter.TEMPERATURE): pd.Timedelta("PT3H"),
        (NWPProvider.ECMWF, NWPParameter.SOLAR): pd.Timedelta("PT1H"),
        (NWPProvider.DMI, NWPParameter.WIND): pd.Timedelta("PT1H"),
        (NWPProvider.DMI, NWPParameter.TEMPERATURE): pd.Timedelta("PT1H"),
        (NWPProvider.DMI, NWPParameter.SOLAR): pd.Timedelta("PT1H"),
        (NWPProvider.CONWX, NWPParameter.WIND): pd.Timedelta("PT1H"),
        (NWPProvider.CONWX, NWPParameter.TEMPERATURE): pd.Timedelta("PT1H"),
        (NWPProvider.CONWX, NWPParameter.SOLAR): pd.Timedelta("PT1H"),
    }

    def __init__(
        self,
        db: pdz.Database,
        time_interval: pdz.TimeInterval,
        resolution: pd.Timedelta,
    ):
        self.db = db
        self.time_interval = time_interval
        self.resolution = resolution

        self._nwp_coordinates_kd_tree = dict()
        self._nwp_table_name_prefix = "forecastNwp"

    @classmethod
    def get_nwp_resolution(
        cls, provider: NWPProvider, parameter: NWPParameter
    ) -> pd.Timedelta:
        """
        Get the resolution of the NWP parameter.
        """
        return cls.NWP_RESOLUTIONS[(provider, parameter)]

    @classmethod
    def get_nwp_interpolation_method(cls, parameter: NWPParameter) -> tuple[str, str]:
        """
        Get the interpolation method and temporal aggregation for the NWP parameter.
        """
        return cls.NWP_INTERPOLATION_METHODS[parameter]

    @staticmethod
    def calculate_wind_speed_from_vectors(u: pd.Series, v: pd.Series) -> pd.Series:
        return np.sqrt(u**2 + v**2)

    def _get_table_name(
        self,
        provider: NWPProvider,
        parameter: NWPParameter,
    ) -> str:
        """
        Get the table name for a given NWP parameter.
        """
        return self._nwp_table_name_prefix + provider.value + parameter.value

    def _get_kd_tree(self, provider: NWPProvider, parameter: NWPParameter) -> KDTree:
        """
        Create a KDTree from the coordinates from the nwp parameter table.
        This is done lazily, so that the KDTree is only created once.
        """
        key = (provider, parameter)
        if key not in self._nwp_coordinates_kd_tree:
            # Base KDTree on one hour of data
            query_time_interval = pdz.TimeInterval(
                self.time_interval.left, self.time_interval.left + pd.Timedelta("PT1H")
            )

            df = self.db.query(
                table_name=self._get_table_name(provider, parameter),
                time_interval=query_time_interval,
            )

            self._nwp_coordinates_kd_tree[key] = dict()

            # Make KDTree for altitude
            self._nwp_coordinates_kd_tree[key]["altitude"] = KDTree(
                df[["altitude_m"]].drop_duplicates()
            )

            # Make KDTree for latitude and longitude
            self._nwp_coordinates_kd_tree[key]["plane"] = KDTree(
                df[["latitude", "longitude"]].drop_duplicates()
            )

        return self._nwp_coordinates_kd_tree[key]

    def get_nwp_neighbors(
        self,
        provider: NWPProvider,
        parameter: NWPParameter,
        neighborhood: Neighborhood,
    ) -> list[Coordinate]:
        """
        Find n closest coordinates based on the NWP parameter table.

        Note: This assumes that coordinates does not change over time.
        """
        kd_tree = self._get_kd_tree(provider, parameter)

        altitude_indices = kd_tree["altitude"].query(
            np.c_[neighborhood.coordinate.altitude],
            k=1,
            return_distance=False,
        )
        # TODO: Allow this to handle multiple altitudes
        nearest_altitude = kd_tree["altitude"].data.base[altitude_indices][0][0][0]

        plane_indices = kd_tree["plane"].query(
            np.c_[neighborhood.coordinate.latitude, neighborhood.coordinate.longitude],
            k=neighborhood.num_neighbors,
            return_distance=False,
        )
        nearest_planes = kd_tree["plane"].data.base[plane_indices][0]

        coordinates = [
            Coordinate(latitude=plane[0], longitude=plane[1], altitude=nearest_altitude)
            for plane in nearest_planes
        ]

        return coordinates

    def _get_nwp_parameter(
        self,
        provider: NWPProvider,
        parameter: NWPParameter,
        coordinate: Coordinate,
    ) -> pd.DataFrame:
        """
        Get NWP data for a given parameter, coordinate and altitude.
        """
        table = self._get_table_name(provider, parameter)

        filters = {
            "latitude": coordinate.latitude,
            "longitude": coordinate.longitude,
            "altitude_m": coordinate.altitude,
        }

        # Pad time interval with one resolution
        # This is needed for the interpolation to work as we shift back in time
        nwp_resolution = self.get_nwp_resolution(provider, parameter)

        # Pad time interval to make sure interpolation is possible
        padded_time_interval = pdz.TimeInterval(
            self.time_interval.left - (nwp_resolution / 2),
            self.time_interval.right + (nwp_resolution * 1.5),
        )

        df = self.db.query(table, padded_time_interval, filters=filters)

        df = df.drop(
            columns=[
                "created_time_utc",
                "valid_from_time_utc",
                "valid_to_time_utc",
                "altitude_m",
                "longitude",
                "latitude",
            ],
            errors="ignore",
        )

        return df

    def _get_interpolated_nwp_parameter(
        self,
        provider: NWPProvider,
        parameter: NWPParameter,
        coordinate: Coordinate,
    ):
        """
        Get NWP data for a given parameter, coordinate and altitude,
        using the proper interpolation technique.
        """
        df = self._get_nwp_parameter(provider, parameter, coordinate)

        nwp_resolution = self.get_nwp_resolution(provider, parameter)
        interpolation_method, temporal_aggregation = self.get_nwp_interpolation_method(
            parameter
        )

        match temporal_aggregation:
            # if the parameter is an interval average,
            # it makes best sense to interpolate from
            # midpoint to midpoint. Otherwise, we just
            # interpolate regularly.
            case "interval_average":
                shift = -1 / 2
            case "instantanous":
                shift = 0

        df_shifted = pdz.shift_time(df, on="time_utc", period=shift * nwp_resolution)

        # Interpolate
        df_resampled = pdz.resample(
            df_shifted, on="time_utc", resolution=self.resolution / 2
        ).interpolate(interpolation_method)

        # Shift back time, so that the output time series again represents
        # the value by the endpoint.
        df_re_shifted = pdz.shift_time(
            df_resampled, on="time_utc", period=-shift * self.resolution
        )

        # Make sure times is divisible by the resolution
        df_resolution = df_re_shifted[
            df_re_shifted["time_utc"].dt.round(self.resolution)
            == df_re_shifted["time_utc"]
        ]

        return df_resolution

    def get_nwp_parameter(
        self,
        provider: NWPProvider,
        parameter: NWPParameter,
        coordinate: Coordinate,
    ):
        df_nwp = self._get_interpolated_nwp_parameter(provider, parameter, coordinate)

        # Ensure data is within time_interval defined by user
        df_nwp = df_nwp.query(
            f"time_utc >= '{self.time_interval.left}' "
            f"and time_utc <= '{self.time_interval.right}'",
        )

        return df_nwp

    def get_nwp_parameter_in_neighborhood(
        self,
        provider: NWPProvider,
        parameter: NWPParameter,
        neighborhood: Neighborhood,
    ) -> pd.DataFrame:
        """
        Get average NWP data for a given parameter, coordinates and altitude.
        """
        dfs = []

        neighbors = self.get_nwp_neighbors(provider, parameter, neighborhood)
        for coordinate in neighbors:
            df_coordinate = self.get_nwp_parameter(provider, parameter, coordinate)
            dfs.append(df_coordinate)

        df = pd.concat(dfs)
        df = pdz.group(df, "time_utc").agg("mean")

        return df

    def get_nwp(
        self,
        provider: NWPProvider,
        parameters: list[NWPParameter],
        neighborhood: Neighborhood,
    ) -> pd.DataFrame:
        """
        Get weather features for a given coordinate.
        """
        dfs = []
        for parameter in parameters:
            df_param = self.get_nwp_parameter_in_neighborhood(
                provider,
                parameter,
                neighborhood,
            )
            dfs.append(df_param)

        df = pdz.merge_many(dfs=dfs, on=["time_utc"])

        return df
