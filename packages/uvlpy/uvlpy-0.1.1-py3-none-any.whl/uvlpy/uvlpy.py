import os
import subprocess
import uuid
import shutil


def to_uv(name: str, val: int, deps=[], build=True):
    dirname = name + "-" + str(val)
    full_dirname = os.path.join(dirname, "src", name) if build else dirname
    if not os.path.isdir(dirname):
        os.makedirs(full_dirname)

    os.chdir(full_dirname)

    if build:
        f = open("__init__.py", "w")
        f.close()

        os.chdir(os.path.join("..", ".."))

    with open("pyproject.toml", "w") as f:
        f.write(
            f"""[project]
name = "{name}"
version = "{val}"
dependencies = {deps}
            """
            + (
                """
[build-system]
requires = [ "uv_build>=0.7.19,<0.8.0" ]
build-backend = "uv_build" """
                if build
                else ""
            )
        )

    os.chdir("..")


class Constraint:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind

    def __repr__(self):
        if self.kind:
            return f'"{self.x} {self.kind} {self.y}"'
        else:
            return f'"{self.x}"'

    def __contains__(self, z):
        return self.x == z


class Var:
    range: list[tuple]

    def __init__(self, range):
        self.name = uuid.uuid4().hex
        range.sort()
        self.range = [(x, []) for x in range]

    def to_constr(self):
        return Constraint(self, None, None)

    def val_constr(self, val, *args):
        for x, constrs in self.range:
            if x == val:
                constrs += args
                return

    def constr(self, *args):
        for _, constrs in self.range:
            constrs += args

    def devar(self, right, op):
        if isinstance(right, Var):
            raise ValueError("Cannot have a variable on right side")
        else:
            return Constraint(self, right, op)

    def __lt__(self, other):
        return self.devar(other, "<")

    def __le__(self, other):
        return self.devar(other, "<=")

    def __gt__(self, other):
        return self.devar(other, ">")

    def __ge__(self, other):
        return self.devar(other, ">=")

    def __eq__(self, other):
        if isinstance(other, Var):
            return self.range is other.range
        else:
            return Constraint(self, other, "==")

    def __ne__(self, other):
        if isinstance(other, Var):
            return self.range is not other.range
        else:
            return Constraint(self, other, "!=")

    def __repr__(self):
        return self.name


class System:
    vars: list[Var]
    constrs: list[Constraint]
    keep_work: bool
    done_work: bool

    def __init__(self, keep_work=False):
        self.vars = []
        self.constrs = []
        self.keep_work = keep_work
        self.done_work = False

    def make_vars(self, *args):
        tmp = [Var(v) for v in args]
        self.vars += tmp
        return tmp

    def constr(self, *args):
        self.constrs += args

    def execute(self, *args):
        if not os.path.isdir("work"):
            os.makedirs("work")
        os.chdir("work")

        if not self.done_work:
            for v in self.vars:
                for val, constrs in v.range:
                    to_uv(v.name, val, constrs)
                    proc = subprocess.run(
                        ["uv", "build", "-o", ".."],
                        cwd=v.name + "-" + str(val),
                        stdout=None,
                        stderr=None,
                    )
                    if proc.returncode != 0:
                        print("Failed to construct a variable")
                        return False

        if not self.done_work:
            to_uv("result", "0.1", self.constrs, False)

        proc = subprocess.run(
            ["uv", "lock", "--find-links", ".."],
            cwd="result-0.1",
            stdout=None,
            stderr=None,
        )

        if proc.returncode != 0:
            print("Impossible to solve")
            return False

        res = True
        if args:
            res = []
            with open(os.path.join("result-0.1", "uv.lock"), "r") as f:
                lines = f.read().splitlines()
                for arg in args:
                    try:
                        idx = lines.index(f'name = "{arg.name}"')
                        res.append(int(lines[idx + 1].partition('"')[2][-2]))
                    except ValueError:
                        # Assumes that the value was given, just not mentioned
                        # rather than it never existing to begin with
                        res.append("Any")

        os.chdir("..")
        if not self.keep_work:
            self.done_work = True
            shutil.rmtree("work")
        return res

    def clear(self):
        self.vars = []
        self.constrs = []
