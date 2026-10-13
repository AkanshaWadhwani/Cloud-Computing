# Member 3 — CI/CD implementation notes

## Implemented
- `.github/workflows/ci-cd.yml`: GitHub Actions workflow for Python dependency installation, automated tests, and Docker image build.
- `pytest.ini`: corrected test discovery path from the absent `05_API_TESTS` folder to the repository's actual `tests` folder.
- `README.md`: local run, tests, Docker commands, workflow behavior, and security notes.

## Workflow behavior
The workflow runs for pushes to `main` and pull requests targeting `main`. It checks out the repository, sets up Python 3.12, installs requirements, runs `pytest -q`, and builds the Docker image.

## Not yet configured
Publishing an image and cloud deployment are intentionally not enabled yet. Confirm the container registry with Member 2 and the cloud provider/deployment method with Member 4 before adding secrets or deployment actions.
