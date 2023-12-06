class Env:
    _path = '.env'
    _data = {}

    def __init__(self, path='.env'):
        self._path = path
        self.safeLoad()

    def create(self, path: str, file: str):
        self._path = path + '/' + file
        return self

    def safeLoad(self):
        self.__read()

    def get(self, key: str, default=None) -> any:
        if key in self._data:
            value = self._data[key]
            if type(value) == bool:
                return value

            if value == 'null' or (type(value) == 'str' and len(value) == 0):
                return default

            return self._data[key]
        return default

    def set(self, key, default):
        self._data[key] = default

    def has(self, key):
        return key in self._data

    def all(self):
        return self._data

    def dump(self):
        print(self._data)

    def __read(self):
        with open(self._path, 'r') as file:
            for line in file.readlines():
                line = line.strip()

                # ignore comment line and blank/bad line
                if line.startswith('#') or '=' not in line:
                    continue

                self.__read_line(line)

    def __read_line(self, line):
        # find second quote mark
        quote_delimit = max(line.find("'", line.find("'") + 1), line.find('"', line.rfind('"')) + 1)

        # find comment at end of line
        comment_delimit = line.find('#', quote_delimit)

        # remove comment if exist at end of line
        if comment_delimit >= 0:
            line = line[:comment_delimit]

        key, value = map(lambda x: x.strip().strip("'").strip('"'), line.split('=', 1))

        # ignore bad key
        if len(key) == 0:
            return

        self._data[key] = self._get(value)

    def _get(self, value, typeName='int'):
        if typeName == 'int':
            try:
                return int(value)
            except:
                return self._get(value, 'float')

        if typeName == 'float':
            try:
                return float(value)
            except:
                return self._get(value, 'bool')

        if typeName == 'bool' and (value == 'True' or value == 'False'):
            if value == 'True':
                return True
            if value == 'False':
                return False

        return value
