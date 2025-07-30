import pytest

import pyrequire


@pytest.mark.parametrize(
    "current_version, required_version, flag",
    (
        ("1.2.3", "", True),
        ("1.2.3", "<1.2.3", False),
        ("1.2.2", "<1.2.3", True),
        ("1.2.4", "<=1.2.3", False),
        ("1.2.3", "<=1.2.3", True),
        ("1.2.2", "==1.2.3", False),
        ("1.2.3", "==1.2.3", True),
        ("1.2.2", ">=1.2.3", False),
        ("1.2.3", ">=1.2.3", True),
        ("1.2.3", ">1.2.3", False),
        ("1.2.4", ">1.2.3", True),
        ("1.2.3", ">2", False),
        ("1.2.3", ">1", True),
    ),
)
def test_require_package(current_version, required_version, flag, monkeypatch):
    monkeypatch.setattr("importlib.import_module", lambda name: None)
    monkeypatch.setattr("importlib.metadata.version", lambda name: current_version)

    if flag:

        @pyrequire.require_package(f"pytest{required_version}")
        def foobar():
            return

        foobar()

    else:
        with pytest.raises(ModuleNotFoundError):

            @pyrequire.require_package(f"pytest{required_version}")
            def foobar():
                return


def test_require_package_not_installed(monkeypatch):
    with pytest.raises(ModuleNotFoundError):

        @pyrequire.require_package("dummy_package")
        def foobar():
            return


@pytest.mark.parametrize(
    "current_version, required_version, flag",
    (
        ((3, 9, 0), ">=3.9", True),
        ((3, 8, 0), ">=3.9", False),
        ((3, 9, 0), "<3.10", True),
        ((3, 10, 0), "<3.10", False),
        ((3, 9, 0), "==3.9", True),
        ((3, 8, 0), "==3.9", False),
        ((3, 9, 0), ">=3.9", True),
        ((3, 8, 0), ">=3.9", False),
        ((3, 9, 0), ">3.8", True),
        ((3, 8, 0), ">3.9", False),
    ),
)
def test_require_python(current_version, required_version, flag, monkeypatch):
    monkeypatch.setattr("sys.version_info", current_version)

    if flag:

        @pyrequire.require_python(required_version)
        def foobar():
            return

        foobar()

    else:
        with pytest.raises(RuntimeError):

            @pyrequire.require_python(required_version)
            def foobar():
                return
