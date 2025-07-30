.. These are ReST substitutions and links that can be used throughout the docs
   (and docstrings) because they are added to ``docs/conf.py::rst_epilog``.

.. --------------------
.. asyncio replacements
.. --------------------

.. _`event loop`: https://docs.python.org/3/library/asyncio-eventloop.html
.. _coroutine: https://docs.python.org/3/library/asyncio-task.html#coroutines

.. ------------------
.. NumPy replacements
.. ------------------

.. |inf| replace:: `~numpy.inf`
.. |nan| replace:: `~numpy.nan`
.. |ndarray| replace:: :class:`~numpy.ndarray`

.. --------------------
.. Astropy replacements
.. --------------------

.. |Quantity| replace:: :class:`~astropy.units.Quantity`
.. |Time| replace:: :class:`~astropy.time.Time`
.. |TimeDelta| replace:: :class:`~astropy.time.TimeDelta`
.. |Unit| replace:: :class:`~astropy.units.UnitBase`


.. ------
.. Actors
.. ------

.. |Motor| replace:: :class:`~bapsf_motion.actors.motor_.Motor`
.. |Axis| replace:: :class:`~bapsf_motion.actors.axis_.Axis`
.. |Drive| replace:: :class:`~bapsf_motion.actors.drive_.Drive`
.. |MotionGroup| replace:: :class:`~bapsf_motion.actors.motion_group_.MotionGroup`
.. |RunManager| replace:: :class:`~bapsf_motion.actors.manager_.RunManager`

.. ------------------------
.. PKG Common Functionality
.. ------------------------

.. |MotionBuilder| replace:: :class:`~bapsf_motion.motion_builder.core.MotionBuilder`


.. ----------------------
.. PlasmaPy documentation
.. ----------------------

.. The backslash is needed for the substitution to work correctly when
   used just before a period.

.. |bibliography| replace:: :ref:`bibliography`\
.. .. |coding guide| replace:: :ref:`coding guide`\
.. .. |contributor guide| replace:: :ref:`contributor guide`\
.. .. |documentation guide| replace:: :ref:`documentation guide`\
.. |glossary| replace:: :ref:`glossary`\
.. |minpython| replace:: 3.8
.. .. |plasma-calculator| replace:: :ref:`plasmapy-calculator`\
.. .. |release guide| replace:: :ref:`release guide`\
.. .. |testing guide| replace:: :ref:`testing guide`\

.. --------
.. Websites
.. --------

.. _Astropy docs: https://docs.astropy.org
.. _Astropy: https://www.astropy.org
.. _BibTeX format: https://www.bibtex.com/g/bibtex-format
.. _BibTeX: http://www.bibtex.org
.. _black: https://black.readthedocs.io
.. _Conda: https://docs.conda.io
.. _Contributor Covenant: https://www.contributor-covenant.org
.. _create an issue: https://github.com/PlasmaPy/PlasmaPy/issues/new/choose
.. _CSS: https://www.w3schools.com:443/css
.. _DOI: https://www.doi.org
.. _flake8: https://flake8.pycqa.org/en/latest
.. _git: https://git-scm.com
.. _GitHub Actions: https://docs.github.com/en/actions
.. _GitHub Discussions page: https://github.com/PlasmaPy/PlasmaPy/discussions
.. _GitHub Flavored Markdown: https://github.github.com/gfm
.. _GitHub: https://github.com
.. _Gitter bridge: https://gitter.im/PlasmaPy/Lobby
.. _Graphviz: https://graphviz.org
.. _hypothesis: https://hypothesis.readthedocs.io
.. _intersphinx: https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
.. _isort: https://pycqa.github.io/isort
.. _Jinja: https://jinja.palletsprojects.com
.. _Jupyter: https://jupyter.org
.. _LaTeX: https://www.latex-project.org
.. _mailing list: https://groups.google.com/forum/#!forum/plasmapy
.. _make: https://www.gnu.org/software/make
.. _Markdown: https://www.markdownguide.org
.. _MathJax: https://www.mathjax.org
.. _matplotlib: https://matplotlib.org
.. _Matrix chat room: https://app.element.io/#/room/#plasmapy:openastronomy.org
.. _numpydoc: https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard
.. _NumPy: https://numpy.org
.. _OpenPMD: https://www.openpmd.org/
.. _pandas: https://pandas.pydata.org
.. _pip: https://pip.pypa.io
.. _Plasma Hack Week: https://hack.plasmapy.org
.. _PlasmaPy: https://www.plasmapy.org
.. _PlasmaPy meetings: https://www.plasmapy.org/meetings
.. _PlasmaPy's documentation: https://docs.plasmapy.org/en/stable
.. _PlasmaPy's GitHub repository: https://github.com/PlasmaPy/plasmapy
.. _PlasmaPy's Matrix chat room: https://app.element.io/#/room/#plasmapy:openastronomy.org
.. _pre-commit: https://pre-commit.com
.. _`pre-commit.ci`: https://pre-commit.ci
.. _pydocstyle: https://www.pydocstyle.org/en/stable
.. _pygments: https://pygments.org
.. _PyPI: https://pypi.org
.. _pytest: https://docs.pytest.org
.. _Python: https://www.python.org
.. _Python's documentation: https://docs.python.org/3
.. _Read the Docs: https://readthedocs.org
.. _reST: https://docutils.sourceforge.io/rst.html
.. _reStructuredText (reST): https://docutils.sourceforge.io/rst.html
.. _SciPy: https://scipy.org
.. _sphinx_automodapi: https://sphinx-automodapi.readthedocs.io
.. _sphinx-build: https://www.sphinx-doc.org/en/master/man/sphinx-build.html
.. _Sphinx: https://www.sphinx-doc.org
.. _suggestion box: https://docs.google.com/forms/d/e/1FAIpQLSdT3O5iHZrLJRuavFyzoR23PGy0Prfzx2SQOcwJGWtvHyT2lw/viewform?usp=sf_link
.. _towncrier: https://github.com/twisted/towncrier
.. _tox: https://tox.wiki/en/latest
.. _virtualenv: https://pypi.org/project/virtualenv
.. _Wikipedia: https://www.wikipedia.org
.. _Zenodo: https://zenodo.org

