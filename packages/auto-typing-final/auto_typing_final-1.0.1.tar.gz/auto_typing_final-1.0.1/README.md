# auto-typing-final

Auto-fixer for Python code that adds `typing.Final` annotation to variable assignments inside functions that are not reassigned, and removes the annotation from variables that _are_ mutated.

```diff
 def foo() -> None:
-    a = 2
+    a: typing.Final = 2

-    b: typing.Final = 2
+    b = 2
     b = 3
```

Basically, this, but handles different operations (like usage of `nonlocal`, augmented assignments: `+=`, etc) as well.

- Keeps type checker happy.
- Adds global import if it's not imported yet (`import typing`/`from typing import Final`).
- Inspects one file at a time.
- Is careful with global variables: adds Final only for uppercase variables, ignores variable that are referenced in `global` statement inside functions in current file, and avoids removing Final when it already was set ([docs](docs/global_vars_enabled.md)).
- Ignores class variables: it is common to use `typing.ClassVar` instead of `typing.Final`.

## How To Use

Having uv installed:

```sh
uvx auto-typing-final .
```

or:

```sh
pipx run auto-typing-final .
```

### Options

You can specify `--check` flag to check the files instead of actually fixing them:

```sh
auto-typing-final . --check
```

Also, you can choose import style from two options: `typing-final` (default) and `final`:

```sh
auto-typing-final . --import-style typing-final
```

- `typing-final` enforces `import typing` and `typing.Final`,
- `final` enforces `from typing import Final` and `Final`.

Also, you can set `--ignore-global-vars` flag to ignore global variables:

```sh
auto-typing-final . --ignore-global-vars
```

### Ignore comment

You can ignore variables by adding `# auto-typing-final: ignore` comment to the line ([docs](docs/ignore_comment.md)).

### VS Code Extension

<img width="768" alt="image" src="https://github.com/community-of-python/auto-typing-final/assets/75225148/f1541056-06f5-4caa-8c94-0a5eaf98ba15">

The extension uses LSP server bundled with the CLI (executable name is `auto-typing-final-lsp-server`). To get started, add `auto-typing-final` to your project:

```sh
uv add auto-typing-final --dev
```

After that, install the extension: https://marketplace.visualstudio.com/items?itemName=vrslev.auto-typing-final. In Python environments that have `auto-typing-final` installed, extension will be activated automatically.

### Settings

- Import style can be configured in settings: `"auto-typing-final.import-style": "typing-final"` or `"auto-typing-final.import-style": "final"`.
- Ignore global variables can be configured in settings: `"auto-typing-final.ignore-global-vars": true`.

### Notes

Library code of currently activated environment will be ignored (for example, `.venv/bin/python` is active interpreter, all code inside `.venv` will be ignored).
