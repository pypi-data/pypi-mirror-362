import qiskit.qasm3 as qasm3
from qiskit import QuantumCircuit, transpile
from qiskit_aer import qasm_simulator
from uqc_client.validator import ensure_static_qasm

qasm_code = """
OPENQASM 3.0;
include "stdgates.inc";
gate rzz(p0) _gate_q_0, _gate_q_1 {  
  cx _gate_q_0, _gate_q_1;  
  rz(p0) _gate_q_1;  
  cx _gate_q_0, _gate_q_1;
} 
bit[2] meas;qubit[2] q;
ry(pi/2) q[0];
rx(pi) q[0];
ry(pi/2) q[1];
rx(pi) q[1];
rzz(pi/2) q[0], q[1];
rx(pi/2) q[0];
ry(pi/2) q[0];
rx(-pi/2) q[0];
ry(pi/2) q[1];
rx(pi/2) q[1];
barrier q[0], q[1];
meas[0] = measure q[0];
meas[1] = measure q[1];
"""

qasm_code_2 = """
  OPENQASM 3.0;
  include "stdgates.inc";
  gate rzz(p0) _gate_q_0, _gate_q_1 {
    cx _gate_q_0, _gate_q_1;
    rz(p0) _gate_q_1;
    cx _gate_q_0, _gate_q_1;
  }

  qubit[2] q;
  rzz(pi/2) q[0], q[1];
  rx(0.3, 1.2) q[0];
"""

# ensure_static_qasm

ensure_static_qasm(qasm_code)

shot = 100
circ = qasm3.loads(qasm_code)

# 打印线路
print("构造的量子线路:")
print(circ)
