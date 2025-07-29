from typing import Any, Callable, Dict, List, Union, Awaitable, TypedDict
from typing_extensions import NotRequired

from ....types import IntFloat
from .literals import ChartAggregator

ChartSeriesDataKey = Union[str, int, float]
ChartSeriesDataRow = Dict[ChartSeriesDataKey, Any]
ChartSeriesData = List[ChartSeriesDataRow]

ChartSeriesValueFnResult = Union[None, IntFloat, Awaitable[IntFloat], Awaitable[None]]
ChartSeriesGroupFnResult = Union[
    ChartSeriesDataKey, None, Awaitable[ChartSeriesDataKey], Awaitable[None]
]


class ChartAdvancedSeries(TypedDict):
    label: NotRequired[str]
    aggregate: NotRequired[ChartAggregator]
    value: Union[
        ChartSeriesDataKey,
        Callable[[], ChartSeriesValueFnResult],
        Callable[[ChartSeriesDataRow], ChartSeriesValueFnResult],
        Callable[[ChartSeriesDataRow, int], ChartSeriesValueFnResult],
    ]


ChartBasicSeries = ChartSeriesDataKey
ChartSeries = Union[ChartBasicSeries, ChartAdvancedSeries]


CHART_LABEL_SERIES_KEY = "_c*id_"
