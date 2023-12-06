from pythoniq.framework.illuminate.support.traits.macroable import Macroable
import re


def Stringable(*args):
    from pythoniq.framework.illuminate.support.stringable import Stringable as StringableClass
    return StringableClass(*args)


class Str(Macroable):
    # The cache of snake-cased words.
    _snakeCache: dict = {}

    # The cache of camel-cased words.
    _camelCache: dict = {}

    # The cache of studly-cased words.
    _studlyCache: dict = {}

    # The callback that should be used to generate UUIDs.
    _uuidFactory: callable = None

    # The callback that should be used to generate random strings.
    _randomStringFactory: callable = None

    # Get a new stringable object from the given string.
    @staticmethod
    def of(string: str | None = None) -> Stringable:
        return Stringable(string)

    # Return the remainder of a string after the first occurrence of a given value.
    @staticmethod
    def after(subject: str, search: str) -> str:
        return '' if search == '' else subject.partition(search)[2]

    # Return the remainder of a string after the last occurrence of a given value.
    @staticmethod
    def afterLast(subject: str, search: str) -> str:
        if search == '':
            return subject

        pos = subject.rfind(search)

        if pos == -1:
            return subject

        return subject[pos + len(search):]

    # Transliterate a UTF-8 value to ASCII.
    @staticmethod
    def ascii(value: str, language='en') -> str:
        raise NotImplementedError

    # Transliterate a string to its closest ASCII representation.
    @staticmethod
    def transliterate(string: str, unknown: str | None = '?', strict: bool = False) -> str:
        raise NotImplementedError

    # Get the portion of a string before the first occurrence of a given value.
    @staticmethod
    def before(subject: str, search: str) -> str:
        return '' if search == '' else subject.partition(search)[0]

    # Get the portion of a string before the last occurrence of a given value.
    @staticmethod
    def beforeLast(subject: str, search: str) -> str:
        if search == '':
            return subject

        pos = subject.rfind(search)

        if pos == -1:
            return subject

        return subject[:pos]

    # Get the portion of a string between two given values.
    @staticmethod
    def between(subject: str, from_: str, to: str) -> str:
        if from_ == '' or to == '':
            return subject

        return Str.beforeLast(Str.after(subject, from_), to)

    # Get the smallest possible portion of a string between two given values.
    @staticmethod
    def betweenFirst(subject: str, from_: str, to: str) -> str:
        if from_ == '' or to == '':
            return subject

        return Str.before(Str.after(subject, from_), to)

    # Convert a value to camel case.
    @staticmethod
    def camel(value: str) -> str:
        if value in Str._camelCache:
            return Str._camelCache[value]

        value = str(value)

        Str._camelCache[value] = Str.lcfirst(Str.studly(value))
        return Str._camelCache[value]

    # Get the character at the specified index.
    @staticmethod
    def charAt(string: str, index: int) -> str | bool:
        length = len(string)

        if index < 0 or index >= length:
            return False

        return string[index]

    # Determine if a given string contains a given substring.
    @staticmethod
    def contains(haystack: str, needles: str | list, ignoreCase=False) -> bool:
        if ignoreCase:
            haystack = haystack.lower()

        if not isinstance(needles, list):
            needles = [needles]

        for needle in needles:
            if ignoreCase:
                needle = needle.lower()

            if needle != '' and needle in haystack:
                return True

        return False

    # Determine if a given string contains all array values.
    @staticmethod
    def containsAll(haystack: str, needles: str | list, ignoreCase=False) -> bool:
        for needle in needles:
            if not Str.contains(haystack, needle, ignoreCase):
                return False

        return True

    # Determine if a given string ends with a given substring.
    @staticmethod
    def endsWith(haystack: str, needles: str | list) -> bool:
        if not isinstance(needles, list):
            needles = [needles]

        for needle in needles:
            if str(needle) != '' and haystack.endswith(str(needle)):
                return True

        return False

    # Extracts an excerpt from text that matches the first instance of a phrase.
    @staticmethod
    def excerpt(text: str, phrase: str = '', options: dict = {}) -> str | bool:
        radius = options['radius'] if 'radius' in options else 100
        omission = options['omission'] if 'omission' in options else '...'

        raise NotImplementedError

    # Cap a string with a single instance of a given value.
    @staticmethod
    def finish(value: str, cap: str) -> str:
        if not Str.endsWith(value, cap):
            value += cap

        return value

    # Wrap the string with the given strings.
    @staticmethod
    def wrap(value: str, before: str, after: str = '') -> str:
        return before + value + (after or before)

    # Determine if a given string matches a given pattern.
    @staticmethod
    def is_(pattern: str, value: str) -> bool:
        value = str(value)

        pattern = [pattern]

        for pattern in pattern:
            pattern = str(pattern)

            # If the given value is an exact match we can of course return true right
            # from the beginning. Otherwise, we will translate asterisks and do an
            # actual pattern match against the two strings to see if they match.
            if pattern == value:
                return True

            pattern = pattern.replace('#', '\\#')

            # Asterisks are translated into zero-or-more regular expression wildcards
            # to make it convenient to check if the strings starts with the given
            # pattern such as "library/*", making any string check convenient.
            pattern = pattern.replace('*', '.*')

            if re.search(pattern, value):
                return True

        return False

    # Determine if a given string is 7 bit ASCII.
    @staticmethod
    def isAscii(value: str) -> bool:
        return all(ord(c) < 128 for c in value)

    # Determine if a given string is valid JSON.
    @staticmethod
    def isJson(value: str) -> bool:
        if not isinstance(value, str):
            return False

        try:
            import json
            json.loads(value)
        except ValueError:
            return False

        return True

    # Determine if a given string is a valid UUID.
    @staticmethod
    def isUuid(value: str) -> bool:
        if not isinstance(value, str):
            return False

        import uuid
        try:
            uuid.UUID(value)
        except ValueError:
            return False

        return True

    # Determine if a given string is a valid ULID.
    @staticmethod
    def isUlid(value: str) -> bool:
        raise NotImplementedError

    # Convert a string to kebab case.
    @staticmethod
    def kebab(value: str) -> str:
        return Str.snake(value, '-')

    # Return the length of the given string.
    @staticmethod
    def length(value: str, encoding: str | None = None) -> int:
        return len(value)

    # Limit the number of characters in a string.
    @staticmethod
    def limit(value: str, limit: int = 100, end: str = '...') -> str:
        if len(value) <= limit:
            return value

        return str(Str.of(value[:limit]).trim()) + end

    # Convert the given string to lower-case.
    @staticmethod
    def lower(value: str) -> str:
        return value.lower()

    # Limit the number of words in a string.
    @staticmethod
    def words(value: str, words: int = 100, end: str = '...') -> str:
        matches = re.findall(r'\/^\s*+(?:\S++\s*+){1,' + str(words) + '}/u', value)

        if len(matches) == 0 or Str.length(value) == len(matches[0]):
            return value

        return Str.rtrim(matches[0] + end)

    # Converts GitHub flavored Markdown into HTML.
    @staticmethod
    def markdown(string: str, options=[]) -> str:
        raise NotImplementedError

    # Converts inline Markdown into HTML.
    @staticmethod
    def inlineMarkdown(string: str, options=[]) -> str:
        raise NotImplementedError

    # Masks a portion of a string with a repeated character.
    @staticmethod
    def mask(string: str, character: str, index: int, length: int = None, encoding='UTF-8') -> str:
        if character == '':
            return string

        segment = Str.substr(string, index, length, encoding)

        if segment == '':
            return string

        strlen = Str.length(string, encoding)
        startIndex = index

        if index < 0:
            startIndex = index < -strlen and 0 or strlen + index

        start = Str.substr(string, 0, startIndex, encoding)
        segmentLength = Str.length(segment, encoding)
        end = Str.substr(string, startIndex + segmentLength)

        return start + Str.repeat(Str.substr(character, 0, 1, encoding), segmentLength) + end

    # Get the string matching the given pattern.
    @staticmethod
    def match(pattern: str, subject: str) -> str:
        matches = re.search(pattern, subject)

        if matches is None:
            return ''

        return subject[matches.start():matches.end()]

    # Determine if a given string matches a given pattern.
    @staticmethod
    def isMatch(pattern: str | list, value: str) -> bool:
        value = str(value)

        if not isinstance(pattern, list):
            pattern = [pattern]

        for p in pattern:
            p = str(p)

            if Str.match(p, value):
                return True

        return False

    # Get the string matching the given pattern.
    @staticmethod
    def matchAll(pattern: str, subject: str) -> list:
        matches = re.findall(pattern, subject)

        if len(matches) == 0:
            return []

        return matches

    # Pad both sides of a string with another.
    @staticmethod
    def padBoth(value: str, length: int, pad: str = ' ') -> str:
        short = max(0, length - Str.length(value))

        import math
        shortLeft = math.floor(short / 2)
        shortRight = math.ceil(short / 2)

        return Str.repeat(pad, shortLeft) + value + Str.repeat(pad, shortRight)

    # Pad the left side of a string with another.
    @staticmethod
    def padLeft(value: str, length: int, pad: str = ' ') -> str:
        short = max(0, length - Str.length(value))

        return Str.substr(Str.repeat(pad, short), 0, short) + value

    # Pad the right side of a string with another.
    @staticmethod
    def padRight(value: str, length: int, pad: str = ' ') -> str:
        short = max(0, length - Str.length(value))

        return value + Str.repeat(pad, short)

    # Parse a Class[@]method style callback into class and method.
    @staticmethod
    def parseCallback(callback: str, default: callable = None) -> list:
        return Str.contains(callback, '@') and callback.split('@', 2) or [callback, default]

    # Get the plural form of an English word.
    @staticmethod
    def plural(value: str, count: int = 2) -> str:
        raise NotImplementedError

    # Pluralize the last word of an English, studly caps case string.
    @staticmethod
    def pluralStudly(value: str, count: int = 2) -> str:
        raise NotImplementedError

    # Generate a random, secure password.
    @staticmethod
    def password(length: int = 16, letters: bool = True, numbers: bool = True, symbols: bool = True,
                 spaces: bool = False) -> str:
        raise NotImplementedError

    # Generate a more truly "random" alpha-numeric string.
    @staticmethod
    def random(length: int = 16) -> str:
        import random
        if Str._randomStringFactory is None:
            string = ''

            while len(string) < length:
                size = length - len(string)
                string += Str.substr(str(random.random()), 0, size)

            return string

    # Set the callable that will be used to generate random strings.
    @staticmethod
    def createRandomStringsUsing(factory: callable = None) -> None:
        Str._randomStringFactory = factory

    # Set the sequence that will be used to generate random strings.
    @staticmethod
    def createRandomStringsUsingSequence(sequence: list, whenMissing: callable = None) -> None:
        raise NotImplementedError

    # Indicate that random strings should be created normally and not using a custom factory.
    @staticmethod
    def createRandomStringsNormally() -> None:
        raise NotImplementedError

    # Repeat the given string.
    @staticmethod
    def repeat(value: str, times: int) -> str:
        return value * times

    # Replace a given value in the string sequentially with an array.
    @staticmethod
    def replaceArray(search: str, replace: list, subject: str) -> str:
        if not isinstance(replace, list):
            replace = [replace]

        for value in replace:
            subject = subject.replace(search, value, 1)

        return subject

    # Replace the given value in the given string.
    @staticmethod
    def replace(search: str | list, replace: str | list, subject: str, caseSensitive: bool = True) -> str:
        if not isinstance(search, list):
            search = [search]

        if not isinstance(replace, list):
            replace = [replace]

        if len(search) == len(replace):
            for i in range(len(search)):
                subject = subject.replace(search[i], replace[i])
        elif len(search) > 1 and len(replace) == 1:
            for i in range(len(search)):
                subject = subject.replace(search[i], replace[0])
        elif len(search) == 1 and len(replace) > 0:
            for i in range(len(replace)):
                subject = subject.replace(search[0], replace[i])

        return subject

    # Replace the first occurrence of a given value in the string.
    @staticmethod
    def replaceFirst(search: str, replace: str, subject: str) -> str:
        search = str(search)

        if search == '':
            return subject

        position = subject.find(search)

        if position == -1:
            return subject

        return subject[:position] + str(replace) + subject[position + len(search):]

    # Replace the last occurrence of a given value in the string.
    @staticmethod
    def replaceLast(search: str, replace: str, subject: str) -> str:
        search = str(search)

        if search == '':
            return subject

        position = subject.rfind(search)

        if position == -1:
            return subject

        return subject[:position] + str(replace) + subject[position + len(search):]

    # Remove any occurrence of the given string in the subject.
    @staticmethod
    def remove(search: str | list, subject: str, caseSensitive: bool = True) -> str:
        if not isinstance(search, list):
            search = [search]

        return Str.replace(search, '', subject, caseSensitive)

    # Reverse the given string.
    @staticmethod
    def reverse(string: str) -> str:
        return string[::-1]

    # Begin a string with a single instance of a given value.
    @staticmethod
    def start(value: str, prefix: str) -> str:
        if not Str.startsWith(value, prefix):
            value = prefix + value

        return value

    # Convert the given string to upper-case.
    @staticmethod
    def upper(value: str) -> str:
        return value.upper()

    # Convert the given string to title case.
    @staticmethod
    def title(value: str) -> str:
        return ' '.join(map(Str.ucfirst, Str.of(value).explode(' ')))

    # Convert the given string to title case for each word.
    @staticmethod
    def headline(value: str) -> str:
        parts = value.split(' ')

        if len(parts) > 1:
            parts = map(Str.title, parts)
        else:
            parts = map(Str.title, Str.ucsplit(''.join(parts)))

        collapsed = Str.replace(['-', '_', ' '], '_', '_'.join(parts))

        collapsed = list(filter(lambda x: x != '', collapsed.split('_')))
        collapsed = ' '.join(collapsed)

        return collapsed

    # Get the singular form of an English word.
    @staticmethod
    def singular(value: str) -> str:
        raise NotImplementedError

    # Generate a URL friendly "slug" from a given string.
    @staticmethod
    def slug(title: str, separator: str = '-', language: str | None = 'en', dictionary: dict = {'@': 'at'}) -> str:
        raise NotImplementedError
        title = language and Str.ascii(title, language) or title

        # Convert all dashes/underscores into separator
        flip = separator == '-' and '_' or '-'

        title = title.replace(flip, separator)

    # Convert a string to snake case.
    def snake(value: str, delimiter: str = '_') -> str:
        key = value

        if key in Str._snakeCache:
            return Str._snakeCache[key]

        if not value.islower():
            value = re.sub(r'(.)([A-Z])', r'\1' + delimiter + r'\2', value)

        return value.lower()

    # Remove all "extra" blank space from the given string.
    @staticmethod
    def squish(string: str) -> str:
        return re.sub(r'\s+', ' ', string).strip()

    # Determine if a given string starts with a given substring.
    @staticmethod
    def startsWith(string: str, needles: str | list) -> bool:
        if not isinstance(needles, list):
            needles = [needles]

        for needle in needles:
            if string.startswith(needle):
                return True

        return False

    @staticmethod
    def capitalize(string: str) -> str:
        return string[0].upper() + string[1:]

    # Convert a value to studly caps case.
    @staticmethod
    def studly(value: str) -> str:
        key = value

        if key in Str._studlyCache:
            return Str._studlyCache[key]

        word = Str.replace(['-', '_'], ' ', value)

        word = ''.join([Str.capitalize(w) for w in word.split(' ')])

        return word

    # Returns the portion of the string specified by the start and length parameters.
    @staticmethod
    def substr(string: str, start: int, length: int = None, encoding: str | None = None) -> str:
        if length is None or length == 0:
            return string[start:Str.length(string)]
        elif start < 0:
            length = Str.length(string) - length
            return string[start:Str.length(string) - length]
        elif length > 0:
            return string[start:start + length]

        return string[start:length]

    # Returns the number of substring occurrences.
    @staticmethod
    def substrCount(haystack: str, needle: str, offset: int = 0, length: int = None) -> int:
        if length is None:
            length = Str.length(haystack)

        return haystack[offset:length].count(needle)

    # Replace text within a portion of a string.
    @staticmethod
    def substrReplace(string: str, replace: str | list[str], offset: int = 0, length: int = None):
        if isinstance(replace, list):
            replace = replace[0]

        if length is None:
            length = Str.length(string)

        return string[:offset] + replace + string[offset + length:]

    # Swap multiple keywords in a string with other keywords.
    @staticmethod
    def swap(_map: dict, subject: str) -> str:
        for key, value in _map.items():
            subject = subject.replace(key, value)
        return subject

    # Make a string's first character lowercase.
    @staticmethod
    def lcfirst(string: str) -> str:
        return Str.lower(Str.substr(string, 0, 1)) + Str.substr(string, 1)

    # Make a string's first character uppercase.
    @staticmethod
    def ucfirst(string: str) -> str:
        return Str.upper(Str.substr(string, 0, 1)) + Str.substr(string, 1)

    # Split a string into pieces by uppercase characters.
    @staticmethod
    def ucsplit(value: str) -> list[str]:
        return re.sub('([a-z])([A-Z])', r'\1 \2', value).split()

    # Get the number of words a string contains.
    @staticmethod
    def wordCount(string: str, characters: str = None) -> int:
        if Str.squish(string) == '' or Str.squish(string) == ' ':
            return 0
        return sum(1 for c in Str.squish(string) if c in ' \t\n') + 1

    # Generate a UUID (version 4).
    @staticmethod
    def uuid() -> str:
        if Str._uuidFactory is None:
            import uuid
            return str(uuid.uuid4())

        return Str._uuidFactory()

    # Generate a time-ordered UUID (version 4).
    @staticmethod
    def orderedUuid() -> str:
        raise NotImplementedError

    # Set the sequence that will be used to generate UUIDs.
    @staticmethod
    def createUuidsUsing(factory: callable = None) -> None:
        Str._uuidFactory = factory

    # Set the sequence that will be used to generate UUIDs.
    @staticmethod
    def createUuidsUsingSequence(sequence: list, whenMissing: callable = None) -> None:
        raise NotImplementedError

    # Always return the same UUID when generating new UUIDs.
    def freezeUuid(callback: callable = None) -> None:
        uuid = Str.uuid()

        Str.createUuidsUsing(lambda: uuid)

        if callback is None:
            try:
                callback(uuid)
            finally:
                Str.createUuidsNormally()

        return uuid

    # Indicate that UUIDs should be created normally and not using a custom factory.
    @staticmethod
    def createUuidsNormally() -> None:
        Str._uuidFactory = None

    # Generate a ULID.
    @staticmethod
    def ulid() -> str:
        raise NotImplementedError

    # Extract the file name from a file path.
    @staticmethod
    def name(string: str) -> str:
        return Str.of(string).basename().beforeLast('.' + Str.extension(string)).value()

    # Extract the file extension from a file path.
    @staticmethod
    def extension(string: str) -> str:
        return string.split('.')[-1]

    # Get the trailing name component of the path.
    @staticmethod
    def basename(string: str, suffix: str = "") -> str:
        if string == '':
            return string

        value = string.rsplit('/')
        if len(value) == 1:
            return value[0]

        value = value[len(value) - 1]
        if suffix != '':
            return value.removesuffix(suffix)

        return value

    # Get the parent directory's path.
    @staticmethod
    def dirname(string: str, level: int = 1):
        if string == '':
            return string

        value = string.rsplit('/')

        for _ in range(level):
            del value[len(value) - 1:]

        if len(value) == 0:
            return '.'

        return '/'.join(value)

    # Remove all strings from the casing caches.
    @staticmethod
    def flushCaches() -> None:
        Str._snakeCache = {}
        Str._camelCache = {}
        Str._studlyCache = {}
