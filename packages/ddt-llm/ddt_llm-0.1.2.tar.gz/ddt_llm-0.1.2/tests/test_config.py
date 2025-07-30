from pathlib import Path
import sys
from ddt import config, tokenizer


def test_config_happy_path():
    root = Path(".")
    is_verbose = True
    include_gitignore = True
    include_dotfiles = True
    include_symlinks = True
    include_images = True
    resolve_paths = True
    model = tokenizer.Model("gpt-4o")
    output = sys.stdout
    output_format = "txt"
    exclude = ["foo"]
    include = ["bar"]

    cfg = config.Config(
        root,
        is_verbose,
        include_gitignore,
        include_dotfiles,
        include_symlinks,
        include_images,
        resolve_paths,
        model,
        output,
        output_format,
        exclude,
        include,
    )

    assert cfg.root == root
    assert cfg.is_verbose
    assert cfg.include_gitignore
    assert cfg.include_dotfiles
    assert cfg.include_symlinks
    assert cfg.include_images
    assert cfg.resolve_paths
    assert cfg.model == tokenizer.Model("gpt-4o")
    assert cfg.output == sys.stdout
    assert cfg.output_format == "txt"
    assert cfg.exclude == ["foo"]
    assert cfg.include == ["bar"]


def test_generate_config():
    args = [
        {
            "root": Path("."),
            "verbose": True,
            "include_gitignore": True,
            "include_dotfiles": True,
            "include_symlinks": True,
            "include_images": True,
            "resolve_paths": True,
            "model": tokenizer.Model("gpt-4o"),
            "output": sys.stdout,
            "output_type": "txt",
            "json": False,  # to fix test, goes away when output config changes
            "html": False,  # to fix test, goes away when output config changes
            "exclude": ["foo"],
            "include": ["bar"],
        },
        {
            "root": Path("."),
            "verbose": True,
            "include_gitignore": True,
            "include_dotfiles": True,
            "include_symlinks": True,
            "include_images": True,
            "resolve_paths": True,
            "model": tokenizer.Model("gpt-4o"),
            "output": sys.stdout,
            "output_type": "json",
            "json": True,  # to fix test, goes away when output config changes
            "html": False,  # to fix test, goes away when output config changes
            "exclude": ["foo"],
            "include": ["bar"],
        },
        {
            "root": Path("."),
            "verbose": True,
            "include_gitignore": True,
            "include_dotfiles": True,
            "include_symlinks": True,
            "include_images": True,
            "resolve_paths": True,
            "model": tokenizer.Model("gpt-4o"),
            "output": sys.stdout,
            "output_type": "html",
            "json": False,  # to fix test, goes away when output config changes
            "html": True,  # to fix test, goes away when output config changes
            "exclude": ["foo"],
            "include": ["bar"],
        },
    ]

    for argset in args:
        cfg = config.generate_config(argset)

        assert cfg.root == Path(".").resolve()
        assert cfg.is_verbose
        assert cfg.include_gitignore
        assert cfg.include_dotfiles
        assert cfg.include_symlinks
        assert cfg.include_images
        assert cfg.resolve_paths
        assert cfg.model == tokenizer.Model("gpt-4o")
        assert cfg.output == sys.stdout
        assert cfg.output_format == argset["output_type"]
        assert cfg.exclude == ["foo"]
        assert cfg.include == ["bar"]
