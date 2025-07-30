# Core
from copy import deepcopy
from datetime import (
    datetime,
    timezone
)
from sys import getrecursionlimit
from typing import Iterator, Optional, Union
from warnings import warn

# PyPI
from requests import Response

# Local
from . api_client import ApiClient, normalize_url
from . common import (
    datetime_intervals,
    requires_success,
    singular_name,
    strftime,
    strptime,
    successful_response,
    truncate_text,
    try_decoding,
)
from . errors import (
    ServerHttpError,
    UrlError
)

#######################
### CLIENT DEFAULTS ###
#######################

ITERATION_LIMIT = 10000
"""
The maximum position of a result in classic pagination.

The offset plus limit parameter may not exceed this number. This is enforced server-side
and is not something the client may override. Rather, this value is reproduced in the
client to enable short-circuiting pagination, so that the client can avoid the HTTP 400
error that will result if the sum of the limit and offset parameters exceeds it.

See: `Pagination
<https://developer.pagerduty.com/docs/ZG9jOjExMDI5NTU4-pagination>`_.
"""

RECURSION_LIMIT = getrecursionlimit() // 2
"""
Maximum depth of recursion when using functions that use recursion.

For example, :attr:`pagerduty.RestApiV2Client.iter_history` will call itself recursively
if the number of results in the data set to be queried exceeds :attr:`ITERATION_LIMIT`.

Its value is arbitrary and meant to guard against excessive depth. For safety, it is set
to half the hard recursion limit in Python.
"""

ITER_HIST_RECURSION_WARNING_TEMPLATE = """RestApiV2Client.iter_history cannot continue
bisecting historical time intervals because {reason}, but the total number of results in
the current requested time sub-interval ({since_until}) still exceeds the hard limit for
classic pagination, {iteration_limit}. Results will be incomplete.{suggestion}
""".replace("\n", " ")

# List of canonical REST API paths
#
# Supporting a new API for entity wrapping will require adding its patterns to
# this list. If it doesn't follow standard naming conventions, it will also
# require one or more new entries in ENTITY_WRAPPER_CONFIG.
#
# To generate new definitions for CANONICAL_PATHS and
# CURSOR_BASED_PAGINATION_PATHS based on the API documentation's source code,
# use scripts/get_path_list/get_path_list.py

CANONICAL_PATHS = [
    '/{entity_type}/{id}/change_tags',
    '/{entity_type}/{id}/tags',
    '/abilities',
    '/abilities/{id}',
    '/addons',
    '/addons/{id}',
    '/alert_grouping_settings',
    '/alert_grouping_settings/{id}',
    '/analytics/metrics/incidents/all',
    '/analytics/metrics/incidents/escalation_policies',
    '/analytics/metrics/incidents/escalation_policies/all',
    '/analytics/metrics/incidents/services',
    '/analytics/metrics/incidents/services/all',
    '/analytics/metrics/incidents/teams',
    '/analytics/metrics/incidents/teams/all',
    '/analytics/metrics/pd_advance_usage/features',
    '/analytics/metrics/responders/all',
    '/analytics/metrics/responders/teams',
    '/analytics/raw/incidents',
    '/analytics/raw/incidents/{id}',
    '/analytics/raw/incidents/{id}/responses',
    '/analytics/raw/responders/{responder_id}/incidents',
    '/audit/records',
    '/automation_actions/actions',
    '/automation_actions/actions/{id}',
    '/automation_actions/actions/{id}/invocations',
    '/automation_actions/actions/{id}/services',
    '/automation_actions/actions/{id}/services/{service_id}',
    '/automation_actions/actions/{id}/teams',
    '/automation_actions/actions/{id}/teams/{team_id}',
    '/automation_actions/invocations',
    '/automation_actions/invocations/{id}',
    '/automation_actions/runners',
    '/automation_actions/runners/{id}',
    '/automation_actions/runners/{id}/teams',
    '/automation_actions/runners/{id}/teams/{team_id}',
    '/business_services',
    '/business_services/{id}',
    '/business_services/{id}/account_subscription',
    '/business_services/{id}/subscribers',
    '/business_services/{id}/supporting_services/impacts',
    '/business_services/{id}/unsubscribe',
    '/business_services/impactors',
    '/business_services/impacts',
    '/business_services/priority_thresholds',
    '/change_events',
    '/change_events/{id}',
    '/escalation_policies',
    '/escalation_policies/{id}',
    '/escalation_policies/{id}/audit/records',
    '/event_orchestrations',
    '/event_orchestrations/{id}',
    '/event_orchestrations/{id}/integrations',
    '/event_orchestrations/{id}/integrations/{integration_id}',
    '/event_orchestrations/{id}/integrations/migration',
    '/event_orchestrations/{id}/global',
    '/event_orchestrations/{id}/router',
    '/event_orchestrations/{id}/unrouted',
    '/event_orchestrations/services/{service_id}',
    '/event_orchestrations/services/{service_id}/active',
    '/event_orchestrations/{id}/cache_variables',
    '/event_orchestrations/{id}/cache_variables/{cache_variable_id}',
    '/event_orchestrations/services/{service_id}/cache_variables',
    '/event_orchestrations/services/{service_id}/cache_variables/{cache_variable_id}',
    '/extension_schemas',
    '/extension_schemas/{id}',
    '/extensions',
    '/extensions/{id}',
    '/extensions/{id}/enable',
    '/incident_workflows',
    '/incident_workflows/{id}',
    '/incident_workflows/{id}/instances',
    '/incident_workflows/actions',
    '/incident_workflows/actions/{id}',
    '/incident_workflows/triggers',
    '/incident_workflows/triggers/{id}',
    '/incident_workflows/triggers/{id}/services',
    '/incident_workflows/triggers/{trigger_id}/services/{service_id}',
    '/incidents',
    '/incidents/{id}',
    '/incidents/{id}/alerts',
    '/incidents/{id}/alerts/{alert_id}',
    '/incidents/{id}/business_services/{business_service_id}/impacts',
    '/incidents/{id}/business_services/impacts',
    '/incidents/{id}/custom_fields/values',
    '/incidents/{id}/log_entries',
    '/incidents/{id}/merge',
    '/incidents/{id}/notes',
    '/incidents/{id}/outlier_incident',
    '/incidents/{id}/past_incidents',
    '/incidents/{id}/related_change_events',
    '/incidents/{id}/related_incidents',
    '/incidents/{id}/responder_requests',
    '/incidents/{id}/snooze',
    '/incidents/{id}/status_updates',
    '/incidents/{id}/status_updates/subscribers',
    '/incidents/{id}/status_updates/unsubscribe',
    '/incidents/count',
    '/incidents/custom_fields',
    '/incidents/custom_fields/{field_id}',
    '/incidents/custom_fields/{field_id}/field_options',
    '/incidents/custom_fields/{field_id}/field_options/{field_option_id}',
    '/license_allocations',
    '/licenses',
    '/log_entries',
    '/log_entries/{id}',
    '/log_entries/{id}/channel',
    '/maintenance_windows',
    '/maintenance_windows/{id}',
    '/notifications',
    '/oauth_delegations',
    '/oauth_delegations/revocation_requests/status',
    '/oncalls',
    '/paused_incident_reports/alerts',
    '/paused_incident_reports/counts',
    '/priorities',
    '/response_plays',
    '/response_plays/{id}',
    '/response_plays/{response_play_id}/run',
    '/rulesets',
    '/rulesets/{id}',
    '/rulesets/{id}/rules',
    '/rulesets/{id}/rules/{rule_id}',
    '/schedules',
    '/schedules/{id}',
    '/schedules/{id}/audit/records',
    '/schedules/{id}/overrides',
    '/schedules/{id}/overrides/{override_id}',
    '/schedules/{id}/users',
    '/schedules/preview',
    '/service_dependencies/associate',
    '/service_dependencies/business_services/{id}',
    '/service_dependencies/disassociate',
    '/service_dependencies/technical_services/{id}',
    '/services',
    '/services/{id}',
    '/services/{id}/audit/records',
    '/services/{id}/change_events',
    '/services/{id}/integrations',
    '/services/{id}/integrations/{integration_id}',
    '/services/{id}/rules',
    '/services/{id}/rules/convert',
    '/services/{id}/rules/{rule_id}',
    '/standards',
    '/standards/{id}',
    '/standards/scores/{resource_type}',
    '/standards/scores/{resource_type}/{id}',
    '/status_dashboards',
    '/status_dashboards/{id}',
    '/status_dashboards/{id}/service_impacts',
    '/status_dashboards/url_slugs/{url_slug}',
    '/status_dashboards/url_slugs/{url_slug}/service_impacts',
    '/status_pages',
    '/status_pages/{id}/impacts',
    '/status_pages/{id}/impacts/{impact_id}',
    '/status_pages/{id}/services',
    '/status_pages/{id}/services/{service_id}',
    '/status_pages/{id}/severities',
    '/status_pages/{id}/severities/{severity_id}',
    '/status_pages/{id}/statuses',
    '/status_pages/{id}/statuses/{status_id}',
    '/status_pages/{id}/posts',
    '/status_pages/{id}/posts/{post_id}',
    '/status_pages/{id}/posts/{post_id}/post_updates',
    '/status_pages/{id}/posts/{post_id}/post_updates/{post_update_id}',
    '/status_pages/{id}/posts/{post_id}/postmortem',
    '/status_pages/{id}/subscriptions',
    '/status_pages/{id}/subscriptions/{subscription_id}',
    '/tags',
    '/tags/{id}',
    '/tags/{id}/users',
    '/tags/{id}/teams',
    '/tags/{id}/escalation_policies',
    '/teams',
    '/teams/{id}',
    '/teams/{id}/audit/records',
    '/teams/{id}/escalation_policies/{escalation_policy_id}',
    '/teams/{id}/members',
    '/teams/{id}/notification_subscriptions',
    '/teams/{id}/notification_subscriptions/unsubscribe',
    '/teams/{id}/users/{user_id}',
    '/templates',
    '/templates/{id}',
    '/templates/{id}/render',
    '/templates/fields',
    '/users',
    '/users/{id}',
    '/users/{id}/audit/records',
    '/users/{id}/contact_methods',
    '/users/{id}/contact_methods/{contact_method_id}',
    '/users/{id}/license',
    '/users/{id}/notification_rules',
    '/users/{id}/notification_rules/{notification_rule_id}',
    '/users/{id}/notification_subscriptions',
    '/users/{id}/notification_subscriptions/unsubscribe',
    '/users/{id}/oncall_handoff_notification_rules',
    '/users/{id}/oncall_handoff_notification_rules/{oncall_handoff_notification_rule_id}',
    '/users/{id}/sessions',
    '/users/{id}/sessions/{type}/{session_id}',
    '/users/{id}/status_update_notification_rules',
    '/users/{id}/status_update_notification_rules/{status_update_notification_rule_id}',
    '/users/me',
    '/vendors',
    '/vendors/{id}',
    '/webhook_subscriptions',
    '/webhook_subscriptions/{id}',
    '/webhook_subscriptions/{id}/enable',
    '/webhook_subscriptions/{id}/ping',
    '/workflows/integrations',
    '/workflows/integrations/{id}',
    '/workflows/integrations/connections',
    '/workflows/integrations/{integration_id}/connections',
    '/workflows/integrations/{integration_id}/connections/{id}',
]
"""
Explicit list of supported canonical REST API v2 paths

:meta hide-value:
"""

