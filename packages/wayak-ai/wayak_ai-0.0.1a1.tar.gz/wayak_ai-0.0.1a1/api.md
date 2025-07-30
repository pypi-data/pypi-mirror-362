# Users

Types:

```python
from wayak_ai.types import (
    UserCreateResponse,
    UserListContextsResponse,
    UserListProjectsResponse,
    UserListThreadsResponse,
)
```

Methods:

- <code title="post /api/users">client.users.<a href="./src/wayak_ai/resources/users/users.py">create</a>(\*\*<a href="src/wayak_ai/types/user_create_params.py">params</a>) -> <a href="./src/wayak_ai/types/user_create_response.py">UserCreateResponse</a></code>
- <code title="get /api/users/{user_id}/contexts">client.users.<a href="./src/wayak_ai/resources/users/users.py">list_contexts</a>(user_id) -> <a href="./src/wayak_ai/types/user_list_contexts_response.py">UserListContextsResponse</a></code>
- <code title="get /api/users/{user_id}/projects">client.users.<a href="./src/wayak_ai/resources/users/users.py">list_projects</a>(user_id, \*\*<a href="src/wayak_ai/types/user_list_projects_params.py">params</a>) -> <a href="./src/wayak_ai/types/user_list_projects_response.py">UserListProjectsResponse</a></code>
- <code title="get /api/users/{user_id}/threads">client.users.<a href="./src/wayak_ai/resources/users/users.py">list_threads</a>(user_id, \*\*<a href="src/wayak_ai/types/user_list_threads_params.py">params</a>) -> <a href="./src/wayak_ai/types/user_list_threads_response.py">UserListThreadsResponse</a></code>

## Context

Types:

```python
from wayak_ai.types.users import PersistentUserContext
```

Methods:

- <code title="post /api/users/context">client.users.context.<a href="./src/wayak_ai/resources/users/context.py">create</a>(\*\*<a href="src/wayak_ai/types/users/context_create_params.py">params</a>) -> <a href="./src/wayak_ai/types/users/persistent_user_context.py">PersistentUserContext</a></code>
- <code title="put /api/users/context/{context_id}">client.users.context.<a href="./src/wayak_ai/resources/users/context.py">update</a>(context_id, \*\*<a href="src/wayak_ai/types/users/context_update_params.py">params</a>) -> <a href="./src/wayak_ai/types/users/persistent_user_context.py">PersistentUserContext</a></code>
- <code title="delete /api/users/context/{context_id}">client.users.context.<a href="./src/wayak_ai/resources/users/context.py">delete</a>(context_id) -> None</code>

## Profile

Types:

```python
from wayak_ai.types.users import PersistentUserProfile
```

Methods:

- <code title="get /api/users/profile/find">client.users.profile.<a href="./src/wayak_ai/resources/users/profile.py">find_by_email</a>(\*\*<a href="src/wayak_ai/types/users/profile_find_by_email_params.py">params</a>) -> <a href="./src/wayak_ai/types/users/persistent_user_profile.py">PersistentUserProfile</a></code>

# Files

Types:

```python
from wayak_ai.types import PersistentFile, FileListFileTypesResponse
```

Methods:

- <code title="get /api/files/{file_id}">client.files.<a href="./src/wayak_ai/resources/files.py">retrieve</a>(file_id) -> <a href="./src/wayak_ai/types/persistent_file.py">PersistentFile</a></code>
- <code title="delete /api/files/{file_id}">client.files.<a href="./src/wayak_ai/resources/files.py">delete</a>(file_id) -> None</code>
- <code title="put /api/files/{file_id}/index">client.files.<a href="./src/wayak_ai/resources/files.py">create_embeddings</a>(file_id) -> <a href="./src/wayak_ai/types/persistent_file.py">PersistentFile</a></code>
- <code title="get /api/files/file_types">client.files.<a href="./src/wayak_ai/resources/files.py">list_file_types</a>() -> <a href="./src/wayak_ai/types/file_list_file_types_response.py">FileListFileTypesResponse</a></code>
- <code title="post /api/files/{project_id}/web">client.files.<a href="./src/wayak_ai/resources/files.py">scrape_web</a>(project_id, \*\*<a href="src/wayak_ai/types/file_scrape_web_params.py">params</a>) -> object</code>
- <code title="post /api/files/{project_id}/upload">client.files.<a href="./src/wayak_ai/resources/files.py">upload</a>(project_id, \*\*<a href="src/wayak_ai/types/file_upload_params.py">params</a>) -> object</code>

# Projects

Types:

```python
from wayak_ai.types import PersistentProject, ProjectListThreadsResponse
```

