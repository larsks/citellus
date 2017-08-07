#!/usr/bin/env python
# encoding: utf-8
#
# Description: Multiple Analysis Generic Unifier and Interpreter aka Magui
#              This program processes several snapshoot/sosreport files
#              and processes citellus output for combined issues via plugins
#              that search for specific plugin and data
#
# Copyright (C) 2017  Pablo Iranzo Gómez (Pablo.Iranzo@redhat.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import print_function

import argparse
import gettext
import logging
import os
import os.path
import pprint

import citellus

LOG = logging.getLogger('magui')

# Where are we?
maguidir = os.path.abspath(os.path.dirname(__file__))
localedir = os.path.join(maguidir, 'locale')

trad = gettext.translation('citellus', localedir, fallback=True)
_ = trad.ugettext


def show_logo():
    """
    Prints Magui Logo
    :return:
    """

    logo = "    _    ", \
           "  _( )_  Magui:", \
           " (_(ø)_) ",\
           "  /(_)   Multiple Analisis Generic Unifier and Interpreter", \
           " \|      ", \
           "  |/     " \

    print("\n".join(logo))


def parse_args():
    """
    Parses arguments on commandline
    :return: parsed arguments
    """
    description = _('Processes several generic archives/sosreports scripts in a uniform way, to interpret status that depend on several systems data')

    # Option parsing
    p = argparse.ArgumentParser("magui.py [arguments]", description=description)
    p.add_argument('-d', "--loglevel",
                   help=_("Set log level"),
                   default="info",
                   type=lambda x: x.upper(),
                   choices=["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"])
    p.add_argument('-p', "--pluginpath", dest="pluginpath",
                   help=_("Set path for Citellus plugin location if not default"),
                   action='append')
    p.add_argument('-m', "--mpath", dest="mpath",
                   help=_("Set path for Magui plugin location if not default"),
                   action='append')
    p.add_argument("-s", "--silent", dest="silent", help=_("Enable silent mode, only errors on tests written"),
                   default=False,
                   action='store_true')
    p.add_argument("-f", "--filter", dest="filter",
                   help=_("Only include Citellus plugins that contains in full path that substring"),
                   default=[],
                   action='append')
    p.add_argument("-mf", "--mfilter", dest="mfilter",
                   help=_("Only include Magui plugins that contains in full path that substring"),
                   default=False,
                   action='append')

    p.add_argument('sosreports', nargs='*')

    return p.parse_args()


def main():
    """
    Main code stub
    """
    options = parse_args()

    # Configure logging
    logging.basicConfig(level=options.loglevel)

    if not options.silent:
        show_logo()

    # Each argument in sosreport is a sosreport

    # Grab data from citellus for the sosreports provided
    results = {}
    for sosreport in options.sosreports:
        if not options.silent:
            print(_("Gathering analysis for %s") % sosreport)
        results[sosreport] = citellus.docitellus(live=False, path=sosreport, plugins=citellus.findplugins(filters=options.filter, folders=options.pluginpath))

    # Precreate multidimensional array
    grouped = {}
    plugins = []
    for sosreport in options.sosreports:
        plugins = []
        for plugin in results[sosreport]:
            plugins.append(plugin)
            grouped[plugin] = {}

    # Get commonpath for printing
    commonpath = citellus.commonpath(plugins)

    # Fill the data
    for sosreport in options.sosreports:
        plugins = 0
        for plugin in results[sosreport]:
            grouped[plugin][sosreport] = results[sosreport][plugin]['output']

    # We've now a matrix of grouped[plugin][sosreport] and then [text] [out] [err] [rc]

    # For now, let's only print plugins that have rc ! 0

    if options.silent:
        toprint = {}
        for plugin in grouped:
            pplug = 0
            for host in grouped[plugin]:
                if grouped[plugin][host]['rc'] != 0 and grouped[plugin][host]['rc'] != 2:
                    pplug = 1
            if pplug == 1:
                newplugin = plugin.replace(commonpath, '')
                toprint[newplugin] = {}
                for host in grouped[plugin]:
                    toprint[newplugin][host] = {}
                    toprint[newplugin][host] = grouped[plugin][host]
    else:
        toprint = grouped

    pprint.pprint(toprint, width=1)
    # We need to run our plugins against that data

    # TODO(iranzo): write code for processing plugins once decided what to use and process (rather than feding above data outputed to the full scripts)


if __name__ == "__main__":
    main()
