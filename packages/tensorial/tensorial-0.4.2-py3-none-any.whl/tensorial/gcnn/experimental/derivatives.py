import abc
from collections.abc import Sequence
import dataclasses
import re
from typing import TYPE_CHECKING, Final, Optional, Protocol

from flax import linen
import jax
import jaxtyping as jt
import jraph

from .. import _base, _tree
from ... import base

if TYPE_CHECKING:
    from tensorial import gcnn

__all__ = ("diff",)

DERIV_DELIMITER: Final[str] = ","


class DerivableGraphFunction(Protocol):
    def __call__(
        self, graph: jraph.GraphsTuple, *args: jt.PyTree
    ) -> jt.Array | tuple[jt.Array, jraph.GraphsTuple]: ...


@dataclasses.dataclass(frozen=True, slots=True)
class GraphEntrySpec:
    """
    A specification that identifies a particular entry in a hierarchical data structure
    (e.g., a PyTree) along with optional index labels used for differentiable computations.

    Attributes:
        key_path (Optional[gcnn.typing.TreePath]): A path to the target node in the PyTree,
            typically represented as a tuple of keys (e.g., strings or integers).
        indices (Optional[str]): A string representing symbolic indices, often used to
            annotate tensor dimensions for operations like differentiation.
    """

    key_path: "Optional[gcnn.typing.TreePath]"
    indices: Optional[str]

    @classmethod
    def create(cls, spec: "GraphEntrySpecLike") -> "GraphEntrySpec":
        if isinstance(spec, GraphEntrySpec):
            return spec
        if spec is None:
            return GraphEntrySpec(None, None)

        match = re.match(r"^(?:(.*?))?(?::(.*))?$", spec)
        if not match:
            raise ValueError(f"Could not parse the expression: {spec}")

        groups = match.groups()
        return GraphEntrySpec(_tree.path_from_str(groups[0]), groups[1])

    @property
    def safe_indices(self) -> str:
        return self.indices if self.indices is not None else ""

    def __str__(self) -> str:
        rep = []
        if self.key_path is not None:
            rep.append(f"{_tree.path_to_str(self.key_path)}")
        if self.indices is not None:
            rep.append(f":{self.indices}")
        return "".join(rep)

    def __truediv__(self, other: "GraphEntrySpecLike") -> "SingleDerivative":
        return SingleDerivative.create(self, other)

    def index_union(self, other: "GraphEntrySpec") -> Optional[str]:
        # use dictionary keys as a set
        out = dict() if not self.indices else dict.fromkeys(self.indices)
        if other.indices:
            out |= dict.fromkeys(other.indices)
        if not out:
            return None

        return "".join(out)

    def indices_intersection(self, other: "GraphEntrySpec") -> str:
        if not self.indices or not other.indices:
            return ""

        out = [index for index in self.indices if index in other.indices]
        return "".join(out)


GraphEntrySpecLike = str | GraphEntrySpec


class Derivative(abc.ABC):
    @property
    @abc.abstractmethod
    def of(self) -> GraphEntrySpec:
        """Derivative of"""

    @property
    @abc.abstractmethod
    def wrt_paths(self) -> "tuple[gcnn.typing.TreePath, ...]":
        """Derivative output"""

    @property
    @abc.abstractmethod
    def out(self) -> GraphEntrySpec:
        """Derivative output"""

    def evaluator(
        self,
        func: DerivableGraphFunction,
        return_graph: bool,
        argnum: int = 0,
        scale: float = 1.0,
    ) -> "Evaluator":
        return Evaluator(func, self, return_graph, argnum, scale=scale)

    @abc.abstractmethod
    def build_derivative_fn(
        self, func: DerivableGraphFunction, return_graph: bool, argnum: int
    ) -> DerivableGraphFunction:
        """Get evaluate function from derivative"""


