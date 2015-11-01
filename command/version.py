from cement.core.controller import CementBaseController

VERSION = '2.0.1-dev'

BANNER = """
QL Dedicated Server Manager v%s
Copyright (c) 2015 Piotr Rzeczkowski
""" % VERSION

class VersionController(CementBaseController):
    class Meta:
        label = 'version'
        description = 'Version command :)'
        arguments = [
            (['-v', '--version'], dict(action='version', version=BANNER)),
        ]
