import copy
from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional

import pendulum

from sklik.api import SklikApi
from sklik.object import Account
from sklik.util import API_MAX_PAGE_SIZE


def _restriction_filter_validator(
        since: Optional[str] = None,
        until: Optional[str] = None,
        restriction_filter: Optional[Dict] = None
) -> Dict[str, Any]:
    """Validate and construct date restriction parameters for a report.

    Parses the provided `since` and `until` dates and returns a dictionary
    containing the validated date range along with any additional filtering
    criteria provided in `restriction_filter`.

    Args:
        since: Start date in 'YYYY-MM-DD' format. If not provided, defaults to
            29 days before today.
        until: End date in 'YYYY-MM-DD' format. If not provided, defaults to
            yesterday's date.
        restriction_filter: Additional filtering criteria as a dictionary.

    Returns:
        A dictionary with keys 'dateFrom', 'dateTo', and any keys from
        `restriction_filter`.
    """
    since = pendulum.parse(since).to_date_string() if since else None
    until = pendulum.parse(until).to_date_string() if until else None
    today = pendulum.today()

    restriction_filter = restriction_filter or {}

    full_filter = restriction_filter.copy()
    full_filter["dateFrom"] = since or today.subtract(days=29).to_date_string()
    full_filter["dateTo"] = until or today.subtract(days=1).to_date_string()

    return full_filter


def _display_option_validator(granularity: Optional[str] = None) -> Dict[str, Any]:
    """Validate and construct display options for a report.

    Args:
        granularity: Time granularity for the report (e.g., 'daily', 'weekly').
            If not provided, defaults to 'daily'.

    Returns:
        A dictionary with key 'statGranularity' set to the provided or default value.
    """

    return {"statGranularity": granularity or "daily"}


@dataclass
class ReportPage:
    """Iterator for a single page of report data.

    This class handles the pagination of report data returned by the Sklik API.
    It loads a page of data and iterates over each item, fetching new pages as needed.

    Attributes:
        service: Name of the Sklik service being called.
        args: List of arguments to be passed to the API call.
        total_count: Optional total count of items in the report, used for optimizing
            pagination limits.
        api: An instance of SklikApi used for making API calls.
    """

    service: str
    args: List
    total_count: Optional[int] = None
    api: SklikApi = field(default_factory=SklikApi.get_default_api)

    def __post_init__(self) -> None:
        """Initialize pagination parameters and load the first page."""

        self._current_index: int = 0
        self._current_offset: int = 0
        self._current_limit: int = API_MAX_PAGE_SIZE if self.total_count is None or self.total_count == 0 or self.total_count > 5000 else self.total_count

        self._items_iter = self._item_generator()

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        return self

    def __next__(self) -> Dict[str, Any]:
        """Return the next report item or raise StopIteration if exhausted."""
        return next(self._items_iter)

    def _item_generator(self) -> Iterator[Dict[str, Any]]:
        """Generator that yields report items, loading new pages as necessary."""
        while True:
            page = self.load_data(self._current_offset, self._current_limit)
            if not page:
                break
            for item in page:
                yield item
            self._current_offset += self._current_limit

    def _load_raw_data(self, offset: int, limit: int) -> List[Dict[str, Any]]:
        """Load raw report data from the API.

        Modifies the last element of `args` to include the pagination parameters.

        Args:
            offset: The offset index to start loading data.
            limit: The maximum number of records to load.

        Returns:
            A list of dictionaries representing raw report data.
        """

        payload = copy.deepcopy(self.args)
        payload[-1]["offset"] = offset
        payload[-1]["limit"] = limit
        return self.api.call(self.service, "readReport", args=payload)["report"]

    def load_data(self, offset: int, limit: int) -> List[Dict[str, Any]]:
        """Process and load report data for the given page.

        Transforms the raw report data into a flat structure by merging
        each stat dictionary with its parent item data.

        Args:
            offset: The offset index for pagination.
            limit: The number of records to retrieve.

        Returns:
            A list of processed report items.
        """

        report = self._load_raw_data(offset, limit)
        return [
            {**stat, **{key: value for key, value in item.items() if key != "stats"}}
            for item in report
            for stat in item.get("stats", [])
        ]


