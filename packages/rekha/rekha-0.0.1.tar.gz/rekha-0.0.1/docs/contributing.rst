Contributing to Rekha
=====================

We welcome contributions to Rekha! This guide will help you get started.

Getting Started
---------------

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

   .. code-block:: bash

      git clone https://github.com/yourusername/rekha.git
      cd rekha

3. **Create a virtual environment**:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

4. **Install in development mode**:

   .. code-block:: bash

      make install-dev

5. **Install pre-commit hooks**:

   .. code-block:: bash

      pre-commit install

Development Workflow
--------------------

1. **Create a feature branch**:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. **Make your changes** following our coding standards

3. **Run quality checks**:

   .. code-block:: bash

      make format      # Format all code
      make lint        # Run all linters
      make test        # Run all tests

4. **Build documentation**:

   .. code-block:: bash

      make docs

5. **Commit your changes**:

   .. code-block:: bash

      git add .
      git commit -m "feat: add your feature description"

6. **Push and create a pull request**

Coding Standards
----------------

Code Style
~~~~~~~~~~

- Follow **PEP 8** Python style guidelines
- Use **Black** for code formatting (line length: 88)
- Use **isort** for import sorting
- Follow **Google-style docstrings** with NumPy extensions

Documentation
~~~~~~~~~~~~~

- All public functions must have comprehensive docstrings
- Include **Parameters**, **Returns**, **Examples** sections
- Use **reStructuredText** for documentation files
- Include type hints for all function parameters and returns

Testing
~~~~~~~

- Write **pytest** tests for all new functionality
- Aim for **>90% code coverage**
- Include **integration tests** for plot generation
- Test **both light and dark themes**
- Test **export functionality**

Examples
~~~~~~~~

- Provide **working examples** for new features
- Include examples in **docstrings**
- Add **gallery examples** for significant features
- Test examples in **CI/CD pipeline**

Types of Contributions
----------------------

Bug Fixes
~~~~~~~~~~

- Check existing issues before reporting
- Include **minimal reproduction** example
- Add **test case** that fails before fix
- Update documentation if needed

New Features
~~~~~~~~~~~~

- **Discuss in an issue** before implementing large features
- Follow existing **API patterns**
- Include comprehensive **documentation**
- Add **examples** and **tests**

Documentation
~~~~~~~~~~~~~

- Fix **typos** and **unclear explanations**
- Add **missing examples**
- Improve **API documentation**
- Translate documentation (contact maintainers)

Performance
~~~~~~~~~~~

- Profile **before and after** changes
- Include **benchmarks** for performance improvements
- Consider **memory usage** impact
- Test with **large datasets**

Architecture Guidelines
-----------------------

Plot Class Design
~~~~~~~~~~~~~~~~~

All plot types should:

- **Inherit from BasePlot** for consistency
- **Override _create_plot()** method for plot-specific logic
- **Follow uniform parameter naming** conventions
- **Support all common styling options**

Color and Theme System
~~~~~~~~~~~~~~~~~~~~~~

- Use **theme-aware colors** from color palette
- Support **dark mode** automatically
- Include **grayscale printing** optimization
- Follow **accessibility guidelines**

Data Handling
~~~~~~~~~~~~~

- Support **pandas DataFrames**, **dictionaries**, and **arrays**
- **Validate input data** appropriately
- Handle **missing values** gracefully
- Provide **clear error messages**

API Design Principles
~~~~~~~~~~~~~~~~~~~~~

- **Consistent naming** across all functions
- **Sensible defaults** for all parameters
- **Comprehensive docstrings** with examples
- **Backward compatibility** when possible

Release Process
---------------

Version Numbering
~~~~~~~~~~~~~~~~~

We follow **Semantic Versioning (SemVer)**:

- **MAJOR**: Incompatible API changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

Release Checklist
~~~~~~~~~~~~~~~~~

1. **Update version** in ``pyproject.toml``
2. **Update CHANGELOG.md** with release notes
3. **Run full test suite** on multiple Python versions
4. **Build and test documentation**
5. **Create release tag** and **GitHub release**
6. **Publish to PyPI** via GitHub Actions

Documentation Build
-------------------

Building Locally
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   cd docs
   pip install -r requirements.txt
   make html
   # Open _build/html/index.html

Live Reload
~~~~~~~~~~~

.. code-block:: bash

   cd docs
   make livehtml
   # Opens browser with auto-reload

API Documentation
~~~~~~~~~~~~~~~~~

API docs are **auto-generated** from docstrings using Sphinx autodoc.
To rebuild API docs:

.. code-block:: bash

   sphinx-apidoc -o docs/api rekha/

Testing Guidelines
------------------

Unit Tests
~~~~~~~~~~

- Test **individual functions** in isolation
- Mock **external dependencies** when appropriate
- Use **parametrized tests** for multiple inputs
- Test **edge cases** and **error conditions**

Integration Tests
~~~~~~~~~~~~~~~~~

- Test **complete workflows** end-to-end
- Generate **actual plots** and verify output
- Test **different data formats** and sizes
- Verify **export functionality** works


Community Guidelines
--------------------

Code of Conduct
~~~~~~~~~~~~~~~

- Be **respectful** and **inclusive**
- Focus on **constructive feedback**
- **Help newcomers** get started
- **Credit contributions** appropriately

Communication
~~~~~~~~~~~~~

- Use **GitHub issues** for bug reports and feature requests
- Use **GitHub discussions** for questions and ideas
- Be **clear and specific** in issue descriptions
- **Search existing issues** before creating new ones

Review Process
~~~~~~~~~~~~~~

- All changes require **code review**
- **Maintainers** will review pull requests
- Address **feedback promptly** and professionally
- **Squash commits** before merging when appropriate

Recognition
-----------

Contributors are recognized in:

- **CONTRIBUTORS.md** file
- **Release notes** for significant contributions
- **Documentation credits**
- **GitHub contributors** page

Maintainer Responsibilities
---------------------------

Current maintainers handle:

- **Code review** and **merging** pull requests
- **Release management** and **versioning**
- **Issue triage** and **bug prioritization**
- **Community communication** and **support**
- **Strategic direction** and **roadmap planning**

Getting Help
------------

If you need help:

- **Check the documentation** first
- **Search existing issues** and discussions
- **Create a new issue** with detailed description
- **Join community discussions** for broader questions

Resources
---------

- **Repository**: https://github.com/project-vajra/rekha
- **Documentation**: https://project-vajra.github.io/rekha
- **Issue Tracker**: https://github.com/project-vajra/rekha/issues
- **Discussions**: https://github.com/project-vajra/rekha/discussions

Thank you for contributing to Rekha! 🎨📊