CURSOR_BASED_PAGINATION_PATHS = [
    '/audit/records',
    '/automation_actions/actions',
    '/automation_actions/runners',
    '/escalation_policies/{id}/audit/records',
    '/incident_workflows/actions',
    '/incident_workflows/triggers',
    '/schedules/{id}/audit/records',
    '/services/{id}/audit/records',
    '/teams/{id}/audit/records',
    '/users/{id}/audit/records',
    '/workflows/integrations',
    '/workflows/integrations/connections',
    '/workflows/integrations/{integration_id}/connections',
]
"""
Explicit list of paths that support cursor-based pagination

:meta hide-value:
"""

HISTORICAL_RECORD_PATHS = [
    '/audit/records',
    '/change_events',
    '/escalation_policies/{id}/audit/records',
    '/incidents',
    '/log_entries',
    '/oncalls',
    '/schedules/{id}/audit/records',
    '/services/{id}/audit/records',
    '/teams/{id}/audit/records',
    '/users/{id}/audit/records'
]
"""
Explicit list of paths that represent date-specific resources.

These index endpoints support the "since" and "until" parameters and represent events.

:meta hide-value:
"""

ENTITY_WRAPPER_CONFIG = {
    # Abilities
    'GET /abilities/{id}': None,
    # Add-ons follows orthodox schema patterns
    # Alert grouping settings follows orthodox schema patterns
    # Analytics
    '* /analytics/metrics/incidents/all': None,
    '* /analytics/metrics/incidents/escalation_policies': None,
    '* /analytics/metrics/incidents/escalation_policies/all': None,
    '* /analytics/metrics/incidents/services': None,
    '* /analytics/metrics/incidents/services/all': None,
    '* /analytics/metrics/incidents/teams': None,
    '* /analytics/metrics/incidents/teams/all': None,
    '* /analytics/metrics/pd_advance_usage/features': None,
    '* /analytics/metrics/responders/all': None,
    '* /analytics/metrics/responders/teams': None,
    '* /analytics/raw/incidents': None,
    '* /analytics/raw/incidents/{id}': None,
    '* /analytics/raw/incidents/{id}/responses': None,

    # Automation Actions
    'POST /automation_actions/actions/{id}/invocations': (None,'invocation'),

    # Paused Incident Reports
    'GET /paused_incident_reports/alerts': 'paused_incident_reporting_counts',
    'GET /paused_incident_reports/counts': 'paused_incident_reporting_counts',

    # Business Services
    '* /business_services/{id}/account_subscription': None,
    'POST /business_services/{id}/subscribers': ('subscribers', 'subscriptions'),
    'POST /business_services/{id}/unsubscribe': ('subscribers', None),
    '* /business_services/priority_thresholds': None,
    'GET /business_services/impacts': 'services',
    'GET /business_services/{id}/supporting_services/impacts': 'services',

    # Change Events
    'POST /change_events': None, # why not just use EventsApiV2Client?
    'GET /incidents/{id}/related_change_events': 'change_events',

    # Event Orchestrations
    '* /event_orchestrations': 'orchestrations',
    '* /event_orchestrations/services/{id}': 'orchestration_path',
    '* /event_orchestrations/services/{id}/active': None,
    '* /event_orchestrations/{id}': 'orchestration',
    '* /event_orchestrations/{id}/global': 'orchestration_path',
    '* /event_orchestrations/{id}/integrations/migration': None,
    '* /event_orchestrations/{id}/router': 'orchestration_path',
    '* /event_orchestrations/{id}/unrouted': 'orchestration_path',

    # Extensions
    'POST /extensions/{id}/enable': (None, 'extension'),

    # Incidents
    'PUT /incidents/{id}/merge': ('source_incidents', 'incident'),
    'POST /incidents/{id}/responder_requests': (None, 'responder_request'),
    'POST /incidents/{id}/snooze': (None, 'incident'),
    'POST /incidents/{id}/status_updates': (None, 'status_update'),
    'POST /incidents/{id}/status_updates/subscribers': ('subscribers', 'subscriptions'),
    'POST /incidents/{id}/status_updates/unsubscribe': ('subscribers', None),
    'GET /incidents/{id}/business_services/impacts': 'services',
    'PUT /incidents/{id}/business_services/{business_service_id}/impacts': None,
    '* /incidents/{id}/custom_fields/values': 'custom_fields',
    'POST /incidents/{id}/responder_requests': None,

    # Incident Custom Fields
    '* /incidents/custom_fields': ('field', 'fields'),
    '* /incidents/custom_fields/{field_id}': 'field',

    # Incident Types
    # TODO: Update after this is GA and no longer early-access (for now we are manually
    # excluding the canonical paths in the update)

    # Incident Workflows
    'POST /incident_workflows/{id}/instances': 'incident_workflow_instance',
    'POST /incident_workflows/triggers/{id}/services': ('service', 'trigger'),

    # Response Plays
    'POST /response_plays/{response_play_id}/run': None, # (deprecated)

    # Schedules
    'POST /schedules/{id}/overrides': ('overrides', None),

    # Service Dependencies
    'POST /service_dependencies/associate': 'relationships',

    # Webhooks
    'POST /webhook_subscriptions/{id}/enable': (None, 'webhook_subscription'),
    'POST /webhook_subscriptions/{id}/ping': None,

    # Status Dashboards
    'GET /status_dashboards/{id}/service_impacts': 'services',
    'GET /status_dashboards/url_slugs/{url_slug}': 'status_dashboard',
    'GET /status_dashboards/url_slugs/{url_slug}/service_impacts': 'services',

    # Status Pages
    # Adheres to orthodox API conventions / fully supported via inference from path

    # Tags
    'POST /{entity_type}/{id}/change_tags': None,

    # Teams
    'PUT /teams/{id}/escalation_policies/{escalation_policy_id}': None,
    'POST /teams/{id}/notification_subscriptions': ('subscribables', 'subscriptions'),
    'POST /teams/{id}/notification_subscriptions/unsubscribe': ('subscribables', None),
    'PUT /teams/{id}/users/{user_id}': None,
    'GET /teams/{id}/notification_subscriptions': 'subscriptions',

    # Templates
    'POST /templates/{id}/render': None,

    # Users
    '* /users/{id}/notification_subscriptions': ('subscribables', 'subscriptions'),
    'POST /users/{id}/notification_subscriptions/unsubscribe': ('subscribables', None),
    'GET /users/{id}/sessions': 'user_sessions',
    'GET /users/{id}/sessions/{type}/{session_id}': 'user_session',
    'GET /users/me': 'user',

    # Workflow Integrations
    # Adheres to orthodox API conventions / fully supported via inference from path

    # OAuth Delegations
    'GET /oauth_delegations/revocation_requests/status': None
} #: :meta hide-value:
"""
Wrapped entities antipattern handling configuration.

When trying to determine the entity wrapper name, this dictionary is first
checked for keys that apply to a given request method and canonical API path
based on a matching logic. If no keys are found that match, it is assumed that
the API endpoint follows classic entity wrapping conventions, and the wrapper
name can be inferred based on those conventions (see
:attr:`pagerduty.infer_entity_wrapper`). Any new API that does not follow these
conventions should therefore be given an entry in this dictionary in order to
properly support it for entity wrapping.

Each of the keys should be a capitalized HTTP method (or ``*`` to match any method),
followed by a space, followed by a canonical path i.e. as returned by
:attr:`pagerduty.canonical_path` and included in
:attr:`pagerduty.rest_api_v2_client.CANONICAL_PATHS`. Each value is either a tuple with
request and response body wrappers (if they differ), a string (if they are the same for
both cases) or ``None`` (if wrapping is disabled and the data is to be marshaled or
unmarshaled as-is). Values in tuples can also be None to denote that either the request
or response is unwrapped.

An endpoint, under the design logic of this client, is said to have entity
wrapping if the body (request or response) has only one property containing
the content requested or transmitted, apart from properties used for
pagination. If there are any secondary content-bearing properties (other than
those used for pagination), entity wrapping should be disabled to avoid
discarding those properties from responses or preventing the use of those
properties in request bodies.

:meta hide-value:
"""


