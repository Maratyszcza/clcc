# This file is part of clcc package and is licensed under the Simplified BSD license.
#    See LICENSE.rst for the full text of the license.


from __future__ import print_function, absolute_import
import sys


def message(text, function=None, cl_status=None):
	if function is None:
		print(message, file=sys.stderr)
	else:
		if cl_status is None:
			print("%s: %s failed" % (message, function), file=sys.stderr)
		else:
			print("%s: %s failed with error code %d" % (message, function, cl_status), file=sys.stderr)


def error(message, function=None, cl_status=None):
	message("Error: " + message, function, cl_status)
	sys.exit(1)


def warning(message, function=None, cl_status=None):
	message("Warning: " + message, function, cl_status)
