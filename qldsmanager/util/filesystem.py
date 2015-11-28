import os


class FSCheck:
    def __init__(self, filepath, name=None):
        if name is None:
            name = filepath

        self.filepath = os.path.expanduser(filepath)
        self.name = name

    def exists(self, error=True):
        if not os.path.exists(self.filepath):
            if error:
                print('%s executable doesn\'t exist. Install it first' % self.name)
                exit(32)
            else:
                return False

        return True

    def access(self, type_, error=True):
        if type_ in ['read', 'r']:
            access = os.R_OK
            access_human = 'read'
        elif type_ in ['write', 'w']:
            access = os.W_OK
            access_human = 'write'
        elif type_ in ['exec', 'x', 'execute']:
            access = os.X_OK
            access_human = 'exec'
        else:
            access = None
            access_human = None

        if access is None:
            raise AttributeError('Unknown access type')

        if not os.access(self.filepath, access):
            if error:
                print('No %s access to %s' % (access_human, self.name))
                exit(31)
            else:
                return False

        return True
