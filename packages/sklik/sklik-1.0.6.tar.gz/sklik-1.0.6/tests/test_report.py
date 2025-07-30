from unittest.mock import patch

import pendulum
import pytest

from sklik.report import (
    _restriction_filter_validator,
    _display_option_validator,
    ReportPage,
    Report,
    create_report,
)
from sklik.util import SKLIK_DATE_FORMAT


# ========= Tests for _restriction_filter_validator =========

def test_restriction_filter_validator_with_all_parameters():
    # Given
    since = "2024-01-01"
    until = "2024-01-31"
    extra_filter = {"campaignId": 123}
    # When
    result = _restriction_filter_validator(since, until, extra_filter)
    # Then: since/until should be passed through if provided.
    assert result["dateFrom"] == since
    assert result["dateTo"] == until
    # Extra filter is merged in.
    assert result["campaignId"] == 123


def test_restriction_filter_validator_defaults(monkeypatch):
    # Given: no since/until provided.
    fake_today = pendulum.datetime(2024, 2, 10)
    monkeypatch.setattr(pendulum, "today", lambda: fake_today)

    # When
    result = _restriction_filter_validator()
    print("***")
    print(result)

    # Then: dateFrom is today - 29 days and dateTo is today - 1 day.
    expected_date_from = fake_today.subtract(days=29).to_date_string()
    expected_date_to = fake_today.subtract(days=1).to_date_string()
    assert result["dateFrom"] == expected_date_from
    assert result["dateTo"] == expected_date_to


def test_restriction_filter_validator_with_none_extra():
    # When no restriction_filter is provided, only the dates appear.
    since = "2024-03-01"
    until = "2024-03-31"
    result = _restriction_filter_validator(since, until)
    assert "dateFrom" in result and result["dateFrom"] == since
    assert "dateTo" in result and result["dateTo"] == until
    # No extra keys should be present.
    assert len(result) == 2


# ========= Tests for _display_option_validator =========

def test_display_option_validator_with_granularity():
    granularity = "weekly"
    result = _display_option_validator(granularity)
    assert result["statGranularity"] == granularity


def test_display_option_validator_default():
    result = _display_option_validator(None)
    assert result["statGranularity"] == "daily"


def test_display_option_validator_with_empty_string():
    # When passing an empty string for granularity, the default "daily" should be used.
    result = _display_option_validator("")
    # Even if empty string is passed, our implementation chooses granularity or "daily"
    assert result["statGranularity"] == "daily"


# ========= Tests for ReportPage =========

class FakeApi:
    def __init__(self):
        self.call_count = 0

    def call(self, service, method, args):
        # Simulate pagination based on the offset in args.
        # The last element in args is assumed to be a dict we can modify.
        offset = args[-1].get("offset", 0)
        limit = args[-1].get("limit", 100)
        # For offset 0, return a first "page" of data with two items.
        if offset == 0:
            # Each item contains a "stats" key with a list of stat dictionaries,
            # plus some extra keys that should be merged.
            return {
                "report": [
                    {"stats": [{"val": 1}, {"val": 2}], "extra": "x"},
                    {"stats": [{"val": 3}], "extra": "y"},
                ]
            }
        # For subsequent offsets, return an empty list (end of data)
        return {"report": []}


@patch("sklik.SklikApi.get_default_api")
def test_reportpage_iteration(mock_get_default_api):
    # Arrange: Set up our fake API and patch the get_default_api method.
    fake_api = FakeApi()
    mock_get_default_api.return_value = fake_api

    # Create a ReportPage with dummy service and arguments.
    # The actual values of service and args do not matter as long as the fake API returns data.
    rp = ReportPage(service="dummyService", args=["dummy_account", "dummy_report", {"displayColumns": ["val"]}],
                    api=fake_api)

    # Act: Iterate over ReportPage and collect items.
    items = list(rp)
    # The expected behavior: load_data returns a flattened list:
    # From first item: two stats dictionaries merged with {"extra": "x"}
    #   -> {"val": 1, "extra": "x"}, {"val": 2, "extra": "x"}
    # From second item: one stat merged with {"extra": "y"}
    #   -> {"val": 3, "extra": "y"}
    expected = [
        {"val": 1, "extra": "x"},
        {"val": 2, "extra": "x"},
        {"val": 3, "extra": "y"},
    ]
    assert items == expected

    # Iteration should stop after all items are read.
    with pytest.raises(StopIteration):
        next(iter(rp))


class MultiPageFakeApi:
    """Fake API that simulates multiple pages of report data."""

    def __init__(self, pages):
        """
        pages: a list of pages where each page is a list of report items.
        Each report item is a dict with 'stats' key (list of stat dicts)
        and possibly additional keys.
        """
        self.pages = pages
        self.call_count = 0

    def call(self, service, method, args):
        offset = args[-1].get("offset", 0)
        limit = args[-1].get("limit", 100)
        # Calculate which page to return based on offset/limit.
        page_index = self.call_count
        self.call_count += 1
        if page_index < len(self.pages):
            return {"report": self.pages[page_index]}
        return {"report": []}


