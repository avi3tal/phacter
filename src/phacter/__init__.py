# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import platform
import sys
import urllib
import httplib

from types import ModuleType

class Lazy(object):
    def __init__(self, func):
        self._func = func

    def __get__(self, obj, _=None):
        if obj is None:
            return self
        value = self._func()
        setattr(obj, self._func.func_name, value)
        return value

class Phacter(object):

    __version__ = '0.2.0'
    __license__ = 'GPLv2'
    __author__ = 'Dan Radez <dradez@redhat.com>'

    facts = ['kernel']
    platform_name = platform.system().lower()
    kernel = property(lambda self: self.platform_name)
    phacterversion = __version__

    def __init__(self):
        platform_imp = __import__('phacter', None, None, [self.platform_name])
        platform_obj = getattr(platform_imp, self.platform_name)

        for method in dir(platform_obj):
            if '__' not in method:
                call = getattr(platform_obj, method)
                if type(call) is not ModuleType:
                    setattr(self.__class__, method, Lazy(call))
                    self.facts.append(method)
        self.facts.sort()


if __name__ == 'phacter':
    sys.modules[__name__] = Phacter()