# Copyright 2023-2025 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Library of functions for iterating iterables.
---------------------------------------------

- Concatenating and merging iterables
- Dropping and taking values from iterables
- Reducing and accumulating iterables
- Assumptions

  - iterables are not necessarily iterators
  - at all times iterator protocol is assumed to be followed

    - all iterators are assumed to be iterable
    - for all iterators ``foo`` we assume ``iter(foo) is foo``

"""

from __future__ import annotations

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2023-2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'

from collections.abc import Callable, Iterable, Iterator
from enum import auto, Enum
from typing import cast, Never
from pythonic_fp.containers.box import Box
from pythonic_fp.containers.maybe import MayBe
from pythonic_fp.fptools.function import negate, swap
from pythonic_fp.fptools.singletons import NoValue

__all__ = [
    'FM',
    'concat',
    'merge',
    'exhaust',
    'drop',
    'drop_while',
    'take',
    'take_while',
    'take_split',
    'take_while_split',
    'accumulate',
    'reduce_left',
    'fold_left',
    'maybe_fold_left',
    'sc_reduce_left',
    'sc_reduce_right',
]

# Iterate over multiple iterables


class FM(Enum):
    """Iterable Blending Enums.

    - *CONCAT:* Concatenate iterables first to last
    - *MERGE:* Merge iterables until one is exhausted
    - *EXHAUST:* Merge iterables until all are exhausted

    """
    CONCAT = auto()
    MERGE = auto()
    EXHAUST = auto()


def concat[D](*iterables: Iterable[D]) -> Iterator[D]:
    """Sequentially concatenate multiple iterables together.

    .. code:: python

        def concat[D](iterable: Iterable[D]) -> Iterator[D]

    - pure Python version of standard library's ``itertools.chain``
    - iterator sequentially yields each iterable until all are exhausted
    - an infinite iterable will prevent subsequent iterables from yielding any values
    - performant to ``itertools.chain``

    :param iterables: iterables to concatenate
    :return: concatenated iterators

    """
    for iterator in map(lambda x: iter(x), iterables):
        while True:
            try:
                value = next(iterator)
                yield value
            except StopIteration:
                break


def merge[D](*iterables: Iterable[D], yield_partials: bool = False) -> Iterator[D]:
    """Shuffle together ``iterables`` until one is exhausted.

    .. code:: python

        def merge[D](iterable: Iterable[D], yield_partials: bool) -> Iterator[D]

    If ``yield_partials`` is true

    - yield any unmatched yielded values from other iterables
    - prevents data lose if any of the iterables are iterators with external references

    :param iterables: iterables to merge until one gets exhausted
    :return: merged iterators

    """
    iter_list = list(map(lambda x: iter(x), iterables))
    values = []
    if (num_iters := len(iter_list)) > 0:
        while True:
            try:
                for ii in range(num_iters):
                    values.append(next(iter_list[ii]))
                yield from values
                values.clear()
            except StopIteration:
                break
        if yield_partials:
            yield from values


def exhaust[D](*iterables: Iterable[D]) -> Iterator[D]:
    """Shuffle together multiple iterables until all are exhausted.

    .. code:: python

        def exhaust[D](iterable: Iterable[D]) -> Iterator[D]

    :param iterables: iterables to exhaustively merge
    :return: merged iterators

    """
    iter_list = list(map(lambda x: iter(x), iterables))
    if (num_iters := len(iter_list)) > 0:
        ii = 0
        values = []
        while True:
            try:
                while ii < num_iters:
                    values.append(next(iter_list[ii]))
                    ii += 1
                yield from values
                ii = 0
                values.clear()
            except StopIteration:
                num_iters -= 1
                if num_iters < 1:
                    break
                del iter_list[ii]

        yield from values


## dropping and taking


def drop[D](iterable: Iterable[D], n: int) -> Iterator[D]:
    """Drop the next n values from iterable.

    .. code:: python

        def drop[D](
            iterable: Iterable[D],
            n: int
        ) -> Iterator[D]

    :param iterable: iterable whose values are to be dropped
    :param n: number of values to be dropped
    :return: an iterator of the remaining values

    """
    it = iter(iterable)
    for _ in range(n):
        try:
            next(it)
        except StopIteration:
            break
    return it


def drop_while[D](iterable: Iterable[D], pred: Callable[[D], bool]) -> Iterator[D]:
    """Drop initial values from iterable while predicate is true.

    .. code:: python

        def drop_while[D](
            iterable: Iterable[D],
            pred: Callable[[D], bool]
        ) -> Iterator[D]

    :param iterable: iterable whose values are to be dropped
    :param pred: Boolean valued function
    :return: an iterator beginning where pred returned false

    """
    it = iter(iterable)
    while True:
        try:
            value = next(it)
            if not pred(value):
                it = concat((value,), it)
                break
        except StopIteration:
            break
    return it


def take[D](iterable: Iterable[D], n: int) -> Iterator[D]:
    """Return an iterator of up to n initial values of an iterable.

    .. code:: python

        def take[D](
            iterable: Iterable[D],
            n: int
        ) -> Iterator[D]

    :param iterable: iterable providing the values to be taken
    :param n: number of values to be dropped
    :return: an iterator of up to n initial values from iterable

    """
    it = iter(iterable)
    for _ in range(n):
        try:
            value = next(it)
            yield value
        except StopIteration:
            break


def take_while[D](iterable: Iterable[D], pred: Callable[[D], bool]) -> Iterator[D]:
    """Yield values from iterable while predicate is true.

    .. code:: python

        def take_while[D](
            iterable: Iterable[D],
            pred: Callable[[D], bool]
        ) -> Iterator[D]

    .. warning::
        Risk of value loss if iterable is multiple referenced iterator.

    :param iterable: iterable providing the values to be taken
    :param pred: Boolean valued function
    :return: an Iterator of up to n initial values from the iterable

    """
    it = iter(iterable)
    while True:
        try:
            value = next(it)
            if pred(value):
                yield value
            else:
                break
        except StopIteration:
            break


def take_split[D](iterable: Iterable[D], n: int) -> tuple[Iterator[D], Iterator[D]]:
    """Same as take except also return iterator of remaining values.

    .. code:: python

        def take_split[D](
            iterable: Iterable[D],
            n: int
        ) -> tuple[Iterator[D], Iterator[D]]

    .. Warning::

       **CONTRACT:** Do not access the second returned iterator until the
       first one is exhausted.

    :param iterable: iterable providing the values to be taken
    :param n: maximum number of values to be taken
    :return: an iterator of values taken and an iterator of remaining values

    """
    it = iter(iterable)
    itn = take(it, n)

    return itn, it


def take_while_split[D](
    iterable: Iterable[D], pred: Callable[[D], bool]
) -> tuple[Iterator[D], Iterator[D]]:
    """Yield values from iterable while predicate is true.

    .. code:: python

        def take_while_split[D](
            iterable: Iterable[D],
            pred: Callable[[D], bool]
        ) -> tuple[Iterator[D], Iterator[D]]

    .. Warning::

       **CONTRACT:** Do not access the second returned iterator until
       the first one is exhausted.

    :param iterable: iterable providing the values to be taken
    :param pred: Boolean valued function
    :return: an iterator of values taken and an iterator of remaining values

    """
    def _take_while(
        it: Iterator[D], pred: Callable[[D], bool], val: Box[D]
    ) -> Iterator[D]:
        while True:
            try:
                val.put(next(it))
                if pred(val.get()):
                    yield val.pop()
                else:
                    break
            except StopIteration:
                break

    it = iter(iterable)
    value: Box[D] = Box()
    it_pred = _take_while(it, pred, value)

    return (it_pred, concat(value, it))


## reducing and accumulating


def accumulate[D, L](
        iterable: Iterable[D],
        f: Callable[[L, D], L],
        initial: L | NoValue = NoValue()
    ) -> Iterator[L]:
    """Returns an iterator of partial fold values.

    .. code:: python

        def accumulate[D, L](
            iterable: Iterable[D],
            f: Callable[[L, D], L],
            initial: L
        ) -> Iterator[L]

    A pure Python version of standard library's ``itertools.accumulate``

    - function ``f`` does not default to addition (for typing flexibility)
    - begins accumulation with an "optional" ``initial`` value

    :param iterable: iterable to be folded
    :param f: 2 parameter function, first parameter for accumulated value
    :param initial: "optional" initial value to start fold
    :return: an iterator of the intermediate fold values

    """
    it = iter(iterable)
    try:
        it0 = next(it)
    except StopIteration:
        if initial is NoValue():
            return
        yield cast(L, initial)
    else:
        if initial is not NoValue():
            init = cast(L, initial)
            yield init
            acc = f(init, it0)
            for ii in it:
                yield acc
                acc = f(acc, ii)
            yield acc
        else:
            acc = cast(L, it0)  # in this case L = D
            for ii in it:
                yield acc
                acc = f(acc, ii)
            yield acc


def reduce_left[D](iterable: Iterable[D], f: Callable[[D, D], D]) -> D | Never:
    """Fold an iterable left with a function.

    .. code:: python

        def reduce_left[D](
            iterable: Iterable[D],
            f: Callable[[D, D], D]
        ) -> D | Never

    .. Warning::

       This function never return if given an infinite iterable.

    .. Warning::

       This function does not catch or re-raises exceptions from ``f``.

    :param iterable: iterable to be reduced (folded)
    :param f: 2 parameter function, first parameter for accumulated value
    :return: reduced value from the iterable
    :raises StopIteration: when called on an empty circular array
    :raises Exception: does not catch or re-raises exceptions from ``f``.

    """
    it = iter(iterable)
    try:
        acc = next(it)
    except StopIteration as exc:
        msg = 'Attempt to reduce an empty iterable?'
        raise StopIteration(msg) from exc

    for v in it:
        acc = f(acc, v)

    return acc


def fold_left[D, L](
        iterable: Iterable[D],
        f: Callable[[L, D], L],
        initial: L
    ) -> L | Never:
    """Fold an iterable left with a function and initial value.

    .. code:: python

        def fold_left[D, L](
            iterable: Iterable[D],
            f: Callable[[L, D], L],
            initial: L
        ) -> L | Never

    - not restricted to ``__add__`` for the folding function
    - initial value required, does not default to ``0`` for initial value
    - handles non-numeric data just find

    .. Warning::

       This function never return if given an infinite iterable.

    .. Warning::

       This function does not catch any exceptions ``f`` may raise.

    :param iterable: iterable to be folded
    :param f: 2 parameter function, first parameter for accumulated value
    :param initial: mandatory initial value to start fold
    :return: the folded value

    """
    acc = initial
    for v in iterable:
        acc = f(acc, v)
    return acc


def maybe_fold_left[D, L](
        iterable: Iterable[D],
        f: Callable[[L, D], L],
        initial: L | NoValue = NoValue()
    ) -> MayBe[L] | Never:
    """Folds an iterable left with an "optional" initial value..

    .. code:: python

        def maybe_fold_left[D, L](
            iterable: Iterable[D],
            f: Callable[[L, D], L],
            initial: L
        ) -> MayBe[L] | Never

    - traditional FP type order given for function ``f``
    - when an initial value is not given then ``L = D``
    - if iterable empty and no ``initial`` value given, return ``MayBe()``

    .. Warning::

       This function never return if given an infinite iterable.

    .. Warning::

       This function does not catch any exceptions ``f`` may raise.

    :param iterable: The iterable to be folded.
    :param f: First argument is for the accumulated value.
    :param initial: Mandatory initial value to start fold.
    :return: Folded value if it exists.

    """
    acc: L
    it = iter(iterable)
    if initial is NoValue():
        try:
            acc = cast(L, next(it))  # in this case L = D
        except StopIteration:
            return MayBe()
    else:
        acc = cast(L, initial)

    for v in it:
        try:
            acc = f(acc, v)
        except Exception:
            return MayBe()

    return MayBe(acc)


def sc_reduce_left[D](
        iterable: Iterable[D],
        f: Callable[[D, D], D],
        start: Callable[[D], bool] = (lambda d: True),
        stop: Callable[[D], bool] = (lambda d: False),
        include_start: bool = True,
        include_stop: bool = True,
    ) -> tuple[MayBe[D], Iterator[D]]:
    """Short circuit version of a left reduce.

    .. code:: python

        def sc_reduce_left[D](
            iterable: Iterable[D],
            f: Callable[[D, D], D],
            start: Callable[[D], bool],
            stop: Callable[[D], bool],
            include_start: bool,
            include_stop: bool
        ) -> tuple[MayBe[D], Iterator[D]]

    Useful for infinite iterables.

    Behavior for default arguments will

    - left reduce finite iterable
    - start folding immediately
    - continue folding until end (of a possibly infinite iterable)

    :param iterable: iterable to be reduced from the left
    :param f: 2 parameter function, first parameter for accumulated value
    :param start: delay starting the fold until it returns true
    :param stop: prematurely stop the fold when it returns true
    :param include_start: if true, include fold starting value in fold
    :param include_stop: if true, include stopping value in fold
    :return: MayBe of the folded value and remaining iterables

    """
    it_start = drop_while(iterable, negate(start))
    if not include_start:
        try:
            next(it_start)
        except StopIteration:
            pass
    it_reduce, it_rest = take_while_split(it_start, negate(stop))
    mb_reduced = maybe_fold_left(it_reduce, f)
    if include_stop:
        if mb_reduced:
            try:
                last = next(it_rest)
                mb_reduced = MayBe(f(mb_reduced.get(), last))
            except StopIteration:
                pass
        else:
            try:
                last = next(it_rest)
                mb_reduced = MayBe(last)
            except StopIteration:
                pass

    return (mb_reduced, it_rest)


def sc_reduce_right[D](
        iterable: Iterable[D],
        f: Callable[[D, D], D],
        start: Callable[[D], bool] = (lambda d: False),
        stop: Callable[[D], bool] = (lambda d: False),
        include_start: bool = True,
        include_stop: bool = True,
    ) -> tuple[MayBe[D], Iterator[D]]:
    """Short circuit version of a right reduce.

    .. code:: python

        def sc_reduce_left[D](
            iterable: Iterable[D],
            f: Callable[[D, D], D],
            start: Callable[[D], bool],
            stop: Callable[[D], bool],
            include_start: bool,
            include_stop: bool
        ) -> Tuple[MayBe[D] | Iterator[D]

    Useful for infinite and non-reversible iterables.

    Behavior for default arguments will

    - right reduce finite iterable
    - start folding at end (of a possibly infinite iterable)
    - continue reducing right until beginning

    :param iterable: iterable to be reduced from the right
    :param f: 2 parameter function, second parameter for accumulated value
    :param start: delay starting the fold until it returns true
    :param stop: prematurely stop the fold when it returns true
    :param include_start: if true, include fold starting value in fold
    :param include_stop: if true, include stopping value in fold
    :return: MayBe of the folded value and remaining iterables

    """
    it_start, it_rest = take_while_split(iterable, negate(start))
    list1 = list(it_start)
    if include_start:
        try:
            begin = next(it_rest)
        except StopIteration:
            pass
        else:
            list1.append(begin)

    list1.reverse()
    it_reduce, it_stop = take_while_split(list1, negate(stop))

    mb_reduced = maybe_fold_left(it_reduce, swap(f))
    if include_stop:
        try:
            end = next(it_stop)
        except StopIteration:
            pass
        else:
            if mb_reduced:
                mb_reduced = MayBe(f(end, mb_reduced.get()))
            else:
                mb_reduced = MayBe(end)

    return (mb_reduced, it_rest)
