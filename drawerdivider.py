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
import pathlib

class HorzLine():
    def __init__(self, x1, y1, x2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2

class VertLine():
    def __init__(self, x1, y1, y2):
        self.x1 = x1
        self.y1 = y1
        self.y2 = y2

class DrawerDivider(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--depth", type=float, default=2,
                          help="Height/depth of the drawer the dividers are")
        pars.add_argument("--thickness", type=float, default=2.0,
                          help="Material thickness to be laser cut")
        pars.add_argument("--units", help="Inches or mm")

    def effect(self):
        with open(str(pathlib.Path().absolute()) + r'\test.txt', 'w') as f:
            for elem in self.svg.get_selected_or_all(inkex.PathElement):
                path = elem.path #.to_absolute()
                if len(path) != 1:
                    # warning: can only process singular, simple paths
                    pass
                else:
                    # Classify path as horz or vert, ignore others
                    for cp in path.control_points:
                        f.write(str(cp) + '\n')
                
if __name__ == '__main__':
    DrawerDivider().run()
