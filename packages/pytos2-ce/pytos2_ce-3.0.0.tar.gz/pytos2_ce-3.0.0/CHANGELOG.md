# Changelog
All notable changes to this project will be documented in this file

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [3.0.0] - 2025-07-14
#### Added
- Fix: Task.create_field wasn't working for all field types 
- Fix: NetworkObject was not being properly classified on rule modification tickets.
- Fix: St.search_services() not classifying objects correctly
- Fix: Work around for St.search_services() not paging properly because endpoint doesn't return a correct total
- Method: St.search_network_objects() - Search network objects using search endpoint
- `add_parent_objects` argument to St.get_network_objects()
- Method: Sa.update_application() - Update an application in SecureApp.
- Method: Sa.bulk_update_applications() - Update multiple applications in SecureApp.
- Method: Sa.get_application_access_requests() - Get all access requests for a specific application.
- Method: Sa.get_application_access_request() - Get a specific access request for an application.
- Method: Sa.add_application_access_request() - Add an access request for an application.
- Method: Sa.approve_application_access_request() - Approve an access request for an application.
- method: Sa.reject_application_access_request() - Reject an access request for an application.
- Method: Sa.bulk_update_application_access_requests() - Update multiple access requests for an application. 
- Method: Sa.get_extended_application_connections() - Get extended application connection information for a specific application.
- Method: Sa.get_application_connections() - Get all application connections from a specific application in SecureApp.
- Method: Sa.get_application_connection() - Get a specific application connection in SecureApp.
- Method: Sa.add_application_connection() - Add a new application connection to SecureApp.
- Method: Sa.update_application_connection() - Update an application connection in SecureApp.
- Method: Sa.bulk_update_application_connections() - Update multiple application connections in SecureApp.
- Method: Sa.delete_application_connection() - Delete an application connection from SecureApp.
- Method: Sa.get_application_interfaces() - Get all interfaces for a specific application in SecureApp.
- Method: Sa.get_application_interface() - Get a specific interface for an application in SecureApp.
- Method: Sa.add_application_interface() - Add a new interface to an application in SecureApp.
- Method: Sa.update_application_interface() - Update an interface for an application in SecureApp.
- Method: Sa.delete_application_interface() - Delete an interface from an application in SecureApp.
- Method: Sa.get_application_interface_connections() - Get all interface connections for a specific application interface in SecureApp.
- Method: Sa.get_application_interface_connection() - Get a specific interface connection for an application interface in SecureApp.
- Method: Sa.add_application_interface_connection() - Add a new interface connection to an application interface in SecureApp.
- Method: Sa.update_application_interface_connection() - Update an interface connection for an application interface in SecureApp.
- Method: Sa.delete_application_interface_connection() - Delete an interface connection from an application interface in SecureApp.
- Method: Sa.get_application_connections_to_applications() - Get all connections to applications for a specific application in SecureApp.
- Method: Sa.get_application_connection_to_application() - Get a specific connection to an application for an application in SecureApp.
- Method: Sa.add_application_connection_to_application() - Add a new connection to an application for an application in SecureApp.
- Method: Sa.update_application_connection_to_application() - Update a connection to an application for an application in SecureApp.
- Method: Sa.delete_application_connection_to_application() - Delete a connection to an application for an application in SecureApp.
- Method: Sa.repair_connection() - Create a ticket for repairing a connection in SecureApp.
- Method: St.get_internet_object() - Get the internet representation object for a device.
- Method: St.get_internet_resolved_object() - Get the Tufin network object representation for an internet object.
- Method: St.add_internet_object() - Add or create an internet representation object for a device.
- Method: St.update_internet_object() - Update an internet representation object for a device.
- Method: st.get_topology_subnets() - Get a list of topology subnets - Returns a pager, use pager.fetch_all()
- Method: st.get_topology_subnet() - Get a detailed subnet object by id
- Method: St.export_security_rules - Initiates a filtered export of Security Rules to the SecureTrack Reports Repository

## [2.5.2] - 2025-06-17
#### Fixed
- Reverted a change to APISession which broke an internal API which was depending on it.