@patch("sklik.SklikApi.get_default_api")
def test_reportpage_multiple_pages(mock_get_default_api):
    # Setup multiple pages:
    pages = [
        # Page 1: two items with stats
        [
            {"stats": [{"val": 10}], "extra": "a"},
            {"stats": [{"val": 20}], "extra": "b"},
        ],
        # Page 2: one item with two stats entries
        [
            {"stats": [{"val": 30}, {"val": 40}], "extra": "c"},
        ],
        # Page 3: empty page signaling the end.
        []
    ]
    fake_api = MultiPageFakeApi(pages)
    mock_get_default_api.return_value = fake_api

    rp = ReportPage(service="dummyService", args=["dummy", "dummy", {"displayColumns": ["val"]}], api=fake_api)
    items = list(rp)

    # Expect a flattened list:
    expected = [
        {"val": 10, "extra": "a"},
        {"val": 20, "extra": "b"},
        {"val": 30, "extra": "c"},
        {"val": 40, "extra": "c"},
    ]
    assert items == expected

    # Iterating further should raise StopIteration.
    rp_iter = iter(rp)
    with pytest.raises(StopIteration):
        for _ in range(10):
            next(rp_iter)


# ========= Tests for Report =========

class FakeApiReport:
    """A fake API to simulate both createReport and readReport calls.
    
    This class has been updated to handle the new behavior of the _load_report_chunk method
    in the Report class, which now uses a 4-step process: PROBE, CALCULATE, ADJUST, and EXECUTE.
    """

    def __init__(self):
        self.create_report_called = 0
        self.read_report_called = 0
        # Track the last date range used in createReport
        self.last_date_from = None
        self.last_date_to = None

    def call(self, service, method, args):
        if method == "createReport":
            self.create_report_called += 1
            # Extract date range from args to track it
            if len(args) > 1 and isinstance(args[1], dict):
                self.last_date_from = args[1].get("dateFrom")
                self.last_date_to = args[1].get("dateTo")
            
            # Return a fake reportId and totalCount
            # For the first call (PROBE), return a higher totalCount to simulate a large date range
            # For subsequent calls (ADJUST), return a smaller totalCount
            total_count = 5000 if self.create_report_called == 1 else 1
            
            return {"reportId": f"fake_report_{self.create_report_called}", "totalCount": total_count}
        elif method == "readReport":
            self.read_report_called += 1
            # Simulate returning one page with one item.
            return {
                "report": [
                    {"stats": [{"metric": 100}], "other": "test"}
                ]
            }
        raise ValueError("Unknown method")


class MultiPageFakeApiReport:
    """A fake API that simulates multiple createReport and readReport calls.
    
    This class has been updated to handle the new behavior of the _load_report_chunk method
    in the Report class, which now uses a 4-step process: PROBE, CALCULATE, ADJUST, and EXECUTE.
    """

    def __init__(self, pages_per_report):
        """
        pages_per_report: a list where each element is a list of pages.
        Each pages element is a list of pages for one report creation call.
        """
        self.pages_per_report = pages_per_report
        self.create_report_calls = 0
        self.read_report_calls = 0
        # Track whether we're in a PROBE or ADJUST phase for each date range
        self.probe_phase = True
        # Track the current date range index
        self.current_range_index = 0
        # Track the last date range used in createReport
        self.last_date_from = None
        self.last_date_to = None
        # Track which report ID is currently being read
        self.current_report_id = None

    def call(self, service, method, args):
        if method == "createReport":
            # Extract date range from args to track it
            if len(args) > 1 and isinstance(args[1], dict):
                self.last_date_from = args[1].get("dateFrom")
                self.last_date_to = args[1].get("dateTo")
            
            # Each call to createReport is either a PROBE or an ADJUST for a date range
            self.create_report_calls += 1
            report_id = f"report_{self.create_report_calls}"
            
            # For PROBE calls, return a higher totalCount to force the ADJUST phase
            # For ADJUST calls, return a smaller totalCount
            total_count = 5000 if self.probe_phase else 100
            
            # Toggle the phase for the next call
            # If we were in PROBE phase, next call will be ADJUST
            # If we were in ADJUST phase, next call will be PROBE for a new date range
            if self.probe_phase:
                self.probe_phase = False
            else:
                self.probe_phase = True
                self.current_range_index += 1
            
            # Reset read_report_calls when creating a new report
            self.read_report_calls = 0
            
            return {"reportId": report_id, "totalCount": total_count}
        elif method == "readReport":
            # Extract the report ID from args
            if len(args) > 1:
                self.current_report_id = args[1]
            
            # Parse the report number from the report ID
            # The format is "report_N" where N is the create_report_calls value
            try:
                report_num = int(self.current_report_id.split('_')[1])
                # Calculate which date range this report belongs to
                # Each date range has 2 reports (PROBE and ADJUST)
                # PROBE reports have odd numbers, ADJUST reports have even numbers
                range_index = (report_num - 1) // 2
                is_adjust = report_num % 2 == 0  # Even numbers are ADJUST reports
                
                # Only return data for ADJUST reports
                if is_adjust and range_index < len(self.pages_per_report):
                    pages = self.pages_per_report[range_index]
                    # Return one page per readReport call
                    if self.read_report_calls < len(pages):
                        result = {"report": pages[self.read_report_calls]}
                        self.read_report_calls += 1
                        return result
            except (ValueError, IndexError, AttributeError):
                pass  # If there's any error parsing the report ID, return empty data
            
            return {"report": []}
        raise ValueError("Unknown method")


