"""
The MIT License (MIT)

Copyright (c) 2015-present Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""


from inspect import Parameter
from typing import TYPE_CHECKING, Optional, List, Tuple
from fortnitepy.errors import FortniteException

if TYPE_CHECKING:
    from .cooldown import Cooldown, BucketType
    from .converter import Converter


__all__ = (
    'CommandError',
    'UserInputError',
    'CommandNotFound',
    'MissingRequiredArgument',
    'TooManyArguments',
    'BadArgument',
    'CheckFailure',
    'CheckAnyFailure',
    'PrivateMessageOnly',
    'PartyMessageOnly',
    'NotOwner',
    'DisabledCommand',
    'CommandInvokeError',
    'CommandOnCooldown',
    'MaxConcurrencyReached',
    'ConversionError',
    'BadUnionArgument',
    'ArgumentParsingError',
    'UnexpectedQuoteError',
    'InvalidEndOfQuotedStringError',
    'ExpectedClosingQuoteError',
    'ExtensionError',
    'ExtensionAlreadyLoaded',
    'ExtensionNotLoaded',
    'ExtensionMissingEntryPoint',
    'ExtensionFailed',
    'ExtensionNotFound',
)


class CommandError(FortniteException):
    r"""The base exception type for all command related errors.

    This inherits from :exc:`fortnitepy.FortniteException`.

    This exception and exceptions inherited from it are handled
    in a special way as they are caught and passed into a special event
    from :class:`.Bot`\, :func:`event_command_error`.
    """

    def __init__(self, message: Optional[str] = None, *args: list) -> None:
        if message is not None:
            super().__init__(message, *args)
        else:
            super().__init__(*args)


class UserInputError(CommandError):
    """The base exception type for errors that involve errors
    regarding user input.

    This inherits from :exc:`CommandError`.
    """
    pass


class CommandNotFound(CommandError):
    """Exception raised when a command is attempted to be invoked
    but no command under that name is found.

    This is not raised for invalid subcommands, rather just the
    initial main command that is attempted to be invoked.

    This inherits from :exc:`CommandError`.
    """
    pass


class MissingRequiredArgument(UserInputError):
    """Exception raised when parsing a command and a parameter
    that is required is not encountered.

    This inherits from :exc:`UserInputError`

    Attributes
    -----------
    param: :class:`inspect.Parameter`
        The argument that is missing.
    """

    def __init__(self, param: Parameter) -> None:
        self.param = param
        super().__init__('{0.name} is a required argument that is '
                         'missing.'.format(param))


class TooManyArguments(UserInputError):
    """Exception raised when the command was passed too many arguments and its
    :attr:`.Command.ignore_extra` attribute was not set to ``True``.

    This inherits from :exc:`UserInputError`
    """
    pass


class BadArgument(UserInputError):
    """Exception raised when a parsing or conversion failure is encountered
    on an argument to pass into a command.

    This inherits from :exc:`UserInputError`
    """
    pass


class CheckFailure(UserInputError):
    """Exception raised when the predicates in :attr:`.Command.checks` have failed.

    This inherits from :exc:`CommandError`
    """
    pass


class CheckAnyFailure(CheckFailure):
    """Exception raised when all predicates in :func:`check_any` fail.

    This inherits from :exc:`CheckFailure`.

    Attributes
    ------------
    errors: List[:class:`CheckFailure`]
        A list of errors that were caught during execution.
    checks: List[Callable[[:class:`Context`], :class:`bool`]]
        A list of check predicates that failed.
    """

    def __init__(self, checks: List[callable],
                 errors: List[CheckFailure]) -> None:
        self.checks = checks
        self.errors = errors
        super().__init__('You do not have permission to run this command.')


class PrivateMessageOnly(CheckFailure):
    """Exception raised when an operation does not work outside of private
    message contexts.

    This inherits from :exc:`CheckFailure`
    """

    def __init__(self, message: Optional[str] = None) -> None:
        super().__init__(
            message or 'This command can only be used in private messages.'
        )


class PartyMessageOnly(CheckFailure):
    """Exception raised when an operation does not work outside of party
    message contexts.

    This inherits from :exc:`CheckFailure`
    """
    def __init__(self, message: Optional[str] = None) -> None:
        super().__init__(
            message or 'This command can only be used in party messages.'
        )


class NotOwner(CheckFailure):
    """Exception raised when the message author is not the owner of the bot.

    This inherits from :exc:`CheckFailure`
    """
    pass


class DisabledCommand(CommandError):
    """Exception raised when the command being invoked is disabled.

    This inherits from :exc:`CommandError`
    """
    pass


class CommandInvokeError(CommandError):
    """Exception raised when the command being invoked raised an exception.

    This inherits from :exc:`CommandError`

    Attributes
    ----------
    original
        The original exception that was raised. You can also get this via
        the ``__cause__`` attribute.
    """

    def __init__(self, e: Exception) -> None:
        self.original = e
        super().__init__('Command raised an exception: '
                         '{0.__class__.__name__}: {0}'.format(e))


class CommandOnCooldown(CommandError):
    """Exception raised when the command being invoked is on cooldown.

    This inherits from :exc:`CommandError`

    Attributes
    -----------
    cooldown: Cooldown
        A class with attributes ``rate``, ``per``, and ``type`` similar to
        the :func:`.cooldown` decorator.
    retry_after: :class:`float`
        The amount of seconds to wait before you can retry again.
    """

    def __init__(self, cooldown: 'Cooldown', retry_after: float) -> None:
        self.cooldown = cooldown
        self.retry_after = retry_after
        super().__init__('You are on cooldown. Try again in '
                         '{:.2f}s'.format(retry_after))


class MaxConcurrencyReached(CommandError):
    """Exception raised when the command being invoked has reached its maximum
    concurrency.

    This inherits from :exc:`CommandError`.

    Attributes
    ----------
    number: :class:`int`
        The maximum number of concurrent invokers allowed.
    per: :class:`BucketType`
        The bucket type passed to the :func:`.max_concurrency` decorator.
    """

    def __init__(self, number: int, per: 'BucketType') -> None:
        self.number = number
        self.per = per
        name = per.name
        suffix = 'per %s' % name if per.name != 'default' else 'globally'
        plural = '%s times %s' if number > 1 else '%s time %s'
        fmt = plural % (number, suffix)
        super().__init__('Too many people using this command. It can only '
                         'be used {} concurrently.'.format(fmt))


class ConversionError(CommandError):
    """Exception raised when a Converter class raises non-CommandError.

    This inherits from :exc:`CommandError`.

    Attributes
    ----------
    converter: :class:`fortnitepy.ext.commands.Converter`
        The converter that failed.
    original
        The original exception that was raised. You can also get this via
        the ``__cause__`` attribute.
    """

    def __init__(self, converter: 'Converter', original: Exception) -> None:
        self.converter = converter
        self.original = original


class BadUnionArgument(UserInputError):
    """Exception raised when a :data:`typing.Union` converter fails for all
    its associated types.

    This inherits from :exc:`UserInputError`

    Attributes
    -----------
    param: :class:`inspect.Parameter`
        The parameter that failed being converted.
    converters: Tuple[Type, ...]
        A tuple of converters attempted in conversion, in order of failure.
    errors: List[:class:`CommandError`]
        A list of errors that were caught from failing the conversion.
    """

    def __init__(self, param: Parameter,
                 converters: Tuple['Converter'],
                 errors: List[CommandError]) -> None:
        self.param = param
        self.converters = converters
        self.errors = errors

        def _get_name(x):
            try:
                return x.__name__
            except AttributeError:
                return x.__class__.__name__

        to_string = [_get_name(x) for x in converters]
        if len(to_string) > 2:
            fmt = '{}, or {}'.format(', '.join(to_string[:-1]), to_string[-1])
        else:
            fmt = ' or '.join(to_string)

        super().__init__('Could not convert "{0.name}" into '
                         '{1}.'.format(param, fmt))


class ArgumentParsingError(UserInputError):
    """An exception raised when the parser fails to parse a user's input.

    This inherits from :exc:`UserInputError`.

    There are child classes that implement more granular parsing errors for
    i18n purposes.
    """
    pass


class UnexpectedQuoteError(ArgumentParsingError):
    """An exception raised when the parser encounters a quote mark inside a
    non-quoted string.

    This inherits from :exc:`ArgumentParsingError`.

    Attributes
    ------------
    quote: :class:`str`
        The quote mark that was found inside the non-quoted string.
    """

    def __init__(self, quote: str) -> None:
        self.quote = quote
        super().__init__('Unexpected quote mark, {0!r}, in non-quoted '
                         'string'.format(quote))


class InvalidEndOfQuotedStringError(ArgumentParsingError):
    """An exception raised when a space is expected after the closing quote in
    a string but a different character is found.

    This inherits from :exc:`ArgumentParsingError`.

    Attributes
    -----------
    char: :class:`str`
        The character found instead of the expected string.
    """

    def __init__(self, char: str) -> None:
        self.char = char
        super().__init__('Expected space after closing quotation but '
                         'received {0!r}'.format(char))


class ExpectedClosingQuoteError(ArgumentParsingError):
    """An exception raised when a quote character is expected but not found.

    This inherits from :exc:`ArgumentParsingError`.

    Attributes
    -----------
    close_quote: :class:`str`
        The quote character expected.
    """

    def __init__(self, close_quote: str) -> None:
        self.close_quote = close_quote
        super().__init__('Expected closing {}.'.format(close_quote))


# Extension

class ExtensionError(FortniteException):
    """Base exception for extension related errors.

    This inherits from :exc:`~fortnitepy.FortniteException`.

    Attributes
    ------------
    name: :class:`str`
        The extension that had an error.
    """

    def __init__(self, message: Optional[str] = None,
                 *args: list,
                 name: str) -> None:
        self.name = name
        message = message or 'Extension {!r} had an error.'.format(name)
        super().__init__(message, *args)


class ExtensionAlreadyLoaded(ExtensionError):
    """An exception raised when an extension has already been loaded.

    This inherits from :exc:`ExtensionError`
    """

    def __init__(self, name: str) -> None:
        super().__init__('Extension {!r} is already loaded.'
                         ''.format(name), name=name)


class ExtensionNotLoaded(ExtensionError):
    """An exception raised when an extension was not loaded.

    This inherits from :exc:`ExtensionError`
    """

    def __init__(self, name: str) -> None:
        super().__init__('Extension {!r} has not been loaded.'
                         ''.format(name), name=name)


class ExtensionMissingEntryPoint(ExtensionError):
    """An exception raised when an extension does not have a
    ``extension_setup`` entry point function.

    This inherits from :exc:`ExtensionError`
    """

    def __init__(self, name: str) -> None:
        super().__init__("Extension {!r} has no 'setup' function."
                         "".format(name), name=name)


class ExtensionFailed(ExtensionError):
    """An exception raised when an extension failed to load during execution
    of the module or ``extension_setup`` entry point.

    This inherits from :exc:`ExtensionError`

    Attributes
    -----------
    name: :class:`str`
        The extension that had the error.
    original: :exc:`Exception`
        The original exception that was raised. You can also get this via
        the ``__cause__`` attribute.
    """

    def __init__(self, name: str, original: Exception) -> None:
        self.original = original
        fmt = 'Extension {0!r} raised an error: {1.__class__.__name__}: {1}'
        super().__init__(fmt.format(name, original), name=name)


class ExtensionNotFound(ExtensionError):
    """An exception raised when an extension is not found.

    This inherits from :exc:`ExtensionError`

    Attributes
    -----------
    name: :class:`str`
        The extension that had the error.
    """

    def __init__(self, name: str) -> None:
        fmt = 'Extension {0!r} could not be loaded.'
        super().__init__(fmt.format(name), name=name)