def infer_out_indices(of: GraphEntrySpec, wrt: GraphEntrySpec) -> str:
    # All indices resulting from differentiating 'of' with respect to 'wrt'
    all_deriv_indices = of.safe_indices + wrt.safe_indices

    # Find indices common to both 'of' and 'wrt' — these will be reduced (summed over)
    shared_indices = of.indices_intersection(wrt)
    of_reduce = tuple(of.indices.index(i) for i in shared_indices)

    return "".join([idx for i, idx in enumerate(all_deriv_indices) if i not in of_reduce])


@dataclasses.dataclass(frozen=True, slots=True)
class SingleDerivative(Derivative):
    _of: GraphEntrySpec
    _wrt: GraphEntrySpec
    _out: GraphEntrySpec

    # will be set in __post_init__
    pre_reduce: tuple[int, ...] = dataclasses.field(init=False)
    post_reduce: tuple[int, ...] = dataclasses.field(init=False)
    post_permute: tuple[int, ...] = dataclasses.field(init=False)
    _actual_out: GraphEntrySpec = dataclasses.field(init=False)

    def __post_init__(self):
        # All indices resulting from differentiating 'of' with respect to 'wrt'
        all_deriv_indices = self.of.safe_indices + self.wrt.safe_indices

        # now check that the output indices are some subset of these
        if self._out.indices is not None and not set(self._out.indices).issubset(all_deriv_indices):
            raise ValueError(
                f"The passed output indices {self._out.indices} include some that are "
                f"not in of ({self.of.indices}) or wrt ({self.wrt.indices})"
            )

        # Find indices common to both 'of' and 'wrt' — these will be reduced (summed over)
        unreduced_indices = []
        pre_reduce = []
        if self.of.indices is not None:
            for i, index in enumerate(self.of.indices):
                index_not_in_out = self._out.indices is not None and index not in self._out.indices
                index_in_wrt = self.wrt.indices is not None and index in self.wrt.indices
                if index_not_in_out or index_in_wrt:
                    pre_reduce.append(i)
                else:
                    unreduced_indices.append(index)
        object.__setattr__(self, "pre_reduce", tuple(pre_reduce))

        num_after_pre_reduce = len(unreduced_indices)
        post_reduce = []
        if self.wrt.indices is not None:
            for i, index in enumerate(self.wrt.indices):
                if self._out.indices is not None and index not in self._out.indices:
                    post_reduce.append(i + num_after_pre_reduce)
                else:
                    unreduced_indices.append(index)
        object.__setattr__(self, "post_reduce", tuple(post_reduce))

        # Map output indices to their new position in the output tensor
        post_permute = (
            find_index_permutation(unreduced_indices, self._out.indices)
            if self._out.indices is not None
            else []
        )
        object.__setattr__(self, "post_permute", tuple(post_permute))

        if self._out.indices is None:
            out_indices = "".join(unreduced_indices)
            if post_permute:
                out_indices = "".join(out_indices for i in post_permute)

            out = GraphEntrySpec(self._out.key_path, out_indices)
        else:
            out = self._out

        object.__setattr__(self, "_actual_out", out)

    @classmethod
    def create(
        cls,
        of: GraphEntrySpecLike,
        wrt: GraphEntrySpecLike,
        out: Optional[GraphEntrySpecLike] = None,
    ) -> "SingleDerivative":
        of = GraphEntrySpec.create(of)
        wrt = GraphEntrySpec.create(wrt)
        out = GraphEntrySpec.create(out)
        return SingleDerivative(of, wrt, out)

    @property
    def of(self) -> GraphEntrySpec:
        """Derivative of"""
        return self._of

    @property
    def wrt(self) -> GraphEntrySpec:
        """Derivative output"""
        return self._wrt

    @property
    def wrt_paths(self) -> "tuple[gcnn.typing.TreePath, ...]":
        return (self._wrt.key_path,)

    @property
    def out(self) -> GraphEntrySpec:
        """Derivative output"""
        return self._actual_out

    def __str__(self) -> str:
        return f"∂{self.of}/∂{self.wrt}->{self.out}"

    def __truediv__(self, other: "GraphEntrySpecLike | SingleDerivative") -> "MultiDerivative":
        if isinstance(other, SingleDerivative):
            return MultiDerivative((self, other))

        wrt = GraphEntrySpec.create(other)
        return MultiDerivative((self, SingleDerivative.create(self.out, wrt)))

    def build_derivative_fn(
        self, func: DerivableGraphFunction, return_graph: bool, argnum: int
    ) -> DerivableGraphFunction:
        if not argnum >= 0:
            raise ValueError(f"argnum must be >= 0, got: {argnum}")

        if not self.out.indices:
            # Scalar valued
            diff_fn = jax.grad
        else:
            # Vector valued
            diff_fn = jax.jacrev

        def _diff_and_pre_process(
            graph: jraph.GraphsTuple, *args: jt.PyTree
        ) -> tuple[jt.Array, jraph.GraphsTuple]:
            value, graph = func(graph, *args)
            value, graph = self._pre_process(value, graph)
            return value, graph

        do_diff = diff_fn(_diff_and_pre_process, argnums=1 + argnum, has_aux=True)

        def _diff_fn(
            graph: jraph.GraphsTuple, *args: jt.PyTree
        ) -> jt.Array | tuple[jt.Array, jraph.GraphsTuple]:
            if len(args) <= argnum:
                raise ValueError(
                    f"Derivative needs to be taken wrt argument {argnum}, "
                    f"but only {len(args)} were passed"
                )
            self._check_shape("wrt", self.wrt, args[argnum])

            value, graph = do_diff(graph, *args)
            value, graph = self._post_process(value, graph)

            if return_graph:
                return value, graph

            return value

        return _diff_fn

    def _pre_process(
        self, value: jt.Array, graph: jraph.GraphsTuple
    ) -> tuple[jt.Array, jraph.GraphsTuple]:
        self._check_shape("of", self.of, value)

        if self.pre_reduce:
            value = base.as_array(value).sum(axis=self.pre_reduce)

        return value, graph

    def _post_process(
        self, value: jt.Array, graph: jraph.GraphsTuple
    ) -> tuple[jt.Array, jraph.GraphsTuple]:
        if self.post_reduce:
            value = base.as_array(value).sum(axis=self.post_reduce)
        if self.post_permute:
            value = value.transpose(self.post_permute)
        self._check_shape("out", self.out, value)

        return value, graph

    @staticmethod
    def _check_shape(stage: str, spec: GraphEntrySpec, value: jt.Array):
        if spec.indices is None:
            return  # Nothing to check

        value = base.as_array(value)
        if len(spec.indices) != len(value.shape):
            raise ValueError(
                f"The passed '{stage}' indices `{spec.indices}` do not match the sape of the "
                f"value shape: {value.shape}"
            )


