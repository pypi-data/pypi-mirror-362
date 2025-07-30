from __future__ import annotations
from pathlib import Path
from snakemake.ruleinfo import InOutput, RuleInfo
from snakemake.shell import shell
from snakemake.workflow import Workflow
import yaml
import inspect
import ast


def get_object_location(obj):
    """获取对象在源代码中的位置信息"""
    try:
        # 获取文件路径和源代码
        file_path = inspect.getsourcefile(obj)
        source, start_line = inspect.getsourcelines(obj)

        # 如果是类方法，尝试精确定位
        if inspect.ismethod(obj):
            class_name = obj.__qualname__.split('.')[0]
            source_code = ''.join(source)
            module = ast.parse(source_code)

            # 查找类定义
            class_node = None
            for node in module.body:
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    class_node = node
                    break

            if class_node:
                # 查找方法定义
                for method_node in class_node.body:
                    if isinstance(method_node, ast.FunctionDef) and method_node.name == obj.__name__:
                        method_start = start_line + method_node.lineno - 1
                        method_end = start_line + method_node.end_lineno - 1
                        return {
                            "file": file_path,
                            "start_line": method_start,
                            "end_line": method_end,
                            "source": ''.join(source[method_node.lineno-1:method_node.end_lineno])
                        }

        # 通用情况
        end_line = start_line + len(source) - 1
        return {
            "file": file_path,
            "start_line": start_line,
            "end_line": end_line,
            "source": ''.join(source)
        }

    except Exception as e:
        return {"error": f"无法获取位置: {str(e)}"}


class BaseRule:
    def __init__(self):
        self.pre_rule = set()
        self.out_prefix: Path | str = ""

    def add_pre(self, obj):
        if isinstance(obj, set):
            self.pre_rule = self.pre_rule.union(obj)
        else:
            self.pre_rule.add(obj)

    def pre_rules(self) -> list:
        all_rules = []
        for pre in self.pre_rule:
            if isinstance(pre, RuleSet):
                all_rules += pre.rules()
            elif isinstance(pre, MyRule):
                all_rules.append(pre)
            all_rules += pre.pre_rules()
        return all_rules

    def add_out_prefix2(self, file):
        return BaseRule.add_dir_prefix(self.out_prefix, file)

    def out_prefix_call(self, file):
        return BaseRule.create_call(self.add_out_prefix2, file)

    @classmethod
    def add_out_prefix(self, cls, file):
        return BaseRule.add_dir_prefix(cls.out_prefix, file)

    @classmethod
    def try_call(self, obj):
        if callable(obj):
            return obj()
        else:
            return obj

    @classmethod
    def add_dir_prefix(self, prefix, files):
        if isinstance(files, list):
            return [Path(prefix, file) for file in files]
        elif isinstance(files, dict):
            return {key: Path(prefix, file) for key, file in files.items()}
        else:
            return Path(prefix, files)

    @classmethod
    def create_call(self, func, *args, **kwarg):
        def fun():
            return func(*args, **kwarg)
        return fun


class MyRule(BaseRule):
    def __init__(self):
        super().__init__()
        self.name: str = type(self).__name__
        self._input: dict = {}
        self._output: dict = {}
        self._params: dict = {}
        self.script_path: Path | str = ""
        self.command = ""
        self.script: str = ""
        self.args: str | list[str] = ""
        self._init_info_flag = True
        self.snakefile = None  # __file__
        self.lineno = None  # get_object_location(self)

    def shellcmd(self) -> str:
        if isinstance(self.args, list):
            args = " ".join([f"'{str(v)}'" for v in self.args])
        else:
            args = self.args
        if self.script_path is None:
            script = self.script
        else:
            script = Path(self.script_path, self.script)
        if self.command != "":
            script = f"{self.command} {str(script)}"
        return " ".join([str(script), args])

    def func(self):
        def func(input,
                 output,
                 params,
                 wildcards,
                 threads,
                 resources,
                 log,
                 rule,
                 conda_env,
                 container_img,
                 singularity_args,
                 use_singularity,
                 env_modules,
                 bench_record,
                 jobid,
                 is_shell,
                 bench_iteration,
                 cleanup_scripts,
                 passed_shadow_dir,
                 edit_notebook,
                 conda_base_path,
                 basedir,
                 sourcecache_path,
                 runtime_sourcecache_path,):
            shell(self.shellcmd(), bench_record=bench_record,
                  bench_iteration=bench_iteration)
        return func

    def input(self):
        _input = self._input
        if isinstance(_input, dict):
            return {k: str(MyRule.try_call(v)) for k, v in _input.items()}
        elif isinstance(_input, list):
            return [str(MyRule.try_call(v)) for v in _input]
        else:
            return str(MyRule.try_call(_input))

    def kwparams(self):
        return {k: str(MyRule.try_call(v)) for k, v in self._params.items()}

    def output(self):
        if str(self.out_prefix) == "":
            return self._output
        else:
            return self.add_out_prefix2(self._output)

    def all_out(self):
        output = self.output()
        if isinstance(output, dict):
            return list(output.values())
        elif isinstance(output, list):
            return output
        else:
            return [output]

    def init_info(self):
        prefix = self.name
        self._benchmark = Path("benchmark", f"{prefix}.xls")
        self._log = Path("logs", f"{prefix}.txt")
        self._message = self.name

    def benchmark(self):
        if self._init_info_flag:
            self.init_info()
            self._init_info_flag = False
        return self._benchmark

    def log(self):
        if self._init_info_flag:
            self.init_info()
            self._init_info_flag = False
        return self._log

    def message(self):
        if self._init_info_flag:
            self.init_info()
            self._init_info_flag = False
        return self._message

    def join_files_call(self, files_call: list):
        def func():
            files = [str(self.try_call(file)) for file in files_call]
            return ",".join(files)
        return func