## [2.5.0] - 2025-02-14 
#### Added
- Model: DeviceLicenseStatus
- Adds ST Device Support for Azure, Meraki, GCP, and Checkpoint Smart One
- Adds support show_os_version and show_licenses for devices via license and version arguments to get_device, get_devices methods
- Method: st.search_services() - Search services on devices filtered by name, comment, protocol, port, and device
- Method: st.get_service_groups() - Get all ServiceGroup objects for a specific service using service ID
- Method: st.get_service_rules() - Get all rules for a specified service using service ID
- Method: st.get_services() - Expanded to include filtering as well as ability to fetch by revision. You may also get specific object IDs.
- Method: st.get_internet_representing_address() - Get the internet representing address value for network simulations
- Method: st.set_internet_representing_address() - Set the internet representing address value for network simulations
- Method: st.get_revision_rule_documentation() - Get documentation object for a single rule by revision ID and rule ID
- Method: st.update_rule_documentation_by_revision() - Update documentation object for a single rule by revision ID and rule ID
- Method: st.delete_rule_documentation() - Delete documentation for specified rule using device info and rule info
- Method: st.delete_rule_documentation_by_revision() - Delete documentation for specified rule using revision ID and rule info
- Method: st.get_usp_violating_rules() - Get a list of violating rules for a given device, severity, and type
- Method: st.get_usp_violating_rules_count() - Get a count of all violating rules for a given device
- Method: Scw.add_user_group() - Add a SecureChange User Group
- Method: Scw.add_user() - Add a new local user in SecureChange
- Method: Scw.update_user_group() - Update a SecureChange User Group
- Method: Scw.delete_user_or_group() - Delete a SecureChange User or User Group
- Method: Scw.user_import_ldap() - Import an LDAP User or Group into SecureChange using the LDAP already configured in SecureChange
- Method: Scw.user_login() - Implicitly imports an LDAP user as "automatic users" to SecureChange by simulating their login
- Method: Scw.group_login() - Implicitly imports an LDAP group as "automatic users" to SecureChange by simulating their login
- Method: Scw.get_roles() - Get a list of User Roles from SecureChange
- Method: Scw.get_role() - Get a User Role by Id from SecureChange
- Method: Scw.update_user_roles() - Update a list of User Roles in SecureChange
- Method: Scw.get_domains() - Get a list of all Domains from SecureChange
- Method: Scw.get_domain() - Get a single Domain from SecureChange by Id
- Method: Scw.synchronize_domains() - Synchronizes SecureTrack Domains to SecureChange
- Method: scw.get_requests() - Get all tickets and ticket drafts in SecureChange
- Method: scw.cancel_request() - Cancel a ticket or ticket draft in SecureChange
- Method: Scw.ticket_search_by_details() - Get a list of tickets from SecureChange by search details.
- Method: Scw.ticket_search_by_saved_search() - Get a list of tickets from SecureChange by Query Id.
- Method: Scw.ticket_search_by_group() - Get a list of tickets from SecureChange by Group Id.
- Method: Scw.ticket_search_by_free_text() - Get a list of tickets from SecureChange by FreeText.
- Method: Scw.get_network_objects() - Expanded to include filtering as well as ability to fetch by revision. You may also get specific object IDs.
- Method: St.get_network_object_groups() - Get a list of network groups that contain the specified Network Object ID
- Method: St.get_network_object_rules() - Get a list of rules that contain the specified Network Object ID

#### Changed
- Device object added licenses, module_type, status attributes

## [2.4.4] - 2024-12-12
#### Added
- `add_parent_objects` argument to St.get_network_objects()

## [2.4.3] - 2024-12-11
#### Fixed
- Correctly handle typing.Dict type hint in propify declarations.

## [2.4.2] - 2024-12-06
#### Fixed
- Correctly handle multiple targets in multi_server_decommission_request

