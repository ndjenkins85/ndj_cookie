# Release

Releases to be carried out from the master branch with a tagged commit.
We have Github actions which will:

- Run all tests
- Publish codebase to jFrog
- Publish documentation to confluence
- Update the README badges

The process for performing a release is as follows:

- [ ] Merge all feature branches into dev branch
- [ ] On local dev branch, increment the project version by updating `lighthouse_fd.__init__.py`
- [ ] Ensure the project README is current
- [ ] Commit changes, and use `git tag` to tag the comment using the same version as per poetry
- [ ] Push to Github using `git push origin master --tags`
- [ ] Raise a pull request for `dev -> master`
- [ ] Draft new release, referencing the latest tag
