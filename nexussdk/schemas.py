import json
from nexussdk.utils.http import http_get
from nexussdk.utils.http import http_put
from nexussdk.utils.http import http_post
from nexussdk.utils.http import http_delete
from urllib.parse import quote_plus as url_encode


def list(org_label, project_label, pagination_from=0, pagination_size=20,
         deprecated=None, full_text_search_query=None):
    """
        List all the schemas available

        :param org_label: Label of the organization to which listing the schema
        :param project_label: Label of the project to which listing the schema
        :param pagination_from: OPTIONAL The pagination index to start from (default: 0)
        :param pagination_size: OPTIONAL The maximum number of elements to returns at once (default: 20)
        :param deprecated:  OPTIONAL Get only deprecated resource if True and get only non-deprecated results if False.
        If not specified (default), return both deprecated and not deprecated resource.
        :param full_text_search_query: A string to look for as a full text query
        :return: The raw payload as a dictionary
        :return: List of schema and some Nexus metadata
    """

    org_label = url_encode(org_label)
    project_label = url_encode(project_label)

    path = "/schemas/" + org_label + "/" + project_label

    path = path + "?from=" + str(pagination_from) + "&size=" + str(pagination_size)

    if deprecated is not None:
        deprecated = "true" if deprecated else "false"
        path = path + "&deprecated=" + deprecated

    if full_text_search_query:
        full_text_search_query = url_encode(full_text_search_query)
        path = path + "&q=" + full_text_search_query

    return http_get(path, use_base=True)


def fetch(org_label, project_label, schema_id, rev=None, tag=None):
    """
        Fetches a distant schema and returns the payload as a dictionary.
        In case of error, an exception is thrown.

        :param org_label: The label of the organization that the resource belongs to
        :param project_label: The label of the project that the resource belongs to
        :param schema_id: id of the schema
        :return: Payload of the whole schema as a dictionary
    """

    if rev is not None and tag is not None:
        raise Exception("The arguments rev and tag are mutually exclusive. One or the other must be chosen.")

    org_label = url_encode(org_label)
    project_label = url_encode(project_label)
    schema_id = url_encode(schema_id)
    path = "/schemas/" + org_label + "/" + project_label + "/" + schema_id

    if rev is not None:
        path = path + "?rev=" + str(rev)

    if tag is not None:
        path = path + "?tag=" + str(tag)

    return http_get(path, use_base=True)


def create(org_label, project_label, schema_obj, id=None):
    """
        Create a new schema

        :param org_label: Label of the organization in which to create the schema
        :param project_label: label of the project in which to create a schema
        :param schema_obj: Schema, can be a dictionary or a JSON string
        :return: payload of the schema as a Python dictionary. This payload is partial and contains only Nexus metadata.
        To get the full schema payload, use the fetch() method.
    """

    # we give the possibility to use a JSON string instead of a dict
    if (not isinstance(schema_obj, dict)) and isinstance(schema_obj, str):
        schema_obj = json.loads(schema_obj)

    org_label = url_encode(org_label)
    project_label = url_encode(project_label)
    path = "/schemas/" + org_label + "/" + project_label

    if id is None:
        return http_post(path, schema_obj, use_base=True)
    else:
        schema_id = url_encode(id)
        path = path + "/" + schema_id
        return http_put(path, schema_obj, use_base=True)



def update(schema, previous_rev=None):
    """
        Update a schema. The schema object is most likely the returned value of a
        nexus.schema.fetch(), where some fields where modified, added or removed.
        Note that the returned payload only contains the Nexus metadata and not the
        complete resource.

        :param schema: payload of a previously fetched resource, with the modification to be updated
        :param previous_rev: OPTIONAL The previous revision you want to update from.
        If not provided, the rev from the schema argument will be used.
        :return: A payload containing only the Nexus metadata for this updated schema.
    """

    if previous_rev is None:
        previous_rev = schema["_rev"]

    path = schema["_self"] + "?rev=" + str(previous_rev)

    return http_put(path, schema, use_base=False)


def deprecate(schema, previous_rev=None):
    """
       Flag a schema as deprecated. Schema cannot be deleted in Nexus, once one is deprecated, it is no longer
       possible to update it.

       :param schema: payload of a previously fetched resource
       :param previous_rev: OPTIONAL The previous revision you want to update from.
       If not provided, the rev from the schema argument will be used.
       :return: A payload containing only the Nexus metadata for this deprecated schema.
    """

    if previous_rev is None:
        previous_rev = schema["_rev"]

    path = schema["_self"] + "?rev=" + str(previous_rev)

    return http_delete(path, use_base=False)


def tag(schema, tag_value, rev_to_tag=None, previous_rev=None):
    """
        Add a tag to a a specific revision of the schema. Note that a new revision (untagged) will be created

        :param schema: payload of a previously fetched schema
        :param tag_value: The value (or name) of a tag
        :param rev_to_tag: OPTIONAL Number of the revision to tag. If not provided, this will take the revision number
        from the provided schema payload.
        :param previous_rev: OPTIONAL The previous revision you want to update from.
        If not provided, the rev from the schema argument will be used.
        :return: A payload containing only the Nexus metadata for this schema.
    """

    if previous_rev is None:
        previous_rev = schema["_rev"]

    if rev_to_tag is None:
        rev_to_tag = schema["_rev"]

    path = schema["_self"] + "/tags?rev=" + str(previous_rev)

    data = {
        "tag": tag_value,
        "rev": rev_to_tag
    }

    return http_put(path, body=data, use_base=False)