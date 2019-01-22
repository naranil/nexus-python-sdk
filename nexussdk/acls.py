from typing import Dict, List

from nexussdk.utils.http import http_delete, http_get, http_patch, http_put

SEGMENT = "acls"


# Read functions.

def fetch(subpath: str, rev: int = None, self: bool = True) -> Dict:
    """Fetch the ACLs on a subpath.

    :param subpath: Subpath on which fetching the ACLs.
    :param rev: (optional) Revision number of the ACLs.
    :param self: (optional) If 'True', only the ACLs containing the identities
    found in the authentication token are returned. If 'False', all the ACLs
    on the current subpath are returned.
    :return: A Nexus results list with the Nexus payloads of the ACLs.
    """
    return http_get([SEGMENT, subpath], rev=rev, self=self)


def fetch_(path: str, rev: int = None, self: bool = True) -> Dict:
    """Fetch the ACLs on a full path.

    :param path: Full path on which fetching the ACLs.
    :param rev: (optional) Revision number of the ACLs.
    :param self: (optional) If 'True', only the ACLs containing the identities
    found in the authentication token are returned. If 'False', all the ACLs
    on the current subpath are returned.
    :return: A Nexus results list with the Nexus payloads of the ACLs.
    """
    return http_get(path, rev=rev, self=self)


def list(subpath: str, ancestors: bool = False, self: bool = True) -> Dict:
    """List ACLs on a subpath.

    :param subpath: Subpath on which listing the ACLs.
    :param ancestors: (optional) If 'True', the ACLs on the parent path of the
    subpath are returned. If 'False', only the ACLs on the current subpath are
    returned.
    :param self: (optional) If 'True', only the ACLs containing the identities
    found in the authentication token are returned. If 'False', all the ACLs
    on the current subpath are returned.
    :return: A Nexus results list with the Nexus payloads of the ACLs.
    """
    return http_get([SEGMENT, subpath], ancestors=ancestors, self=self)


def list_(path: str, ancestors: bool = False, self: bool = True) -> Dict:
    """List ACLs on a full path.

    :param path: Full path on which listing the ACLs.
    :param ancestors: (optional) If 'True', the ACLs on the parent path of the
    subpath are returned. If 'False', only the ACLs on the current subpath are
    returned.
    :param self: (optional) If 'True', only the ACLs containing the identities
    found in the authentication token are returned. If 'False', all the ACLs
    on the current subpath are returned.
    :return: A Nexus results list with the Nexus payloads of the ACLs.
    """
    return http_get(path, ancestors=ancestors, self=self)


# Update functions.

def replace(subpath: str, permissions: List[str], identity: Dict, rev: int) -> Dict:
    """Replace ACLs on a subpath.

    :param subpath: Subpath on which replacing the ACLs.
    :param permissions: List of permissions.
    :param identity: Payload of the identity to which grant the permissions.
    :param rev: Last revision of the ACLs.
    :return: The Nexus metadata of the ACLs.
    """
    payload = _payload(permissions, identity)
    return http_put([SEGMENT, subpath], payload, rev=rev)


def replace_(path: str, payload: Dict, rev: int) -> Dict:
    """Replace ACLs on a full path.

    :param path: Full path on which replacing the ACLs.
    :param payload: Payload of the ACLs.
    :param rev: Last revision of the ACLs.
    :return: The Nexus metadata of the ACLs.
    """
    return http_put(path, payload, rev=rev)


def append(subpath: str, permissions: List[str], identity: Dict, rev: int) -> Dict:
    """Append ACLs on a subpath.

    :param subpath: Subpath on which appending ACLs.
    :param permissions: List of permissions.
    :param identity: Payload of the identity to which grant the permissions.
    :param rev: Last revision of the ACLs.
    :return: The Nexus metadata of the ACLs.
    """
    payload = _payload(permissions, identity, "Append")
    return http_patch([SEGMENT, subpath], payload, rev=rev)


def append_(path: str, payload: Dict, rev: int) -> Dict:
    """Append ACLs on a full path.

    :param path: Full path on which appending ACLs.
    :param payload: Payload of the ACLs to append.
    :param rev: Last revision of the ACLs.
    :return: The Nexus metadata of the ACLs.
    """
    return http_patch(path, payload, rev=rev)


def subtract(subpath: str, permissions: List[str], identity: Dict, rev: int) -> Dict:
    """Subtract ACLs on a subpath.

    :param subpath: Subpath on which subtracting ACLs.
    :param permissions: List of permissions.
    :param identity: Payload of the identity to which remove the permissions.
    :param rev: Last revision of the ACLs.
    :return: The Nexus metadata of the ACLs.
    """
    payload = _payload(permissions, identity, "Subtract")
    return http_patch([SEGMENT, subpath], payload, rev=rev)


def subtract_(path: str, payload: Dict, rev: int) -> Dict:
    """Subtract ACLs on a full path.

    :param path: Full path on which subtracting ACLs.
    :param payload: Payload of the ACLs to subtract.
    :param rev: Last revision of the ACLs.
    :return: The Nexus metadata of the ACLs.
    """
    return http_patch(path, payload, rev=rev)


# Delete functions.

def delete(subpath: str, rev: int) -> Dict:
    """Delete ACLs on a subpath.

    :param subpath: Subpath on which deleting ACLs.
    :param rev: Last revision of the ACLs.
    :return: The Nexus metadata of the ACLs.
    """
    return http_delete([SEGMENT, subpath], rev=rev)


def delete_(path: str, rev: int) -> Dict:
    """Delete ACLs on a full path.

    :param path: Full path on which deleting ACLs.
    :param rev: Last revision of the ACLs.
    :return: The Nexus metadata of the ACLs.
    """
    return http_delete(path, rev=rev)


# Internal helpers

def _payload(permissions: List[str], identity: Dict, operation: str = None) -> Dict:
    """Create an ACLs payload.

    :param permissions: List of permissions.
    :param identity: Payload of the identity on which the permissions apply.
    :param operation: (optional) Corresponding operation: 'Append' or 'Subtract'.
    :return: Payload of the ACLs.
    """
    payload = {
        "acl": [
            {
                "permissions": permissions,
                "identity": identity,
            },
        ]
    }
    if operation is not None:
        payload["@type"] = operation
    return payload