## [2.4.1] - 2024-10-28
#### Added
- Method: St.bulk_delete_devices() - Delete multiple monitored devices from securetrack.
- Method: St.bulk_update_topology() - Synchronizes of topology for specific devices.
- Method: St.get_bulk_device_tasks() - Get bulk operation task results.
- Method: Sa.get_application_connections() - Get all application connections from a specific application in SecureApp.
- Method: Sa.get_application_connection() - Get a specific application connection in SecureApp.
- Method: Sa.get_application_history() - Get application history by application ID.
- Method: Sa.add_application() - Add a new application to SecureApp.
- Method: Sa.delete_application() - Delete an application from SecureApp.
- Rename: St.remove_usp_map() to St.delete_usp_map()

## [2.4.0] - 2024-09-27
#### Added
- Adds support for multiple devices in rule operation tickets.
- Adds related rules result to tickets.
- Adds graphql support to St.
- Models to support the methods listed below.
- Fixes ticket save function.
- Method: Device.get_time_objects() - Get time objects for a specific device.
- Method: Scw.get_triggers() - Get all configured workflow triggers
- Method: Scw.get_trigger() - Get a specific trigger by name or ID.
- Method: Scw.add_trigger() - Add a new trigger
- Method: Scw.change_requester() - Change the requester of a ticket.
- Method: Scw.get_ticket_events() - Get historical events for a specific ticket.
- Method: Scw.backfill_ticket_events() - Backfill historical events for tickets from a specified date.
- Method: Scw.get_ticket_historical_events_status() - Get the status of a backfill request.
- Method: Scw.map_rules() - Map ticket to rules in SecureTrack.
- Method: Scw.designer_redesign() - Designer redesign for SecureChange.
- Method: Scw.designer_device_commit() - Designer device commit for SecureChange.
- Method: Scw.designer_device_update() - Designer device update for SecureChange.
- Method: Scw.get_workflows() - Get basic workflow information.
- Method: Scw.get_workflow() - Get detailed workflow information.
- Method: Sa.get_applications() - Get all applications from SecureApp.
- Method: Sa.get_application() - Get a specific application from SecureApp.
- Method: St.get_change_windows() - Get all change windows configured in SecureTrack R22-2+
- Method: St.get_change_window_tasks() - Get all tasks for a specific change window.
- Method: St.get_device_applications() - Get application objects on a specific device.
- Method: St.get_device_rule_last_usage() - Get the last usage of rules from a specific device.
- Method: St.get_device_rule_last_usage_for_uid() - Get the last usage of device rule by UID.
- Method: St.get_properties() - Get SecureTrack properties.
- Method: St.set_license_notification_days() - Set the number of days before license expiration to send a notification.
- Method: St.get_time_objects() - Get time objects by revision, optionally specifying which time object ids.
- Method: St.get_time_objects_by_device() - Get time objects by device.
- Method: St.get_licenses() - Get SecureTrack licenses.
- Method: St.get_license() - Get specific SecureTrack license.
- Method: St.get_tiered_license() - Get tiered license information if it exists.
- Method: St.get_extensions() - Get installed custom extensions.
- Method: St.get_usp_policies() - Get customer's USP policies.
- Method: St.export_usp_policy() - Get CSV string of USP policy.
- Method: St.delete_usp_policy() - Delete USP policy.
- Method: St.get_usp_map() - Get interface mappings for USP policy.
- Method: St.add_usp_map() - Adds USP mapping for device and interface.
- Method: St.remove_usp_map() - Removes USP mapping for device and interface.
- Method: St.get_clouds() - Get topology clouds.
- Method: St.get_cloud() - Get specific topology cloud.
- Method: St.get_cloud_internal_networks() - Get a list of internal networks for a specific cloud.
- Method: St.add_topology_cloud() - Add a new topology cloud.
- Method: St.update_topology_cloud() - Update a topology cloud.
- Method: St.get_cloud_suggestions() - Get cloud suggestions.
- Method: St.get_cloud_suggestions_by_id() - Returns information about a specific cloud in the topology.
- Method: Ticket.map_rules() - Map ticket to rules in SecureTrack.
- Method: Ticket.designer_redesign() - Ticket helper for designer redesign.
- Method: Ticket.designer_device_commit() - Ticket helper for designer device commit.
- Method: Ticket.designer_device_update() - Ticket helper for designer device update.
- Method: Ticket.cancel() - Cancel a ticket.
- Method: Ticket.confirm() - Confirm a ticket.

