from constants import REPOSITORY_OWNER, PROJECT_ID
from request_generic_graphql import graphql_request


def get_project_node_id_graphql() -> str:
    query = f'query{{organization(login:"{REPOSITORY_OWNER}") {{projectV2(number: {PROJECT_ID}){{id}}}}}}'
    response = graphql_request('POST', query)

    if response.status_code == 200:
        response_data = response.json()
        try:
            project_data = response_data['data'].get('organization') or response_data['data'].get('user')
            if project_data is None:
                raise Exception('Project not found')
            node_id = project_data['id']
        except KeyError as exc:
            raise Exception(
                f'Could not obtain the project node id for project {PROJECT_ID}.\n'
                f'Exception: {exc}\n'
                f'Response: {response_data}'
            )
    else:
        raise Exception(f'Could not obtain the project node id. Status code: {response.status_code}')

    return node_id