class RuleSet(BaseRule):
    def __init__(self, config):
        super().__init__()
        if not isinstance(config, dict):
            config = yaml.load(open(config), Loader=yaml.FullLoader)
        self.config = config
        self.name: str = type(self).__name__
        self.out_prefix: Path | str = ""
        self.script_path: Path | str = " "
        self.rule_sets: list[MyRule | RuleSet] = []
        self.__ext_out_prefix_flag = False
        self.key = None
        self.key_sets: dict[MyRule | RuleSet] = {}
        self.confirm_file = self.out_prefix_call("confirm.yaml")

    def all_out(self):
        all_files = []
        for rule in self.rules():
            all_files += rule.all_out()
        return all_files

    def rules(self) -> list[MyRule]:
        all_rules = []
        for rule in self.rule_sets:
            if isinstance(rule, MyRule):
                all_rules.append(rule)
            elif isinstance(rule, RuleSet):
                all_rules += rule.rules()
        return all_rules

    def bound_workflow(self, workflow: Workflow):
        for r in self.rules():
            ruleinfo = RuleInfo(r.func())
            ruleinfo.shellcmd = r.shellcmd()
            ruleinfo.message = r.message()
            ruleinfo.log = InOutput(
                [r.log()], {}, workflow.modifier.path_modifier)
            # or ruleinfo = workflow.log(r.log())(ruleinfo)
            ruleinfo.benchmark = InOutput(
                r.benchmark(), {}, workflow.modifier.path_modifier)
            # or ruleinfo = workflow.benchmark(r.benchmark())(ruleinfo)
            ruleinfo.params = ([], r.kwparams())
            ruleinfo.output = InOutput(
                [], r.output(), workflow.modifier.path_modifier)
            ruleinfo.input = InOutput(
                [], r.input(), workflow.modifier.path_modifier)
            workflow.rule(name=r.name, lineno=r.lineno,
                          snakefile=r.snakefile)(ruleinfo)

    def ext_out_prefix(self, out_prefix: Path, recurse=True):
        if self.__ext_out_prefix_flag:
            raise RuntimeError(
                "ext_out_prefix can only be executed once! It had been executed.")
        self.__ext_out_prefix_flag = True
        self.out_prefix = Path(out_prefix, self.out_prefix)
        if recurse:
            for rule in self.rule_sets:
                if isinstance(rule, MyRule):
                    rule.out_prefix = Path(self.out_prefix, rule.out_prefix)
                elif isinstance(rule, RuleSet):
                    rule.ext_out_prefix(self.out_prefix, True)

    def ext_script_path(self, script_path: Path, recurse=True):
        self.script_path = script_path
        if recurse:
            for rule in self.rule_sets:
                if isinstance(rule, MyRule):
                    rule.script_path = script_path
                elif isinstance(rule, RuleSet):
                    rule.ext_script_path(script_path, True)

    def ext_rule_name(self, suffix: str, recurse=True):
        self.name = self.name + suffix
        if recurse:
            for rule in self.rule_sets:
                if isinstance(rule, MyRule):
                    rule.name = rule.name + suffix
                elif isinstance(rule, RuleSet):
                    rule.ext_rule_name(suffix, recurse=True)

    def append(self, obj):
        for pre in obj.pre_rule:
            if pre not in self.rule_sets:
                raise ValueError(f"{str(obj)} need pre-rule {str(pre)}")
        if isinstance(obj, RuleSet) and obj.key is not None:
            self.key_sets.update({obj.key: obj})
        self.rule_sets.append(obj)