#### Fixed
- Generic Interface functions are now operable.

## [2.3.15] - 2024-01-03
#### Added
- Method: Scw.get_ticket_history() -  Get ticket history by ticket ID. 
- Method: Ticket object helper method ticket.get_history()

#### Fixed
- Dependency issues preventing install. 
- Bugfix: SDK properly handles reverse IP ranges.
-
#### Changed
- mypy unit testing updates. 
- Documentation updates


## [2.3.14] - 2023-08-02
#### Added 
- Model: support for ModificationIPService field from OtherIPServiceObject within SecureChange rule operations.

## [2.3.13] - 2023-03-09
#### Changed
- converted usage example to jupyter 
- added trigger example
#### Added 
- Method: Scw.add_comment()
- Method: Scw.delete_comment()
- Network Object Model: VMInstanceDTO

## [2.3.12] - 2023-02-16
#### Added 
- Method: Scw.add_comment() - Add a comment to a specific ticket, step and task
- Method: Scw.delete_comment() - Remove a comment from a ticket
- Method: Added comment helpers to Ticket Model:
  - add_comment - add comment to ticket (current step and task used by default)
  - add_comments - add a list of comments to ticket (current step and task used by default)
  - delete_comment - remove a comment from ticket by id
  - delete_comments - remove a list of comments by ids
#### Changed
- Added types to Ticket Model: 
  - create_step
- Added types to AccessRequest Model: 
  - sources
  - destinations
  - add_target
  - add_ar
  - add_group_change

## [2.3.11] - 2023-02-10
#### Added 
- Method: Scw.add_attachment() - Add file attchment to SecureChange
- Model: GenericIgnoredInterface
- Model: GenericInterfaceCustomer
- Model: GenericRoute
- Model: GenericVpn
- Model: JoinCloud
- Model: GenericTransparentFirewall
- Model: GenericIgnoredInterface
- Model: GenericInterfaceCustomer
- Method: St.add_generic_route() - Add Generic Route
- Method: St.add_generic_routes() - Add multiple Generic Routes
- Method: St.get_generic_route() - Get Generic Route by id
- Method: St.get_generic_rotues() - Get Generic Routes
- Method: St.update_generic_route() - Update Generic Route
- Method: St.update_generic_routes() - Update Multiple Generic Routes
- Method: St.delete_generic_route() - Delete Generic Route by id 
- Method: St.delete_generic_routes() - Delete Generic Routes by device
- Method: St.add_generic_vpn() - Add Generic VPN
- Method: St.add_generic_vpns()  - Add Multiple Generic VPN
- Method: St.get_generic_vpn() - Get Generic VPN by id
- Method: St.get_generic_vpns() - Get Generic VPN by device
- Method: St.update_generic_vpn() - Update Generic VPN by id
- Method: St.update_generic_vpns() - Update Generic VPN by device
- Method: St.delete_generic_vpn() - Delete Generic VPN by id
- Method: St.delete_generic_vpns() - Delete Generic VPN by device
- Method: St.add_generic_transparent_firewalls() - Add Generic Transparent Firewalls
- Method: St.get_generic_transparent_firewalls() - Get Generic Transparent Firewalls by device
- Method: St.update_generic_transparent_firewalls() - Update Generic Transparent Firewalls
- Method: St.delete_generic_transparent_firewall() - Delete Transparent Firewall by id
- Method: St.add_generic_ignored_interfaces() - Add ignored interfaces
- Method: St.get_generic_ignored_interfaces() - Get ignored interfaces by device
- Method: St.delete_generic_ignored_interfaces() - Delete ignored interface by device
- Method: St.add_generic_interface_customer()  - Add Generic Interface Customer Tag
- Method: St.add_generic_interface_customers() - Add Multiple Generic Interface Customer Tags
- Method: St.get_generic_interface_customer() - Get Interface Customer Tag by device
- Method: St.get_generic_interface_customers() = Get Interface Customer Tags by device
- Method: St.update_generic_interface_customer()
- Method: St.update_generic_interface_customers()
- Method: St.delete_generic_interface_customer()
- Method: St.delete_generic_interface_customers()
- Method: St.add_join_cloud() - Add join cloud
- Method: St.get_join_cloud() - Get join clouds by id
- Method: St.update_join_cloud() - Update join cloud
- Method: St.delete_join_cloud() - Deletee join cloud
#### Fixed
- BUGFIX: Correctly handle payloads for updated to RecordSets

