from cement.core.controller import CementBaseController

VERSION = '2.2.5'

BANNER = """
QL Dedicated Server Manager v%s
Copyright (c) 2015 Piotr Rzeczkowski
https://github.com/rzeka/QLDS-Manager
""" % VERSION


class VersionController(CementBaseController):
    class Meta:
        label = 'version'
        description = 'Version command'
        arguments = [
            (['-v', '--version'], dict(action='version', version=BANNER)),
        ]