@dataclasses.dataclass(frozen=True, slots=True)
class MultiDerivative(Derivative):
    parts: tuple[SingleDerivative, ...]

    # will be set in __post_init__
    paths: "linen.FrozenDict[gcnn.typing.TreePath, int]" = dataclasses.field(init=False)

    def __post_init__(self):
        paths = {}
        wrt_map = []
        for part in self.parts:
            wrt_map.append(paths.setdefault(part.wrt.key_path, len(paths)))
        object.__setattr__(self, "paths", linen.FrozenDict(paths))

    @classmethod
    def create(
        cls,
        of: GraphEntrySpecLike,
        wrt: str | Sequence[GraphEntrySpecLike],
        out: Optional[GraphEntrySpecLike] = None,
    ) -> "MultiDerivative":
        if isinstance(wrt, str):
            wrt = wrt.split(",")

        if len(wrt) == 1:
            return MultiDerivative((SingleDerivative.create(of, wrt[0], out),))

        # First
        parts = [SingleDerivative.create(of, wrt[0])]
        # Middle
        for part in wrt[1:-1]:
            parts.append(SingleDerivative.create(parts[-1].out, part))
        # Last
        parts.append(SingleDerivative.create(parts[-1].out, wrt[-1], out))

        return MultiDerivative(tuple(parts))

    @property
    def of(self) -> GraphEntrySpec:
        return self.parts[0].of

    @property
    def wrt_paths(self) -> "tuple[gcnn.typing.TreePath, ...]":
        return tuple(self.paths.keys())

    @property
    def out(self) -> GraphEntrySpec:
        return self.parts[-1].out

    def __str__(self) -> str:
        parts = [f"∂{self.of}/∂{self[0].wrt}"]

        for deriv in self[1:]:
            parts.append(f"∂{deriv.wrt}")

        parts.append(f"->{self.out}")
        return "".join(parts)

    def __len__(self) -> int:
        return len(self.parts)

    def __getitem__(self, item) -> SingleDerivative | tuple[SingleDerivative, ...]:
        return self.parts[item]

    def __iter__(self):
        yield from self.parts.__iter__()

    def build_derivative_fn(
        self, func: DerivableGraphFunction, return_graph: bool, argnum: int
    ) -> DerivableGraphFunction:
        # Work our way from right to left creating the derivative evaluators

        func = self[0].evaluator(func, return_graph)
        for part in self[1:]:
            func = part.evaluator(func, return_graph, argnum=self.paths[part.wrt.key_path])

        return func


