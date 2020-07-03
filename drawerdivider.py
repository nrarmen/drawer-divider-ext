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

class Divider():
    height = 0.0
    thickness = 0.0
    def __init__(self, len):
        self.length = len
        self.notches = []

    def __str__(self):
        return 'Divider ' + str(self.length) + ' units long with notches at: ' + str(self.notches)

    @property
    def path_string(self):
        result = 'M 0.0 0.0 '
        for n in self.notches:
            result += 'H {:.4f} '.format(n - (self.thickness / 2))
            result += 'V {:.4f} '.format(self.height / 2)
            result += 'H {:.4f} '.format(n + (self.thickness / 2))
            result += 'V 0.0 '
        result += 'H {:.4f} '.format(self.length)
        result += 'V {:.4f} '.format(self.height)
        result += 'H 0.0 Z '
        return result

def lines_intersect(hp, vp):
    #assume absolute
    hx1 = hp[0].args[0]
    hy1 = hp[0].args[1]
    hx2 = hp[1].args[0]

    vx1 = vp[0].args[0]
    vy1 = vp[0].args[1]
    vy2 = vp[1].args[0]

    return (vy1 <= hy1 <= vy2 or vy2 <= hy1 <= vy1) and (hx1 <= vx1 <= hx2 or hx2 <= vx1 <= hx1)

class DrawerDivider(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--depth", type=float, default=2,
                          help="Height/depth of the drawer the dividers are")
        pars.add_argument("--thickness", type=float, default=2.0,
                          help="Material thickness to be laser cut")
        pars.add_argument("--units", help="Inches or mm")

    def effect(self):
        # Classify path as horz or vert, ignore others
        horzPaths = []
        vertPaths = []
        for elem in self.svg.get_selected_or_all(inkex.PathElement):
            path = elem.path.to_absolute()
            if len(path) != 2:
                # warning: can only process singular, simple paths
                pass
            else:
                if path[1].letter == 'H':
                    horzPaths.append(path)
                elif path[1].letter == 'V':
                    vertPaths.append(path)
                else:
                    #warning: can only process horizontal or vertical paths
                    pass
        
        line_style = {
            'stroke': '#FF0000', 
            'fill': 'none',
            'stroke-width': str(self.svg.unittouu('{:0.2f}mm'.format(self.options.thickness * 0.1)))
        }

        # Create Divider objects used to generate new divider paths
        Divider.height = self.options.depth
        Divider.thickness = self.options.thickness
        dividers = []
        for hp in horzPaths:
            hx1 = hp[0].args[0]
            hx2 = hp[1].args[0]
            d = Divider(abs(hx1 - hx2))
            for vp in vertPaths:
                if lines_intersect(hp, vp):
                    vx1 = vp[0].args[0]
                    d.notches.append(vx1 - min(hx1, hx2))
                d.notches.sort()
            dividers.append(d)
        
        for vp in vertPaths:
            vy1 = vp[0].args[1]
            vy2 = vp[1].args[0]
            d = Divider(abs(vy1 - vy2))
            for hp in horzPaths:
                if lines_intersect(hp, vp):
                    hy1 = hp[0].args[1]
                    d.notches.append(hy1 - min(vy1, vy2))
                d.notches.sort()
            dividers.append(d)

        # Render Dividers
        for d in dividers:
            index = dividers.index(d)
            pe = self.svg.get_current_layer().add(inkex.PathElement(id='Divider ' + str(index)))
            pe.set_path(Path(d.path_string).translate(0, (index * (d.height + d.thickness))).rotate(180))
            pe.style = line_style
                
if __name__ == '__main__':
    DrawerDivider().run()
