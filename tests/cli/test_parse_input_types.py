"""CLI input suffix checks for `he parse` and `he feed`.

LLM calls are mocked: Template.create, feed_text, and dump are never real.
"""

import json
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from hyperextract.cli.cli import app

runner = CliRunner()


def _mock_ka():
    ka = MagicMock()
    ka.feed_text = MagicMock(return_value=ka)
    ka.dump = MagicMock()
    ka.load = MagicMock()
    ka.build_index = MagicMock()
    return ka


def _mock_template_config():
    cfg = MagicMock()
    cfg.name = "general/graph"
    return cfg


@contextmanager
def _mock_parse(ka=None):
    ka = ka or _mock_ka()
    with (
        patch("hyperextract.cli.cli.validate_config"),
        patch(
            "hyperextract.cli.cli.Template.get",
            return_value=_mock_template_config(),
        ),
        patch("hyperextract.cli.cli.Template.create", return_value=ka),
    ):
        yield ka


@contextmanager
def _mock_feed(ka=None):
    ka = ka or _mock_ka()
    with (
        patch("hyperextract.cli.cli.validate_config"),
        patch("hyperextract.cli.cli.Template.create", return_value=ka),
    ):
        yield ka


def _invoke_parse(path, output, input_text=None):
    args = [
        "parse",
        str(path),
        "-o",
        str(output),
        "-t",
        "general/graph",
        "-l",
        "en",
        "--no-index",
    ]
    return runner.invoke(app, args, input=input_text)


def _make_ka(tmp_path):
    ka = tmp_path / "ka"
    ka.mkdir()
    (ka / "data.json").write_text("{}", encoding="utf-8")
    (ka / "metadata.json").write_text(
        json.dumps({"template": "general/graph", "lang": "en"}),
        encoding="utf-8",
    )
    return ka


class TestParseInputTypes:
    def test_single_pdf_exits_and_mentions_txt_md(self, tmp_path):
        pdf = tmp_path / "notes.pdf"
        pdf.write_bytes(b"%PDF-1.4 fake")
        out = tmp_path / "out"
        with _mock_parse() as ka:
            result = _invoke_parse(pdf, out)

        assert result.exit_code == 1
        combined = result.output.lower()
        assert "txt" in combined
        assert "md" in combined
        ka.feed_text.assert_not_called()
        ka.dump.assert_not_called()

    def test_directory_only_pdf_exits(self, tmp_path):
        folder = tmp_path / "docs"
        folder.mkdir()
        (folder / "only.pdf").write_bytes(b"%PDF-1.4 fake")
        out = tmp_path / "out"
        with _mock_parse() as ka:
            result = _invoke_parse(folder, out)

        assert result.exit_code == 1
        ka.feed_text.assert_not_called()
        ka.dump.assert_not_called()

    def test_directory_md_and_pdf_warns_and_reads_md(self, tmp_path):
        folder = tmp_path / "docs"
        folder.mkdir()
        (folder / "a.md").write_text("markdown body", encoding="utf-8")
        (folder / "b.pdf").write_bytes(b"%PDF-1.4 fake")
        out = tmp_path / "out"
        with _mock_parse() as ka:
            result = _invoke_parse(folder, out)

        assert result.exit_code == 0
        assert "Warning" in result.output
        assert "b.pdf" in result.output
        ka.feed_text.assert_called_once()
        assert ka.feed_text.call_args[0][0] == "markdown body"
        ka.dump.assert_called()

    def test_uppercase_txt_and_md_are_accepted(self, tmp_path):
        notes = tmp_path / "NOTES.TXT"
        notes.write_text("upper txt", encoding="utf-8")
        out = tmp_path / "out"
        with _mock_parse() as ka:
            result = _invoke_parse(notes, out)

        assert result.exit_code == 0
        ka.feed_text.assert_called_once_with("upper txt", source_id=None)

        folder = tmp_path / "mixed"
        folder.mkdir()
        (folder / "README.MD").write_text("upper md", encoding="utf-8")
        out2 = tmp_path / "out2"
        with _mock_parse() as ka2:
            result2 = _invoke_parse(folder, out2)

        assert result2.exit_code == 0
        ka2.feed_text.assert_called_once_with("upper md", source_id=None)

    def test_stdin_is_not_suffix_checked(self, tmp_path):
        out = tmp_path / "out"
        with _mock_parse() as ka:
            result = _invoke_parse("-", out, input_text="hello from stdin")

        assert result.exit_code == 0
        ka.feed_text.assert_called_once_with("hello from stdin", source_id=None)


class TestFeedInputTypes:
    def test_feed_docx_exits(self, tmp_path):
        ka_dir = _make_ka(tmp_path)
        docx = tmp_path / "notes.docx"
        docx.write_bytes(b"PK fake docx")
        with _mock_feed() as ka:
            result = runner.invoke(app, ["feed", str(ka_dir), str(docx)])

        assert result.exit_code == 1
        combined = result.output.lower()
        assert "txt" in combined
        assert "md" in combined
        ka.feed_text.assert_not_called()
        ka.dump.assert_not_called()

    def test_feed_stdin_is_not_suffix_checked(self, tmp_path):
        ka_dir = _make_ka(tmp_path)
        with _mock_feed() as ka:
            result = runner.invoke(
                app,
                ["feed", str(ka_dir), "-"],
                input="feed stdin text",
            )

        assert result.exit_code == 0
        ka.feed_text.assert_called_once_with("feed stdin text", source_id=None)
        ka.dump.assert_called()
