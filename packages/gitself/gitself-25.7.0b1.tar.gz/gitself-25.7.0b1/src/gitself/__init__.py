# License: AGPL-3.0-or-later
# Copyright 2025, Wayne Werner
import argparse
import email
import email.parser
import email.policy
import enum
import os
import pathlib
import subprocess
import sys
import tempfile
import textwrap
import tomllib
import itertools
from textwrap import dedent

from .vendored import pushid
from . import templates

MESSAGE_POLICY = email.policy.EmailPolicy(utf8=True)
HEADER_PARSER = email.parser.BytesHeaderParser()


class InteractiveMode:
    none = None
    editor = "editor"
    stdin = "stdin"


class GitVcs:
    def __init__(self):
        self.cmd = "git"

    def commit(self, message):
        self.run(self.cmd, "commit", message)

    def run(self, *args):
        subprocess.run(args, check=True)


class Editor:
    def __init__(self, override=None):
        self._editor = override or os.environ.get("EDITOR")
        if not self._editor:
            print(
                "No config value set for EDITOR, falling back to vim."
                " Set your environment variable or config if you don't"
                " like that."
            )
            self._editor = "vim"

    def edit(self, filename):
        filename = str(filename)
        subprocess.run([self._editor, "-c", "$", "-c", "startinsert!", filename])

    def tmp_edit(
        self, *, text="", suffix=".txt", filename="input", cursor_at_eof=False
    ):
        """
        Launch the EDITOR with the provided text pre-populating it.

        Return the result of the edit process as bytes.
        """
        with tempfile.TemporaryDirectory() as dirname:
            dir_ = pathlib.Path(dirname)
            edit_file = (dir_ / filename).with_suffix(suffix)
            edit_file.write_text(text)
            self.edit(edit_file)
            return edit_file.read_bytes()


ISSUE_PARSER = email.parser.BytesParser()
EDITOR = Editor()
for path in ("gitself/INBOX", "INBOX"):
    inbox = pathlib.Path(path)
    if inbox.is_dir():
        INBOX = inbox
        break
else:
    INBOX = None


def interactive_input(prompt, *, mode=InteractiveMode.stdin):
    """
    Get input via the preferred method; if InteractiveMode.none then
    simply return a blank string.

    If InteractiveMode.editor, then `prompt` will be written to the file
    first, and then removed from the start of the file if present.

    **note** prompt will strip off leading/trailing whitespace when checking.

    For example:

        >>> interactive_input("Hello: ", mode=InteractiveMode.editor)
        'World'

    Is what you will see if the user changes the contents of the file to

    ```
            Hello:                          World
    ```
    """

    match mode:
        case InteractiveMode.none:
            return ""
        case InteractiveMode.stdin:
            return input(prompt)
        case InteractiveMode.editor:
            with tempfile.TemporaryDirectory() as dirname:
                dir_ = pathlib.Path(dirname)
                edit_file = dir_ / "input.txt"
                edit_file.write_text(prompt)
                EDITOR.edit(edit_file)
                text = edit_file.read_text().strip()
                if text.startswith(prompt.strip()):
                    text = text[len(prompt) :].strip()
                return text


def git_from():
    """
    Request the configured git user.name and user.email, and return it in the
    form of `User Name <email@example.com>`
    """
    user = (
        subprocess.run(["git", "config", "--get", "user.name"], capture_output=True)
        .stdout.decode()
        .strip()
    )
    email = (
        subprocess.run(["git", "config", "--get", "user.email"], capture_output=True)
        .stdout.decode()
        .strip()
    )
    return f"{user} <{email}>"


def pyproject_find_key(key):
    """
    Find a given key in pyproject.toml, using a dotted path.

    Return the value or None if not found.

        >>> with open('pyproject.toml', 'w') as f:
        ...  f.write('''
        ... [a]
        ... c = 'see?'
        ... [a.b.c.d]
        ... e = 'f'
        ... ''')
        >>> pyproject_find_key(key='a.c')
        'See?'
        >>> pyproject_find_key(key='a.b.c.d.e')
        'f'
    """
    pyproject = pathlib.Path("pyproject.toml")
    contact = None
    if pyproject.exists():
        with pyproject.open("rb") as f:
            data = tomllib.load(f)
            for part in key.split("."):
                data = data.get(part)
                if data is None:
                    return None
    return data


def find_project_contact():
    """
    Try to find a project contact email. If none is found, return
    `issues@yourproject.com`
    """
    pyproject = pathlib.Path("pyproject.toml")
    contact = None
    if pyproject.exists():
        with pyproject.open("rb") as f:
            data = tomllib.load(f)
            contact = data.get("tool", {}).get("gitself", {}).get("contact", "").strip()
    return contact or "issues@yourproject.com"


