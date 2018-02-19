# coding: utf-8
"""Configuration of available ticket types for the system."""

from __future__ import unicode_literals

from eisitirio.helpers import ticket_type
# from eisitirio.logic.custom_logic import ticket_logic

# The default ticket type must count towards the guest limit, as it is the
# ticket type assigned to people on the waiting list.
DEFAULT_TICKET_TYPE = ticket_type.TicketType("Standard", "standard", 9900, -1,
                                             -1, True,
                                             True)#ticket_logic.can_buy_standard)

TICKET_TYPES = [
    ticket_type.TicketType("Keblite", "keblite", 8900, 1, -1, True,
                           True),#ticket_logic.can_buy_keblite),
    ticket_type.TicketType("Keble Graduand", "keble_graduand", 9400, 1, -1,
                           True, True),#ticket_logic.can_buy_keble_graduand),
    ticket_type.TicketType("Keble Staff", "keble_staff", 4900, -1, -1, True,
                           True),  #ticket_logic.can_buy_keble_staff),
    DEFAULT_TICKET_TYPE,
    ticket_type.TicketType("Committee", "committee", 0, -1, -1, False,
                           lambda _, __=False: False),
    ticket_type.TicketType("Committee Guest", "committee_guest", 0, -1, -1,
                           True, lambda _, __=False: False),
    ticket_type.TicketType("Entz", "entz", 0, -1, -1, False,
                           lambda _, __=False: False),
    ticket_type.TicketType("Employee", "employee", 0, -1, -1, False,
                           lambda _, __=False: False),
]

TICKET_TYPES_BY_SLUG = {
    ticket_type.slug: ticket_type
    for ticket_type in TICKET_TYPES
}

GUEST_TYPE_SLUGS = [
    t_type.slug for t_type in TICKET_TYPES if t_type.counts_towards_guest_limit
]
