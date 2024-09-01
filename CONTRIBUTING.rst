How to contribute
=================

**Reporting a bug?**

Check if the bug was already reported under
`issues <https://github.com/igor-sb/bluprint/issues>`_. If you are not able to
find an open issue addressing the problem, open a
`new issue <https://github.com/igor-sb/bluprint/issues/new>`_.

**Did you write a patch that fixes a bug?**

* Fork the repo, make changes, then create a Pull Request with the patch.
* Ensure the PR description clearly describes the problem and a solution. Link
  the relevant issue if any.
* See code guidelines below.

**Do you intend to add a new feature or change an existing one?**

* Suggest your change as an `issue <https://github.com/igor-sb/bluprint/issues>`_.
* See code guidelines below.

Contributing code guidelines
----------------------------

1. Fork and clone the repo.
2. Ensure you have a development environment setup. This includes correct
   versions of Python, uv as well as R and it's relevant packages if you intend
   to change R project code. Run ``uv venv && uv sync`` to install all
   dependencies, including those in the development group in *pyproject.toml*.
3. After creating a new code, ensure it passes linting and static typing checks;
   run ``make lint``.
4. Add appropriate unit tests and ensure it passes all unit tests; run
   ``make test``.
5. If you make changes to the documentation, you can build it locally using
   ``make docs``, then open *docs/build/index.html* file in your browser.
6. If everything passes correctly, update the Bluprint version in
   *pyproject.toml*.
7. Push the changes to Github.
8. Open a PR from your forked repo.


Thank you for contributing!

Igor