Methods:

- <code title="post /api/projects">client.projects.<a href="./src/wayak_ai/resources/projects/projects.py">create</a>(\*\*<a href="src/wayak_ai/types/project_create_params.py">params</a>) -> <a href="./src/wayak_ai/types/persistent_project.py">PersistentProject</a></code>
- <code title="get /api/projects/{project_id}">client.projects.<a href="./src/wayak_ai/resources/projects/projects.py">retrieve</a>(project_id) -> <a href="./src/wayak_ai/types/persistent_project.py">PersistentProject</a></code>
- <code title="put /api/projects/{project_id}">client.projects.<a href="./src/wayak_ai/resources/projects/projects.py">update</a>(project_id, \*\*<a href="src/wayak_ai/types/project_update_params.py">params</a>) -> <a href="./src/wayak_ai/types/persistent_project.py">PersistentProject</a></code>
- <code title="delete /api/projects/{project_id}">client.projects.<a href="./src/wayak_ai/resources/projects/projects.py">delete</a>(project_id) -> None</code>
- <code title="get /api/projects/{project_id}/threads">client.projects.<a href="./src/wayak_ai/resources/projects/projects.py">list_threads</a>(project_id) -> <a href="./src/wayak_ai/types/project_list_threads_response.py">ProjectListThreadsResponse</a></code>

## Files

Types:

```python
from wayak_ai.types.projects import FileListResponse
```

Methods:

- <code title="get /api/projects/{project_id}/files">client.projects.files.<a href="./src/wayak_ai/resources/projects/files.py">list</a>(project_id) -> <a href="./src/wayak_ai/types/projects/file_list_response.py">FileListResponse</a></code>
- <code title="get /api/projects/{project_id}/files/index">client.projects.files.<a href="./src/wayak_ai/resources/projects/files.py">index</a>(project_id) -> object</code>

# Threads

Types:

```python
from wayak_ai.types import PersistentThread, ThreadListMessagesResponse
```

Methods:

- <code title="post /api/threads">client.threads.<a href="./src/wayak_ai/resources/threads.py">create</a>(\*\*<a href="src/wayak_ai/types/thread_create_params.py">params</a>) -> <a href="./src/wayak_ai/types/persistent_thread.py">PersistentThread</a></code>
- <code title="get /api/threads/{thread_id}">client.threads.<a href="./src/wayak_ai/resources/threads.py">retrieve</a>(thread_id) -> <a href="./src/wayak_ai/types/persistent_thread.py">PersistentThread</a></code>
- <code title="put /api/threads/{thread_id}">client.threads.<a href="./src/wayak_ai/resources/threads.py">update</a>(thread_id, \*\*<a href="src/wayak_ai/types/thread_update_params.py">params</a>) -> <a href="./src/wayak_ai/types/persistent_thread.py">PersistentThread</a></code>
- <code title="delete /api/threads/{thread_id}">client.threads.<a href="./src/wayak_ai/resources/threads.py">delete</a>(thread_id) -> None</code>
- <code title="get /api/threads/{thread_id}/messages">client.threads.<a href="./src/wayak_ai/resources/threads.py">list_messages</a>(thread_id) -> <a href="./src/wayak_ai/types/thread_list_messages_response.py">ThreadListMessagesResponse</a></code>

# Brains

Types:

```python
from wayak_ai.types import PersistentBrain, BrainListResponse
```

Methods:

- <code title="post /api/brains">client.brains.<a href="./src/wayak_ai/resources/brains.py">create</a>(\*\*<a href="src/wayak_ai/types/brain_create_params.py">params</a>) -> <a href="./src/wayak_ai/types/persistent_brain.py">PersistentBrain</a></code>
- <code title="put /api/brains/{brain_id}">client.brains.<a href="./src/wayak_ai/resources/brains.py">update</a>(brain_id, \*\*<a href="src/wayak_ai/types/brain_update_params.py">params</a>) -> <a href="./src/wayak_ai/types/persistent_brain.py">PersistentBrain</a></code>
- <code title="get /api/brains/{user_id}">client.brains.<a href="./src/wayak_ai/resources/brains.py">list</a>(user_id) -> <a href="./src/wayak_ai/types/brain_list_response.py">BrainListResponse</a></code>
- <code title="delete /api/brains/{brain_id}">client.brains.<a href="./src/wayak_ai/resources/brains.py">delete</a>(brain_id) -> None</code>

# Messages

Types:

```python
from wayak_ai.types import DocumentResult, PersistentMessage, TokenUsage
```

Methods:

