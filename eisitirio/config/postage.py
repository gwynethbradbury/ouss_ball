# coding: utf-8
"""Postage options."""

from __future__ import unicode_literals

from eisitirio.helpers import postage_option

NO_POSTAGE_OPTION = postage_option.PostageOption(
    'Collection',
    'collection',
    0,
    'Collect your tickets from OUSS at fixed times before the ball.',
    False
)

POSTAGE_OPTIONS = {
    option.slug: option
    for option in [
        NO_POSTAGE_OPTION,
        postage_option.PostageOption(
            '1st Class Post',
            '1st_class',
            380,
            'Have your tickets posted to you two weeks before the ball.',
            True
        ),
        postage_option.PostageOption(
            '2nd Class Post',
            '2nd_class',
            350,
            'Have your tickets posted to you two weeks before the ball.',
            True
        )
    ]
}

# Quick way to generate a JS array.
POSTAGE_OPTIONS_NEED_ADDRESS = [
    option.slug
    for option in POSTAGE_OPTIONS.values()
    if option.needs_address
]

GRADUAND_POSTAGE_OPTION = postage_option.PostageOption(
    'Tickets included in Graduand pack',
    'graduand',
    0,
    'Your tickets will be included in your Graduand pack.',
    False
)
