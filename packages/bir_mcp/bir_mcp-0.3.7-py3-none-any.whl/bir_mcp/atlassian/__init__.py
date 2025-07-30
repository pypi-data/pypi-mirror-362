import inspect
from typing import Annotated, Iterable, override

import atlassian
import fastmcp.tools
import httpx
import pydantic

from bir_mcp.atlassian.utils import (
    generate_directed_linked_issues,
    infer_jira_field_representation,
    normalize_line_breaks,
)
from bir_mcp.core import BaseMcp, build_readonly_tools, build_write_tools
from bir_mcp.utils import (
    araise_for_status,
    filter_dict_by_keys,
    llm_friendly_http_request,
    prepend_url_path_prefix_if_not_present,
    to_maybe_ssl_context,
)

IssueKeyType = Annotated[
    str,
    pydantic.Field(
        description="The Jira issue key in the format {jira_project_key}-{issue_sequntial_number}, for example ABC-123"
    ),
]


class Atlassian(BaseMcp):
    def __init__(
        self,
        token: str,
        url: str = "https://jira-support.kapitalbank.az",
        api_version: int = 2,
        http_timeout_seconds: int = 10,
        backoff_and_retry: bool = True,
        retry_status_codes: Iterable[int] = (413, 429, 503, 504),
        max_backoff_seconds: int = 10,
        max_backoff_retries: int = 3,
        timezone: str = "UTC",
        ssl_verify: bool | str = True,
    ):
        super().__init__(timezone=timezone)
        self.jira = atlassian.Jira(
            url=url,
            token=token,
            api_version=api_version,
            verify_ssl=bool(ssl_verify),
            timeout=http_timeout_seconds,
            backoff_and_retry=backoff_and_retry,
            retry_status_codes=retry_status_codes,
            max_backoff_retries=max_backoff_retries,
            max_backoff_seconds=max_backoff_seconds,
        )
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.ahttpx = httpx.AsyncClient(
            base_url=url,
            headers=headers,
            event_hooks={"response": [araise_for_status]},
            timeout=http_timeout_seconds,
            verify=to_maybe_ssl_context(ssl_verify),
        )
        self.api_version = api_version
        # anon_codec: AnonCodec
        # anon_codec.anonymize

    @override
    def get_tag(self):
        return "atlassian"

    @override
    def get_mcp_server_without_components(self):
        server = fastmcp.FastMCP(
            name="Bir Atlassian MCP server",
            instructions=inspect.cleandoc("""
                Atlassian related tools, such as Jira, Jira Service Desk, Confluence, etc.
            """),
        )
        return server

    @override
    def get_mcp_tools(self, max_output_length: int | None = None, tags: set[str] | None = None):
        read_tools = [
            self.get_raw_jira_issue_fields,  # TODO: need to use anon_codec.anonymize on its output.
            self.get_allowed_issue_types_for_project,
            self.search_users,
            self.get_jira_issue_overview,
        ]
        write_tools = [
            self.create_jira_issue,
            self.jira_http_request,
        ]
        tools = build_readonly_tools(read_tools, max_output_length=max_output_length, tags=tags)
        tools.extend(build_write_tools(write_tools, max_output_length=max_output_length, tags=tags))
        return tools

    def build_issue_url(self, issue_key: str) -> str:
        return f"{self.jira.url}/browse/{issue_key}"

    def get_allowed_issue_types_for_project(self, project_key: str) -> dict:
        """
        Fetch all Jira issue types allowed in the project, grouped into tasks and subtasks,
        with optional descriptions.
        """
        project = self.jira.project(project_key)
        issue_types = project["issueTypes"]
        tasks = {}
        subtasks = {}
        for issue_type in issue_types:
            filtered_issue_type = {issue_type["name"]: issue_type["description"]}
            if issue_type["subtask"]:
                subtasks |= filtered_issue_type
            else:
                tasks |= filtered_issue_type

        issue_types = dict(tasks=tasks, subtasks=subtasks)
        return issue_types

    def prepend_api_version(self, path: str) -> str:
        return prepend_url_path_prefix_if_not_present(f"rest/api/{self.api_version}", path)

    async def ahttpx_get(self, endpoint: str, **kwargs) -> httpx.Response:
        endpoint = self.prepend_api_version(endpoint)
        response = await self.ahttpx.get(url=endpoint, params=kwargs)
        return response

    async def jira_http_request(
        self,
        path: Annotated[
            str,
            pydantic.Field(
                description=inspect.cleandoc("""
                    The path to the Jira API endpoint, relative to the base URL.
                    Should not include the /rest/api/version prefix.
                """)
            ),
        ],
        http_method: str = "GET",
        json_query_params: Annotated[
            str | None,
            pydantic.Field(description="The url query parameters dict, serialized to JSON."),
        ] = None,
        content: Annotated[
            str | dict | None,
            pydantic.Field(description="The request body."),
        ] = None,
    ) -> dict:
        """
        Performs a HTTP request to the Jira REST API. Can be used when no specialized tool is available for the task.
        The arguments are passed to a httpx.Client.request method, with base_url set to local
        Jira instance and API key set in headers, so the result looks like this:
        return client.request(method=http_method, url=path, params=json.loads(json_query_params), content=content).json()
        """
        data = await llm_friendly_http_request(
            client=self.ahttpx,
            url=self.prepend_api_version(path),
            http_method=http_method,
            json_query_params=json_query_params,
            content=content,
            ensure_dict_output=True,
        )
        return data

    async def get_raw_jira_issue_fields(
        self,
        issue_key: IssueKeyType,
        issue_fields: Annotated[
            Iterable[str],
            pydantic.Field(description="The fields to fetch from the Jira issue"),
        ] = ("summary", "description"),
    ) -> dict:
        """Fetch raw issue fields for given Jira issue."""
        response = await self.ahttpx_get(f"issue/{issue_key}", fields=",".join(issue_fields))
        response = response.json()
        fields = response["fields"]
        return fields

    async def get_jira_issue_overview(self, issue_key: IssueKeyType) -> dict:
        """
        Fetch a preformatted set of general Jira issue fields and attributes,
        such as summary, description, comments, issue type, parent, subtasks,
        issue links, priority.
        """
        fields = [
            "summary",
            "description",
            "comment",
            "issuetype",
            "parent",
            "subtasks",
            "issuelinks",
            "priority",
        ]
        response = await self.ahttpx_get(f"issue/{issue_key}", fields=",".join(fields))
        fields = response.json()["fields"]
        fields = {k: infer_jira_field_representation(v) for k, v in fields.items()}

        comments = fields.pop("comment")["comments"]
        comments = sorted(comments, key=lambda c: c["created"])
        comments = [f"{c['author']['displayName']}: {c['body']}" for c in comments]
        fields["comments"] = comments

        fields["issuelinks"] = [
            f"{directed_link}: {linked_issue['key']}"
            for directed_link, linked_issue in generate_directed_linked_issues(fields)
        ]

        fields = {
            key: normalize_line_breaks(value) if isinstance(value, str) else value
            for key, value in fields.items()
        }
        return fields

    def create_jira_issue(
        self,
        project_key: Annotated[
            str, pydantic.Field(description="The key of a Jira project to create an issue in.")
        ],
        description: str,
        summary: str,
        issue_type: Annotated[
            str,
            pydantic.Field(
                description=inspect.cleandoc(f"""
                    The name of a Jira issue type to create, for example Development Task, Bug, Kanban Feature.
                    Note that each project has its own set of allowed issue types, for details refer to the 
                    "{get_allowed_issue_types_for_project.__name__}" tool.
                """),
            ),
        ],
        assignee: Annotated[
            str | None,
            pydantic.Field(description="The name of a Jira user to assign the issue to."),
        ] = None,
        additional_fields: Annotated[
            dict | None, pydantic.Field(description="Additional fields to set on the Jira issue.")
        ] = None,
    ) -> dict:
        """Create a new Jira issue and get its key."""
        fields = additional_fields or {}
        fields |= {
            "summary": summary,
            "description": description,
            "project": {"key": project_key},
            "issuetype": {"name": issue_type},
        }
        if assignee:
            fields["assignee"] = {"name": assignee}

        issue = self.jira.create_issue(fields=fields)
        issue_key = issue["key"]
        created_issue = {
            "created_issue_key": issue_key,
            "url": self.build_issue_url(issue_key),
        }
        return created_issue

    def search_users(
        self,
        query: Annotated[
            str,
            pydantic.Field(
                description="The query to search users by a non-case-sensitive match of username, name or email."
            ),
        ],
    ) -> dict:
        """Search for Jira users, primarily usefull to find an exact user name."""
        users = self.jira.user_find_by_user_string(username=query)
        users = [
            filter_dict_by_keys(user, ["name", "displayName", "emailAddress"]) for user in users
        ]
        users = dict(users=users)
        return users