################################
### REST API V2 URL HANDLING ###
################################

def canonical_path(base_url: str, url: str) -> str:
    """
    The canonical path from the API documentation corresponding to a URL

    This is used to identify and classify URLs according to which particular API
    within REST API v2 it belongs to.

    Explicitly supported canonical paths are defined in the list
    :attr:`pagerduty.rest_api_v2.CANONICAL_PATHS` and are the path part of any given
    API's URL. The path for a given API is what is shown at the top of its reference
    page, i.e.  ``/users/{id}/contact_methods`` for retrieving a user's contact methods
    (GET) or creating a new one (POST).

    :param base_url:
        The base URL of the API
    :param url:
        A non-normalized URL (a path or full URL)
    :returns:
        The canonical REST API v2 path corresponding to a URL.
    """
    full_url = normalize_url(base_url, url)
    # Starting with / after hostname before the query string:
    url_path = full_url.replace(base_url.rstrip('/'), '').split('?')[0]
    # Root node (blank) counts so we include it:
    n_nodes = url_path.count('/')
    # First winnow the list down to paths with the same number of nodes:
    patterns = list(filter(
        lambda p: p.count('/') == n_nodes,
        CANONICAL_PATHS
    ))
    # Match against each node, skipping index zero because the root node always
    # matches, and using the adjusted index "j":
    for i, node in enumerate(url_path.split('/')[1:]):
        j = i+1
        patterns = list(filter(
            lambda p: p.split('/')[j] == node or is_path_param(p.split('/')[j]),
            patterns
        ))
        # Don't break early if len(patterns) == 1, but require an exact match...

    if len(patterns) == 0:
        raise UrlError(f"URL {url} does not match any canonical API path " \
            'supported by this client.')
    elif len(patterns) > 1:
        # If there's multiple matches but one matches exactly, return that.
        if url_path in patterns:
            return url_path

        # ...otherwise this is ambiguous.
        raise Exception(f"Ambiguous URL {url} matches more than one " \
            "canonical path pattern: "+', '.join(patterns)+'; this is likely ' \
            'a bug.')
    else:
        return patterns[0]

def endpoint_matches(endpoint_pattern: str, method: str, path: str) -> bool:
    """
    Whether an endpoint (method and canonical path) matches a given pattern

    This is the filtering logic used for finding the appropriate entry in
    :attr:`pagerduty.rest_api_v2_client.ENTITY_WRAPPER_CONFIG` to use for a given method
    and API path.

    :param endpoint_pattern:
        The endpoint pattern in the form ``METHOD PATH`` where ``METHOD`` is the
        HTTP method in uppercase or ``*`` to match all methods, and ``PATH`` is
        a canonical API path.
    :param method:
        The HTTP method.
    :param path:
        The canonical API path (i.e. as returned by :func:`canonical_path`)
    :returns:
        True or False based on whether the pattern matches the endpoint
    """
    return (
        endpoint_pattern.startswith(method.upper()) \
            or endpoint_pattern.startswith('*')
    ) and endpoint_pattern.endswith(f" {path}")

def is_path_param(path_node: str) -> bool:
    """
    Whether a part of a canonical path represents a variable parameter

    :param path_node: The node (value between slashes) in the path
    :returns:
        True if the node is an arbitrary variable, False if it is a fixed value
    """
    return path_node.startswith('{') and path_node.endswith('}')

###############################
### ENTITY WRAPPING HELPERS ###
###############################

