# (c) 2015-2023 Acellera Ltd http://www.acellera.com
# All Rights Reserved
# Distributed under HTMD Software License Agreement
# No redistribution in whole or part
#
import re


class _Tests:
    def __init__(self, config, cls) -> None:
        if cls.files is None:
            return

        for key in config:
            attr_name = key

            # Ensure attribute name starts with a letter
            if not attr_name[0].isalpha():
                attr_name = f"test_{attr_name}"

            # Replace non-alphanumeric (and _) characters with _
            attr_name = re.sub(r"[^a-zA-Z0-9_]", "_", attr_name)

            try:
                setattr(self, attr_name, _Test(attr_name, config[key], cls))
            except Exception:
                import traceback

                print(
                    f"Failed to set-up test {key} for app {cls} with traceback: {traceback.format_exc()}"
                )

    def __str__(self) -> str:
        descr = ""
        for key in self.__dict__:
            descr += f"{self.__dict__[key]}\n"
        return descr

    def __repr__(self) -> str:
        return self.__str__()


def _convert_test_files(cls, val, name):
    if val.startswith("tests/"):
        if val.endswith("/"):
            val = val[:-1]
        return cls.files[val]
    if val.startswith("datasets/"):
        return getattr(cls.datasets, val.replace("datasets/", ""))
    if val.startswith("artifacts/"):
        if not hasattr(cls, "artifacts"):
            raise RuntimeError(
                f"Test {name} of app '{cls._name}' requires file {val} but the app manifest is missing the artifacts section"
            )
        return getattr(cls.artifacts, val.replace("artifacts/", ""))
    return val


class _Test:
    def __init__(self, name, config, cls) -> None:
        args = config["arguments"].copy()
        for key, vals in args.items():
            if not isinstance(vals, (list, tuple)):
                vals = [vals]

            for i in range(len(vals)):
                val = vals[i]
                if isinstance(val, dict):
                    for k, v in val.items():
                        if not isinstance(v, str):
                            continue
                        val[k] = _convert_test_files(cls, v, name)
                if not isinstance(val, str):
                    continue
                vals[i] = _convert_test_files(cls, val, name)
            args[key] = vals if len(vals) > 1 else vals[0]
        config["arguments"] = args

        self.name = name
        self.config = config
        self.cls = cls
        self.function = config["function"]

    def run(self, queue=None, dir=None, **kwargs):
        """Run the test

        Parameters
        ----------
        queue : str
            The name of the queue on which to run the test. By default it will be run locally.
            For options check the documentation of the ExecutableDirectory.run method.
        dir : str, Path
            Directory in which to execute the tests. By default they will be executed under
            the /tmp/ folder. However this is usually not accessible over SLURM, therefore
            if queue="slurm" is used, choose a network mounted path in which to execute the tests.
        kwargs : dict
            Additional arguments for the queue execution. For options check the documentation
            of the ExecutableDirectory.run method.
        """
        from playmolecule import PM_APP_ROOT, JobStatus
        from playmolecule._appfiles import _File
        from glob import glob
        import tempfile
        import time
        import inspect
        import os

        with tempfile.TemporaryDirectory(dir=dir) as tmpdir:
            func = getattr(self.cls, self.function)
            testargs = self.config["arguments"].copy()
            func_sig = inspect.signature(func).parameters
            if "outdir" in func_sig:
                testargs["outdir"] = tmpdir
            if "execdir" in func_sig:
                tmpdir = testargs["execdir"]
                if isinstance(tmpdir, _File):
                    tmpdir = tmpdir.path

            print(
                f"Running test '{self.name}' at location {tmpdir} with args {testargs}"
            )

            t = time.time()

            ed = func(**testargs)
            ed.run(queue=queue, **kwargs)

            while ed.status not in (JobStatus.COMPLETED, JobStatus.ERROR):
                time.sleep(10)

            for ff in self.config["expected_outputs"]:
                if len(glob(os.path.join(tmpdir, ff))) == 0:
                    raise RuntimeError(
                        f"Test failed. Could not find expected output file: {ff} in {tmpdir}"
                    )
            print(
                f"\n🎉 Test '{self.name}' succeeded in {time.time()-t:.2f} seconds! 🎉"
            )

    def __str__(self) -> str:
        descr = self.config["description"]
        string = f"[{self.name}] '{descr}'\n- Arguments:\n"
        for arg, val in self.config["arguments"].items():
            string += f"  {arg} = {val}\n"
        string += "- Expected outputs:\n"
        for outp in self.config["expected_outputs"]:
            string += f"  {outp}\n"
        return string

    def __repr__(self) -> str:
        return self.__str__()
