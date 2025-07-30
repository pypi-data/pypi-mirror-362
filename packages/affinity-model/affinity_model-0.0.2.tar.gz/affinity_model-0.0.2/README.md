# affinity-model

[![PyPI version](https://img.shields.io/pypi/v/affinity-model)](https://pypi.org/project/affinity-model/)

Pydantic data model for [Affinity](https://www.affinity.co).

## 🚀 Releasing a New Version

To release a new version of this package to PyPI:

1. **Decide on the new version number** following
   [semantic versioning](https://semver.org/) (e.g., v1.2.3).
2. **Create a new git tag** with the version number:

   ```sh
   git tag v1.2.3
   git push origin v1.2.3
   ```

3. **(Optional)**: Create a GitHub Release for the tag to add release notes.

This will trigger the GitHub Actions workflow to build
and publish the package to PyPI automatically.
The version in the published package will match the tag
(thanks to dynamic versioning).

For more details, see the workflow and dynamic versioning setup in `pyproject.toml`.
