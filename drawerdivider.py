#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2020 Nathan Armentrout, nrarmen@gmail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import inkex
from inkex.paths import Line, Path

class DrawerDivider(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--depth", type=float, default=2,
                          help="Height/depth of the drawer the dividers are")
        pars.add_argument("--thickness", type=float, default=2.0,
                          help="Material thickness to be laser cut")
        pars.add_argument("--units", help="Inches or mm")

    def effect(self):
        with open(r'C:\Users\nrarm\Desktop\test.txt', 'w') as f:
            for node in self.svg.get_selected(inkex.PathElement):
                path = node.path #.to_absolute()
                #for cmd_proxy in path.proxy_iterator():  # type: inkex.Path.PathCommandProxy
                #    prev = cmd_proxy.previous_end_point
                #    end = cmd_proxy.end_point
                #for line in lines:
                f.write(str(path) + '\n')
                
if __name__ == '__main__':
    DrawerDivider().run()