@dataclasses.dataclass(frozen=True)
class Evaluator:
    func: DerivableGraphFunction
    spec: Derivative
    return_graph: bool
    argnum: int
    scale: float = 1.0

    # will be set in __post_init__
    _evaluate_at: DerivableGraphFunction = dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self,
            "_evaluate_at",
            self.spec.build_derivative_fn(self.func, return_graph=True, argnum=self.argnum),
        )

    def __call__(
        self, graph: jraph.GraphsTuple, *args: jt.PyTree
    ) -> jt.Array | tuple[jt.Array, jraph.GraphsTuple]:
        value, graph_out = self._evaluate_at(graph, *args)
        if self.spec.out.indices is not None and not len(value.shape) == len(self.spec.out.indices):
            raise ValueError(
                f"The output array rank ({len(value.shape)}) does not match the "
                f"passed number of output indices '{self.spec.out.indices}' "
                f"({len(self.spec.out.indices)})"
            )
        value = self.scale * value

        if self.return_graph:
            return value, graph_out

        return value


def diff(
    *func_of,
    wrt: GraphEntrySpecLike | Sequence[GraphEntrySpecLike],
    out: GraphEntrySpecLike = None,
    scale: float = 1.0,
    return_graph=False,
) -> Evaluator:
    of: Optional[GraphEntrySpecLike]

    if len(func_of) == 1:
        func, of = func_of[0], None
    else:
        func, of = func_of

    if isinstance(wrt, str):
        deriv = SingleDerivative.create(of, wrt, out)
    elif len(wrt) == 1:
        deriv = SingleDerivative.create(of, wrt[0], out)
    else:
        deriv = MultiDerivative.create(of, wrt, out)

    transformed = _base.transform_fn(
        func,
        *deriv.wrt_paths,
        outs=tuple() if not deriv.of or not deriv.of.key_path else [deriv.of.key_path],
        return_graphs=True,
    )

    return deriv.evaluator(transformed, return_graph, scale=scale)


def ordered_unique_indices(lst):
    seen = {}
    return [i for i, x in enumerate(lst) if x not in seen and not seen.setdefault(x, True)]


def find_index_permutation(lst_a, lst_b) -> list[int]:
    index_map = {value: idx for idx, value in enumerate(lst_a)}
    return [index_map[x] for x in lst_b]