# {{{
# ADR 2025.06.22 - ParserNaming
# Author: Wayne Werner
#
# The parser naming functions should be <type>_<action>, so anything
# pertaining to issues should be `issue_ACTION` that way when searching
# in here for issue functions they'll just be present with that name.
# }}}
def issue_create(title="", autocommit=True):
    new_id = pushid.make_push()
    template = dedent(f"""
    From: {git_from()}
    To: {find_project_contact()}
    Date: {email.utils.formatdate()}
    Message-ID: {new_id}@yourproject
    X-Gitself-Type: issue
    Subject: {title}


    """).lstrip()

    if not title:
        template = template.rstrip() + " "

    issue_bytes = EDITOR.tmp_edit(text=template, suffix=".eml")
    if issue_bytes == template.encode():
        print("No change, not adding issue")
    else:
        issue_path = INBOX / f"{new_id}.eml"
        issue_path.write_bytes(issue_bytes)
        if autocommit:
            git_commit(path=issue_path)


# TODO: Reorganize the location of this function -W. Werner, 2025-07-06
def git_commit(*, path):
    """
    Create a git commit using the provided title. If the entire title is
    longer than 50 characters, then it will be wrapped into the full message

    Examples:

        This is a short message

    Becomes:

        Create issue: This is a short message

    Meanwhile:

        This is a very long message with a lot of text.

    Becomes:


        Create issue: This is a very long message with ...

        a lot of text.
    """

    with path.open("rb") as f:
        headers = HEADER_PARSER.parse(f)
    title = f"Create issue: {headers['Subject']}"
    if len(title) <= 50:
        message = title
    else:
        first_line, *rest = textwrap.wrap(title, width=47)

        rest = textwrap.wrap(" ".join(rest), width=72)
        message = f"{first_line}...\n\n{' '.join(rest)}"
    with tempfile.NamedTemporaryFile() as f:
        f.write(message.encode())
        f.flush()
        subprocess.run(["git", "add", str(path)])
        with open(f.name) as p:
            print(p.read())
        subprocess.run(["git", "commit", "-F", f.name])


def issue_max_id(issue_dir):
    max_id = 0
    parser = email.parser.BytesHeaderParser()
    for msg in sorted(issue_dir.iterdir()):
        with msg.open(mode="rb") as f:
            headers = parser.parse(f)
            msg_id = headers["message-id"]
            msg_id = int(msg_id.partition("@")[0])
            max_id = max(max_id, msg_id)
    return max_id + 1


def issue_accept(*, all=False):
    for path in ("gitself/INBOX", "INBOX"):
        inbox = pathlib.Path(path)
        if inbox.is_dir():
            break
    else:
        exit("Unable to find gitself inbox in gitself/INBOX or INBOX")

    issues_dir = inbox.parent / "ISSUES"
    if not issues_dir.exists():
        issues_dir.mkdir(parents=True, exist_ok=True)

    max_issue_id = issue_max_id(issues_dir)
    zfill = 4  # TODO: Probably a different zfill, maybe configured with a toml file? -W. Werner, 2025-06-22
    messages = sorted(inbox.glob("*.eml"))
    if not messages:
        print(f"No messages found in {inbox!s}")
    else:
        for file in sorted(inbox.glob("*.eml")):
            with file.open(mode="rb+") as f:
                msg = email.message_from_binary_file(f)
            do_import = all or input(
                f"Import {msg['subject']} - {file!s}? "
            ).strip().lower() in ("y", "yes")
            if do_import:
                issue_num = str(max_issue_id).zfill(zfill)
                max_issue_id += 1
                old, _, domain = msg["message-id"].partition("@")
                del msg["message-id"]
                msg["Message-ID"] = f"{issue_num}@{domain}"
                print("issue num: ", issue_num)
                new_file = issues_dir / file.with_stem(issue_num).name
                new_file.write_bytes(msg.as_bytes(policy=MESSAGE_POLICY))
                file.unlink()
                # TODO: get new issue # -W. Werner, 2025-06-22
                print(f"Imported issue #{issue_num}")


def issue_to_link(issue):
    issue_id = issue['Message-ID'].partition('@')[0]
    issue_title = issue['Subject']
    return f'<td>{issue_id}</td><td><a href="{issue_id}.html">{issue_title}</a></td>'