def entity_wrappers(method: str, path: str) -> tuple:
    """
    Obtains entity wrapping information for a given endpoint (path and method)

    :param method:
        The HTTP method
    :param path:
        A canonical API path i.e. as returned by ``canonical_path``
    :returns:
        A 2-tuple. The first element is the wrapper name that should be used for
        the request body, and the second is the wrapper name to be used for the
        response body. For either elements, if ``None`` is returned, that
        signals to disable wrapping and pass the user-supplied request body or
        API response body object unmodified.
    """
    m = method.upper()
    endpoint = "%s %s"%(m, path)
    match = list(filter(
        lambda k: endpoint_matches(k, m, path),
        ENTITY_WRAPPER_CONFIG.keys()
    ))

    if len(match) == 1:
        # Look up entity wrapping info from the global dictionary and validate:
        wrapper = ENTITY_WRAPPER_CONFIG[match[0]]
        invalid_config_error = 'Invalid entity wrapping configuration for ' \
                    f"{endpoint}: {wrapper}; this is most likely a bug."
        if wrapper is not None and type(wrapper) not in (tuple, str):
            raise Exception(invalid_config_error)
        elif wrapper is None or type(wrapper) is str:
            # Both request and response have the same wrapping at this endpoint.
            return (wrapper, wrapper)
        elif type(wrapper) is tuple and len(wrapper) == 2:
            # Endpoint uses different wrapping for request and response bodies.
            #
            # Both elements must be either str or None. The first element is the
            # request body wrapper and the second is the response body wrapper.
            # If a value is None, that indicates that the request or response
            # value should be encoded and decoded as-is without modifications.
            if False in [w is None or type(w) is str for w in wrapper]:
                # One or both is neither a string nor None, which is invalid:
                raise Exception(invalid_config_error)
            return wrapper
        else:
            # If not a tuple of length 2, or a string, or None, what are we doing here:
            raise Exception(invalid_config_error)
    elif len(match) == 0:
        # Nothing in entity wrapper config matches. In this case it is assumed
        # that the endpoint follows classic API patterns and the wrapper name
        # can be inferred from the URL and request method:
        wrapper = infer_entity_wrapper(method, path)
        return (wrapper, wrapper)
    else:
        matches_str = ', '.join(match)
        raise Exception(f"{endpoint} matches more than one pattern:" + \
            f"{matches_str}; this is most likely a bug.")

def infer_entity_wrapper(method: str, path: str) -> str:
    """
    Infer the entity wrapper name from the endpoint using orthodox patterns.

    This is based on patterns that are broadly applicable but not universal in
    the v2 REST API, where the wrapper name is predictable from the path and
    method. This is the default logic applied to determine the wrapper name
    based on the path if there is no explicit entity wrapping defined for the
    given path in :attr:`pagerduty.rest_api_v2_client.ENTITY_WRAPPER_CONFIG`.

    :param method:
        The HTTP method
    :param path:
        A canonical API path i.e. from
        :attr:`pagerduty.rest_api_v2_client.CANONICAL_PATHS`
    """
    m = method.upper()
    path_nodes = path.split('/')
    if is_path_param(path_nodes[-1]):
        # Singular if it's an individual resource's URL for read/update/delete
        # (named similarly to the second to last node, as the last is its ID and
        # the second to last denotes the API resource collection it is part of):
        return singular_name(path_nodes[-2])
    elif m == 'POST':
        # Singular if creating a new resource by POSTing to the index containing
        # similar resources (named simiarly to the last path node):
        return singular_name(path_nodes[-1])
    else:
        # Plural if listing via GET to the index endpoint, or doing a multi-put:
        return path_nodes[-1]

def unwrap(response: Response, wrapper: Optional[str]) -> Union[dict, list]:
    """
    Unwraps a wrapped entity from a HTTP response.

    :param response:
        The response object.
    :param wrapper:
        The entity wrapper (string), or None to skip unwrapping
    :returns:
        The value associated with the wrapper key in the JSON-decoded body of
        the response, which is expected to be a dictionary (map).
    """
    body = try_decoding(response)
    endpoint = "%s %s"%(response.request.method.upper(), response.request.url)
    if wrapper is not None:
        # There is a wrapped entity to unpack:
        bod_type = type(body)
        error_msg = f"Expected response body from {endpoint} after JSON-" \
            f"decoding to be a dictionary with a key \"{wrapper}\", but "
        if bod_type is dict:
            if wrapper in body:
                return body[wrapper]
            else:
                keys = truncate_text(', '.join(body.keys()))
                raise ServerHttpError(
                    error_msg + f"its keys are: {keys}",
                    response
                )
        else:
            raise ServerHttpError(
                error_msg + f"its type is {bod_type}.",
                response
            )
    else:
        # Wrapping is disabled for responses:
        return body

###########################
### FUNCTION DECORATORS ###
###########################

def auto_json(method: callable) -> callable:
    """
    Makes methods return the full response body object after decoding from JSON.

    Intended for use on functions that take a URL positional argument followed
    by keyword arguments and return a `requests.Response`_ object.
    """
    doc = method.__doc__
    def call(self, url, **kw):
        return try_decoding(successful_response(method(self, url, **kw)))
    call.__doc__ = doc
    return call

def resource_url(method: callable) -> callable:
    """
    API call decorator that allows passing a resource dict as the path/URL

    Most resources returned by the API will contain a ``self`` attribute that is
    the URL of the resource itself.

    Using this decorator allows the implementer to pass either a URL/path or
    such a resource dictionary as the ``path`` argument, thus eliminating the
    need to re-construct the resource URL or hold it in a temporary variable.
    """
    doc = method.__doc__
    name = method.__name__
    def call(self, resource, **kw):
        url = resource
        if type(resource) is dict:
            if 'self' in resource: # passing an object
                url = resource['self']
            else:
                # Unsupported APIs for this feature:
                raise UrlError(f"The dict object passed to {name} in place of a URL "
                    "has no 'self' key and cannot be used in place of an API resource "
                    "path/URL.")
        elif type(resource) is not str:
            name = method.__name__
            raise UrlError(f"Value passed to {name} is not a str or dict with "
                "key 'self'")
        return method(self, url, **kw)
    call.__doc__ = doc
    return call

def wrapped_entities(method: callable) -> callable:
    """
    Automatically wrap request entities and unwrap response entities.

    Used for methods :attr:`RestApiV2Client.rget`, :attr:`RestApiV2Client.rpost` and
    :attr:`RestApiV2Client.rput`. It makes them always return an object representing
    the resource entity in the response (whether wrapped in a root-level
    property or not) rather than the full response body. When making a post /
    put request, and passing the ``json`` keyword argument to specify the
    content to be JSON-encoded as the body, that keyword argument can be either
    the to-be-wrapped content or the full body including the entity wrapper, and
    the ``json`` keyword argument will be normalized to include the wrapper.

    Methods using this decorator will raise a :class:`HttpError` with its
    ``response`` property being being the `requests.Response`_ object in the
    case of any error (as of version 4.2 this is subclassed as
    :class:`HttpError`), so that the implementer can access it by catching the
    exception, and thus design their own custom logic around different types of
    error responses.

    :param method:
        Method being decorated. Must take one positional argument after ``self`` that is
        the URL/path to the resource, followed by keyword any number of keyword
        arguments, and must return an object of class `requests.Response`_, and be named
        after the HTTP method but with "r" prepended.
    :returns:
        A callable object; the reformed method
    """
    http_method = method.__name__.lstrip('r')
    doc = method.__doc__
    def call(self, url, **kw):
        pass_kw = deepcopy(kw) # Make a copy for modification
        path = canonical_path(self.url, url)
        endpoint = "%s %s"%(http_method.upper(), path)
        req_w, res_w = entity_wrappers(http_method, path)
        # Validate the abbreviated (or full) request payload, and automatically
        # wrap the request entity for the implementer if necessary:
        if req_w is not None and http_method in ('post', 'put') \
                and 'json' in pass_kw and req_w not in pass_kw['json']:
            pass_kw['json'] = {req_w: pass_kw['json']}

        # Make the request:
        r = successful_response(method(self, url, **pass_kw))

        # Unpack the response:
        return unwrap(r, res_w)
    call.__doc__ = doc
    return call

####################
### CLIENT CLASS ###
####################

