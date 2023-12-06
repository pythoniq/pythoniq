from pythoniq.framework.illuminate.support.traits.macroable import Macroable
from pythoniq.framework.illuminate.support.str import Str
from pythoniq.framework.illuminate.support.traits.conditionable import Conditionable
from pythoniq.framework.illuminate.support.traits.tappable import Tappable


class Stringable(Conditionable, Macroable, Tappable):
    # The underlying string value.
    _value: str | None = None

    # Create a new stringable object.
    def __init__(self, value: str | None = None) -> None:
        self._value = str(value)

    # Return the remainder of a string after the first occurrence of a given value.
    def after(self, search: str):
        return Stringable(Str.after(self._value, search))

    # Return the remainder of a string after the last occurrence of a given value.
    def afterLast(self, search: str):
        return Stringable(Str.afterLast(self._value, search))

    # Append the given values to the string.
    def append(self, values: list | str):
        if not isinstance(values, list):
            values = [values]

        return Stringable(self._value + self._value.join(values))

    # Append a new line to the string.
    def newLine(self, count: int = 1):
        return Stringable(self._value + "\n" * int(count))

    # Transliterate a UTF-8 value to ASCII.
    def ascii(self, language: str = "en"):
        return Stringable(Str.ascii(self._value, language))

    # Get the trailing name component of the path.
    def basename(self, suffix: str = ""):
        return Stringable(Str.basename(self._value, suffix))

    # Get the character at the specified index.
    def charAt(self, index: int):
        return Stringable(Str.charAt(self._value, index))

    # Get the basename of the class path.
    def classBasename(self):
        # @todo
        raise NotImplementedError('The method "basename" is not implemented yet.')

    # Get the portion of a string before the first occurrence of a given value.
    def before(self, search: str):
        return Stringable(Str.before(self._value, search))

    # Get the portion of a string before the last occurrence of a given value.
    def beforeLast(self, search: str):
        return Stringable(Str.beforeLast(self._value, search))

    # Get the portion of a string between two given values.
    def between(self, _from: str, to: str):
        return Stringable(Str.between(self._value, _from, to))

    # Get the smallest possible portion of a string between two given values.
    def betweenFirst(self, _from: str, to: str):
        return Stringable(Str.betweenFirst(self._value, _from, to))

    # Convert a value to camel case.
    def camel(self):
        return Stringable(Str.camel(self._value))

    # Determine if a given string contains a given substring.
    def contains(self, needles: str | list, ignoreCase: bool = False) -> bool:
        return Str.contains(self._value, needles, ignoreCase)

    # Determine if a given string contains all array values.
    def containsAll(self, needles: list, ignoreCase: bool = False) -> bool:
        return Str.containsAll(self._value, needles, ignoreCase)

    # Get the parent directory's path.
    def dirname(self, level: int = 1):
        return Stringable(Str.dirname(self._value, level))

    # Determine if a given string ends with a given substring.
    def endsWith(self, needles: str | list) -> bool:
        return Str.endsWith(self._value, needles)

    # Determine if the string is an exact match with the given value.
    def exactly(self, value: str) -> bool:
        if isinstance(value, Stringable):
            value = value.toString()

        return self._value == value

    # Extracts an excerpt from text that matches the first instance of a phrase.
    def excerpt(self, phrase: str, options: dict = {}) -> str | None:
        return Str.excerpt(self._value, phrase, options)

    # Explode the string into an array.
    def explode(self, delimiter: str, limit: int = -1) -> list[str]:
        return self._value.split(delimiter, limit)

    # Split a string using a regular expression or by length.
    def split(self, pattern: str | int, limit: int = -1):
        # todo
        raise NotImplementedError('The method "split" is not implemented yet.')

    # Cap a string with a single instance of a given value.
    def finish(self, cap: str):
        return Stringable(Str.finish(self._value, cap))

    # Determine if a given string matches a given pattern.
    def is_(self, pattern: str) -> bool:
        return Str.is_(pattern, self._value)

    # Determine if a given string is 7 bit ASCII.
    def isAscii(self) -> bool:
        return Str.isAscii(self._value)

    # Determine if a given string is valid JSON.
    def isJson(self) -> bool:
        return Str.isJson(self._value)

    # Determine if a given string is a valid UUID.
    def isUuid(self) -> bool:
        return Str.isUuid(self._value)

    # Determine if a given string is a valid ULID.
    def isUlid(self) -> bool:
        return Str.isUlid(self._value)

    # Determine if the given string is empty.
    def isEmpty(self) -> bool:
        return self._value == ''

    # Determine if the given string is not empty.
    def isNotEmpty(self) -> bool:
        return not self.isEmpty()

    # Convert a string to kebab case.
    def kebab(self):
        return Stringable(Str.kebab(self._value))

    # Return the length of the given string.
    def length(self, encoding: str | None = None) -> int:
        return Str.length(self._value, encoding)

    # Limit the number of characters in a string.
    def limit(self, limit: int = 100, end: str = '...'):
        return Stringable(Str.limit(self._value, limit, end))

    # Convert the given string to lower-case.
    def lower(self):
        return Stringable(Str.lower(self._value))

    # Convert GitHub flavored Markdown into HTML.
    def markdown(self, options: list = []):
        return Stringable(Str.markdown(self._value, options))

    # Convert inline Markdown into HTML.
    def inlineMarkdown(self, options: list = []):
        return Stringable(Str.inlineMarkdown(self._value, options))

    # Masks a portion of a string with a repeated character.
    def mask(self, character: str, index: int, length: int = 0, encoding: str | None = None):
        return Stringable(Str.mask(self._value, character, index, length, encoding))

    # Get the string matching the given pattern.
    def match(self, pattern: str) -> str:
        return Str.match(pattern, self._value)

    # Determine if a given string matches a given pattern.
    def isMatch(self, pattern: str) -> bool:
        return Str.isMatch(pattern, self._value)

    # Get the string matching the given pattern.
    def matchAll(self, pattern: str):
        return Str.matchAll(pattern, self._value)

    # Determine if the string matches the given pattern.
    def test(self, pattern: str) -> bool:
        return self.isMatch(pattern)

    # Pad both sides of the string with another.
    def padBoth(self, length: int, pad: str = ' '):
        return Stringable(Str.padBoth(self._value, length, pad))

    # Pad the left side of the string with another.
    def padLeft(self, length: int, pad: str = ' '):
        return Stringable(Str.padLeft(self._value, length, pad))

    # Pad the right side of the string with another.
    def padRight(self, length: int, pad: str = ' '):
        return Stringable(Str.padRight(self._value, length, pad))

    # Parse a Class@method style callback into class and method.
    def parseCallback(self, default: str = None) -> list:
        return Str.parseCallback(self._value, default)

    # Call the given callback and return a new string.
    def pipe(self, callback: callable):
        return Stringable(callback(self._value))

    # Get the plural form of an English word.
    def plural(self, count: int | list = 2):
        return Stringable(Str.plural(self._value, count))

    # Pluralize the last word of an English, studly caps case string.
    def pluralStudly(self, count: int | list = 2):
        return Stringable(Str.pluralStudly(self._value, count))

    # Prepend the given values to the string.
    def prepend(self, *values: list):
        value = ''
        for v in values:
            value += str(v)
        return Stringable(value + self._value)

    # Remove any occurrence of the given string in the subject.
    def remove(self, search: str | list, caseSensitive: bool = True):
        return Stringable(Str.remove(search, self._value, caseSensitive))

    # Reverse the string.
    def reverse(self):
        return Stringable(Str.reverse(self._value))

    # Repeat the string.
    def repeat(self, times: int):
        return Stringable(self._value * times)

    # Replace the given value in the given string.
    def replace(self, search: str | list, replace: str | list, caseSensitive: bool = True):
        return Stringable(Str.replace(search, replace, self._value, caseSensitive))

    # Replace a given value in the string sequentially with an array.
    def replaceArray(self, search: str, replace: list):
        return Stringable(Str.replaceArray(search, replace, self._value))

    # Replace the first occurrence of a given value in the string.
    def replaceFirst(self, search: str, replace: str):
        return Stringable(Str.replaceFirst(search, replace, self._value))

    # Replace the last occurrence of a given value in the string.
    def replaceLast(self, search: str, replace: str):
        return Stringable(Str.replaceLast(search, replace, self._value))

    # Replace the patterns matching the given regular expression.
    def replaceMatches(self, pattern: str, replace: str, limit: int = -1):
        # @todo
        raise NotImplementedError('The method "replaceMatches" is not implemented yet.')

    # Parse input from a string to a collection, according to a format.
    def scan(self, format: str) -> list:
        raise NotImplementedError('The method "scan" is not implemented yet.')

    # Remove all "extra" blank space from the given string.
    def squish(self):
        return Stringable(Str.squish(self._value))

    # Begin a string with a single instance of a given value.
    def start(self, prefix: str):
        return Stringable(Str.start(self._value, prefix))

    # Strip HTML and PHP tags from the given string.
    def stripTags(self, allowedTags: str = None):
        raise NotImplementedError('The method "stripTags" is not implemented yet.')

    # Convert the given string to upper-case.
    def upper(self):
        return Stringable(Str.upper(self._value))

    # Convert the given string to title case.
    def title(self):
        return Stringable(Str.title(self._value))

    # Convert the given string to title case for each word.
    def headline(self):
        return Stringable(Str.headline(self._value))

    # Get the singular form of an English word.
    def singular(self):
        return Stringable(Str.singular(self._value))

    # Generate a URL friendly "slug" from a given string.
    def slug(self, separator: str = '-', language: str = 'en', directory: dict = {}):
        return Stringable(Str.slug(self._value, separator, language, directory))

    # Convert a string to snake case.
    def snake(self, delimiter: str = '_'):
        return Stringable(Str.snake(self._value, delimiter))

    # Determine if a given string starts with a given substring.
    def startsWith(self, needles: str | list):
        return Str.startsWith(self._value, needles)

    # Convert a value to studly caps case.
    def studly(self):
        return Stringable(Str.studly(self._value))

    # Returns the portion of the string specified by the start and length parameters.
    def substr(self, start: int, length: int = None, encoding='UTF-8'):
        return Stringable(Str.substr(self._value, start, length, encoding))

    # Returns the number of substring occurrences.
    def substrCount(self, needle: str, offset: int = 0, length: int = None):
        return Str.substrCount(self._value, needle, offset, length)

    # Replace text within a portion of a string.
    def substrReplace(self, replace: str | list, offset: int = 0, length: int = None):
        return Stringable(Str.substrReplace(self._value, replace, offset, length))

    # Swap multiple keywords in a string with other keywords.
    def swap(self, _map: dict):
        return Stringable(Str.swap(_map, self._value))

    # Trim the string of the given characters.
    def trim(self, *characters: list[str]):
        if len(characters) == 0:
            characters = [' ']

        for value in characters:
            self._value = self._value.strip(value)
        return Stringable(self._value)

    # Left trim the string of the given characters.
    def ltrim(self, *characters: list[str]):
        if len(characters) == 0:
            characters = [' ']

        for value in characters:
            self._value = self._value.lstrip(value)
        return Stringable(self._value)

    # Right trim the string of the given characters.
    def rtrim(self, *characters: list[str]):
        if len(characters) == 0:
            characters = [' ']

        for value in characters:
            self._value = self._value.rstrip(value)
        return Stringable(self._value)

    # Make a string's first character lowercase.
    def lcfirst(self):
        return Stringable(Str.lcfirst(self._value))

    # Make a string's first character uppercase.
    def ucfirst(self):
        return Stringable(Str.ucfirst(self._value))

    # Split a string by uppercase characters.
    def ucsplit(self) -> list[str]:
        return Str.ucsplit(self._value)

    # Execute the given callback if the string contains a given substring.
    def whenContains(self, needles: str | list, callback: callable, default: callable = None):
        return self.when(self.contains(needles), callback, default)

    # Execute the given callback if the string contains all array values.
    def whenContainsAll(self, needles: list, callback: callable, default: callable = None):
        return self.when(self.containsAll(needles), callback, default)

    # Execute the given callback if the string is empty.
    def whenEmpty(self, callback: callable, default: callable = None):
        return self.when(self.isEmpty(), callback, default)

    # Execute the given callback if the string is not empty.
    def whenNotEmpty(self, callback: callable, default: callable = None):
        return self.when(self.isNotEmpty(), callback, default)

    # Execute the given callback if the string ends with a given substring.
    def whenEndsWith(self, needles: str | list, callback: callable, default: callable = None):
        return self.when(self.endsWith(needles), callback, default)

    # Execute the given callback if the string is an exact match with the given value.
    def whenExactly(self, value: str, callback: callable, default: callable = None):
        return self.when(self.exactly(value), callback, default)

    # Execute the given callback if the string is not an exact match with the given value.
    def whenNotExactly(self, value: str, callback: callable, default: callable = None):
        return self.when(not self.exactly(value), callback, default)

    # Execute the given callback if the string matches a given pattern.
    def whenIs(self, pattern: str, callback: callable, default: callable = None):
        return self.when(self.is_(pattern), callback, default)

    # Execute the given callback if the string is 7 bit ASCII.
    def whenIsAscii(self, callback: callable, default: callable = None):
        return self.when(self.isAscii(), callback, default)

    # Execute the given callback if the string is a valid UUID.
    def whenIsUuid(self, callback: callable, default: callable = None):
        return self.when(self.isUuid(), callback, default)

    # Execute the given callback if the string is a valid ULID.
    def whenIsUlid(self, callback: callable, default: callable = None):
        return self.when(self.isUlid(), callback, default)

    # Execute the given callback if the string starts with a given substring.
    def whenStartsWith(self, needles: str | list, callback: callable, default: callable = None):
        return self.when(self.startsWith(needles), callback, default)

    # Execute the given callback if the string matches the given pattern.
    def whenTest(self, pattern: str, callback: callable, default: callable = None):
        return self.when(self.test(pattern), callback, default)

    # Limit the number of words in a string.
    def words(self, words: int = 100, end: str = '...'):
        return Stringable(Str.words(self._value, words, end))

    # Get the number of words a string contains.
    def wordCount(self) -> int:
        return Str.wordCount(self._value)

    # Wrap the string with the given strings.
    def wrap(self, before: str, after: str = None):
        return Stringable(Str.wrap(self._value, before, after))

    # Convert the string into a `HtmlString` instance.
    def toHtmlString(self):
        raise NotImplementedError('The method "toHtmlString" is not implemented yet.')

    # Extract the file name from a file path.
    def name(self):
        return Stringable(Str.name(self._value))

    # Extract the file extension from a file path.
    def extension(self):
        return Stringable(Str.extension(self._value))

    # Dump the string.
    def dump(self):
        print(self._value)
        return self

    # Dump the string and end the script.
    def dd(self):
        self.dump()

        import sys
        sys.exit(1)

    # Get the underlying string value.
    def value(self) -> str:
        return self.toString()

    # Get the underlying string value.
    def toString(self) -> str:
        return self._value

    # Get the underlying string value as an integer.
    def toInteger(self) -> int:
        return int(self._value)

    # Get the underlying string value as a float.
    def toFloat(self) -> float:
        return float(self._value)

    # Get the underlying string value as a boolean.
    def toBoolean(self) -> bool:
        return bool(self._value)

    # Get the underlying string value as a Carbon instance.
    def toDate(self):
        raise NotImplementedError('The method "toDate" is not implemented yet.')

    # Convert the object to a string when JSON encoded.
    def jsonSerialize(self) -> str:
        import json
        return json.dumps(self._value)

    # Determine if a given offset exists.
    def offsetExists(self, offset: str) -> bool:
        return offset in self._value

    # Get the value at a given offset.
    def offsetGet(self, offset: str) -> any:
        return self._value[offset]

    # Set the value at a given offset.
    def offsetSet(self, offset: str, value: any) -> None:
        self._value[offset] = value

    # Unset the value at a given offset.
    def offsetUnset(self, offset: str) -> None:
        del self._value[offset]

    def __getitem__(self, key) -> any:
        return self.offsetGet(key)

    def __setitem__(self, key, value) -> None:
        self.offsetSet(key, value)

    def __delitem__(self, key) -> None:
        self.offsetUnset(key)

    # Proxy dynamic properties onto methods.
    def __get__(self, key: str) -> any:
        return self[key]()

    # Get the raw string value.
    def __str__(self) -> str:
        return self._value