## [2.3.10] - 2022-10-31
#### Added 
- Method: Scw.get_attachment() - Get attachment from SecureChange by file_id
- Method: St.add_generic_interface() - Add Generic Interface
- Method: St.add_generic_interfaces() - Add Multiple Generic Interfaces
- Method: St.get_generic_interface() - Get Generic Interface by id
- Method: St.get_generic_interfaces() - Get all generic interfaces by device
- Method: St.update_generic_interface() - Update generic interface by id
- Method: St.update_generic_interfaces() 
- Method: St.delete_generic_interface() - Delete generic Interface by id
- Method: St.delete_generic_interfaces()) - Delete generic Interfaces by device
- Model: Ticket.Attachment
- Model: GenericInterface

## [2.3.9] - 2022-10-26
### Added
- Additional test data and tests
- Tox configuration for testing
### Fixed
- BUGFIX: Fix duplicate target issue for Fortimanager when using multiple policies
- BUGFIX: Handle miissing singleServiceDTO.class_name for some Aur object results
- BUGFIX: Correct model for bindable objects
- BUGFIX: Correct issue with policies when device is ASA

## [2.3.8] - 2022-08-03
### API Changes
- Adds `AnyNetworkObject` mapping for SecureChange network objects.

## [2.3.7] - 2022-08-03
### API Changes
- Adds `HostNetworkObjectWithInterfaces` mapping for SecureChange network objects.

## [2.3.6] - 2022-08-03
### Fixes
- Fixes mismapped `Instruction.sources` and `Instruction.destinations`

## [2.3.5] - 2022-08-02
### API Changes
- Adds an `AnyService` mapping for service objects in `SlimRule`.
- Adds `comment`, `version_id`, `referenced`, `type_on_device`, `negate`, and `match_for_any` to `ServiceObject`

## [2.3.4] - 2022-08-02
### API Changes
- Adds a CloneServerPolicyRequest mapping to pytos2.securechange.fields
- Changes mapping type for `ServerDecommissionRequest.servers` from `IPObject` to `Object`

## [2.3.3] - 2022-08-01
### Fixes
- Changes mapping type for `ServerDecommissionRequest.servers` from `IPObject` to `Object`
- Updates cache when user not found in Scw.get_user(...)
- Handles "localuser" XSI type properly.
### API Changes
- Re-type several fields in SCWParty and SCWUser.
- Adds update_cache: bool to Scw.get_user(...)

## [2.3.2] - 2022-07-29
### Fixes
- Moves instruction mappings around.

## [2.3.1] - 2022-07-12
### Fixes
- Combines designer.Rule and rule.SlimRule
### API Changes
- Deprecates `SlimRule.source_networks` in favor of `SlimRule.source_objects`
- Deprecates `SlimRule.destination_networks` in favor of `SlimRule.destination_objects`
- Deprecates `SlimRule.destination_services` in favor of `SlimRule.services`
- Deprecates `designer.Rule`

## [2.3.0] - 2022-07-08
### Fixes
- Adds missing fields to SlimRule mapping
### API Changes
- Adds `TicketHistory` mappings

## [2.3.0] - 2022-08-11
### Added
- Added license
- Documentation updates
### Changed
- BUGFIX: Desginer/Verifier syntax error.

## [2.2.1] - 2021-12-23
- First public release!
