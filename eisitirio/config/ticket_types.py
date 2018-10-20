# coding: utf-8
"""Configuration of available ticket types for the system."""

from __future__ import unicode_literals

from eisitirio.helpers import ticket_type
# from eisitirio.logic.custom_logic import ticket_logic

# The default ticket type must count towards the guest limit, as it is the
# ticket type assigned to people on the waiting list.
DEFAULT_TICKET_TYPE = ticket_type.TicketType("Standard", "standard", 1800, 2,
                                             -1, True,
                                             True)#ticket_logic.can_buy_standard)

TICKET_TYPES = [
    ticket_type.TicketType("OUSS Member (Early Bird)", "early_member", 1400, 1, 5,
                           True, True),
    ticket_type.TicketType("Standard (Early Bird)", "early_standard", 1700, 1, 5,
                           True, True),
    ticket_type.TicketType("OUSS Member", "member", 1500, 1, -1,
                           True, True),
    ticket_type.TicketType("OUSS Comittee", "comittee", 0, 1, -1,
                           True, True),
    ticket_type.TicketType("OUSS Comittee", "cash", 0, -1, -1,
                           True, True),
    # ticket_type.TicketType("OUSS Extended Comittee", "extended_comittee", 2000, 1, -1, True,
    #                        True),
    # ticket_type.TicketType("Artist", "artist", 0, 1, -1,
    #                        True, lambda _, __=False: False),
    DEFAULT_TICKET_TYPE,
]

TICKET_TYPES_BY_SLUG = {
    ticket_type.slug: ticket_type
    for ticket_type in TICKET_TYPES
}

GUEST_TYPE_SLUGS = [
    t_type.slug for t_type in TICKET_TYPES if t_type.counts_towards_guest_limit
]


# REFERENCE
#
# _TicketType = collections.namedtuple(
#     "TicketType",
#     [
#         "name",
#         "slug",
#         "price",
#         "limit_per_person",
#         "total_limit",
#         "counts_towards_guest_limit",
#         "can_buy_",
#     ]
# )
