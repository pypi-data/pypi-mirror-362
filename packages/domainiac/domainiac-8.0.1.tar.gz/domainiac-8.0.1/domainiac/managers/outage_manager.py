import datamazing.pandas as pdz
import pandas as pd


class OutageManager:
    """
    Manager which simplifies the process of getting outage data.
    """

    def __init__(
        self,
        db: pdz.Database,
        time_interval: pdz.TimeInterval,
        resolution: pd.Timedelta,
    ) -> None:
        self.db = db
        self.time_interval = time_interval
        self.resolution = resolution

    def get_plant_outage_time_series(self) -> pd.DataFrame:
        df_outage = self.db.query("scheduleOutage")

        df_outage = df_outage[~df_outage["is_unapproved"]]

        df_outage = df_outage.dropna(subset="plant_gsrn")

        df_times = self.time_interval.to_range(self.resolution).to_frame(
            index=False, name="time_utc"
        )

        df_outage = pdz.merge(
            df_times,
            df_outage,
            left_time="time_utc",
            right_period=("start_time_utc", "end_time_utc"),
        )

        df_outage = df_outage.filter(
            [
                "plant_gsrn",
                "time_utc",
            ]
        )

        df_outage = df_outage.reset_index(drop=True)

        return df_outage
