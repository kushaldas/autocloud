# -*- coding: utf-8 -*-
# Copyright (C) 2017 Red Hat, Inc.
#
# bugyou_plugins is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# bugyou_plugins is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# bugyou_plugins.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Sayan Chowdhury  <sayanchowdhury@fedoraproject.org>
#

from abc import ABCMeta, abstractmethod

import six

@six.add_metaclass(abc.ABCMeta)
class AutocloudBaseWorker():

    def system(self, cmd):
    """
    Runs the shell command provided to the method.

    Args:
        cmd (str): The command to execute.

    Returns:
        output, err, returncode (tuple): Retuns a tuple containing the output,
        error, returncode
    """
    ret = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    out, err = ret.communicate()
    returncode = ret.returncode
    return out, err, returncode


    @abstractmethod
    def handle_err():
        pass

    @abstractmethod
    def consume():

