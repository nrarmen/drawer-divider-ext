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
from inkex.paths import Path

class Divider():

    height = 0.0
    thickness = 0.0

    def __init__(self, len: float):
        """! Constructor

            @param The total length of this drawer divider
        """
        self.length = len
        self.notches = []

    @property
    def path_string(self):
        """! Translates the parameters of the Divider into a string path Inkscape can interpret

            @return A string path Inkscape can interpret
        """

        # Start at 0,0
        result = 'M 0.0 0.0 '

        # Create each notch
        for n in self.notches:
            result += f'H {n - (self.thickness / 2):.4f} '
            result += f'V {self.height / 2:.4f} '
            result += f'H {n + (self.thickness / 2):.4f} '
            result += 'V 0.0 '

        # Finish the remaining length of the divider
        result += f'H {self.length:.4f} '

        # Go up for the divider height
        result += f'V {self.height:.4f} '

        # Go back to 0 and end the path
        result += 'H 0.0 Z '

        return result

def lines_intersect(horz_path, vert_path):
    """! Helper function to determine if given horizontal and vertical paths intersect

        Assumes the paths are in absolute coordinates.

        @param horz_path  Horizontal Inkscape PathElement
        @param vert_path  Vertical Inkscape PathElement

        @return True if paths intersect, else False
    """
    hx1 = horz_path[0].args[0]
    hy1 = horz_path[0].args[1]
    hx2 = horz_path[1].args[0]

    vx1 = vert_path[0].args[0]
    vy1 = vert_path[0].args[1]
    vy2 = vert_path[1].args[0]

    return (vy1 <= hy1 <= vy2 or vy2 <= hy1 <= vy1) and (hx1 <= vx1 <= hx2 or hx2 <= vx1 <= hx1)

class DrawerDivider(inkex.EffectExtension):

    def _find_horz_and_vert_paths(self):
        """! Iterates over every Inkscape path to find horizontal and vertial paths
        """
        self.horz_paths = []
        self.vert_paths = []
        for elem in self.svg.get_selected_or_all(inkex.PathElement):
            path = elem.path.to_absolute()
            if len(path) != 2:
                # Warning: can only process singular, simple paths; ignore this path
                pass
            else:
                if path[1].letter == 'H':
                    self.horz_paths.append(path)
                elif path[1].letter == 'V':
                    self.vert_paths.append(path)
                else:
                    # Warning: can only process horizontal or vertical paths; ignore this path
                    pass

    def _define_dividers(self):
        """! Creates Divider objects used to generate new divider paths
        """
        self.dividers = []

        # Set static Divider members
        Divider.height = self.options.depth
        Divider.thickness = self.options.thickness

        # For each horz divider, find intersecting vert dividers and note where notches should be
        for hp in self.horz_paths:
            hx1 = hp[0].args[0]
            hx2 = hp[1].args[0]
            d = Divider(abs(hx1 - hx2))
            for vp in self.vert_paths:
                if lines_intersect(hp, vp):
                    vx1 = vp[0].args[0]
                    d.notches.append(vx1 - min(hx1, hx2))
                d.notches.sort()
            self.dividers.append(d)
        
        # For each vert divider, find intersecting horz dividers and note where notches should be
        for vp in self.vert_paths:
            vy1 = vp[0].args[1]
            vy2 = vp[1].args[0]
            d = Divider(abs(vy1 - vy2))
            for hp in self.horz_paths:
                if lines_intersect(hp, vp):
                    hy1 = hp[0].args[1]
                    d.notches.append(hy1 - min(vy1, vy2))
                d.notches.sort()
            self.dividers.append(d)

    def _render_dividers(self):
        """! Renders the Divider objects into paths Inkscape can interpret
        """
        # Set the stroke properties
        line_style = {
            'stroke': '#FF0000', 
            'fill': 'none',
            'stroke-width': str(self.svg.unittouu('{:0.2f}mm'.format(self.options.thickness * 0.1)))
        }

        # Render dividers
        for d in self.dividers:
            index = self.dividers.index(d)
            pe = self.svg.get_current_layer().add(inkex.PathElement(id='Divider ' + str(index)))
            pe.set_path(Path(d.path_string).translate(0, (index * (d.height + d.thickness))).rotate(180))
            pe.style = line_style

    def add_arguments(self, pars):
        pars.add_argument("--depth", type=float, default=2,
                          help="Height/depth of the drawer the dividers")
        pars.add_argument("--thickness", type=float, default=2.0,
                          help="Material thickness to be laser cut")
        pars.add_argument("--units", help="Inches or mm")

    def effect(self):
        self._find_horz_and_vert_paths()
        self._define_dividers()
        self._render_dividers()       
                
if __name__ == '__main__':
    DrawerDivider().run()