.. ----------------------
.. Nested inline literals
.. ----------------------

.. A workaround for nested inline literals so that the filename will get
   formatted like a file but will be a link. In the text, these get used
   with the syntax for a substitution followed by an underscore to
   indicate that it's for a link: |docs/_static|_

.. For these workarounds, if the replacement is something in single back
   ticks (e.g., `xarray`), then it should also be added to
   nitpick_ignore_regex in docs/conf.py so that it doesn't get counted
   as an error in a nitpicky doc build (e.g., tox -e doc_build_nitpicky).

.. _`docs/_static`: https://github.com/PlasmaPy/PlasmaPy/tree/main/docs/_static
.. |docs/_static| replace:: :file:`docs/_static`

.. _`docs/_static/css`: https://github.com/PlasmaPy/PlasmaPy/tree/main/docs/_static/css
.. |docs/_static/css| replace:: :file:`docs/_static/css`

.. _`docs/api_static`: https://github.com/PlasmaPy/PlasmaPy/tree/main/docs/api_static
.. |docs/api_static| replace:: :file:`docs/api_static`

.. _`docs/conf.py`: https://github.com/PlasmaPy/PlasmaPy/blob/main/docs/conf.py
.. |docs/conf.py| replace:: :file:`docs/conf.py`

.. _`docs/glossary.rst`: https://github.com/PlasmaPy/PlasmaPy/blob/main/docs/glossary.rst
.. |docs/glossary.rst| replace:: :file:`docs/glossary.rst`

.. _`docs/common_links.rst`: https://github.com/PlasmaPy/PlasmaPy/blob/main/docs/common_links.rst
.. |docs/common_links.rst| replace:: :file:`docs/common_links.rst`

.. _`docs/bibliography.bib`: https://github.com/PlasmaPy/PlasmaPy/blob/main/docs/bibliography.bib
.. |docs/bibliography.bib| replace:: :file:`docs/bibliography.bib`

.. _h5py: https://www.h5py.org/
.. |h5py| replace:: `h5py`

.. _`IPython.sphinxext.ipython_console_highlighting`: https://ipython.readthedocs.io/en/stable/sphinxext.html?highlight=IPython.sphinxext.ipython_console_highlighting#ipython-sphinx-directive-module
.. |IPython.sphinxext.ipython_console_highlighting| replace:: `IPython.sphinxext.ipython_console_highlighting`

.. _lmfit: https://lmfit.github.io/lmfit-py/
.. |lmfit| replace:: `lmfit`

.. _mpmath: https://mpmath.org/doc/current/
.. |mpmath| replace:: `mpmath`

.. _nbsphinx: https://nbsphinx.readthedocs.io
.. |nbsphinx| replace:: `nbsphinx`

.. _numba: https://numba.readthedocs.io
.. |numba| replace:: `numba`

.. _`setup.cfg`: https://github.com/PlasmaPy/PlasmaPy/blob/main/setup.cfg
.. |setup.cfg| replace:: :file:`setup.cfg`

.. _`sphinxcontrib-bibtex`: https://sphinxcontrib-bibtex.readthedocs.io
.. |sphinxcontrib-bibtex| replace:: `sphinxcontrib-bibtex`

.. _`sphinx_copybutton`: https://sphinx-copybutton.readthedocs.io
.. |sphinx_copybutton| replace:: `sphinx_copybutton`

.. _`sphinx_gallery.load_style`: https://sphinx-gallery.github.io/stable/advanced.html?highlight=load_style#using-only-sphinx-gallery-styles
.. |sphinx_gallery.load_style| replace:: `sphinx_gallery.load_style`

.. _`sphinx_changelog`: https://sphinx-changelog.readthedocs.io
.. |sphinx_changelog| replace:: `sphinx_changelog`

.. _`sphinx-reredirects`: https://documatt.gitlab.io/sphinx-reredirects
.. |sphinx-reredirects| replace:: `sphinx-reredirects`

.. _`sphinx-hoverxref`: https://sphinx-hoverxref.readthedocs.io
.. |sphinx-hoverxref| replace:: `sphinx-hoverxref`

.. _`sphinx-issues`: https://github.com/sloria/sphinx-issues
.. |sphinx-issues| replace:: `sphinx-issues`

.. _`sphinx-notfound-page`: https://sphinx-notfound-page.readthedocs.io
.. |sphinx-notfound-page| replace:: `sphinx-notfound-page`

.. _xarray: https://docs.xarray.dev
.. |xarray| replace:: `xarray`
