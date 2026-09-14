---
benchmark: linux--process-thread
version: 0
domain: linux
capability: process-thread-diagnosis
jurisdiction: UK
expected_output: analysis-and-commands
scoring: qualitative
---
You are troubleshooting a production Linux service.

A service is consuming unexpectedly high CPU and appears to have many threads.

Explain:

1. How you would determine which process is responsible.
2. How you would determine how many threads the process has.
3. How you would identify which individual threads are consuming CPU.
4. Which Linux commands you would use and what each command tells you.
5. How you would distinguish a process-level CPU problem from a single-thread bottleneck.
6. What additional information you would collect before deciding how to fix the problem.

Give practical commands suitable for Ubuntu Linux and explain the important parts of their output.
