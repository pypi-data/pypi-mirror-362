# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Request service results."""

from invenio_records_resources.services.records.results import ExpandableField

from ..resolvers.registry import ResolverRegistry


class EntityResolverExpandableField(ExpandableField):
    """Expandable entity resolver field.

    It will use the Entity resolver registry to retrieve the service to
    use to fetch records and the fields to return when serializing
    the referenced record.
    """

    entity_proxy = None

    def ghost_record(self, value):
        """Return ghost representation of not resolved value."""
        return self.entity_proxy.ghost_record(value)

    def system_record(self):
        """Return the representation of a system user."""
        return self.entity_proxy.system_record()

    def get_value_service(self, value):
        """Return the value and the service via entity resolvers."""
        self.entity_proxy = ResolverRegistry.resolve_entity_proxy(value)
        v = self.entity_proxy._parse_ref_dict_id()
        _resolver = self.entity_proxy.get_resolver()
        service = _resolver.get_service()
        return v, service

    def pick(self, identity, resolved_rec):
        """Pick fields defined in the entity resolver."""
        return self.entity_proxy.pick_resolved_fields(identity, resolved_rec)
