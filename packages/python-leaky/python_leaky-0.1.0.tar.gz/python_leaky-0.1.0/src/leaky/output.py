from abc import ABC, abstractmethod

from rich.console import Console, RenderableType
from rich.console import NewLine as RichNewLine

from leaky.options import Options
from leaky.themes import DEFAULT_RICH_THEME


class Output(ABC):
    """
    An object that can be sent to an output sink. This may be the console, a file, etc.
    """

    @abstractmethod
    def to_renderables(self) -> list[RenderableType]:
        """
        Converts this object to a list of rich renderable objects.

        This is used when printing the object to the console, log files, etc.
        """
        pass


class RichOutput(Output):
    """
    An output object that returns the passed-in renderable object.
    """

    def __init__(self, renderable: RenderableType) -> None:
        self._renderable = renderable

    def to_renderables(self) -> list[RenderableType]:
        return [self._renderable]


class NewLine(RichOutput):
    """
    A new line output object.
    """

    def __init__(self) -> None:
        super().__init__(RichNewLine())


class OutputWriter(ABC):
    """
    A writer that sends objects to an output sink. This may be the console, a file, etc.
    """

    @abstractmethod
    def write(self, output: Output) -> None:
        pass


class RichConsoleWriter(OutputWriter):
    def __init__(self, options: Options) -> None:
        self._console = Console(
            force_terminal=options.force_terminal,
            theme=DEFAULT_RICH_THEME,
            no_color=not options.color,
        )
        self._options = options

    def write(self, output: Output) -> None:
        if self._options.output_func is not None:
            with self._console.capture() as captured:
                for renderable in output.to_renderables():
                    if type(renderable) is not RichNewLine and renderable != "\n":
                        self._console.print(
                            RichNewLine(),
                            soft_wrap=True,
                            crop=False,
                            overflow="ignore",
                        )
                        self._console.print(
                            renderable,
                            soft_wrap=True,
                            crop=False,
                            overflow="ignore",
                        )
            captured_str = captured.get()
            if captured_str.strip() != "":
                self._options.output_func(captured_str)
        if self._options.output_func is None or self._options.tee_console:
            for renderable in output.to_renderables():
                self._console.print(renderable, soft_wrap=True, crop=False, overflow="ignore")


def get_output_writer(options: Options) -> OutputWriter:
    return RichConsoleWriter(options=options)
