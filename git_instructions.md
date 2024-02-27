# Project Name: Git Command Usage Guide

## Overview:
This guide provides a set of essential Git commands for managing branches, committing changes, and merging branches. It is intended to assist in smooth collaboration and version control within your development workflow.

### Set of Git Commands:

1. Create a Branch: `git checkout -b <branch_name> <from which branch>`

This command is used to create a new branch from an existing one.

2. Change Current Branch: `git checkout <branch_name>`

Use this command to switch to a different branch.

3. Add & Commit Changes: `git commit -am "<message goes here>"`

This command stages all modified files and commits them with a descriptive message.

4. Merge Two Branches:

```
git checkout development
git merge --no-ff <branch_name you worked on>
``` 

These commands merge changes from another branch into the current one.

### Example Workflow:

Given your branching strategy:

- **Main Branch:** `main` (never push changes directly)
- **Development Branch:** `development` (for feature development and testing)

Here's an example workflow:

1. Switch to Development Branch:

`git checkout development`

2. Create a Feature Branch:

`git checkout -b create_neural_network_unity_plot development`

This creates a new branch named `create_neural_network_unity_plot` from `development`.

3. Commit Changes:
```
git add .
git commit -m "<message here>"
```
Ensure to provide a concise message summarizing the changes made.

4. Merge Feature Branch with Development:
```
git checkout development
git merge --no-ff create_neural_network_unity_plot
```
Merge the feature branch into `development`.

5. Push Changes:
```
git push origin development
git push origin create_neural_network_unity_plot
```
Push changes to the remote repository.

6. Finalize Changes:
If everything works fine, merge `development` into `main`:
```
git checkout main
git merge --no-ff development
```
Then push changes to the main branch:

`git push`

### Note:
- Always pull changes from `development` before committing to ensure your branch is up to date:

`
git pull development
`

Following this workflow ensures proper version control and collaboration in your project. Happy coding! 🚀

This markdown can be copied and pasted into a README.md file in your project repository.