@pytest.fixture
def valid_report_args():
    # Valid report_args consists of two dictionaries:
    # First: date parameters with valid 'dateFrom' and 'dateTo'
    # Second: display options with 'statGranularity'
    return [
        {"dateFrom": "2024-01-01", "dateTo": "2024-01-31"},
        {"statGranularity": "daily"}
    ]


def test_report_post_init_validation_invalid_length():
    # Test that Report raises an error if report_args does not have at least two elements.
    with pytest.raises(ValueError, match="report_args must be a list with at least two dictionaries"):
        Report(account_id=123, service="stats", report_args=[{"dateFrom": "2024-01-01"}], display_columns=["a"])


def test_report_post_init_validation_missing_date_keys(valid_report_args):
    # Remove 'dateFrom' key
    bad_args = valid_report_args.copy()
    bad_args[0] = {"dateTo": "2024-01-31"}
    with pytest.raises(ValueError, match="Date range dictionary must contain 'dateFrom' and 'dateTo'"):
        Report(account_id=123, service="stats", report_args=bad_args, display_columns=["a"])

    # Remove 'dateTo' key
    bad_args = valid_report_args.copy()
    bad_args[0] = {"dateFrom": "2024-01-01"}
    with pytest.raises(ValueError, match="Date range dictionary must contain 'dateFrom' and 'dateTo'"):
        Report(account_id=123, service="stats", report_args=bad_args, display_columns=["a"])


def test_report_post_init_validation_missing_statgranularity(valid_report_args):
    # Remove 'statGranularity' from second dict.
    bad_args = valid_report_args.copy()
    bad_args[1] = {}
    with pytest.raises(ValueError, match="Display options dictionary must contain 'statGranularity'"):
        Report(account_id=123, service="stats", report_args=bad_args, display_columns=["a"])


def test_report_post_init_invalid_date_format(valid_report_args):
    # Pass an invalid date format for dateFrom.
    bad_args = valid_report_args.copy()
    bad_args[0] = {"dateFrom": "01-01-2024", "dateTo": "2024-01-31"}
    with pytest.raises(ValueError, match="Invalid date format provided. Expected YYYY-MM-DD."):
        Report(account_id=123, service="stats", report_args=bad_args, display_columns=["a"])


@patch("sklik.SklikApi.get_default_api")
def test_report_iteration(mock_get_default_api, valid_report_args):
    # Arrange: use our fake API to simulate report creation and page reading.
    fake_api = FakeApiReport()
    mock_get_default_api.return_value = fake_api

    # Create a Report with a short interval so that after one iteration, StopIteration occurs.
    report = Report(
        account_id=123,
        service="stats",
        report_args=valid_report_args,
        display_columns=["metric"],
        api=fake_api
    )

    # Act: get one item from the iterator.
    first_item = next(report)
    # Expect the first item to be merged data from ReportPage load.
    assert first_item["metric"] == 100
    assert first_item["other"] == "test"

    # Because our fake API always returns the same page, calling next again will eventually loop.
    # For this test, we simulate only one page. Force StopIteration by altering the API to return an empty report.
    original_call = fake_api.call

    def empty_call(service, method, args):
        if method == "readReport":
            return {"report": []}
        return original_call(service, method, args)

    fake_api.call = empty_call
    with pytest.raises(StopIteration):
        next(report)


# Note: Tests for _update_report_dates have been removed as this method no longer exists
# in the Report class. The functionality has been replaced by the new implementation of
# _load_report_chunk which uses an adaptive optimization strategy for fetching report data.


