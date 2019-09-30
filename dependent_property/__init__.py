from functools import lru_cache, partial

from typing import Any, Callable, Type


__all__ = [
    "__version__",
    "Dependable",
    "dependent_property",
    "dependent_method",
]


__version__ = "0.1.0"


class Dependable:
    """A descriptor that can have children which are notified when its
    value changes
    """

    def __init__(self):
        self.children = set()
        self.values = {}

    def add_child(self, child: "Dependable") -> None:
        """Add a child to the instance

        Parameters
        ----------
        child : Dependable
            Another Dependable instance
        """
        self.children.add(child)

    def notify_change(self) -> None:
        """Notify all children of changes
        """
        for child in self.children:
            child.notify_change()

    def __get__(self, obj: Any, cls: Type) -> Any:
        """Get the value of the instance for ``obj``

        Parameters
        ----------
        obj : Any
            Owning object
        cls : Type
            Type of ``obj``

        Returns
        -------
        Any
            Value stored in the instance of ``obj``
        """
        return self.values.get(obj, None)

    def __set__(self, obj: Any, value: Any) -> None:
        """Set the value in the instance for ``obj``

        Parameters
        ----------
        obj : Any
            Owning object
        value : Any
            Value to store
        """
        current_value = self.values.get(obj, None)
        if value != current_value:
            self.notify_change()
            self.values[obj] = value


class dependent_property(Dependable):
    """A subclass of Dependable which behaves like a property, wrapping
    a method of one argument (self), which clears its cache when
    receiving a change notification

    Parameters
    ---------
        parents : Iterable[Dependable]
            Iterable of Dependable objects on which this instance
            depends
    """

    def __init__(self, *parents):
        self.parents = parents
        self.func = None

        for parent in self.parents:
            parent.add_child(self)

        super().__init__()

    def notify_change(self) -> None:
        """Notify all children of changes
        """
        self.func.cache_clear()
        super().notify_change()

    def __call__(self, func: Callable) -> "dependent_property":
        """Store a cached version of func in the instance

        Parameters
        ----------
        func : Callable
            Method to wrap

        Returns
        -------
        dependent_property
            self
        """
        self.func = lru_cache(None)(func)
        self.func.__doc__ = func.__doc__
        return self

    def __get__(self, obj: Any, cls: Type) -> Any:
        """Get the value of wrapped method for the given object

        Parameters
        ----------
        obj : Any
            Owning object
        cls : Type
            Type of ``obj``

        Returns
        -------
        Any
            The value of the wrapped method for the given object
        """
        return self.func(obj)

    def __set__(self, obj: Any, value: Any) -> None:
        """Raise an error if the user tries to override the instance

        Parameters
        ----------
        obj : Any
            Owning object
        value : Any
            Value it's attempting to store
        """
        raise ValueError("Not writable!")


class dependent_method(dependent_property):
    """A subclass of dependent_property which behaves like a method,
    but only runs if its arguments or dependencies change
    """

    def __get__(self, obj: Any, cls: Type) -> Callable:
        """Get the wrapped method for the given object

        Parameters
        ----------
        obj : Any
            Owning object
        cls : Type
            Type of ``obj``

        Returns
        -------
        Callable
            The wrapped method for the given object with its first
            parameter (``obj``) populated
        """
        part = partial(self.func, obj)
        part.__doc__ = self.func.__doc__
        return part