@dataclass
class Report:
    """Iterator-based interface for handling Sklik API reports.

    Provides functionality to access and iterate through paginated report data
    from the Sklik advertising platform. The class handles pagination automatically
    and formats the data into a consistent structure.

    Attributes:
        account_id: Identifier of the Sklik account.
        service: Name of the Sklik service providing the report.
        report_args: List of dictionaries with report parameters (e.g., date range,
            display options).
        display_columns: List of field names to be included in the report data.
        api: An instance of SklikApi used for API calls.

    Iterator Behavior:
        The class implements the iterator protocol, allowing for easy iteration
        over all report items. Pagination is handled automatically during iteration.

    Example:
        >>> report = Report(
        ...     account_id=123456,
        ...     report_args=[
        ...         {"dateFrom": "2024-01-01", "dateTo": "2024-01-31"},
        ...         {"statGranularity": "daily"}
        ...     ],
        ...     service="stats",
        ...     display_columns=["impressions", "clicks", "cost"]
        ... )
        >>> for item in report:
        ...     print(item["impressions"], item["clicks"])
    """

    account_id: int
    service: str
    report_args: List[Dict[str, Any]]
    display_columns: List[str]
    api: SklikApi = field(default_factory=SklikApi.get_default_api)

    def __post_init__(self) -> None:
        """Initialize the report and validate input parameters.

        Validates that `report_args` contains the required date range and display
        options, and initializes internal state for pagination.

        Raises:
            ValueError: If `report_args` is invalid or missing required keys.
        """

        # Validate that report_args is a list with at least two elements
        if not isinstance(self.report_args, list) or len(self.report_args) < 2:
            raise ValueError(
                "report_args must be a list with at least two dictionaries: one for date range and one for display options."
            )

        # Validate that date_args is a dict containing 'dateFrom' and 'dateTo'
        date_args, display_args = self.report_args[0], self.report_args[1]

        if not all(k in date_args for k in ["dateFrom", "dateTo"]):
            raise ValueError("Date range dictionary must contain 'dateFrom' and 'dateTo'.")
        if "statGranularity" not in display_args:
            raise ValueError("Display options dictionary must contain 'statGranularity'.")

        # Validate and parse the date values
        try:
            self._start_date = pendulum.parse(date_args["dateFrom"])
            self._current_start_date = pendulum.parse(date_args["dateFrom"])
            self._end_date = pendulum.parse(date_args["dateTo"])
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid date format provided. Expected YYYY-MM-DD.") from e

        if self._start_date > self._end_date:
            raise ValueError("The 'since' date cannot be after the 'until' date.")

        # Assign granularity
        self._granularity = display_args["statGranularity"]

        # Initialize the report iterator
        self._current_report_page: Iterator[Dict[str, Any]] = iter([])
        self._is_finished = False

    def __iter__(self) -> "Report":
        return self

    def __next__(self) -> Dict[str, Any]:
        """Return the next report item.

        Iterates over the current page. If the current page is exhausted, attempts
        to load the next page. Stops iteration if the date range has been fully processed.

        Returns:
            The next report item as a dictionary.

        Raises:
            StopIteration: If there are no more report items.
        """

        try:
            return next(self._current_report_page)
        except StopIteration:
            if self._is_finished:
                raise StopIteration()

            self._current_report_page = self._load_report_chunk()
            return next(self._current_report_page)

    def _create_report_for_range(self, start_date: pendulum.DateTime, end_date: pendulum.DateTime) -> Dict[str, Any]:
        """Create a new report via the Sklik API.

        Updates the report date range parameters, creates the report and returns
        the response from the API containing the report identifier and metadata.

        Args:
            start_date: The start date for the report range.
            end_date: The end date for the report range.

        Returns:
            A dictionary containing the report ID and metadata such as totalCount.
        """

        args = copy.deepcopy(self.report_args)
        args[0]["dateFrom"] = start_date.to_date_string()
        args[0]["dateTo"] = end_date.to_date_string()

        payload = [{"userId": self.account_id}, *args]
        return self.api.call(self.service, "createReport", payload)

    def _load_report_chunk(self) -> ReportPage:
        """Load an optimized chunk of report data.
        
        This method implements an adaptive optimization strategy for fetching report data
        efficiently, balancing between API limits and data volume. The process follows
        these steps:
        
        1. PROBE: Create a report for the entire remaining date range to get totalCount.
        2. CALCULATE: Determine the maximum number of days that can be fetched without
           exceeding the API page size limit.
        3. ADJUST: Calculate max end date accepted by API.
        4. EXECUTE: Create and return a ReportPage with the final report data.
        
        This approach dynamically adjusts the date range for each API call based on
        the data density, ensuring optimal performance even with varying data volumes
        across different date ranges.
        
        Returns:
            A ReportPage iterator containing the report data for the current chunk,
            or an empty iterator if there is no more data to fetch.
        """

        if self._is_finished:
            return iter([])

        # --- BRANCH 1: Handle 'total' granularity (no time multiplier) ---
        if self._granularity == "total":
            self._is_finished = True
            response = self._create_report_for_range(self._start_date, self._end_date)
            report_id = response.get("reportId")
            total_count = response.get("totalCount", 0)

            if not report_id or total_count == 0:
                return iter([])
            return ReportPage(
                self.service,
                args=[{"userId": self.account_id}, report_id, {"displayColumns": self.display_columns}],
                total_count=total_count,
                api=self.api
            )

        # --- BRANCH 2: Universal "Probe and Adjust" for ALL time-based granularities ---
        if self._current_start_date > self._end_date:
            self._is_finished = True
            return iter([])

        # 1. PROBE: Create a report for the entire remaining date range to get totalCount.
        probe_response = self._create_report_for_range(self._current_start_date, self._end_date)
        total_count = probe_response.get("totalCount", 0)

        # If there's no data in the entire remaining period, we are done with this part.
        if total_count == 0:
            self._is_finished = True
            return iter([])

        # 2. CALCULATE: Determine the maximum number of units we can fetch.
        # We use max(1, ...) to handle cases where total_count > API_MAX_PAGE_SIZE, ensuring we fetch at least one day.
        max_units = max(1, API_MAX_PAGE_SIZE // total_count)

        # # 3. ADJUST: v
        if self._granularity == 'daily':
            chunk_end_date = self._current_start_date.add(days=max_units - 1)
        elif self._granularity == 'weekly':
            chunk_end_date = self._current_start_date.add(weeks=max_units - 1).end_of('week')
        elif self._granularity == 'monthly':
            chunk_end_date = self._current_start_date.add(months=max_units - 1).end_of('month')
        elif self._granularity == 'quarterly':
            chunk_end_date = self._current_start_date.add(quarters=max_units - 1).end_of('quarter')
        elif self._granularity == 'yearly':
            chunk_end_date = self._current_start_date.add(years=max_units - 1).end_of('year')
        else:
            raise ValueError(f"Unsupported granularity for chunking: {self._granularity}")

        if chunk_end_date > self._end_date:
            chunk_end_date = self._end_date

        final_response = self._create_report_for_range(self._current_start_date, chunk_end_date)
        actual_report_id = final_response["reportId"]

        # Keep track of where we are for the next call to load_report_chunk.
        self._current_start_date = chunk_end_date.add(days=1)

        # 4. EXECUTE: Create a ReportPage with the final, valid report ID.
        return ReportPage(
            self.service,
            args=[{"userId": self.account_id}, actual_report_id, {"displayColumns": self.display_columns}],
            total_count=total_count,  # We can pass total_count for context, though it's not critical for the new logic
            api=self.api
        )


def create_report(
        account: Account,
        service: str,
        fields: List[str],
        since: Optional[str] = None,
        until: Optional[str] = None,
        granularity: Optional[str] = None,
        restriction_filter: Optional[Dict] = None
) -> Report:
    """Create a new report for the specified Sklik service.

    Creates and initializes a new report based on the provided parameters,
    allowing for flexible data retrieval and filtering options.

    Args:
        account: Account object containing the account ID and API instance.
        service: Name of the Sklik service to generate the report for
            (e.g., 'campaigns', 'stats', 'ads').
        fields: List of field names to include in the report.
        since: Start date for the report data in 'YYYY-MM-DD' format.
            If not specified, a default date is used.
        until: End date for the report data in 'YYYY-MM-DD' format.
            If not specified, a default date is used.
        granularity: Time granularity for the report data
            (e.g., 'daily', 'weekly', 'monthly').
        restriction_filter: Additional filtering criteria for the report data.

    Returns:
        A Report object containing the initialized report data and metadata.

    Example:
        >>> report = create_report(
        ...     account=Account(123456),
        ...     service="campaigns",
        ...     fields=["clicks", "impressions"],
        ...     since="2024-01-01",
        ...     until="2024-01-31",
        ...     granularity="daily"
        ... )
    """

    args = [
        _restriction_filter_validator(since, until, restriction_filter),
        _display_option_validator(granularity)
    ]

    return Report(account.account_id, service=service, report_args=args, display_columns=fields, api=account.api)
