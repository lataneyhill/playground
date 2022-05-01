# Playground

## Content

### Projects

- dcomposer: A web front-end for generating docker-compose.yaml files
- life et al: An implementation of game of life with the standard Conway rule and support for custom rules
- pyml: An exceedingly small subset of the OCaml frontend in Python
  - https://craftinginterpreters.com/
  - https://ruslanspivak.com/lsbasi-part1/

### Skeletons

- script.bash: A template for bash scripts

## Style

### Commit Messages

Based on [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0)

Structure:
~~~
<type>(scope): <brief description>

[optional body]

[optional footer(s)]
~~~

where:
1. type is one of
   - build: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
   - chore: non-production changes, repository maintenance
   - ci: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
   - docs: Documentation only changes
   - feature: introduces a new feature to the codebase (this correlates with MINOR in Semantic Versioning).
   - fix: patches a bug in your codebase (this correlates with PATCH in Semantic Versioning).
   - perf: A code change that improves performance
   - refactor: A code change that neither fixes a bug nor adds a feature
   - revert: followed by the original message of the reverted commit. The body should say: This reverts commit <hash>., where the hash is the SHA of the commit being reverted.
   - style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
   - test: Adding missing tests or correcting existing tests
1. scope is the project name
1. BREAKING CHANGE: a commit that has a footer BREAKING CHANGE:, or appends a ! after the type/scope, introduces a breaking API change (correlating with MAJOR in Semantic Versioning). A BREAKING CHANGE can be part of commits of any type.
1. footers other than BREAKING CHANGE: <description> may be provided and follow a convention similar to [git trailer format](https://git-scm.com/docs/git-interpret-trailers).
