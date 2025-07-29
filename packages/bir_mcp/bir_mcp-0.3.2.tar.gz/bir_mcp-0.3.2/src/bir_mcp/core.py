import abc
import datetime
import zoneinfo
from typing import Iterable

import fastmcp.prompts
import fastmcp.resources
import fastmcp.tools
import mcp

from bir_mcp.utils import (
    add_mcp_server_components,
    assign_default_tool_annotation_hints,
    format_datetime_for_ai,
    to_fastmcp_tool,
)


def build_tools(
    functions: Iterable[callable],
    annotations: mcp.types.ToolAnnotations | None = None,
    max_output_length: int | None = None,
    tags: set[str] | None = None,
) -> list[fastmcp.tools.FunctionTool]:
    tools = [
        to_fastmcp_tool(
            function,
            tags=tags,
            annotations=annotations,
            max_output_length=max_output_length,
        )
        for function in functions
    ]
    return tools


def build_readonly_tools(
    functions: Iterable[callable],
    max_output_length: int | None = None,
    tags: set[str] | None = None,
) -> list[fastmcp.tools.FunctionTool]:
    tools = build_tools(
        functions=functions,
        annotations=mcp.types.ToolAnnotations(
            readOnlyHint=True, destructiveHint=False, idempotentHint=True
        ),
        max_output_length=max_output_length,
        tags=tags,
    )
    return tools


def build_write_tools(
    functions: Iterable[callable],
    max_output_length: int | None = None,
    tags: set[str] | None = None,
) -> list[fastmcp.tools.FunctionTool]:
    tools = build_tools(
        functions=functions,
        annotations=mcp.types.ToolAnnotations(
            readOnlyHint=False, destructiveHint=False, idempotentHint=False
        ),
        max_output_length=max_output_length,
        tags=tags,
    )
    return tools


def build_resources(
    resource_uri_functions: dict[str, callable], tags: set[str] | None = None
) -> list[fastmcp.resources.Resource]:
    resources = [
        fastmcp.resources.Resource.from_function(function, uri=uri, tags=tags)
        for uri, function in resource_uri_functions.items()
    ]
    return resources


def build_prompts(
    prompts: Iterable[callable], tags: set[str] | None = None
) -> list[fastmcp.prompts.Prompt]:
    prompts = [fastmcp.prompts.Prompt.from_function(function, tags=tags) for function in prompts]
    return prompts


class BaseMcp(abc.ABC):
    def __init__(self, timezone: str = "UTC"):
        self.timezone = zoneinfo.ZoneInfo(timezone)

    def format_datetime_for_ai(self, date: datetime.datetime | str) -> str:
        return format_datetime_for_ai(date, timezone=self.timezone)

    def get_tag(self) -> str | None:
        return

    def get_mcp_server_without_components(self) -> fastmcp.FastMCP:
        return fastmcp.FastMCP()

    def get_tools(self) -> list[callable]:
        return []

    def get_uri_resources(self) -> dict[str, callable]:
        return {}

    def get_prompts(self) -> list[callable]:
        return []

    def get_mcp_tools(
        self, max_output_length: int | None = None, tags: set[str] | None = None
    ) -> list[fastmcp.tools.FunctionTool]:
        tools = self.get_tools()
        tools = build_tools(functions=tools, max_output_length=max_output_length, tags=tags)
        return tools

    def get_mcp_resources(self, tags: set[str] | None = None) -> list[fastmcp.resources.Resource]:
        uri_resources = self.get_uri_resources()
        resources = build_resources(resource_uri_functions=uri_resources, tags=tags)
        return resources

    def get_mcp_prompts(self, tags: set[str] | None = None) -> list[fastmcp.prompts.Prompt]:
        prompts = self.get_prompts()
        prompts = build_prompts(prompts=prompts, tags=tags)
        return prompts

    def get_mcp_server(
        self,
        server_to_extend: fastmcp.FastMCP | None = None,
        include_non_readonly_tools: bool = False,
        include_destructive_tools: bool = False,
        max_output_length: int | None = None,
        tags: set[str] | None = None,
        prompts_to_tools: bool = False,
    ) -> fastmcp.FastMCP:
        server = server_to_extend or self.get_mcp_server_without_components()
        tags = {self.get_tag()} if tags is None and self.get_tag() else tags
        tools = self.get_mcp_tools(max_output_length=max_output_length, tags=tags)
        filtered_tools = []
        for tool in tools:
            tool.annotations = assign_default_tool_annotation_hints(tool.annotations)
            if not include_non_readonly_tools and not tool.annotations.readOnlyHint:
                continue
            if not include_destructive_tools and tool.annotations.destructiveHint:
                continue
            filtered_tools.append(tool)

        resources = self.get_mcp_resources(tags=tags)
        prompts = self.get_mcp_prompts(tags=tags)
        if prompts_to_tools:
            filtered_tools.extend(build_readonly_tools([p.fn for p in prompts], tags=tags))

        server = add_mcp_server_components(
            server=server,
            tools=filtered_tools,
            resources=resources,
            prompts=prompts,
        )
        return server
