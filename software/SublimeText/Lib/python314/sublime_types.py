from sublime import KindId, CompletionItem

type DIP = float
type Vector = tuple[DIP, DIP]
type Point = int
type Value = bool | str | int | float | list[Value] | dict[str, Value] | None
type CommandArgs = dict[str, Value] | None
type Kind = tuple[KindId, str, str]
type Event = dict[str, Value]
type CompletionValue = str | tuple[str, str] | CompletionItem
