import argparse


LICENSE_TERMS = """
Copyright 2017-2019 Ippei Obayashi
Copyright 2017-2018 Hiraoka lab (AIMR, Tohoku Univ.)
Copyright 2018-2019 Topological Data Analysis Team (AIP, RIKEN)
Copyright 2019 National Institute of Advanced Industrial Science and Technology (AIST)


HomCloud is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

HomCloud is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with HomCloud.  If not, see <http://www.gnu.org/licenses/>.
"""


def add_argument_for_license(parser):
    parser.add_argument("--license", action=ShowLicense, nargs=0, help="show license and exit")


class ShowLicense(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(LICENSE_TERMS)
        exit(0)
