import base64
import inspect
import json
import logging
from typing import Annotated, override

import fastmcp.tools
import gitlab.v4.objects
import httpx
import pydantic

from bir_mcp.core import BaseMcp, build_readonly_tools, build_write_tools
from bir_mcp.git_lab.prompts import get_prompts
from bir_mcp.git_lab.utils import GitLabUrl, MergeRequest, aget_merge_request_data
from bir_mcp.utils import (
    araise_for_status,
    filter_dict_by_keys,
    llm_friendly_http_request,
    prepend_url_path_prefix_if_not_present,
    to_maybe_ssl_context,
)

ProjectPathOrUrlType = Annotated[
    str,
    pydantic.Field(
        description=inspect.cleandoc("""
            Either the filesystem-like path to a GitLab project with variable depth, for example:
            "organization/project_name" or "organization/namespace/subgroup/project_name",
            or a full url to a GitLab project in the format:
            "https://{gitlab_domain}/{project_path}/[.git]".
        """)
    ),
]
BranchType = Annotated[
    str,
    pydantic.Field(description="The branch name to fetch files from."),
]


class GitLab(BaseMcp):
    def __init__(
        self,
        private_token: str,
        url: str = "https://gitlab.kapitalbank.az",
        ssl_verify: bool | str = True,
        timezone: str = "UTC",
    ):
        """
        GitLab GraphQL docs: https://docs.gitlab.com/api/graphql/
        Local instance GraphQL explorer: https://gitlab.kapitalbank.az/-/graphql-explorer
        """
        super().__init__(timezone=timezone)
        self.api_version = 4
        self.gitlab = gitlab.Gitlab(
            url=url,
            private_token=private_token,
            ssl_verify=ssl_verify,
            api_version=str(self.api_version),
        )
        self.gitlab.auth()
        self.ahttpx = httpx.AsyncClient(
            base_url=url,
            headers={"PRIVATE-TOKEN": private_token},
            verify=to_maybe_ssl_context(ssl_verify),
            event_hooks={"response": [araise_for_status]},
        )
        self.agraphql = gitlab.AsyncGraphQL(
            url=url,
            token=private_token,
            ssl_verify=ssl_verify,
        )
        self.gitlab_url = GitLabUrl(base_url=url)

    @override
    def get_tag(self):
        return "gitlab"

    @override
    def get_mcp_server_without_components(self):
        server = fastmcp.FastMCP(
            name="Bir GitLab MCP server",
            instructions=inspect.cleandoc("""
                GitLab related tools.
            """),
        )
        return server

    @override
    def get_mcp_tools(self, max_output_length: int | None = None, tags: set[str] | None = None):
        read_tools = [
            self.get_project_info,
            self.list_all_repo_branch_files,
            self.get_file_content,
            self.search_in_repository,
            self.get_latest_pipeline_info,
            self.get_merge_request_data,
            self.get_merge_request_data_from_url,
            self.search_users,
        ]
        write_tools_by_scopes = {
            ("api",): [
                self.create_merge_request,
                self.create_branch,
                self.http_request,
            ],
        }
        tools = build_readonly_tools(read_tools, max_output_length=max_output_length, tags=tags)
        pat_scopes = set(get_gitlab_pat_scopes(self.gitlab))
        for scopes, write_tools in write_tools_by_scopes.items():
            if set(scopes) - pat_scopes:
                logging.info(
                    f"GitLab token doesn't have {scopes} scope, skipping tools {write_tools}."
                )
            else:
                tools.extend(
                    build_write_tools(write_tools, max_output_length=max_output_length, tags=tags)
                )

        return tools

    @override
    def get_prompts(self):
        return get_prompts()

    def get_project_from_url(self, project_path_or_url: str) -> gitlab.v4.objects.Project:
        project_path = self.gitlab_url.extract_project_path(project_path_or_url)
        project = self.gitlab.projects.get(project_path)
        return project

    def prepend_api_version(self, path: str) -> str:
        return prepend_url_path_prefix_if_not_present(f"api/v{self.api_version}", path)

    async def http_request(
        self,
        path: Annotated[
            str,
            pydantic.Field(
                description=inspect.cleandoc("""
                    The path to the GitLab API endpoint, relative to the base URL.
                    Should not include the /api/version prefix.
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
        Performs a HTTP request to the GitLab REST API. Can be used when no specialized tool is available for the task.
        The arguments are passed to a httpx.Client.request method, with base_url set to local
        GitLab instance and API key set in headers, so the result looks like this:
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

    def get_project_info(self, project_path_or_url: ProjectPathOrUrlType) -> dict:
        """
        Retrieves metadata and general info about a GitLab project identified by the repo url,
        such as name, description, branches, last activity, topics (tags), etc.
        """
        project = self.get_project_from_url(project_path_or_url)
        branches = project.branches.list()
        branches = [branch.attributes["name"] for branch in branches]
        info = {
            "name_with_namespace": project.name_with_namespace,
            "topics": project.topics,
            "description": project.description,
            "last_activity_at": self.format_datetime_for_ai(project.last_activity_at),
            "web_url": project.web_url,
            "branches": branches,
        }
        return info

    def list_all_repo_branch_files(
        self,
        project_path_or_url: ProjectPathOrUrlType,
        branch: BranchType,
    ) -> dict:
        """Recursively lists all files and directories in the repository."""
        project = self.get_project_from_url(project_path_or_url)
        tree = project.repository_tree(ref=branch, get_all=True, recursive=True)
        tree = {"files": [{"path": item["path"], "type": item["type"]} for item in tree]}
        return tree

    def get_file_content(
        self,
        project_path_or_url: ProjectPathOrUrlType,
        branch: BranchType,
        file_path: Annotated[
            str,
            pydantic.Field(
                description="The path to the file relative to the root of the repository."
            ),
        ],
    ) -> dict:
        """Retrieves the text content of a specific file."""
        project = self.get_project_from_url(project_path_or_url)
        file = project.files.get(file_path=file_path, ref=branch)
        content = base64.b64decode(file.content).decode()
        content = {"file_content": content}
        return content

    def search_in_repository(
        self,
        project_path_or_url: ProjectPathOrUrlType,
        branch: BranchType,
        query: Annotated[str, pydantic.Field(description="The text query to search for.")],
    ) -> dict:
        """
        Performs a basic search for a text query within the repo's files.
        Doesn't support regex, but is case-insensitive.
        Returns a list of occurences within files, with file path, starting line in the file
        and a snippet of the contextual window in which the query was found.
        For details see the [API docs](https://docs.gitlab.com/api/search/#project-search-api).
        """
        project = self.get_project_from_url(project_path_or_url)
        results = project.search(scope="blobs", search=query, ref=branch)
        results = [
            {
                "file_path": result["path"],
                "starting_line_in_file": result["startline"],
                "snippet": result["data"],
            }
            for result in results
        ]
        results = {"search_results": results}
        return results

    def get_latest_pipeline_info(self, project_path_or_url: ProjectPathOrUrlType) -> dict:
        """Retrieves the latest pipeline info, such as url, status, duration, commit, jobs, etc."""
        project = self.get_project_from_url(project_path_or_url)
        pipeline = project.pipelines.latest()

        commit = project.commits.get(pipeline.sha)
        commit = filter_dict_by_keys(
            commit.attributes,
            ["title", "author_name", "web_url"],
        )

        jobs = pipeline.jobs.list(all=True)
        jobs = [
            filter_dict_by_keys(
                job.attributes,
                ["name", "status", "stage", "allow_failure", "web_url"],
            )
            for job in jobs
        ]

        info = {
            "web_url": pipeline.web_url,
            "created_at": self.format_datetime_for_ai(pipeline.created_at),
            "status": pipeline.status,
            "source": pipeline.source,
            "duration_seconds": pipeline.duration,
            "queued_duration_seconds": pipeline.queued_duration,
            "commit_sha": pipeline.sha,
            "commit": commit,
            "jobs": jobs,
        }
        return info

    async def get_merge_request_data(
        self,
        project_path_or_url: ProjectPathOrUrlType,
        merge_request_iid: Annotated[
            int,
            pydantic.Field(
                description=inspect.cleandoc("""
                    The internal id of a GitLab merge request, can be extracted from a merge request url
                    if it ends in the following suffix: "/-/merge_requests/{merge_request_iid}".
                """)
            ),
        ],
    ) -> dict:
        """Fetch some details about a GitLab merge request, like diffs, title, description."""
        project_path = self.gitlab_url.extract_project_path(project_path_or_url)
        merge_request_data = await aget_merge_request_data(
            project=project_path,
            merge_request_iid=merge_request_iid,
            agraphql=self.agraphql,
            ahttpx_client=self.ahttpx,
        )
        return merge_request_data

    async def get_merge_request_data_from_url(
        self,
        merge_request_url: Annotated[
            str,
            pydantic.Field(
                description=inspect.cleandoc("""
                    The url for merge request, in the format:
                    "https://{gitlab_domain}/{project_path}/-/merge_requests/{merge_request_iid}".
                """)
            ),
        ],
    ) -> dict:
        """Fetch some details about a GitLab merge request, like diffs, title, description."""
        merge_request: MergeRequest = self.gitlab_url.extract_merge_request(merge_request_url)
        merge_request_data = await self.get_merge_request_data(
            project_path_or_url=merge_request.project_path,
            merge_request_iid=merge_request.merge_request_iid,
        )
        return merge_request_data

    def create_merge_request(
        self,
        project_path_or_url: ProjectPathOrUrlType,
        source_branch: Annotated[
            str,
            pydantic.Field(
                description="The source branch name for the merge request, usually a feature or testing branch."
            ),
        ],
        target_branch: Annotated[
            str,
            pydantic.Field(
                description="The target branch name for the merge request, usually 'testing' or 'main'."
            ),
        ],
        title: Annotated[
            str,
            pydantic.Field(description="The title of the merge request."),
        ],
        description: Annotated[
            str,
            pydantic.Field(description="The description of the merge request."),
        ],
        assignee_id: Annotated[
            int | None,
            pydantic.Field(description="The GitLab user id to assign the merge request to."),
        ] = None,
        labels: Annotated[
            list[str] | None,
            pydantic.Field(description="List of labels to add to the merge request."),
        ] = None,
        remove_source_branch: Annotated[
            bool,
            pydantic.Field(
                description="Whether to remove the source branch when the merge request is merged."
            ),
        ] = True,
        squash: Annotated[
            bool,
            pydantic.Field(description="Whether to squash commits when merging."),
        ] = False,
    ) -> dict:
        """Create a new GitLab merge request."""
        project = self.get_project_from_url(project_path_or_url)
        mr_data = {
            "source_branch": source_branch,
            "target_branch": target_branch,
            "title": title,
            "remove_source_branch": remove_source_branch,
            "squash": squash,
            "description": description,
        }
        if assignee_id:
            mr_data["assignee_id"] = assignee_id
        if labels:
            mr_data["labels"] = ",".join(labels)

        merge_request = project.mergerequests.create(mr_data)
        merge_request = {
            "id": merge_request.id,
            "iid": merge_request.iid,
            "web_url": merge_request.web_url,
        }
        merge_request = {"created_merge_request": merge_request}
        return merge_request

    def search_users(
        self,
        query: Annotated[
            str,
            pydantic.Field(description="The query to search users by the username, name or email."),
        ],
    ) -> dict:
        """Search for GitLab users, primarily used to get user emails or internal ids."""
        # Only admin can search by private emails and get other user's private emails.
        users = self.gitlab.users.list(search=query)
        users = [
            filter_dict_by_keys(user.attributes, ["id", "username", "name", "email"])
            for user in users
        ]
        users = {"users": users}
        return users

    def create_branch(
        self,
        project_path_or_url: ProjectPathOrUrlType,
        new_branch_name: str,
        source_ref: Annotated[
            str,
            pydantic.Field(description="The source branch, tag, or commit SHA."),
        ],
    ) -> dict:
        """Creates a new branch in the GitLab project."""
        project = self.get_project_from_url(project_path_or_url)
        branch_data = {"branch": new_branch_name, "ref": source_ref}
        new_branch = project.branches.create(branch_data)
        new_branch = {"new_branch_url": new_branch.web_url}
        return new_branch

    def create_file(
        self,
        project_path_or_url: ProjectPathOrUrlType,
        branch: str,
        file_path: Annotated[
            str,
            pydantic.Field(
                description=inspect.cleandoc("""
                    The path to the file relative to the root of the repository. 
                    Any parent directories will be created if they don't exist.
                """)
            ),
        ],
        file_content: str,
        author_email: str,
        commit_message: str | None = None,
    ) -> dict:
        """Creates a new file in the GitLab project branch. Fails if file already exists."""
        raise_if_branch_editing_not_allowed(branch)
        project = self.get_project_from_url(project_path_or_url)
        commit_message = commit_message or f"Add file {file_path} to {branch} branch"
        actions = [
            {
                "action": "create",
                "file_path": file_path,
                "content": file_content,
                "encoding": "text",
            }
        ]
        commit = {
            "branch": branch,
            "commit_message": commit_message,
            "author_email": author_email,
            "actions": actions,
        }
        commit = project.commits.create(commit)
        status = {"commit_url": commit.web_url}
        return status


def get_gitlab_pat_scopes(gl: gitlab.Gitlab) -> list[str]:
    pat = gl.personal_access_tokens.get("self")
    scopes = sorted(pat.scopes)
    return scopes


def raise_if_branch_editing_not_allowed(branch: str):
    if not branch.startswith("feature/"):
        raise ValueError(
            "Due to safety considerations, modifying branches or content is only allowed in feature branches."
        )
