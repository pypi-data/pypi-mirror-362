"""Generalized truncation framework for tool results."""

from abc import ABC, abstractmethod
from typing import TypeVar, cast

from msgspec.structs import replace

from exponent.core.remote_execution.cli_rpc_types import (
    BashToolResult,
    ErrorToolResult,
    GlobToolResult,
    GrepToolResult,
    ListToolResult,
    ReadToolResult,
    ToolResult,
    WriteToolResult,
)
from exponent.core.remote_execution.utils import truncate_output

DEFAULT_CHARACTER_LIMIT = 90_000
DEFAULT_LIST_ITEM_LIMIT = 1000
DEFAULT_LIST_PREVIEW_ITEMS = 10


class TruncationStrategy(ABC):

    @abstractmethod
    def should_truncate(self, result: ToolResult) -> bool:
        pass

    @abstractmethod
    def truncate(self, result: ToolResult) -> ToolResult:
        pass


class StringFieldTruncation(TruncationStrategy):

    def __init__(
        self,
        field_name: str,
        character_limit: int = DEFAULT_CHARACTER_LIMIT,
    ):
        self.field_name = field_name
        self.character_limit = character_limit

    def should_truncate(self, result: ToolResult) -> bool:
        if hasattr(result, self.field_name):
            value = getattr(result, self.field_name)
            if isinstance(value, str):
                return len(value) > self.character_limit
        return False

    def truncate(self, result: ToolResult) -> ToolResult:
        if not hasattr(result, self.field_name):
            return result

        value = getattr(result, self.field_name)
        if not isinstance(value, str):
            return result

        truncated_value, was_truncated = truncate_output(value, self.character_limit)

        updates = {self.field_name: truncated_value}
        if hasattr(result, "truncated") and was_truncated:
            updates["truncated"] = True

        return replace(result, **updates)


class ListFieldTruncation(TruncationStrategy):

    def __init__(
        self,
        field_name: str,
        item_limit: int = DEFAULT_LIST_ITEM_LIMIT,
        preview_items: int = DEFAULT_LIST_PREVIEW_ITEMS,
    ):
        self.field_name = field_name
        self.item_limit = item_limit
        self.preview_items = preview_items

    def should_truncate(self, result: ToolResult) -> bool:
        if hasattr(result, self.field_name):
            value = getattr(result, self.field_name)
            if isinstance(value, list):
                return len(value) > self.item_limit
        return False

    def truncate(self, result: ToolResult) -> ToolResult:
        if not hasattr(result, self.field_name):
            return result

        value = getattr(result, self.field_name)
        if not isinstance(value, list):
            return result

        total_items = len(value)
        if total_items <= self.item_limit:
            return result

        truncated_count = max(0, total_items - 2 * self.preview_items)
        truncated_list = (
            value[: self.preview_items]
            + [f"... {truncated_count} items truncated ..."]
            + value[-self.preview_items :]
        )

        updates = {self.field_name: truncated_list}
        if hasattr(result, "truncated"):
            updates["truncated"] = True

        return replace(result, **updates)


class CompositeTruncation(TruncationStrategy):

    def __init__(self, strategies: list[TruncationStrategy]):
        self.strategies = strategies

    def should_truncate(self, result: ToolResult) -> bool:
        return any(strategy.should_truncate(result) for strategy in self.strategies)

    def truncate(self, result: ToolResult) -> ToolResult:
        for strategy in self.strategies:
            if strategy.should_truncate(result):
                result = strategy.truncate(result)
        return result


TRUNCATION_REGISTRY: dict[type[ToolResult], TruncationStrategy] = {
    ReadToolResult: StringFieldTruncation("content"),
    WriteToolResult: StringFieldTruncation("message"),
    BashToolResult: StringFieldTruncation("shell_output"),
    GrepToolResult: ListFieldTruncation("matches"),
    GlobToolResult: ListFieldTruncation("filenames"),
    ListToolResult: ListFieldTruncation("files"),
}


T = TypeVar("T", bound=ToolResult)


def truncate_tool_result(result: T) -> T:
    if isinstance(result, ErrorToolResult):
        return result

    result_type = type(result)
    if result_type in TRUNCATION_REGISTRY:
        strategy = TRUNCATION_REGISTRY[result_type]
        if strategy.should_truncate(result):
            return cast(T, strategy.truncate(result))

    return result


def register_truncation_strategy(
    result_type: type[ToolResult],
    strategy: TruncationStrategy,
) -> None:
    TRUNCATION_REGISTRY[result_type] = strategy


def configure_truncation_limits(
    character_limit: int | None = None,
    list_item_limit: int | None = None,
    list_preview_items: int | None = None,
) -> None:
    for strategy in TRUNCATION_REGISTRY.values():
        if isinstance(strategy, StringFieldTruncation) and character_limit is not None:
            strategy.character_limit = character_limit
        elif isinstance(strategy, ListFieldTruncation):
            if list_item_limit is not None:
                strategy.item_limit = list_item_limit
            if list_preview_items is not None:
                strategy.preview_items = list_preview_items
        elif isinstance(strategy, CompositeTruncation):
            for sub_strategy in strategy.strategies:
                if isinstance(sub_strategy, StringFieldTruncation) and character_limit:
                    sub_strategy.character_limit = character_limit
                elif isinstance(sub_strategy, ListFieldTruncation):
                    if list_item_limit is not None:
                        sub_strategy.item_limit = list_item_limit
                    if list_preview_items is not None:
                        sub_strategy.preview_items = list_preview_items