class RestApiV2Client(ApiClient):
    """
    PagerDuty REST API v2 client class.

    Implements the most generic and oft-implemented aspects of PagerDuty's REST
    API v2 as an opinionated wrapper of `requests.Session`_.

    Inherits from :class:`ApiClient`.

    :param api_key:
        REST API access token to use for HTTP requests
    :param default_from:
        The default email address to use in the ``From`` header when making
        API calls using an account-level API access key.
    :param auth_type:
        The type of credential in use. If authenticating with an OAuth access
        token, this must be set to ``oauth2`` or ``bearer``.
    :param debug:
        Sets :attr:`print_debug`. Set to True to enable verbose command line
        output.

    :members:
    """

    api_call_counts = None
    """A dict object recording the number of API calls per endpoint"""

    api_time = None
    """A dict object recording the total time of API calls to each endpoint"""

    default_from = None
    """The default value to use as the ``From`` request header"""

    default_page_size = 100
    """
    This will be the default number of results requested in each page when
    iterating/querying an index (the ``limit`` parameter).
    """

    permitted_methods = ('GET', 'PATCH', 'POST', 'PUT', 'DELETE')

    url = 'https://api.pagerduty.com'
    """Base URL of the REST API"""

    def __init__(self, api_key: str, default_from: Optional[str] = None,
            auth_type: str = 'token', debug: bool = False):
        self.api_call_counts = {}
        self.api_time = {}
        self.auth_type = auth_type
        super(RestApiV2Client, self).__init__(api_key, debug=debug)
        self.default_from = default_from
        self.headers.update({
            'Accept': 'application/vnd.pagerduty+json;version=2',
        })

    def account_has_ability(self, ability: str) -> bool:
        """
        Test that the account has an ability.

        :param ability:
            The named ability, i.e. ``teams``.
        :returns:
            True or False based on whether the account has the named ability.
        """
        r = self.get(f"/abilities/{ability}")
        if r.status_code == 204:
            return True
        elif r.status_code == 402:
            return False
        elif r.status_code == 403:
            # Stop. Authorization failed. This is expected to be non-transient. This
            # may be added at a later time to ApiClient, i.e. to add a new default
            # action similar to HTTP 401. It would be a be a breaking change...
            raise HttpError(
                "Received 403 Forbidden response from the API. The identity "
                "associated with the credentials does not have permission to "
                "perform the requested action.", r)
        elif r.status_code == 404:
            raise HttpError(
                f"Invalid or unknown ability \"{ability}\"; API responded with status "
                "404 Not Found.", r)
        return False

    def after_set_api_key(self):
        self._subdomain = None

    @property
    def api_key_access(self) -> str:
        """
        Memoized API key access type getter.

        Will be "user" if the API key is a user-level token (all users should
        have permission to create an API key with the same permissions as they
        have in the PagerDuty web UI).

        If the API key in use is an account-level API token (as only a global
        administrator user can create), this property will be "account".
        """
        if not hasattr(self, '_api_key_access') or self._api_key_access is None:
            response = self.get('/users/me')
            if response.status_code == 400:
                message = try_decoding(response).get('error', '')
                if 'account-level access token' in message:
                    self._api_key_access = 'account'
                else:
                    self._api_key_access = None
                    self.log.error("Failed to obtain API key access level; "
                        "the API did not respond as expected.")
                    self.log.debug("Body = %s", truncate_text(response.text))
            else:
                self._api_key_access = 'user'
        return self._api_key_access

    @property
    def auth_type(self) -> str:
        """
        Defines the method of API authentication.

        This value determines how the Authorization header will be set. By default this
        is "token", which will result in the format ``Token token=<api_key>``.
        """
        return self._auth_type

    @auth_type.setter
    def auth_type(self, value: str):
        if value not in ('token', 'bearer', 'oauth2'):
            raise AttributeError("auth_type value must be \"token\" (default) "
                "or \"bearer\" or \"oauth\" to use OAuth2 authentication.")
        self._auth_type = value

    @property
    def auth_header(self) -> dict:
        if self.auth_type in ('bearer', 'oauth2'):
            return {"Authorization": "Bearer "+self.api_key}
        else:
            return {"Authorization": "Token token="+self.api_key}

    def dict_all(self, path: str, by: str = 'id', **kw) -> dict:
        """
        Dictionary representation of all results from an index endpoint.

        With the exception of ``by``, all keyword arguments passed to this method are
        also passed to :attr:`iter_all`; see the documentation on that method for
        further details.

        :param path:
            The index endpoint URL to use.
        :param by:
            The attribute of each object to use for the key values of the dictionary.
            This is ``id`` by default. Please note, there is no uniqueness validation,
            so if you use an attribute that is not distinct for the data set, this
            function will omit some data in the results. If a property is named that
            the schema of the API requested does not have, this method will raise
            ``KeyError``.
        :param kw:
            Keyword arguments to pass to :attr:`iter_all`.
        :returns:
            A dictionary keyed by the values of the property of each result specified by
            the ``by`` parameter.
        """
        iterator = self.iter_all(path, **kw)
        return {obj[by]:obj for obj in iterator}

    def find(self, resource: str, query: str, attribute: str = 'name',
            params: Optional[dict] = None) -> Union[dict, None]:
        """
        Finds an object of a given resource type exactly matching a query.

        Works by querying a given resource index endpoint using the ``query`` parameter.
        To use this function on any given resource, the resource's index must support
        the ``query`` parameter; otherwise, the function may not work as expected. If
        the index ignores the parameter, for instance, this function will take much
        longer to return; results will not be constrained to those matching the query,
        and so every result in the index will be downloaded and compared against the
        query up until a matching result is found or all results have been checked.

        The comparison between the query and matching results is case-insenitive. When
        determining uniqueness, APIs are mostly case-insensitive, and therefore objects
        with similar characters but differing case can't even exist. All results (and
        the search query) are for this reason reduced pre-comparison to a common form
        (all-lowercase strings) so that case doesn't need to match in the query argument
        (which is also interpreted by the API as case-insensitive).

        If said behavior differs for a given API, i.e. the uniqueness constraint on a
        field is case-sensitive, it should still return the correct results because the
        search term sent to the index in the querystring is not lower-cased.

        :param resource:
            The name of the resource endpoint to query, i.e.
            ``escalation_policies``
        :param query:
            The string to query for in the the index.
        :param attribute:
            The property of each result to compare against the query value when
            searching for an exact match. By default it is ``name``, but when
            searching for user by email (for example) it can be set to ``email``
        :param params:
            Optional additional parameters to use when querying.
        :returns:
            The dictionary representation of the result, if found; ``None`` will
            be returned if there is no exact match result.
        """
        query_params = {}
        if params is not None:
            query_params.update(params)
        query_params.update({'query': query})
        simplify = lambda s: str(s).lower()
        search_term = simplify(query)
        equiv = lambda s: simplify(s[attribute]) == search_term
        obj_iter = self.iter_all(resource, params=query_params)
        return next(iter(filter(equiv, obj_iter)), None)

    def get_total(self, url: str, params: Optional[dict] = None) -> int:
        """
        Gets the total count of records from a classic pagination index endpoint.

        :param url:
            The URL of the API endpoint to query
        :param params:
            An optional dictionary indicating additional parameters to send to the
            endpoint, i.e. filters, time range (``since`` and ``until``), etc. This may
            influence the total, i.e. if specifying a filter that matches a subset of
            possible results.
        :returns:
            The total number of results from the endpoint with the parameters given.
        """
        query_params = deepcopy(params)
        if query_params is None:
            query_params = {}
        query_params.update({
            'total': True,
            'limit': 1,
            'offset': 0
        })
        response = self.get(url, params=query_params)
        response_json = try_decoding(response)
        if 'total' not in response_json:
            path = canonical_path(self.url, url)
            raise ServerHttpError(
                f"Response from endpoint GET {path} lacks a \"total\" property. This " \
                "may be because the endpoint does not support classic pagination, or " \
                "implements it incompletely or incorrectly.",
                response
            )
        return int(response_json['total'])

    def iter_alert_grouping_settings(self, service_ids: Optional[list] = None,
                limit: Optional[int] = None) -> Iterator[dict]:
        """
        Iterator for the contents of the "List alert grouping settings" endpoint.

        The API endpoint "GET /alert_grouping_settings" has its own unique method of
        pagination. This method provides an abstraction for it similar to what
        :attr:`iter_all` provides for endpoints that implement classic pagination.

        See:
        `List alert grouping settings <https://developer.pagerduty.com/api-reference/b9fe211cc2748-list-alert-grouping-settings>`_

        :param service_ids:
            A list of specific service IDs to which results will be constrained.
        :param limit:
            The number of results retrieved per page. By default, the value
            :attr:`default_page_size` will be used.
        :yields:
            Results from each page in the ``alert_grouping_settings`` response property.
        """
        more = True
        after = None
        page_size = self.default_page_size
        if limit is not None:
            page_size = limit
        while more:
            params = {'limit': page_size}
            if service_ids is not None:
                params['service_ids[]'] = service_ids
            if after is not None:
                params['after'] = after
            page = self.jget('/alert_grouping_settings', params=params)
            for result in page['alert_grouping_settings']:
                yield result
            after = page.get('after', None)
            more = after is not None

    def iter_all(self, url, params: Optional[dict] = None,
                page_size: Optional[int] = None, item_hook: Optional[callable] = None,
                total: bool = False) -> Iterator[dict]:
        """
        Iterator for the contents of an index endpoint or query.

        Automatically paginates and yields the results in each page, until all
        matching results have been yielded or a HTTP error response is received.

        If the URL to use supports cursor-based pagintation, then this will
        return :attr:`iter_cursor` with the same keyword arguments. Otherwise,
        it implements classic pagination, a.k.a. numeric pagination.

        Each yielded value is a dict object representing a result returned from
        the index. For example, if requesting the ``/users`` endpoint, each
        yielded value will be an entry of the ``users`` array property in the
        response.

        :param url:
            The index endpoint URL to use.
        :param params:
            Additional URL parameters to include.
        :param page_size:
            If set, the ``page_size`` argument will override the
            ``default_page_size`` parameter on the session and set the ``limit``
            parameter to a custom value (default is 100), altering the number of
            pagination results. The actual number of results in the response
            will still take precedence, if it differs; this parameter and
            ``default_page_size`` only dictate what is requested of the API.
        :param item_hook:
            Callable object that will be invoked for each item yielded, i.e. for
            printing progress. It will be called with three parameters: a dict
            representing a given result in the iteration, an int representing the number
            of the item in the series, and a value representing the total number of
            items in the series. If the total isn't knowable, i.e. the ``total``
            parameter is ``False`` or omitted, the value passed in for the third
            argument will be the string value ``"?"``.
        :param total:
            If True, the ``total`` parameter will be included in API calls, and
            the value for the third parameter to the item hook will be the total
            count of records that match the query. Leaving this as False confers
            a small performance advantage, as the API in this case does not have
            to compute the total count of results in the query.
        :yields:
            Results from each page of results.
        """
        # Get entity wrapping and validate that the URL being requested is
        # likely to support pagination:
        path = canonical_path(self.url, url)
        endpoint = f"GET {path}"

        # Short-circuit to cursor-based pagination if appropriate:
        if path in CURSOR_BASED_PAGINATION_PATHS:
            return self.iter_cursor(url, params=params, page_size=page_size,
                item_hook=item_hook)

        nodes = path.split('/')
        if is_path_param(nodes[-1]):
            # NOTE: If this happens for a newer API, the path might need to be
            # added to the EXPAND_PATHS dictionary in
            # scripts/get_path_list/get_path_list.py, after which
            # CANONICAL_PATHS will then need to be updated accordingly based on
            # the new output of the script.
            raise UrlError(f"Path {path} (URL={url}) is formatted like an " \
                "individual resource versus a resource collection. It is " \
                "therefore assumed to not support pagination.")
        _, wrapper = entity_wrappers('GET', path)

        if wrapper is None:
            raise UrlError(f"Pagination is not supported for {endpoint}.")

        # Parameters to send:
        data = {
            'limit': (self.default_page_size, page_size)[int(bool(page_size))],
            'total': int(bool(total))
        }
        if isinstance(params, (dict, list)):
            # Override defaults with values given:
            data.update(dict(params))

        more = True
        offset = 0
        if params is not None:
            offset = int(params.get('offset', 0))
        n = 0
        while more:
            # Check the offset and limit:
            data['offset'] = offset
            highest_record_index = int(data['offset']) + int(data['limit'])
            if highest_record_index > ITERATION_LIMIT:
                iter_limit = '%d'%ITERATION_LIMIT
                warn(
                    f"Stopping iter_all on {endpoint} at " \
                    f"limit+offset={highest_record_index} " \
                    'as this exceeds the maximum permitted by the API ' \
                    f"({iter_limit}). The set of results may be incomplete."
                )
                return

            # Make the request and validate/unpack the response:
            r = successful_response(
                self.get(url, params=data.copy()),
                context='classic pagination'
            )
            body = try_decoding(r)
            results = unwrap(r, wrapper)

            # Validate and update pagination parameters
            #
            # Note, the number of the results in the actual response is always
            # the most appropriate amount to increment the offset by after
            # receiving each page. If this is the last page, pagination should
            # stop anyways because the ``more`` parameter should evaluate to
            # false.
            #
            # In short, the reasons why we don't trust the echoed ``limit``
            # value or stick to the limit requested and hope the server honors
            # it is that it could potentially result in skipping results or
            # yielding duplicates if there's a mismatch, or potentially issues
            # like PagerDuty/pdpyras#61
            data['limit'] = len(results)
            offset += data['limit']
            more = False
            if 'total' in body:
                total_count = body['total']
            else:
                total_count = '?'
            if 'more' in body:
                more = body['more']
            else:
                warn(
                    f"Response from endpoint GET {path} lacks a \"more\" property and "
                    "therefore does not support pagination. Only results from the "
                    "first request will be yielded. You can use \"rget\" with this "
                    "endpoint instead to avoid this warning."
                )

            # Perform per-page actions on the response data
            for result in results:
                n += 1
                # Call a callable object for each item, i.e. to print progress:
                if hasattr(item_hook, '__call__'):
                    item_hook(result, n, total_count)
                yield result

    def iter_analytics_raw_incidents(self, filters: dict, order: str = 'desc',
                order_by: str = 'created_at', limit: Optional[int] = None,
                time_zone: Optional[str] = None) -> Iterator[dict]:
        """
        Iterator for raw analytics data on multiple incidents.

        The API endpoint ``POST /analytics/raw/incidents`` has its own unique method of
        pagination. This method provides an abstraction for it similar to
        :attr:`iter_all`.

        See: 
        `Get raw data - multiple incidents <https://developer.pagerduty.com/api-reference/c2d493e995071-get-raw-data-multiple-incidents>`_

        :param filters:
            Dictionary representation of the required ``filters`` parameters.
        :param order:
            The order in which to sort results. Must be ``asc`` or ``desc``.
        :param order_by:
            The attribute of results by which to order results. Must be ``created_at``
            or ``seconds_to_resolve``.
        :param limit:
            The number of results to yield per page before requesting the next page. If
            unspecified, :attr:`default_page_size` will be used. The particular API
            endpoint permits values up to 1000.
        :yields:
            Entries of the ``data`` property in the response body from each page
        """
        page_size = self.default_page_size
        if limit is not None:
            page_size = limit
        more = True
        last = None
        while more:
            body = {
                'filters': filters,
                'order': order,
                'order_by': order_by,
                'limit': page_size
            }
            if time_zone is not None:
                body['time_zone'] = time_zone
            if last is not None:
                body['starting_after'] = last
            page = self.jpost('/analytics/raw/incidents', json=body)
            for result in page['data']:
                yield result
            last = page.get('last', None)
            more = page.get('more', False) and last is not None


    def iter_cursor(self, url: str, params: Optional[dict] = None,
                item_hook: Optional[callable] = None,
                page_size: Optional[int] = None) -> Iterator[dict]:
        """
        Iterator for results from an endpoint using cursor-based pagination.

        :param url:
            The index endpoint URL to use.
        :param params:
            Query parameters to include in the request.
        :param item_hook:
            A callable object that accepts 3 positional arguments; see :attr:`iter_all`
            for details on how this argument is used.
        :param page_size:
            Number of results per page of results (the ``limit`` parameter). If
            unspecified, :attr:`default_page_size` will be used.
        :yields:
            Results from each page of results.
        """
        path = canonical_path(self.url, url)
        if path not in CURSOR_BASED_PAGINATION_PATHS:
            raise UrlError(f"{path} does not support cursor-based pagination.")
        _, wrapper = entity_wrappers('GET', path)
        user_params = {
            'limit': (self.default_page_size, page_size)[int(bool(page_size))]
        }
        if isinstance(params, (dict, list)):
            # Override defaults with values given:
            user_params.update(dict(params))

        more = True
        next_cursor = None
        total = 0

        while more:
            # Update parameters and request a new page:
            if next_cursor:
                user_params.update({'cursor': next_cursor})
            r = successful_response(
                self.get(url, params=user_params),
                context='cursor-based pagination',
            )

            # Unpack and yield results
            body = try_decoding(r)
            results = unwrap(r, wrapper)
            for result in results:
                total += 1
                if hasattr(item_hook, '__call__'):
                    item_hook(result, total, '?')
                yield result

            # Advance to the next page
            next_cursor = body.get('next_cursor', None)
            more = bool(next_cursor)

    def iter_history(self, url: str, since: datetime, until: datetime,
            recursion_depth: int = 0, **kw) -> Iterator[dict]:
        """
        Yield all historical records from an endpoint in a given time interval.

        This method works around the limitation of classic pagination (see
        :attr:`pagerduty.rest_api_v2_client.ITERATION_LIMIT`) by sub-dividing queries
        into lesser time intervals wherein the total number of results does not exceed
        the pagination limit.

        :param url:
            Index endpoint (API URL) from which to yield results. In the event that a
            cursor-based pagination endpoint is given, this method calls
            :attr:`iter_cursor` directly, as cursor-based pagination has no such
            limitation.
        :param since:
            The beginning of the time interval. This must be a non-naïve datetime object
            (i.e. it must be timezone-aware), in order to format the ``since`` parameter
            when transmitting it to the API such that it unambiguously takes the time
            zone into account. See: `datetime (Python documentation)
            <https://docs.python.org/3/library/datetime.html>`_
        :param until:
            The end of the time interval. A timezone-aware datetime object must be
            supplied for the same reason as for the ``since`` parameter.
        :param kw:
            Custom keyword arguments to pass to the iteration method. Note, if providing
            ``params`` in order to add query string parameters for filtering, the
            ``since`` and ``until`` keys (if present) will be ignored.
        :yields:
            All results from the resource collection API within the time range specified
            by ``since`` and ``until``.
        """
        path = canonical_path(self.url, url)
        since_until = {
            'since': strftime(since),
            'until': strftime(until)
        }
        iter_kw = deepcopy(kw)
        if path not in HISTORICAL_RECORD_PATHS:
            # Cannot continue; incompatible endpoint that doesn't accept since/until:
            raise UrlError(f"Method iter_history does not support {path}")
        elif path == '/oncalls':
            # Warn for this specific endpoint but continue:
            warn('iter_history may yield duplicate results when used with /oncalls')
        elif path in CURSOR_BASED_PAGINATION_PATHS:
            # Short-circuit to iter_cursor:
            iter_kw.setdefault('params', {})
            iter_kw['params'].update(since_until)
            return self.iter_cursor(url, **iter_kw)
        # Obtain the total number of records for the interval:
        query_params = kw.get('params', {})
        query_params.update(since_until)
        total = self.get_total(url, params=query_params)

        no_results = total == 0
        can_fully_paginate = total <= ITERATION_LIMIT
        min_interval_len = int((until - since).total_seconds()) == 1
        stop_recursion = recursion_depth >= RECURSION_LIMIT
        if no_results:
            # Nothing to be done for this interval
            pass
        elif can_fully_paginate or min_interval_len or stop_recursion:
            # Do not subdivide any further; it is either not necessary or not feasible.
            if not can_fully_paginate:
                # Issue a warning log message
                if stop_recursion:
                    reason = 'the recursion depth limit has been reached'
                    suggestion = ' To avoid this issue, try requesting a smaller ' \
                        'initial time interval.'
                elif min_interval_len:
                    reason = 'the time interval is already the minimum length (1s)'
                    # In practice, this scenario can only happen when PagerDuty ingests
                    # and processes, for a single account, >10k alert history events per
                    # second (to use `/log_entries` as an example). There is
                    # unfortunately nothing more that can be done in this case.
                    suggestion = ''
                self.log.warning(ITER_HIST_RECURSION_WARNING_TEMPLATE.format(
                    reason = reason,
                    since_until = str(since_until),
                    iteration_limit = ITERATION_LIMIT,
                    suggestion = suggestion
                ))
            iter_kw.setdefault('params', {})
            iter_kw['params'].update(since_until)
            for item in self.iter_all(url, **iter_kw):
                yield item
        else:
            # If total exceeds maximum, bisect the time window and recurse:
            iter_kw['recursion_depth'] = recursion_depth + 1
            for (sub_since, sub_until) in datetime_intervals(since, until, n=2):
                for item in self.iter_history(url, sub_since, sub_until, **iter_kw):
                    yield item

    def iter_incident_notes(self, incident_id: Optional[str] = None, **kw) \
            -> Iterator[dict]:
        """
        Iterator for incident notes.

        This is a filtered iterator for log entries of type ``annotate_log_entry``.

        :param incident_id:
            Optionally, request log entries for a specific incident. If included, the
            ``team_ids[]`` query parameter will be removed and ignored.
        :param kw:
            Custom keyword arguments to send to :attr:`iter_all`.
        :yields:
            Incident note log entries as dictionary objects
        """
        my_kw = deepcopy(kw)
        my_kw.setdefault('params', {})
        url = '/log_entries'
        if incident_id is not None:
            url = f"/incidents/{incident_id}/log_entries"
            # The teams filter is irrelevant for a specific incident's log entries, so
            # it must be removed if present:
            for key in ('team_ids', 'team_ids[]'):
                if 'params' in my_kw and key in my_kw['params']:
                    del(my_kw['params'][key])
        return iter(filter(
            lambda ile: ile['type'] == 'annotate_log_entry',
            self.iter_all(url, **my_kw)
        ))

    @resource_url
    @auto_json
    def jget(self, url: Union[str, dict], **kw) -> Union[dict, list]:
        """
        Performs a GET request, returning the JSON-decoded body as a dictionary
        """
        return self.get(url, **kw)

    @resource_url
    @auto_json
    def jpost(self, url: Union[str, dict], **kw) -> Union[dict, list]:
        """
        Performs a POST request, returning the JSON-decoded body as a dictionary
        """
        return self.post(url, **kw)

    @resource_url
    @auto_json
    def jput(self, url: Union[str, dict], **kw) -> Optional[Union[dict, list]]:
        """
        Performs a PUT request, returning the JSON-decoded body as a dictionary
        """
        return self.put(url, **kw)

    def list_all(self, url: str, **kw) -> list:
        """
        Returns a list of all objects from a given index endpoint.

        All keyword arguments passed to this function are also passed directly
        to :attr:`iter_all`; see the documentation on that method for details.

        :param url:
            The index endpoint URL to use.
        """
        return list(self.iter_all(url, **kw))

    def normalize_params(self, params: dict) -> dict:
        """
        Modify the user-supplied parameters to ease implementation

        Current behavior:

        * If a parameter's value is of type list, and the parameter name does
          not already end in "[]", then the square brackets are appended to keep
          in line with the requirement that all set filters' parameter names end
          in "[]".

        :returns:
            The query parameters after modification
        """
        updated_params = {}
        for param, value in params.items():
            if type(value) is list and not param.endswith('[]'):
                updated_params[param+'[]'] = value
            else:
                updated_params[param] = value
        return updated_params


    def persist(self, resource: str, attr: str, values: dict, update: bool = False) \
            -> dict:
        """
        Finds or creates and returns a resource with a matching attribute

        Given a resource name, an attribute to use as an idempotency key and a
        set of attribute:value pairs as a dict, create a resource with the
        specified attributes if it doesn't exist already and return the resource
        persisted via the API (whether or not it already existed).

        :param resource:
            The URL to use when creating the new resource or searching for an
            existing one. The underlying AP must support entity wrapping to use
            this method with it.
        :param attr:
            Name of the attribute to use as the idempotency key. For instance,
            "email" when the resource is "users" will not create the user if a
            user with the email address given in ``values`` already exists.
        :param values:
            The content of the resource to be created, if it does not already
            exist. This must contain an item with a key that is the same as the
            ``attr`` argument.
        :param update:
            (New in 4.4.0) If set to True, any existing resource will be updated
            with the values supplied.
        """
        if attr not in values:
            raise ValueError("Argument `values` must contain a key equal "
                "to the `attr` argument (expected idempotency key: '%s')."%attr)
        existing = self.find(resource, values[attr], attribute=attr)
        if existing:
            if update:
                original = {}
                original.update(existing)
                existing.update(values)
                if original != existing:
                    existing = self.rput(existing, json=existing)
            return existing
        else:
            return self.rpost(resource, json=values)

    def postprocess(self, response: Response, suffix: Optional[str] = None):
        """
        Records performance information / request metadata about the API call.

        :param response:
            The `requests.Response`_ object returned by the request method
        :param suffix:
            Optional suffix to append to the key
        :type method: str
        :type response: `requests.Response`_
        :type suffix: str or None
        """
        method = response.request.method.upper()
        url = response.request.url
        status = response.status_code
        request_date = response.headers.get('date', '(missing header)')
        request_id = response.headers.get('x-request-id', '(missing header)')
        request_time = response.elapsed.total_seconds()

        try:
            endpoint = "%s %s"%(method, canonical_path(self.url, url))
        except UrlError:
            # This is necessary so that profiling can also support using the
            # basic get / post / put / delete methods with APIs that are not yet
            # explicitly supported by inclusion in CANONICAL_PATHS.
            endpoint = "%s %s"%(method, url)
        self.api_call_counts.setdefault(endpoint, 0)
        self.api_time.setdefault(endpoint, 0.0)
        self.api_call_counts[endpoint] += 1
        self.api_time[endpoint] += request_time

        # Request ID / timestamp logging
        self.log.debug("Request completed: #method=%s|#url=%s|#status=%d|"
            "#x_request_id=%s|#date=%s|#wall_time_s=%g", method, url, status,
            request_id, request_date, request_time)
        if int(status/100) == 5:
            self.log.error("PagerDuty API server error (%d)! "
                "For additional diagnostics, contact PagerDuty support "
                "and reference x_request_id=%s / date=%s",
                status, request_id, request_date)

    def prepare_headers(self, method: str, user_headers: Optional[dict] = None) -> dict:
        """
        Amends and combines default and user-supplied headers for a REST API request.

        :param method:
            The HTTP method
        :param user_headers:
            Any user-supplied headers
        :returns:
            A dictionary of the final headers to use in the request
        """
        headers = deepcopy(self.headers)
        headers['User-Agent'] = self.user_agent
        if self.default_from is not None:
            headers['From'] = self.default_from
        if method in ('POST', 'PUT'):
            headers['Content-Type'] = 'application/json'
        if user_headers:
            headers.update(user_headers)
        return headers

    @resource_url
    @requires_success
    def rdelete(self, resource: Union[str, dict], **kw) -> Response:
        """
        Delete a resource.

        :param resource:
            The path/URL to which to send the request, or a dict object
            representing an API resource that contains an item with key ``self``
            whose value is the URL of the resource.
        :param **kw:
            Custom keyword arguments to pass to ``requests.Session.delete``
        """
        return self.delete(resource, **kw)

    @resource_url
    @wrapped_entities
    def rget(self, resource: Union[str, dict], **kw) -> Union[dict, list]:
        """
        Wrapped-entity-aware GET function.

        Retrieves a resource via GET and returns the wrapped entity in the
        response.

        :param resource:
            The path/URL to which to send the request, or a dict object
            representing an API resource that contains an item with key ``self``
            whose value is the URL of the resource.
        :param **kw:
            Custom keyword arguments to pass to ``requests.Session.get``
        :returns:
            The API response after JSON-decoding and unwrapping
        """
        return self.get(resource, **kw)

    @wrapped_entities
    def rpatch(self, path: str, **kw) -> dict:
        """
        Wrapped-entity-aware PATCH function.

        Currently the only API endpoint that uses or supports this method is "Update
        Workflow Integration Connection": ``PATCH
        /workflows/integrations/{integration_id}/connections/{id}``

        It cannot use the :attr:`resource_url` decorator because the schema in that case
        has no ``self`` property, and so the URL or path must be supplied.

        :param path:
            The URL to be requested
        :param kw:
            Keyword arguments to send to the request function, i.e. ``params``
        :returns:
            The API response after JSON-decoding and unwrapping
        """
        return self.patch(path, **kw)

    @wrapped_entities
    def rpost(self, path: str, **kw) -> Union[dict, list]:
        """
        Wrapped-entity-aware POST function.

        Creates a resource and returns the created entity if successful.

        :param path:
            The path/URL to which to send the POST request, which should be an
            index endpoint.
        :param **kw:
            Custom keyword arguments to pass to ``requests.Session.post``
        :returns:
            The API response after JSON-decoding and unwrapping
        """
        return self.post(path, **kw)

    @resource_url
    @wrapped_entities
    def rput(self, resource: Union[str, dict], **kw) -> Optional[Union[dict, list]]:
        """
        Wrapped-entity-aware PUT function.

        Update an individual resource, returning the wrapped entity.

        :param resource:
            The path/URL to which to send the request, or a dict object
            representing an API resource that contains an item with key ``self``
            whose value is the URL of the resource.
        :param **kw:
            Custom keyword arguments to pass to ``requests.Session.put``
        :returns:
            The API response after JSON-decoding and unwrapping. In the case of at least
            one Teams API endpoint and any other future API endpoint that responds with
            204 No Content, the return value will be None.
        """
        return self.put(resource, **kw)

    @property
    def subdomain(self) -> str:
        """
        Subdomain of the PagerDuty account of the API access token.
        """
        if not hasattr(self, '_subdomain') or self._subdomain is None:
            try:
                url = self.rget('users', params={'limit':1})[0]['html_url']
                self._subdomain = url.split('/')[2].split('.')[0]
            except Error as e:
                self.log.error("Failed to obtain subdomain; encountered error.")
                self._subdomain = None
                raise e
        return self._subdomain

    @property
    def total_call_count(self) -> int:
        """The total number of API calls made by this instance."""
        return sum(self.api_call_counts.values())

    @property
    def total_call_time(self) -> float:
        """The total time spent making API calls."""
        return sum(self.api_time.values())

    @property
    def trunc_token(self) -> str:
        """Truncated API key for secure display/identification purposes."""
        warn("Property trunc_token is deprecated. Use trunc_key instead.")
        return self.trunc_key
