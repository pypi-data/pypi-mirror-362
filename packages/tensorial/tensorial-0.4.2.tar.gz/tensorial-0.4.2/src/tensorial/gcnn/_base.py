import functools
import logging
from typing import TYPE_CHECKING, Protocol, Sequence

from jax import tree_util
import jaxtyping as jt
import jraph

from . import _tree
from .experimental import utils as exp_utils
from .typing import GraphFunction

if TYPE_CHECKING:
    from tensorial import gcnn

__all__ = ("GraphFunction", "shape_check", "transform_fn")

_LOGGER = logging.getLogger(__name__)


def shape_check(func: "gcnn.typing.GraphFunction") -> "gcnn.typing.GraphFunction":
    """
    Decorator that will print to the logger any differences in either the keys present in
    the graph before and after the call, or any differences in their shapes.

    This is super useful for diagnosing jax re-compilation issues.
    """

    @functools.wraps(func)
    def shape_checker(*args) -> jraph.GraphsTuple:
        # Can either be a class method or a free function
        inputs: jraph.GraphsTuple = args[0] if len(args) == 1 else args[1]
        flattened, _ = tree_util.tree_flatten_with_path(inputs)
        in_shapes = {path: array.shape for path, array in flattened}

        out = func(*args)
        out_shapes = {
            (path, array.shape) for path, array in tree_util.tree_flatten_with_path(out)[0]
        }
        diff = out_shapes - set(in_shapes.items())

        messages: list[str] = []
        for path, shape in diff:
            path_str = _tree.path_to_str(tuple(map(_tree.key_to_str, path)))
            try:
                in_shape = in_shapes[path]
            except KeyError:
                messages.append(f"new {path_str}")
            else:
                messages.append(f"{path_str} {in_shape}->{shape}")
        if messages:
            _LOGGER.debug(
                "%s() difference(s) in inputs/outputs: %s",
                func.__qualname__,
                ", ".join(messages),
            )

        return out

    return shape_checker


class TransformedGraphFunction(Protocol):
    """Transformed graph function that returns a value or a tuple of a value and a graph"""

    def __call__(
        self, graph: jraph.GraphsTuple, *args: jt.PyTree
    ) -> jt.PyTree | tuple[jt.PyTree, jraph.GraphsTuple]: ...


def transform_fn(
    fn: "gcnn.typing.ExGraphFunction",
    *ins: "gcnn.TreePathLike",
    outs: "Sequence[gcnn.TreePathLike]" = tuple(),
    return_graphs: bool = False,
) -> TransformedGraphFunction:
    """
    Given a graph function, this will return a function that takes a graph as the first argument
    followed by positional arguments that will be mapped to the fields given by ``ins``.
    Output paths can optionally be specified with ``outs`` which, if supplied, will make the
    function return one or more values from the graph as returned by ``fn``.

    :param fn: the graph function
    :param ins: the input paths
    :param outs: the output paths
    :param return_graphs: if `True` and ``outs`` is specified, this will return a tuple containing
        the output graph followed by the values at ``outs``
    :return: a function that wraps ``fn`` with the above properties
    """
    ins = tuple(_tree.path_from_str(path) for path in ins)
    outs = tuple(_tree.path_from_str(path) for path in outs)

    def _fn(
        graph: jraph.GraphsTuple, *args: jt.PyTree
    ) -> jt.PyTree | tuple[jt.PyTree, jraph.GraphsTuple]:
        # Set the values from graph at the correct paths in the graphs tuple
        updater = exp_utils.update_graph(graph)
        for path, arg in zip(ins, args):
            updater.set(path, arg)
        graph = updater.get()

        # Pass the graph through the original function
        res = fn(graph, *args[len(ins) :])
        if outs:
            # Extract the quantity that we want as outputs
            out_graph: jraph.GraphsTuple = res
            out_vals = _tree.get(out_graph, *outs)
            if return_graphs:
                return out_vals, out_graph

            return out_vals

        if return_graphs:
            # Just return the original input graph
            return res, graph

        return res

    return _fn