- <code title="post /api/messages">client.messages.<a href="./src/wayak_ai/resources/messages.py">create</a>(\*\*<a href="src/wayak_ai/types/message_create_params.py">params</a>) -> <a href="./src/wayak_ai/types/persistent_message.py">PersistentMessage</a></code>
- <code title="get /api/messages/{message_id}">client.messages.<a href="./src/wayak_ai/resources/messages.py">retrieve</a>(message_id) -> <a href="./src/wayak_ai/types/persistent_message.py">PersistentMessage</a></code>
- <code title="put /api/messages/{message_id}">client.messages.<a href="./src/wayak_ai/resources/messages.py">update</a>(message_id, \*\*<a href="src/wayak_ai/types/message_update_params.py">params</a>) -> <a href="./src/wayak_ai/types/persistent_message.py">PersistentMessage</a></code>
- <code title="delete /api/messages/{message_id}">client.messages.<a href="./src/wayak_ai/resources/messages.py">delete</a>(message_id) -> None</code>

# Agents

Types:

```python
from wayak_ai.types import (
    Message,
    MessageRequest,
    AgentExtractContentResponse,
    AgentGetCompletionResponse,
    AgentListSupportedModelsResponse,
)
```

Methods:

- <code title="post /api/agents/extraction">client.agents.<a href="./src/wayak_ai/resources/agents.py">extract_content</a>(\*\*<a href="src/wayak_ai/types/agent_extract_content_params.py">params</a>) -> <a href="./src/wayak_ai/types/agent_extract_content_response.py">AgentExtractContentResponse</a></code>
- <code title="post /api/agents/completion">client.agents.<a href="./src/wayak_ai/resources/agents.py">get_completion</a>(\*\*<a href="src/wayak_ai/types/agent_get_completion_params.py">params</a>) -> <a href="./src/wayak_ai/types/agent_get_completion_response.py">AgentGetCompletionResponse</a></code>
- <code title="get /api/agents/models">client.agents.<a href="./src/wayak_ai/resources/agents.py">list_supported_models</a>() -> <a href="./src/wayak_ai/types/agent_list_supported_models_response.py">AgentListSupportedModelsResponse</a></code>
- <code title="post /api/agents/agent/{agentId}">client.agents.<a href="./src/wayak_ai/resources/agents.py">send_message_to_agent</a>(agent_id, \*\*<a href="src/wayak_ai/types/agent_send_message_to_agent_params.py">params</a>) -> <a href="./src/wayak_ai/types/persistent_message.py">PersistentMessage</a></code>
- <code title="post /api/agents/wayak">client.agents.<a href="./src/wayak_ai/resources/agents.py">send_message_to_wayak</a>(\*\*<a href="src/wayak_ai/types/agent_send_message_to_wayak_params.py">params</a>) -> <a href="./src/wayak_ai/types/persistent_message.py">PersistentMessage</a></code>

# Organizations

Types:

```python
from wayak_ai.types import (
    Organization,
    OrganizationListResponse,
    OrganizationGetBrainsResponse,
    OrganizationGetProjectsResponse,
    OrganizationGetThreadsResponse,
)
```

Methods:

- <code title="post /api/organizations">client.organizations.<a href="./src/wayak_ai/resources/organizations/organizations.py">create</a>(\*\*<a href="src/wayak_ai/types/organization_create_params.py">params</a>) -> <a href="./src/wayak_ai/types/organization.py">Organization</a></code>
- <code title="get /api/organizations/{org_id}">client.organizations.<a href="./src/wayak_ai/resources/organizations/organizations.py">retrieve</a>(org_id) -> <a href="./src/wayak_ai/types/organization.py">Organization</a></code>
- <code title="put /api/organizations/{org_id}">client.organizations.<a href="./src/wayak_ai/resources/organizations/organizations.py">update</a>(org_id, \*\*<a href="src/wayak_ai/types/organization_update_params.py">params</a>) -> <a href="./src/wayak_ai/types/organization.py">Organization</a></code>
- <code title="get /api/organizations">client.organizations.<a href="./src/wayak_ai/resources/organizations/organizations.py">list</a>(\*\*<a href="src/wayak_ai/types/organization_list_params.py">params</a>) -> <a href="./src/wayak_ai/types/organization_list_response.py">OrganizationListResponse</a></code>
- <code title="get /api/organizations/{org_id}/brains">client.organizations.<a href="./src/wayak_ai/resources/organizations/organizations.py">get_brains</a>(org_id) -> <a href="./src/wayak_ai/types/organization_get_brains_response.py">OrganizationGetBrainsResponse</a></code>
- <code title="get /api/organizations/{org_id}/projects">client.organizations.<a href="./src/wayak_ai/resources/organizations/organizations.py">get_projects</a>(org_id) -> <a href="./src/wayak_ai/types/organization_get_projects_response.py">OrganizationGetProjectsResponse</a></code>
- <code title="get /api/organizations/{org_id}/threads">client.organizations.<a href="./src/wayak_ai/resources/organizations/organizations.py">get_threads</a>(org_id) -> <a href="./src/wayak_ai/types/organization_get_threads_response.py">OrganizationGetThreadsResponse</a></code>

