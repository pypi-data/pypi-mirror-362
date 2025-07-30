"""
# MarkTen / Actions / git.py

Actions associated with `git` and Git repos.
"""

from logging import Logger
from pathlib import Path

from markten import ActionSession
from markten.__utils import TextCollector
from markten.actions import fs, process
from markten.actions.__async_process import run_process

log = Logger(__name__)

DEFAULT_REMOTE = "origin"


async def clone(
    action: ActionSession,
    repo_url: str,
    /,
    branch: str | None = None,
    fallback_to_main: bool = False,
    dir: Path | None = None,
) -> Path:
    """Perform a `git clone` operation.

    By default, this clones the project to a temporary directory.

    Parameters
    ----------
    repo_url : str
        URL to clone
    branch : str | None, optional
        Branch to checkout after cloning is complete, by default None
    fallback_to_main : bool, optional
        Whether to fall back to the main branch if the given branch does
        not exist, by default False
    dir : Path | None, optional
        Directory to clone to, by default None for a temporary directory
    """
    repo_url = repo_url.strip()
    branch = branch.strip() if branch else None

    if dir:
        clone_path = dir
    else:
        clone_path = await fs.temp_dir(action.make_child(fs.temp_dir))

    program: tuple[str, ...] = ("git", "clone", repo_url, str(clone_path))

    await process.run(action, *program)

    if branch:
        checkout_action = action.make_child(checkout)
        try:
            await checkout(
                checkout_action,
                clone_path,
                branch,
                create=True,
            )
        except Exception as e:
            checkout_action.fail(str(e))
            if fallback_to_main:
                action.log("Note: remaining on main branch")
            else:
                raise

    return clone_path


async def push(
    action: ActionSession,
    dir: Path,
    /,
    set_upstream: bool | str | tuple[str, str] = False,
):
    if set_upstream is False:
        program: tuple[str, ...] = ("git", "-C", str(dir), "push")
    else:
        if set_upstream is True:
            remote = DEFAULT_REMOTE
            branch = await current_branch(
                action.make_child(current_branch), dir
            )
        elif isinstance(set_upstream, str):
            remote = DEFAULT_REMOTE
            branch = set_upstream
        else:
            remote, branch = set_upstream

        program = ("git", "-C", str(dir), "push", remote, branch)

    await process.run(action, *program)


async def pull(action: ActionSession, dir: Path) -> None:
    program = ("git", "-C", str(dir), "pull")
    await process.run(action, *program)


async def checkout(
    action: ActionSession,
    dir: Path,
    branch_name: str,
    /,
    create: bool = False,
    push_to_remote: str | bool = False,
) -> None:
    """Perform a `git checkout` operation.

    This changes the active branch for the given git repository.

    Parameters
    ----------
    dir : Path
        Path to git repository
    branch_name : str
        Branch to checkout
    create : bool, optional
        Whether to pass a `-b` flag to the `git checkout` operation,
        signalling that `git` should create a new branch.
    push_to_remote : str | bool, optional
        Whether to also push this branch to the given remote. This
        requires the `create` flag to also be `True`. If `True` is given,
        this will create the branch on the `origin` remote. Otherwise, if a
        `str` is given, this will push to that remote.
    """

    if push_to_remote is not None and not create:
        raise ValueError(
            "MarkTen.actions.git.checkout: Cannot specify "
            "`push_to_remote` if `create is False`"
        )
    program: tuple[str, ...] = (
        "git",
        "-C",
        str(dir),
        "checkout",
        *(("-b",) if create else ()),
        branch_name,
    )
    await process.run(action, *program)

    if push_to_remote is not False:
        await push(action.make_child(push), dir, set_upstream=push_to_remote)

    action.succeed(
        f"Switched to{' new' if create else ''} "
        f"branch {branch_name}" + " and pushed to remote"
        if push_to_remote
        else ""
    )


async def add(
    action: ActionSession,
    dir: Path,
    files: list[Path] | None = None,
    /,
    all: bool = False,
) -> None:
    """Perform a `git add` operation

    This stages the given list of changes, making them ready to commit.

    If the `files` list is empty and `all` is not specified, this will have
    no effect.

    Parameters
    ----------
    dir : Path
        Path to git repository.
    files : list[Path] | None, optional
        List of files to add, by default None, indicating that no files
        should be added.
    all : bool, optional
        whether to add all modified files, by default False

    Raises
    ------
    ValueError
        Files were specified when `all` is `True`
    """
    if files is None:
        files = []

    if all and len(files):
        raise ValueError(
            "Should not specify files to commit when using the `all=True` "
            "flag."
        )

    program: tuple[str, ...] = (
        "git",
        "-C",
        str(dir),
        "add",
        *(["-a"] if all else map(str, files)),
    )

    await process.run(action, *program)

    if all:
        action.succeed("Git: staged all files")
    else:
        action.succeed(f"Git: staged files {files}")


async def commit(
    action: ActionSession,
    dir: Path,
    message: str,
    /,
    all: bool = False,
    push_after: bool = False,
    files: list[Path] | None = None,
) -> None:
    if files is not None or all:
        await add(action.make_child(add), dir, files, all=all)

    await process.run(
        action,
        "git",
        "-C",
        str(dir),
        "commit",
        "-m",
        message,
    )

    if push_after:
        await push(action.make_child(push), dir)


async def current_branch(action: ActionSession, dir: Path) -> str:
    program = ("git", "-C", str(dir), "rev-parse", "--abbrev-ref", "HEAD")
    output = TextCollector()
    await run_process(program, on_stdout=output)
    action.succeed()
    return str(output).strip()
