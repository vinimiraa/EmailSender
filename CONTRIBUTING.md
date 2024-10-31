# How to Contribute

### Prerequisites

- **Python 3.6** or higher.
- A Python environment (such as **Anaconda**, **virtualenv**, etc.).
- The following packages should be installed:
  - `smtplib`
  - `dotenv`

---

### Steps to Run the Project

1. **Fork** this repository to your GitHub account.
2. **Clone** your fork to your local machine:
   ```bash
   git clone https://github.com/vinimiraa/EmailSender.git
   ```
3. Create a new **branch** for your changes:
   ```bash
   git checkout -b my-branch
   ```
   > **Note:**
   > - **Do not use** the `main` branch for your changes.
   > - Name your branch with your name or a relevant identifier, so the pull request is easily recognizable.

4. Make your **changes** to the code.
5. **Commit** your changes with a clear message:
   ```bash
   git commit -m "my changes"
   ```
6. **Push** your changes to your remote repository on GitHub:
   ```bash
   git push origin my-branch
   ```
7. **Create a Pull Request** directly on GitHub to request the inclusion of your changes.

---

### Syncing with the Original Repository

To ensure your fork is always updated with the original repository, follow these steps before making changes:

1. **Add the original repository** as a remote called `upstream`:
   ```bash
   git remote add upstream https://github.com/vinimiraa/EmailSender.git
   ```
   
2. **Fetch** updates from the original repository:
   ```bash
   git fetch upstream
   ```
   
3. **Merge** updates from the original repository's `dev` branch into your local branch:
   ```bash
   git checkout dev  # Ensure you are on the dev branch
   git merge upstream/dev
   ```

4. Resolve any **conflicts** (if any) and commit the resolutions:
   ```bash
   git add .
   git commit -m "Resolving merge conflicts"
   ```

5. Update your fork on GitHub with the merged changes:
   ```bash
   git push origin dev
   ```

> **Tip:** Always sync your local repository with the original repository before creating a new branch or making changes. This avoids conflicts and ensures you are working with the most up-to-date version of the project.

---

### Submitting a Pull Request

1. Ensure you have **synchronized your local repository** with the original (see synchronization instructions above).
2. Make your changes in a new **branch** created from the `dev` branch:
   ```bash
   git checkout -b branch-name
   ```
3. After making the changes, **add** the modified files:
   ```bash
   git add .
   ```
4. **Commit** the changes with a descriptive message:
   ```bash
   git commit -m "Description of the changes made"
   ```
5. **Push** the branch to your remote repository:
   ```bash
   git push origin branch-name
   ```
6. On GitHub, go to your forked repository and create a **Pull Request**.
   - Select the `dev` branch as the base and your new branch as the comparison branch.
   - Add a clear and detailed description of the changes made.
7. Wait for the **review** from the project maintainers. They may request adjustments or approve the pull request.

---

### Keeping Your Repository Updated

If your local repository becomes outdated compared to the original repository, follow these steps to update it:

1. Update the local repository with changes from the `upstream`:
   ```bash
   git fetch upstream
   git merge upstream/dev
   ```
2. After merging, resolve any conflicts and **push** the changes to your remote repository:
   ```bash
   git push origin dev
   ```

---

### Commit Rules

Following a clear pattern for commit messages makes it easier to read and understand the project's history. Below are guidelines and suggestions for structuring your commit messages:

#### Commit Message Format

Each commit message should follow the format below:

```
<type>: <concise description>

[Optional body of the message]
```

1. **`<type>`**: The type of change you are making.
2. **`<concise description>`**: A brief description of the changes (max 72 characters).
3. **Body (optional)**: A more detailed explanation of what was changed, if necessary. Here, you can describe the reason for the change and, if applicable, the consequences of the changes. Use lines of up to 72 characters to ensure the commit body is easy to read in various Git tools.

#### Commit Types

Here are some common commit types you can use:

- **feat**: When you are adding a new feature.
  - Example: `feat: implement email sending functionality`
  
- **fix**: When you are fixing a bug.
  - Example: `fix: resolve issue with missing attachments`

- **docs**: For changes in documentation.
  - Example: `docs: update README with usage instructions`

- **style**: Style changes, such as code formatting, without changing logic.
  - Example: `style: adjust indentation in smtp_mail.py`

- **refactor**: For changes to code that do not alter functionality but improve structure.
  - Example: `refactor: reorganize methods for better readability`

- **test**: For adding or fixing unit tests.
  - Example: `test: add test for email sending functionality`

- **perf**: For performance improvements.
  - Example: `perf: optimize email sending for large attachments`

- **build**: Changes that affect the build system or external dependencies (like build configuration files, dependencies).
  - Example: `build: update requirements.txt to include dotenv`

#### Examples of Commit Messages

Here are some complete examples that follow the guidelines above:

1. **Simple commit**:
   ```
   feat: add HTML email support
   ```

2. **Commit with explanatory body**:
   ```
   fix: resolve SMTP authentication error

   The error occurred when trying to send an email with invalid credentials. 
   Added validation to ensure credentials are correct before attempting to connect.
   ```

3. **Commit with body and reference to an issue**:
   ```
   perf: optimize attachment handling

   Improved the attachment validation process to avoid sending non-existent files,
   enhancing performance and user experience.

   Closes #45
   ```

### Suggestions and Best Practices

- **Use verbs in the imperative**: Always start the description with action verbs in the imperative, such as "add", "fix", "remove". Example: `fix: correct error in email attachment handling`.
- **Be clear and specific**: The description should clearly explain what was changed without being ambiguous.
- **Keep the history clean**: Make small, cohesive commits that address a single task or fix at a time, rather than one large commit with multiple changes.
- **Include references to issues whenever possible**: If the commit is related to an issue or bug report, reference it at the end of the commit using the `Closes #number` syntax, where `number` is the issue number.

---

### Contribution Guidelines

- **Clean and Readable Code**: Ensure that your code adheres to the established standards of the project.
- **Tests**: Always include tests when adding new features.
- **Documentation**: Update the project documentation whenever making relevant changes.

> **Important**: All changes should be submitted to the `dev` branch. The `main` branch is reserved for the stable version of the project.

---

## END
