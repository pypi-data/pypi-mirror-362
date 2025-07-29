To do development on the Mock Event Generator package, and more specifically, to run the unit tests, it is required to install the [GraceDB Test Double](), which contains non-public information. That is why it should be installed from the GitLab Package Registry, instead of the Python Package Index.

To do so, let's first create a GitLab [Personal Access Token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) with the read_api scope. Once the token is created, add this line to your .netrc file:

```
machine git.ligo.org login <token-name> password <access-token>
```

To install the package in a virtual environment:
```bash
git clone git@git.ligo.org:emfollow/mock-event-generator.git
cd mock-event-generator
python3.11 -mvenv venv
source venv/bin/activate
pip install --extra-index-url https://git.ligo.org/api/v4/projects/11906/packages/pypi/simple -e ".[tests]"
```

To run the unit tests (with a mocked GraceDB server):
```bash
$ pytest
```

To run the end-to-end tests (using the playground GraceDB server, instead of the Test Double):
```bash
$ pytest e2e
```

The project uses [pre-commit](https://pre-commit.com) to ensure code quality and uniformity. To succeed, every commit requires to pass a list of checkers and formatters.
```bash
pip install --user pre-commit
pre-commit install
```
