CHANGELOG
=========

PyPI pythonic-fp.iterables project.

Semantic Versioning
-------------------

Strict 3 digit semantic versioning adopted 2025-05-19.

- **MAJOR** version incremented for incompatible API changes
- **MINOR** version incremented for backward compatible added functionality
- **PATCH** version incremented for backward compatible bug fixes

See `Semantic Versioning 2.0.0 <https://semver.org>`_.

Releases and Important Milestones
---------------------------------

4.0.0 - 2025-07-16
~~~~~~~~~~~~~~~~~~

Primary purpose was to bring Sphinx documentation in alignment
with other pythonic-fp projects. Ended up making substantial
Sphinx documentation improvements. Will use this documentation
for the other pythonic-fp projects.

- API change

  - renamed pythonic_fp.iterables.foldl to pythonic_fp.iterables.fold_left

3.0.0 - 2025-07-06
~~~~~~~~~~~~~~~~~~

First PyPI release as ``pythonic-fp.iterables``

- dropping dtools namespace name because there is a repo by that name.

2.0.0 - 2025-05-22
~~~~~~~~~~~~~~~~~~

- Moved dtools.fp.iterables to its own PyPI project

  - dtools.iterables

- Moved dtools.fp.err_handling to the dtools.containers PyPI project

  - Moved class MayBe -> module dtools.containers.maybe
  - Moved class Xor -> module dtools.containers.xor
  - dropped lazy methods

    - will import dtools.fp.lazy directly for this functionality

1.7.0 - 2025-04-22
~~~~~~~~~~~~~~~~~~

Last PyPI release as dtools.fp

- API changes along the lines of dtools.ca 3.12
- typing improvements
- docstring changes
- pyproject.toml standardization

1.6.0 - 2025-04-07
~~~~~~~~~~~~~~~~~~

- typing improvements

1.4.0 - 2025-03-16
~~~~~~~~~~~~~~~~~~

- much work dtools.iterables

  - finally implemented scReduceL and scReduceR functions
  - tweaked API across iterables module

1.3.0 - 2025-01-17
~~~~~~~~~~~~~~~~~~

First release as dtools.fp

Repo name changes.

- GitHub: fp -> dtools-fp
- PyPI: grscheller.fp -> dtools.fp

1.0.1 - 2024-10-20
~~~~~~~~~~~~~~~~~~

- removed docs from repo
- docs for all grscheller namespace projects maintained here
 
  - https://grscheller.github.io/grscheller-pypi-namespace-docs/

1.0.0 - 2024-10-18
~~~~~~~~~~~~~~~~~~

Decided to make this release first stable release.

- renamed module fp.woException to fp.err_handling
- pytest improvements based on pytest documentation

0.4.0 - 2024-10-03
~~~~~~~~~~~~~~~~~~

Long overdue PyPI release.

0.3.4.0 - 2024-09-30
~~~~~~~~~~~~~~~~~~~~

Development environment only.

- API change for fp.iterables

  - function name changes

    - ``foldL``, ``foldR``, ``foldLsc``, ``foldRsc``
    - ``sc`` stands for "short circuit"

  - all now return class woException.MB

0.3.3.7 - 2024-09-22
~~~~~~~~~~~~~~~~~~~~

Development environment only.

- added more functions to fp.iterables module

  - take(it: Iterable[D], n: int) -> Iterator[D]
  - takeWhile(it: Iterable[D], pred: Callable\[[D], bool\]) -> Iterator[D]
  - drop(it: Iterable[D], n: int) -> Iterator[D]
  - dropWhile(it: Iterable[D], pred: Callable\[[D], bool\]) -> Iterator[D]

0.3.3.4 - 2024-09-16
~~~~~~~~~~~~~~~~~~~~

Development environment only.

- fp.iterables ``foldL_sc`` & ``foldR_sc`` now have

  - common paradigm
  - similar signatures

0.3.3.3 - 2024-09-15
~~~~~~~~~~~~~~~~~~~~

Development environment only.

- added fp.iterables function ``foldR_sc``

  - shortcut version of ``foldR``
  - not fully tested
  - docstring not updated

0.3.3.2 - 2024-09-14
~~~~~~~~~~~~~~~~~~~~

Development environment only.

- added fp.iterables function ``foldL_sc``

  - shortcut version of foldL

0.3.1 - 2024-08-20
~~~~~~~~~~~~~~~~~~

Now fp.iterables no longer exports ``CONCAT``, ``MERGE``, ``EXHAUST``.

- for grscheller.datastructures

  - grscheller.datastructures.ftuple
  - grscheller.datastructures.split_ends

0.2.0 - 2024-07-26
~~~~~~~~~~~~~~~~~~

- from last PyPI release

  - added accumulate function to fp.iterators

- overall much better docstrings

0.1.0 - 2024-07-11
~~~~~~~~~~~~~~~~~~

Initial PyPI release as grscheller.fp

Replicated functionality from grscheller.datastructures.

- ``grscheller.core.iterlib -> grscheller.fp.iterators``
