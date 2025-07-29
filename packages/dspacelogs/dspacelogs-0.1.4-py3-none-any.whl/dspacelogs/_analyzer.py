import logging
import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator

_logger = logging.getLogger(__name__)


class loganalyzer:

    log_pattern = re.compile(
        r"(?P<ip>[\d\.]+)"
        r" - - \[(?P<timestamp>.*?)\]"
        r" \"(?P<request>.*?)\""
        r" (?P<status>\d{3}) (?P<size>(\d+|-))"
        r' \"(?P<referrer>.*?)\" \"(?P<user_agent>.*?)"'
    )

    def __init__(
        self,
        log_file_path: str,
        suspicious_threshold: int = 15,
        timezone: str = "Europe/Bratislava",
    ):
        self._log_file_path = log_file_path
        self._suspicious_threshold = suspicious_threshold
        self._timezone = timezone
        self._df = None
        _logger.info(f"LogAnalyzer created for the file: {self._log_file_path}")

    def __len__(self) -> int:
        return len(self._df)

    @property
    def valid(self):
        return self._df is not None

    def check_valid(self):
        if not self.valid:
            raise ValueError("LogAnalyzer did not return a valid DataFrame")

    def load_data(self):
        _logger.info("Starting to load and process the log file...")
        try:
            with open(
                self._log_file_path, "r", encoding="utf-8", errors="ignore"
            ) as fin:
                parsed_logs = [
                    match.groupdict()
                    for line in fin
                    if (match := loganalyzer.log_pattern.match(line.strip()))
                ]
            if not parsed_logs:
                _logger.warning("No valid log entries were found in the file.")
                return False
            self._df = pd.DataFrame(parsed_logs)
            self._df["timestamp"] = pd.to_datetime(
                self._df["timestamp"], format="%d/%b/%Y:%H:%M:%S %z", errors="coerce"
            )
            self._df.dropna(subset=["timestamp"], inplace=True)
            self._df.sort_values(by="timestamp", inplace=True, ignore_index=True)

            # >>>>>>>>> TOTO JE MIERO, KDE TO MUSÍ BYŤ <<<<<<<<<
            self._df["status"] = pd.to_numeric(self._df["status"], errors="coerce")
            self._df.dropna(subset=["status"], inplace=True)
            self._df["status"] = self._df["status"].astype(int)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            _logger.info(
                f"✅ Successfully loaded and processed {len(self._df)} records."
            )
            return True
        except FileNotFoundError:
            _logger.error(f"ERROR: File '{self._log_file_path}' was not found.")
            return False
        except Exception as e:
            _logger.error(f"An unexpected error occurred while loading data: {e}")
            return False

    def get_top_requests(self, n: int = 10):
        self.check_valid()
        _logger.info(f"I'm looking for TOP {n} most visited addresses.")
        top_reqs = self._df["request"].value_counts().head(n).reset_index()
        top_reqs.columns = ["Requested address", "Number of accesses"]
        top_reqs.index += 1
        return top_reqs

    def get_suspicious_activity(self):
        self.check_valid()

        _logger.info(
            f"I am detecting suspicious activity. (threshold: >"
            f"{self._suspicious_threshold} of requirements/min)."
        )
        reqs = (
            self._df.groupby(["ip", pd.Grouper(key="timestamp", freq="min")])
            .size()
            .reset_index(name="count")
        )

        suspicious = reqs[reqs["count"] > self._suspicious_threshold].copy()
        if suspicious.empty:
            _logger.info("✅ No suspicious activity was found.")
            return None

        suspicious["timestamp"] = suspicious["timestamp"].dt.tz_convert(self._timezone)
        return suspicious.sort_values(by="timestamp", ascending=True)

    def plot_activity_by_minute(self):
        self.check_valid()

        df_local = self._df.copy()
        df_local["timestamp"] = df_local["timestamp"].dt.tz_convert(self._timezone)
        activity = df_local.groupby(pd.Grouper(key="timestamp", freq="min")).size()
        fig, ax = plt.subplots(figsize=(25, 10))
        ax.stem(
            activity.index,
            activity.values,
            linefmt="dodgerblue",
            markerfmt=" ",
            basefmt="black",
        )
        ax.xaxis.set_major_locator(HourLocator())
        ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))
        ax.set_title(
            f'Server activity by minutes ({
                df_local["timestamp"].min().strftime("%d.%m.%Y")})',
            fontsize=18,
            pad=20,
        )
        ax.set_xlabel("Time (local)", fontsize=14)
        ax.set_ylabel("Number of requests per minute", fontsize=14)
        ax.grid(True, which="major", axis="both", linestyle="--", alpha=0.5)
        plt.show()

    def plot_status_codes_by_hour(self):
        self.check_valid()

        _logger.info(
            "I am plotting a graph of the evolution of status codes over time."
        )
        df_local = self._df.copy()
        df_local["timestamp"] = df_local["timestamp"].dt.tz_convert(self._timezone)
        df_local["status_cat"] = df_local["status"].apply(
            lambda x: (
                "2xx"
                if 200 <= x < 300
                else "3xx" if 300 <= x < 400 else "4xx" if 400 <= x < 500 else "5xx"
            )
        )
        grouped = (
            df_local.groupby([pd.Grouper(key="timestamp", freq="h"), "status_cat"])
            .size()
            .unstack(fill_value=0)
        )

        ax = grouped.plot(
            kind="line",
            figsize=(18, 7),
            style="-o",
            title="Hourly number of requests by status code",
        )
        for hour_tick in grouped.index:
            ax.axvline(
                x=hour_tick, color="grey", linestyle="--", linewidth=0.7, alpha=0.5
            )
        plt.xlabel("Hour of the day (Local time)")
        plt.ylabel("Total number of requests")
        plt.legend(title="Status category")
        plt.show()
