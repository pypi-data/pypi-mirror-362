import base64
import inspect
import logging
import re
from typing import Annotated, override

import fastmcp.tools
import gitlab.v4.objects
import httpx
import pydantic

from bir_mcp.atlassian.utils import collect_jira_issue_keys_in_text
from bir_mcp.core import AhttpxMixin, BaseMcp, build_readonly_tools, build_write_tools
from bir_mcp.git_lab.annotations import BranchType, MergeRequestIidType, ProjectPathOrUrlType
from bir_mcp.git_lab.utils import (
    GitLabUrl,
    MergeRequest,
    aget_project_id_from_path,
    get_ansi_escape_pattern,
    get_gitlab_pat_scopes,
)
from bir_mcp.utils import (
    araise_for_status,
    filter_dict_by_keys,
    get_line_separated_text_overview,
    prepend_url_path_prefix_if_not_present,
    to_maybe_ssl_context,
)


class GitLabTools(BaseMcp, AhttpxMixin):
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
            self.get_merge_request_overview,
            self.get_merge_request_overview_from_url,
            self.get_merge_request_file_diffs,
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
    def prepend_api(self, path: str) -> str:
        return prepend_url_path_prefix_if_not_present(f"api/v{self.api_version}", path)

    def get_project_from_url(self, project_path_or_url: str) -> gitlab.v4.objects.Project:
        project_path = self.gitlab_url.extract_project_path(project_path_or_url)
        project = self.gitlab.projects.get(project_path)
        return project

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

    async def get_merge_request_file_diffs(
        self,
        project_path_or_url: ProjectPathOrUrlType,
        merge_request_iid: MergeRequestIidType,
        file_paths: Annotated[
            list[str],
            pydantic.Field(description="The paths to the new files relative to the merge request."),
        ],
    ) -> dict:
        """
        Fetch full diffs for specific files in a merge request, based on the new file paths.
        Should be called with several paths at once for efficiency.
        """
        merge_request = await self.get_merge_request(project_path_or_url, merge_request_iid)
        diffs = []
        for change in merge_request["changes"]:
            if change["new_path"] in file_paths:
                diff = filter_dict_by_keys(change, ["new_path", "diff"])
                diffs.append(diff)

        diffs = {"diffs": diffs}
        return diffs

    async def get_project_id(self, project_path_or_url: ProjectPathOrUrlType) -> int:
        project_path = self.gitlab_url.extract_project_path(project_path_or_url)
        project_id = await aget_project_id_from_path(graphql=self.agraphql, project=project_path)
        return project_id

    async def get_merge_request(
        self,
        project_path_or_url: ProjectPathOrUrlType,
        merge_request_iid: MergeRequestIidType,
    ) -> dict:
        project_id = await self.get_project_id(project_path_or_url)
        endpoint = f"/projects/{project_id}/merge_requests/{merge_request_iid}/changes"
        response = await self.ahttpx_get(endpoint, access_raw_diffs=True, unidiff=True)
        merge_request = response.json()
        return merge_request

    async def get_merge_request_overview(
        self,
        project_path_or_url: ProjectPathOrUrlType,
        merge_request_iid: MergeRequestIidType,
        first_diff_lines: int = 6,
    ) -> dict:
        """
        Fetch overview details about a GitLab merge request, such as title, description, branches, diffs,
        pipeline status and jobs. The diffs and job traces are truncated, for full diffs and files use
        other tools.
        """
        merge_request = await self.get_merge_request(project_path_or_url, merge_request_iid)
        overview = filter_dict_by_keys(
            merge_request, ["title", "description", "source_branch", "target_branch"]
        )
        changes_overview = []
        for change in merge_request["changes"]:
            change_overview = filter_dict_by_keys(change, ["old_path", "new_path"])
            change_overview["diff_first_lines"] = "\n".join(
                change["diff"].splitlines()[:first_diff_lines]
            )
            if change["new_file"]:
                change_overview.pop("old_path")
            if change["deleted_file"]:
                change_overview.pop("new_path")

            changes_overview.append(change_overview)

        overview["changes_overview"] = changes_overview
        head_pipeline = merge_request["head_pipeline"]
        overview["pipeline_status"] = (head_pipeline or {}).get("status")
        jobs = []
        if head_pipeline:
            project_id = merge_request["project_id"]
            endpoint = f"/projects/{project_id}/pipelines/{head_pipeline['id']}/jobs"
            response = await self.ahttpx_get(endpoint, per_page=100)
            ansi = re.compile(get_ansi_escape_pattern())
            for job in response.json():
                job_id = job["id"]
                trace = await self.ahttpx_get(f"/projects/{project_id}/jobs/{job_id}/trace")
                trace = trace.text
                trace = ansi.sub(repl="", string=trace)
                if job["name"] == "Run Up: PreFlight":
                    if match := re.search("\nJIRA_NAMES: *(.*?)\n", trace):
                        jira_issues = match.group(1)
                        jira_issues = collect_jira_issue_keys_in_text(jira_issues)
                        overview["related_jira_issues"] = jira_issues

                trace_overview = get_line_separated_text_overview(
                    trace, line_chunks_len=first_diff_lines
                )
                job = filter_dict_by_keys(job, ["name", "stage", "status", "web_url"])
                job["trace_overview"] = trace_overview
                jobs.append(job)

        overview["pipeline_jobs"] = jobs
        return overview

    async def get_merge_request_overview_from_url(
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
        """
        Fetch overview about a GitLab merge request, is a convenience function that calls the
        get_merge_request_overview tool.
        """
        merge_request: MergeRequest = self.gitlab_url.extract_merge_request(merge_request_url)
        merge_request_overview = await self.get_merge_request_overview(
            project_path_or_url=merge_request.project_path,
            merge_request_iid=merge_request.merge_request_iid,
        )
        return merge_request_overview

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


def raise_if_branch_editing_not_allowed(branch: str):
    if not branch.startswith("feature/"):
        raise ValueError(
            "Due to safety considerations, modifying branches or content is only allowed in feature branches."
        )
