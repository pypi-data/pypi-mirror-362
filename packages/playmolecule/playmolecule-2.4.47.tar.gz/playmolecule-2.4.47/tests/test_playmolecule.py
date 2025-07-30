from distutils import dir_util
from pytest import fixture
from glob import glob
import json
import os


@fixture
def datadir(tmpdir, request):
    """
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    """
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


def prepare(datadir):
    outdir = str(datadir.join("out"))
    scratchdir = str(datadir.join("scratch"))
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(scratchdir, exist_ok=True)
    return outdir, scratchdir


def _test_old_playmolecule_manifests(datadir):
    datadir = str(datadir)
    os.environ["PM_APP_ROOT"] = datadir

    from playmolecule import apps, datasets, protocols
    import tempfile

    assert hasattr(apps, "proteinprepare")
    assert hasattr(apps.proteinprepare, "tests")
    assert hasattr(apps.proteinprepare, "files")
    assert hasattr(apps.proteinprepare.v1, "tests")
    assert hasattr(apps.proteinprepare.v1, "files")
    assert hasattr(apps.proteinprepare.v1.tests, "simple")
    assert sorted(list(apps.proteinprepare.v1.files.keys())) == sorted(
        [
            "datasets",
            "datasets/3ptb.pdb",
            "tests",
            "tests/web_content.pickle",
            "tests/reprepare.pickle",
            "tests/3ptb.pdb",
            "tests/587HG92V.pdb",
            "tutorials",
            "tutorials/learn_this_app.ipynb",
        ]
    )
    assert hasattr(apps.proteinprepare.v1.datasets, "file_3ptb")
    assert hasattr(datasets, "file_3ptb")
    assert hasattr(protocols, "crypticscout")
    assert hasattr(protocols.crypticscout, "v1")
    assert hasattr(protocols.crypticscout.v1, "crypticscout")
    assert hasattr(protocols.crypticscout.v1.crypticscout, "crypticscout")
    assert callable(protocols.crypticscout.v1.crypticscout.crypticscout)

    expected_files = [
        "run_*.sh",
        "run_*/",
        "run_*/expected_outputs.json",
        "run_*/.pm.done",
        "run_*/.manifest.json",
        os.path.join("run_*", "inputs.json"),
        os.path.join("run_*", "original_paths.json"),
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        apps.proteinprepare(tmpdir, pdbfile=datasets.file_3ptb).run()
        for ef in expected_files:
            assert len(glob(os.path.join(tmpdir, ef))), "could not find " + ef

        with open(glob(os.path.join(tmpdir, "run_*", "inputs.json"))[0], "r") as f:
            inputs = json.load(f)
            assert "function" not in inputs

    expected_files += [os.path.join("run_*", "3ptb.pdb")]
    with tempfile.TemporaryDirectory() as tmpdir:
        apps.proteinprepare(
            tmpdir, pdbfile=os.path.join(datadir, "datasets", "3ptb.pdb")
        ).run()
        for ef in expected_files:
            assert len(glob(os.path.join(tmpdir, ef))), "could not find " + ef


def _test_new_playmolecule_manifests(datadir):
    datadir = str(datadir)
    os.environ["PM_APP_ROOT"] = datadir

    from playmolecule import apps, datasets
    import tempfile

    assert hasattr(apps, "proteinpreparenew")
    assert hasattr(apps.proteinpreparenew, "tests")
    assert hasattr(apps.proteinpreparenew, "files")
    assert hasattr(apps.proteinpreparenew.v1, "tests")
    assert hasattr(apps.proteinpreparenew.v1, "files")
    assert hasattr(apps.proteinpreparenew.v1.tests, "simple")
    assert sorted(list(apps.proteinpreparenew.v1.files.keys())) == sorted(
        [
            "datasets",
            "datasets/3ptb.pdb",
            "tests",
            "tests/web_content.pickle",
            "tests/reprepare.pickle",
            "tests/3ptb.pdb",
            "tests/587HG92V.pdb",
            "tutorials",
            "tutorials/learn_this_app.ipynb",
        ]
    )
    assert hasattr(apps.proteinpreparenew.v1.datasets, "file_3ptb")
    assert hasattr(datasets, "file_3ptb")

    expected_files = [
        "run_*.sh",
        "run_*/",
        "run_*/.pm.done",
        "run_*/.manifest.json",
        "run_*/expected_outputs.json",
        os.path.join("run_*", "inputs.json"),
        os.path.join("run_*", "original_paths.json"),
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        apps.proteinpreparenew(tmpdir, pdbfile=datasets.file_3ptb).run()
        for ef in expected_files:
            assert len(glob(os.path.join(tmpdir, ef))), "could not find " + ef

        with open(glob(os.path.join(tmpdir, "run_*", "inputs.json"))[0], "r") as f:
            inputs = json.load(f)
            assert "function" in inputs
            assert (
                inputs["function"] == "proteinprepare.apps.proteinpreparenew.app.main"
            )

    with tempfile.TemporaryDirectory() as tmpdir:
        apps.proteinpreparenew.v1.bar(tmpdir, pdbid="3ptb").run()
        for ef in expected_files:
            assert len(glob(os.path.join(tmpdir, ef))), "could not find " + ef

        with open(glob(os.path.join(tmpdir, "run_*", "inputs.json"))[0], "r") as f:
            inputs = json.load(f)
            assert "function" in inputs
            assert inputs["function"] == "proteinprepare.apps.proteinpreparenew.app.bar"

    expected_files += [os.path.join("run_*", "3ptb.pdb")]
    with tempfile.TemporaryDirectory() as tmpdir:
        apps.proteinpreparenew(
            tmpdir, pdbfile=os.path.join(datadir, "datasets", "3ptb.pdb")
        ).run()
        for ef in expected_files:
            assert len(glob(os.path.join(tmpdir, ef))), "could not find " + ef