@patch("sklik.SklikApi.get_default_api")
def test_report_multiple_pages_iteration(mock_get_default_api, valid_report_args):
    """
    Simulate a Report that, over successive _create_report calls,
    returns multiple pages and then moves to the next date sub-range.
    
    This test has been updated to work with the new behavior of the _load_report_chunk method
    in the Report class, which now uses a 4-step process: PROBE, CALCULATE, ADJUST, and EXECUTE.
    
    The MultiPageFakeApiReport class now simulates this behavior by:
    1. Having PROBE and ADJUST phases for each date range
    2. Only returning data for ADJUST calls (even-numbered create_report_calls)
    3. Tracking the current date range index separately from the create_report_calls count
    """
    # With the new implementation, each date range requires two createReport calls:
    # - First call (PROBE): Get totalCount for the entire range
    # - Second call (ADJUST): Get data for a smaller, optimized range
    #
    # We define pages for each date range (not for each createReport call)
    pages_per_report = [
        [
            # First date range: two pages.
            [
                {"stats": [{"val": 1}], "info": "page1"},
            ],
            [
                {"stats": [{"val": 2}], "info": "page2"},
            ],
        ],
        [
            # Second date range: one page.
            [
                {"stats": [{"val": 3}], "info": "page3"},
            ],
        ],
        [
            # Third date range: one page.
            [
                {"stats": [{"val": 4}], "info": "final"},
            ],
        ]
    ]
    fake_api = MultiPageFakeApiReport(pages_per_report)
    mock_get_default_api.return_value = fake_api

    # We set report_args such that the overall interval is large and will require multiple
    # date range iterations. The Report class will make two createReport calls for each range:
    # one for PROBE and one for ADJUST.
    report = Report(
        account_id=123,
        service="stats",
        report_args=valid_report_args,
        display_columns=["val"],
        api=fake_api
    )

    # Collect items. They should be yielded in order from all pages.
    items = []
    # Use a while loop to collect until StopIteration.
    try:
        while True:
            items.append(next(report))
    except StopIteration:
        pass

    expected = [
        {"val": 1, "info": "page1"},
        {"val": 2, "info": "page2"},
        {"val": 3, "info": "page3"},
        {"val": 4, "info": "final"},
    ]
    assert items == expected


# ========= Tests for create_report =========

class FakeAccount:
    def __init__(self, account_id, api):
        self.account_id = account_id
        self.api = api


@patch("sklik.SklikApi.get_default_api")
def test_create_report(mock_get_default_api, valid_report_args):
    # Arrange: Create a fake API that we can inspect.
    fake_api = FakeApiReport()
    mock_get_default_api.return_value = fake_api

    account = FakeAccount(account_id=789, api=fake_api)
    service = "campaigns"
    fields = ["clicks", "impressions"]
    since = "2024-02-01"
    until = "2024-02-28"
    granularity = "daily"
    restriction_filter = {"filterKey": "filterValue"}

    # Act: Create the report using the helper function.
    report_obj = create_report(
        account=account,
        service=service,
        fields=fields,
        since=since,
        until=until,
        granularity=granularity,
        restriction_filter=restriction_filter
    )

    # Assert: The report object should be correctly instantiated.
    assert isinstance(report_obj, Report)
    assert report_obj.account_id == 789
    assert report_obj.service == service
    # Also verify that the report_args include our parameters.
    date_args, display_args = report_obj.report_args
    assert date_args["dateFrom"] == pendulum.parse(since).to_date_string()
    assert date_args["dateTo"] == pendulum.parse(until).to_date_string()
    assert date_args["filterKey"] == "filterValue"
    assert display_args["statGranularity"] == granularity
    assert report_obj.display_columns == fields


@patch("sklik.SklikApi.get_default_api")
def test_create_report_with_minimal_parameters(mock_get_default_api):
    """
    Test create_report with only required parameters and ensure the Report is created.
    
    This test has been updated to work with the new behavior of the _load_report_chunk method
    in the Report class, which now uses a 4-step process: PROBE, CALCULATE, ADJUST, and EXECUTE.
    """
    # Use FakeApiReport instead of MultiPageFakeApiReport for simplicity
    fake_api = FakeApiReport()
    # Override the call method to return our test data
    original_call = fake_api.call
    
    def custom_call(service, method, args):
        if method == "readReport":
            return {"report": [{"stats": [{"metric": 55}], "label": "min"}]}
        return original_call(service, method, args)
    
    fake_api.call = custom_call
    mock_get_default_api.return_value = fake_api

    account = FakeAccount(account_id=321, api=fake_api)
    report_obj = create_report(
        account=account,
        service="campaigns",
        fields=["metric"],
        since="2024-04-01",
        until="2024-04-15",
        granularity="daily"
    )

    # The report_args should contain the date range and default display options.
    date_args, display_args = report_obj.report_args
    assert date_args["dateFrom"] == "2024-04-01"
    assert date_args["dateTo"] == "2024-04-15"
    assert display_args["statGranularity"] == "daily"

    # The report's iteration should yield the expected item.
    item = next(report_obj)
    assert item["metric"] == 55
    assert item["label"] == "min"
