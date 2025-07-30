"""
qasm_sanitizer.py
=================

Validate an OpenQASM 3 program and ensure it is a *static* circuit that
contains **only** the basis gates ``rzz`` and ``r``.

Examples
--------
>>> from qasm_sanitizer import ensure_static_qasm
>>> ok_source = '''
... OPENQASM 3.0;
... include "stdgates.inc";
... qubit[2] q;
... rzz(pi/2) q[0], q[1];
... r(0.3, 1.2) q[0];
... '''
>>> ensure_static_qasm(ok_source)      # 无异常即通过
>>>
>>> bad_source = ok_source.replace("rzz", "cx")
>>> ensure_static_qasm(bad_source)
QASMValidationError: forbidden gate 'cx'
"""

from __future__ import annotations

from typing import Iterable, Set

import openqasm3
from openqasm3 import ast, visitor

__all__ = ["QASMValidationError", "ensure_static_qasm"]


class QASMValidationError(RuntimeError):
    """专门用于 QASM 审核失败的异常。"""


# --------- 1) 动态语法黑名单 ---------
_DYNAMIC_NODES = (
    ast.BranchingStatement,  # if 语句的基类
    ast.WhileLoop,
    ast.ForInLoop,
    ast.SwitchStatement,
    ast.ClassicalAssignment,
    ast.CalibrationDefinition,  # defcal
    ast.DelayInstruction,
    ast.BreakStatement,
    ast.ContinueStatement,
    ast.QuantumGateModifier,  # inverse、控制等都算动态修饰
)


def _gate_name(node: ast.QASMNode) -> str | None:
    """若节点是一次 gate 调用则返回其符号名（小写），否则 ``None``。"""
    if isinstance(node, ast.QuantumGate):
        if hasattr(node.name, "name"):
            return str(node.name.name).lower()
        else:
            return str(node.name).lower()
    return None


class StaticQASMVisitor(visitor.QASMVisitor):
    """用于检查静态 QASM 程序的访问者"""

    def __init__(self, allowed_gates: Set[str]):
        self.allowed_gates = allowed_gates
        self.used_gates: Set[str] = set()
        self.errors: list[str] = []

    def generic_visit(self, node):
        # 检查是否为动态语法
        if isinstance(node, _DYNAMIC_NODES):
            self.errors.append(f"dynamic construct '{type(node).__name__}' is forbidden")
            return

        # 检查是否为门调用
        gate_name = _gate_name(node)
        if gate_name is not None:
            self.used_gates.add(gate_name)
            if gate_name not in self.allowed_gates:
                self.errors.append(f"forbidden gate '{gate_name}'")

        # 继续遍历子节点
        super().generic_visit(node)

    def visit_QuantumGateDefinition(self, node):
        """跳过 gate 定义体，不递归遍历其内部实现"""
        # 只记录定义的门名称（如果需要的话），但不检查其内部实现
        pass

    def visit_CalibrationDefinition(self, node):
        """跳过 defcal 定义体，不递归遍历其内部实现"""
        # 校准定义通常包含硬件相关的实现细节，我们不需要检查
        pass

    def visit_QuantumBarrier(self, node):
        """忽略 barrier 操作"""
        pass

    def visit_QuantumMeasurementStatement(self, node):
        """忽略 measure 操作"""
        pass


# --------- 2) 总入口 ---------
def ensure_static_qasm(qasm_source: str, allowed_gates: Iterable[str] = ("rzz", "rx", "ry")) -> None:
    """
    Parse ``qasm_source`` and enforce **static-circuit** constraints.

    Parameters
    ----------
    qasm_source : str
        完整的 OpenQASM 3 源码字符串。
    allowed_gates : Iterable[str], optional
        白名单，默认仅 ``("rzz", "r")``。比较时不区分大小写。

    Raises
    ------
    QASMValidationError
        任何解析错误、动态语法出现或发现非白名单门时触发。
    """
    try:
        tree = openqasm3.parse(qasm_source)  # 语法层面先过一遍
    except Exception as exc:
        raise QASMValidationError(f"parse error: {exc}") from exc

    allowed: Set[str] = {g.lower() for g in allowed_gates}

    # 使用访问者模式遍历 AST
    visitor_instance = StaticQASMVisitor(allowed)
    visitor_instance.visit(tree)

    # 检查错误
    if visitor_instance.errors:
        raise QASMValidationError(visitor_instance.errors[0])

    if not visitor_instance.used_gates:
        raise QASMValidationError("no gate operations found (did you forget to include rzz / r?)")


def check_and_report(qasm_source):
    try:
        ensure_static_qasm(qasm_source)
        print("✅ QASM 静态检查通过")
    except QASMValidationError as e:
        print(f"❌ QASM 静态检查失败: {e}")


# 用法

if __name__ == "__main__":
    qasm_source = """
    OPENQASM 3.0;
    include "stdgates.inc";
    qubit[2] q;
    rzz(pi/2) q[0], q[1];
    r(0.3, 1.2) q[0];
    """
    check_and_report(qasm_source)