## Members

Types:

```python
from wayak_ai.types.organizations import Role, MemberListResponse, MemberAddResponse
```

Methods:

- <code title="get /api/organizations/{org_id}/members">client.organizations.members.<a href="./src/wayak_ai/resources/organizations/members.py">list</a>(org_id) -> <a href="./src/wayak_ai/types/organizations/member_list_response.py">MemberListResponse</a></code>
- <code title="post /api/organizations/{org_id}/members">client.organizations.members.<a href="./src/wayak_ai/resources/organizations/members.py">add</a>(org_id, \*\*<a href="src/wayak_ai/types/organizations/member_add_params.py">params</a>) -> <a href="./src/wayak_ai/types/organizations/member_add_response.py">MemberAddResponse</a></code>
- <code title="delete /api/organizations/{org_id}/members/{user_id}">client.organizations.members.<a href="./src/wayak_ai/resources/organizations/members.py">remove</a>(user_id, \*, org_id, \*\*<a href="src/wayak_ai/types/organizations/member_remove_params.py">params</a>) -> object</code>

# Ontology

Types:

```python
from wayak_ai.types import OntologyExecuteQueryResponse
```

Methods:

- <code title="put /api/ontology/execute-query">client.ontology.<a href="./src/wayak_ai/resources/ontology/ontology.py">execute_query</a>(\*\*<a href="src/wayak_ai/types/ontology_execute_query_params.py">params</a>) -> <a href="./src/wayak_ai/types/ontology_execute_query_response.py">OntologyExecuteQueryResponse</a></code>

## Dashboards

Types:

```python
from wayak_ai.types.ontology import DashboardModel, LayoutItem, DashboardListResponse
```

Methods:

- <code title="post /api/ontology/dashboards">client.ontology.dashboards.<a href="./src/wayak_ai/resources/ontology/dashboards.py">create</a>(\*\*<a href="src/wayak_ai/types/ontology/dashboard_create_params.py">params</a>) -> <a href="./src/wayak_ai/types/ontology/dashboard_model.py">DashboardModel</a></code>
- <code title="get /api/ontology/dashboards/{dashboard_id}">client.ontology.dashboards.<a href="./src/wayak_ai/resources/ontology/dashboards.py">retrieve</a>(dashboard_id) -> <a href="./src/wayak_ai/types/ontology/dashboard_model.py">DashboardModel</a></code>
- <code title="put /api/ontology/dashboards/{dashboard_id}">client.ontology.dashboards.<a href="./src/wayak_ai/resources/ontology/dashboards.py">update</a>(dashboard_id, \*\*<a href="src/wayak_ai/types/ontology/dashboard_update_params.py">params</a>) -> <a href="./src/wayak_ai/types/ontology/dashboard_model.py">DashboardModel</a></code>
- <code title="get /api/ontology/dashboards">client.ontology.dashboards.<a href="./src/wayak_ai/resources/ontology/dashboards.py">list</a>(\*\*<a href="src/wayak_ai/types/ontology/dashboard_list_params.py">params</a>) -> <a href="./src/wayak_ai/types/ontology/dashboard_list_response.py">DashboardListResponse</a></code>
- <code title="delete /api/ontology/dashboards/{dashboard_id}">client.ontology.dashboards.<a href="./src/wayak_ai/resources/ontology/dashboards.py">delete</a>(dashboard_id) -> <a href="./src/wayak_ai/types/ontology/dashboard_model.py">DashboardModel</a></code>

## Datasources

Types:

```python
from wayak_ai.types.ontology import DatasourceListResponse, DatasourceTestConnectionResponse
```

Methods:

