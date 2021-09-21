# -*- coding: utf-8 -*-
# synadm
# Copyright (C) 2021 Callum Brown
#
# synadm is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# synadm is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Registration token-related CLI commands
"""

import click
from click_option_group import optgroup, MutuallyExclusiveOptionGroup
from click_option_group import RequiredAnyOptionGroup

from synadm import cli


@cli.root.group()
def regtok():
    """ Manage registration tokens
    """


@regtok.command(name="list")
@click.option(
    "--valid/--invalid", "-v/-V", default=None, show_default=True,
    help="List only valid/invalid tokens.")
@click.option(
    "--datetime/--timestamp", "-d/-t", default=True,
    help="""Display expiry time in a human readable format, or as a unix
    timestamp in milliseconds.  [default: datetime].""")
@click.pass_obj
def regtok_list_cmd(helper, valid, datetime):
    """ List registration tokens
    """
    regtoks = helper.api.regtok_list(valid, datetime)
    if regtoks is None:
        click.echo("Registration tokens could not be fetched.")
        raise SystemExit(1)
    if "registration_tokens" not in regtoks:
        # Display error
        helper.output(regtoks)
    elif helper.output_format == "human":
        if regtoks["registration_tokens"] == []:
            click.echo("No registration tokens.")
        else:
            helper.output(regtoks["registration_tokens"])
    else:
        helper.output(regtoks)


@regtok.command(name="details")
@click.argument("token", type=str)
@click.option(
    "--datetime/--timestamp", "-d/-t", default=True,
    help="""Display expiry time in a human readable format, or as a unix
    timestamp in milliseconds.  [default: datetime].""")
@click.pass_obj
def regtok_details_cmd(helper, token, datetime):
    """ View details of the given token
    """
    regtok = helper.api.regtok_details(token, datetime)
    if regtok is None:
        click.echo("Registration token could not be fetched.")
        raise SystemExit(1)
    helper.output(regtok)


@regtok.command(name="new")
@click.option(
    "--token", "-n", type=str, default=None,
    help="""Set the registration token. The default is a random value
    generated by the server.""")
@click.option(
    "--length", "-l", type=int, default=16, show_default=True,
    help="""The length of the randomly generated token if the token is not
    specified.""")
@click.option(
    "--uses-allowed", "-u", type=int, default=None,
    help="""The number of times the token can be used to complete a
    registration before it becomes invalid.  [default: unlimited uses]""")
@click.option(
    "--expiry-ts", "-t", type=int, default=None,
    help="""The latest time the registration token is valid.
    Given as the number of milliseconds since 1970-01-01 00:00:00 UTC.
     [default: no expiry]""")
@click.option(
    "--expire-at", "-e", type=click.DateTime(), default=None,
    help="""The latest time the registration token is valid.
    See above for available date/time formats.  [default: no expiry]""")
@click.pass_obj
def regtok_new(helper, token, length, uses_allowed, expiry_ts, expire_at):
    """ Create a new registration token
    """
    regtok = helper.api.regtok_new(
        token, length, uses_allowed, expiry_ts, expire_at
    )
    if regtok is None:
        click.echo("Registration token could not be created.")
        raise SystemExit(1)
    helper.output(regtok)


@regtok.command(name="update")
@click.argument("token", type=str)
@click.option(
    "--uses-allowed", "-u", type=int, default=None,
    help="""The number of times the token can be used to complete a
    registration before it becomes invalid. Use -1 for an unlimited
    number of uses.  [default: unchanged]""")
@click.option(
    "--expiry-ts", "-t", type=int, default=None,
    help="""The latest time the registration token is valid.
    Given as the number of milliseconds since 1970-01-01 00:00:00 UTC.
    Use -1 for no expiration.  [default: unchanged]""")
@click.option(
    "--expire-at", "-e", type=click.DateTime(), default=None,
    help="""The latest time the registration token is valid.
    See above for available date/time formats.  [default: unchanged]""")
@click.pass_obj
def regtok_update(helper, token, uses_allowed, expiry_ts, expire_at):
    """ Update a registration token
    """
    regtok = helper.api.regtok_update(token, uses_allowed, expiry_ts, expire_at)
    if regtok is None:
        click.echo("Registration token could not be created.")
        raise SystemExit(1)
    helper.output(regtok)


@regtok.command(name="delete")
@click.argument("token", type=str)
@click.pass_obj
def regtok_delete(helper, token):
    """ Delete a registration token
    """
    response = helper.api.regtok_delete(token)
    if response is None:
        click.echo("Registration token could not be deleted.")
        raise SystemExit(1)
    if response == {}:
        click.echo("Registration token successfully deleted.")
    else:
        helper.output(response)