def html_render(*, output_dir):
    if output_dir is None:
        output_dir = pathlib.Path(pyproject_find_key("tool.gitself.html.output_dir"))

    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    elif not output_dir.is_dir():
        exit(f"{output_dir!s} exists but is not a directory")

    with (output_dir / "index.html").open("w") as index_page:
        inbox_issues = []
        actual_issues = []
        for issue_file, issue in _issues():
            issue_html = templates.issue_page.format(issue=issue)
            output_page = (output_dir / issue_file.name).with_suffix('.html')
            output_page.write_text(issue_html)
            if issue_file.parent.name == "INBOX":
                inbox_issues.append(issue)
            elif issue_file.parent.name == "ISSUES":
                actual_issues.append(issue)
        # print(issue)
        index_page.write(
            templates.page_template.format(
                title="Gitself Itself",
                body=templates.message_list.format(
                    title=f"Inbox ({len(inbox_issues)})",
                    lower_title="inbox",
                    li_items="</tr><tr>".join(issue_to_link(i) for i in inbox_issues),
                )
                +" "+
                templates.message_list.format(
                    title=f"Open ({len(actual_issues)})",
                    lower_title="open",
                    li_items="</tr><tr>".join(issue_to_link(i) for i in sorted(actual_issues, key=lambda x: x["Message-ID"])))
                ,
            )
        )


def _issues(path=INBOX.parent):
    """
    Find all of the gitself issues for the project. Yield a tuple of (path, issue) for each of the issues.
    """
    dirs = itertools.chain((path / "INBOX").iterdir(), (path / "ISSUES").iterdir())

    for issue in dirs:
        if issue.name == ".keep":
            continue
        with issue.open("rb") as f:
            headers = HEADER_PARSER.parse(f)
            yield (issue, headers)


def issue_list(open=False, closed=False, inbox=False):
    if not any((open, closed)):
        open = True
    if inbox:
        ISSUES = INBOX
    else:
        ISSUES = INBOX.parent / "ISSUES"
    if not ISSUES.exists():
        print("No issues")
    else:
        by_status = {
            "open": {},
            "closed": {},
        }
        for issue in sorted(ISSUES.iterdir()):
            with issue.open("rb") as f:
                headers = HEADER_PARSER.parse(f)
                status = headers.get("X-Gitself-Status", "open")
                issue_id = headers["Message-ID"].partition("@")[0]
                by_status[status][issue_id] = headers["Subject"]

    if open:
        for id in sorted(by_status["open"]):
            print(f"{id}: {by_status['open'][id]}")


def create_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    issue_parser = subparsers.add_parser(
        "issue", help="Create new and otherwise manipulate issues"
    )
    subissue_parsers = issue_parser.add_subparsers()

    new_issue_parser = subissue_parsers.add_parser("new", help="Create new issues.")
    new_issue_parser.add_argument(
        "-t",
        "--title",
        default="",
        help="Title of the issue, or subject of issue message",
    )
    new_issue_parser.set_defaults(func=issue_create)

    accept_issue_parser = subissue_parsers.add_parser("accept", help="Accept issues.")
    accept_issue_parser.add_argument(
        "-a", "--all", action="store_true", default=False, help="Accept all issues."
    )
    accept_issue_parser.set_defaults(func=issue_accept)

    list_parser = subparsers.add_parser("list", help="List issues & things.")
    list_parser.add_argument("--open", action="store_true")
    list_parser.add_argument("--closed", action="store_true")
    list_parser.add_argument(
        "--inbox",
        action="store_true",
        help="List messaes in the inbox instead of accepted issues.",
    )
    list_parser.set_defaults(func=issue_list)

    html_parser = subparsers.add_parser(
        "html",
        help="Render gitself into static HTML. Requires tool.gitself.html.output_dir setting.",
    )
    html_parser.add_argument(
        "--output-dir",
        default=None,
        help="Overrides tool.gitself.html.output_dir; the root of where the pages should be rendered.",
    )
    html_parser.set_defaults(func=html_render)

    new_parser = subparsers.add_parser("new", help="Create new issues.")
    new_parser.add_argument(
        "-t",
        "--title",
        default="",
        help="Title of the issue, or subject of issue message",
    )
    new_parser.set_defaults(func=issue_create)

    return parser


def main() -> None:
    # TODO: definitely could look for the git rootdir -W. Werner, 2025-06-22
    if INBOX is None:
        exit("No ./gitself/INBOX or ./INBOX directory found")
    parser = create_parser()
    args = parser.parse_args()
    kwargs = dict(args._get_kwargs())
    if "func" in kwargs:
        func = kwargs.pop("func")
        func(**kwargs)
    else:
        parser.print_help()
