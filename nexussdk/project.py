import json
from . utils.http import http_get
from . utils.http import is_response_valid
from . utils.http import http_put
from . utils.http import http_delete
import urllib.parse


def fetch(org_label, project_label, rev=None):
    """
    Fetch a project and all its details.
    Note: This does not give the list of resources. To get that, use the `resource` package.

    :param org_label: The label of the organization that contains the project to be fetched
    :param project_label: label of a the project to fetch
    :param rev: OPTIONAL The specific revision of the wanted project. If not provided, will get the last.
    :return: All the details of this project, as a dictionary
    """

    org_label = urllib.parse.quote_plus(org_label)
    project_label = urllib.parse.quote_plus(project_label)
    url = "/projects/" + org_label + "/" + project_label

    if rev is not None:
        url = url + "?rev=" + str(rev)

    response_raw = http_get(url)

    if not is_response_valid(response_raw):
        raise Exception("Invalid http request for " + response_raw.url +
                        " (Status " + str(response_raw.status_code) + ")" + "\n" +
                        response_raw.text)

    response_obj = json.loads(response_raw.text)
    return response_obj


def create(org_label, project_label, config=None):
    """
    Create a new project under an organization.

    :param org_label: The label of the organization to create the project in
    :param project_label: The label of the project to add
    :param config: OPTIONAL if provided, must be a dictionary. Can include data such as `name`, `base` or `prefixMapping`
    see https://bluebrain.github.io/nexus/docs/api/admin/admin-projects-api.html#create-a-project for more info
    :return: The payload from the Nexus API as a dictionary. This contains the Nexus metadata of the project
    """
    org_label = urllib.parse.quote_plus(org_label)
    project_label = urllib.parse.quote_plus(project_label)
    url = "/projects/" + org_label + "/" + project_label

    if config is None:
        config = {}

    response_raw = http_put(url, body=config)

    if not is_response_valid(response_raw):
        raise Exception("Invalid http request for " + response_raw.url +
                        " (Status " + str(response_raw.status_code) + ")" + "\n" +
                        response_raw.text)

    response_obj = json.loads(response_raw.text)
    return response_obj


def update(project, previous_rev=None):
    """
    Update a project. The data to update on a project are mostly related to the prefix mapping. To do so, you must
    get the project information as a payload, most likely using `project.fetch(...)`, then, modify this payload
    according to the update to perform, and finally, use this modified payload as the `project` argument of this method.

    :param project: Project payload as a dictionary. This is most likely the returned value of `project.fetch(...)`
    :param previous_rev: OPTIONAL The last revision number, to make sure the developer is aware of the latest status of
    this project. If not provided, the `_rev` number from the `project` argument will be used.
    :return: The payload from the Nexus API as a dictionary. This contains the Nexus metadata of the project
    """

    if previous_rev is None:
        previous_rev = project["_rev"]

    org_label = urllib.parse.quote_plus(project["_organizationLabel"])
    project_label = urllib.parse.quote_plus(project["_label"])

    url = "/projects/" + org_label + "/" + project_label + "?rev=" + str(previous_rev)

    response_raw = http_put(url, project)

    if not is_response_valid(response_raw):
        raise Exception("Invalid http request for " + response_raw.url +
                        " (Status " + str(response_raw.status_code) + ")" + "\n" +
                        response_raw.text)

    response_obj = json.loads(response_raw.text)
    return response_obj


def list(org_label=None, pagination_from=0, pagination_size=20, deprecated=None, full_text_search_query=None):
    """
    List all the projects. If the arguments org_label is provided, this will list only the projects of this given
    organization. If not provided, all the projects from all organizations will be listed.

    :param org_label: OPTIONAL get only the list of project for this given organization
    :param pagination_from: OPTIONAL Index of the list to start from (default: 0)
    :param pagination_size: OPTIONAL Size of the list (default: 20)
    :param deprecated: OPTIONAL Lists only the deprecated if True,
    lists only the non-deprecated if False,
    lists everything if not provided or None (default: None)
    :param full_text_search_query: OPTIONAL List only the projects that match this query
    :return: The payload from the Nexus API as a dictionary. This contains the Nexus metadata and the list of projects
    """

    url = "/projects"

    if org_label is not None:
        org_label = urllib.parse.quote_plus(org_label)
        url = url + "/" + org_label

    url = url + "?from=" + str(pagination_from) + "&size=" + str(pagination_size)

    if deprecated is not None:
        deprecated = "true" if deprecated else "false"
        url = url + "&deprecated=" + deprecated

    if full_text_search_query is not None:
        full_text_search_query = urllib.parse.quote_plus(full_text_search_query)
        url = url + "&q=" + full_text_search_query

    response_raw = http_get(url)

    if not is_response_valid(response_raw):
        raise Exception("Invalid http request for " + response_raw.url +
                        " (Status " + str(response_raw.status_code) + ")" + "\n" +
                        response_raw.text)

    response_obj = json.loads(response_raw.text)
    return response_obj


def deprecate(org_label, project_label, previous_rev):
    """
    Deprecate a project. Nexus does not allow deleting projects so deprecating is the way to flag them as
    not usable anymore.
    A deprecated project cannot be modified/updated.

    :param org_label: The label of the organization the project to deprecate belongs to
    :param project_label: The label of the project to deprecate
    :param previous_rev: The previous revision number. Provided to make sure the user is well aware of the details
    of the last revision of this project.
    :return: The payload from the Nexus API as a dictionary. This contains the Nexus metadata of the project
    """

    org_label = urllib.parse.quote_plus(org_label)
    project_label = urllib.parse.quote_plus(project_label)

    url = "/projects/" + org_label + "/" + project_label + "?rev=" + str(previous_rev)

    response_raw = http_delete(url)

    if not is_response_valid(response_raw):
        raise Exception("Invalid http request for " + response_raw.url +
                        " (Status " + str(response_raw.status_code) + ")" + "\n" +
                        response_raw.text)

    response_obj = json.loads(response_raw.text)
    return response_obj