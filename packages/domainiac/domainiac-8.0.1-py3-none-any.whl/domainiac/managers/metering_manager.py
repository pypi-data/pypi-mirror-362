import datamazing.pandas as pdz
import pandas as pd
from typeguard import typechecked


class MeteringManager:
    """
    Manager which simplifies the process of getting metering data from datahub.
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

    @typechecked
    def get_plant_settlement(self, datahub_gsrn: str) -> pd.DataFrame:
        """
        Retrieves the settlement data for a given datahub gsrn.
        """
        df = self.db.query(
            "readingSettlement",
            self.time_interval,
            filters={"datahub_gsrn_e18": datahub_gsrn},
        )

        df = df.filter(
            [
                "time_utc",
                "datahub_gsrn_e18",
                "reading_settlement_e18_MW",
            ]
        )

        return df