- <code title="get /api/ontology/datasources/{datasource_id}">client.ontology.datasources.<a href="./src/wayak_ai/resources/ontology/datasources/datasources.py">retrieve</a>(datasource_id) -> <a href="./src/wayak_ai/types/ontology/datasources/data_source_model.py">DataSourceModel</a></code>
- <code title="get /api/ontology/datasources">client.ontology.datasources.<a href="./src/wayak_ai/resources/ontology/datasources/datasources.py">list</a>(\*\*<a href="src/wayak_ai/types/ontology/datasource_list_params.py">params</a>) -> <a href="./src/wayak_ai/types/ontology/datasource_list_response.py">DatasourceListResponse</a></code>
- <code title="post /api/ontology/datasources/{datasource_id}/test">client.ontology.datasources.<a href="./src/wayak_ai/resources/ontology/datasources/datasources.py">test_connection</a>(datasource_id) -> <a href="./src/wayak_ai/types/ontology/datasource_test_connection_response.py">DatasourceTestConnectionResponse</a></code>

### Clickhouse

Types:

```python
from wayak_ai.types.ontology.datasources import (
    ClickhouseConfig,
    DataSourceModel,
    SupportedDataSources,
)
```

Methods:

- <code title="post /api/ontology/datasources/clickhouse">client.ontology.datasources.clickhouse.<a href="./src/wayak_ai/resources/ontology/datasources/clickhouse.py">create</a>(\*\*<a href="src/wayak_ai/types/ontology/datasources/clickhouse_create_params.py">params</a>) -> <a href="./src/wayak_ai/types/ontology/datasources/data_source_model.py">DataSourceModel</a></code>
- <code title="put /api/ontology/datasources/clickhouse/{datasource_id}">client.ontology.datasources.clickhouse.<a href="./src/wayak_ai/resources/ontology/datasources/clickhouse.py">update</a>(datasource_id, \*\*<a href="src/wayak_ai/types/ontology/datasources/clickhouse_update_params.py">params</a>) -> <a href="./src/wayak_ai/types/ontology/datasources/data_source_model.py">DataSourceModel</a></code>
- <code title="delete /api/ontology/datasources/clickhouse/{datasource_id}">client.ontology.datasources.clickhouse.<a href="./src/wayak_ai/resources/ontology/datasources/clickhouse.py">delete</a>(datasource_id) -> <a href="./src/wayak_ai/types/ontology/datasources/data_source_model.py">DataSourceModel</a></code>

### Schema

Methods:

- <code title="put /api/ontology/datasources/{datasource_id}/schema/refresh">client.ontology.datasources.schema.<a href="./src/wayak_ai/resources/ontology/datasources/schema.py">refresh</a>(datasource_id) -> <a href="./src/wayak_ai/types/ontology/datasources/data_source_model.py">DataSourceModel</a></code>

## Agent

Methods:

- <code title="post /api/ontology/agent/chat">client.ontology.agent.<a href="./src/wayak_ai/resources/ontology/agent.py">chat</a>(\*\*<a href="src/wayak_ai/types/ontology/agent_chat_params.py">params</a>) -> <a href="./src/wayak_ai/types/persistent_message.py">PersistentMessage</a></code>

## Metrics

Types:

```python
from wayak_ai.types.ontology import (
    ChartVisualizationType,
    MetricModel,
    MetricStatusEnum,
    MetricListResponse,
)
```

Methods:

- <code title="post /api/ontology/metrics">client.ontology.metrics.<a href="./src/wayak_ai/resources/ontology/metrics.py">create</a>(\*\*<a href="src/wayak_ai/types/ontology/metric_create_params.py">params</a>) -> <a href="./src/wayak_ai/types/ontology/metric_model.py">MetricModel</a></code>
- <code title="get /api/ontology/metrics/{metric_id}">client.ontology.metrics.<a href="./src/wayak_ai/resources/ontology/metrics.py">retrieve</a>(metric_id) -> <a href="./src/wayak_ai/types/ontology/metric_model.py">MetricModel</a></code>
- <code title="put /api/ontology/metrics/{metric_id}">client.ontology.metrics.<a href="./src/wayak_ai/resources/ontology/metrics.py">update</a>(metric_id, \*\*<a href="src/wayak_ai/types/ontology/metric_update_params.py">params</a>) -> <a href="./src/wayak_ai/types/ontology/metric_model.py">MetricModel</a></code>
- <code title="get /api/ontology/metrics">client.ontology.metrics.<a href="./src/wayak_ai/resources/ontology/metrics.py">list</a>(\*\*<a href="src/wayak_ai/types/ontology/metric_list_params.py">params</a>) -> <a href="./src/wayak_ai/types/ontology/metric_list_response.py">MetricListResponse</a></code>
- <code title="delete /api/ontology/metrics/{metric_id}">client.ontology.metrics.<a href="./src/wayak_ai/resources/ontology/metrics.py">delete</a>(metric_id) -> <a href="./src/wayak_ai/types/ontology/metric_model.py">MetricModel</a></code>
