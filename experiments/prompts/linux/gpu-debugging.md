---
benchmark: linux--gpu-debugging
version: 2
domain: linux
capability: gpu-runtime-diagnosis
jurisdiction: UK
expected_output: analysis-and-commands
scoring: qualitative
---
# Task

A synthetic Ubuntu host exposes two GPUs. An inference process starts successfully but reports no CUDA devices. On the host, nvidia-smi lists both GPUs and an active unrelated inference service. Host /dev/nvidia0 and /dev/nvidia1 exist. The failing process runs in an OCI container.

Inside that container, ls /dev/nvidia* returns No such file or directory. Its environment contains CUDA_VISIBLE_DEVICES=0. The recorded container launch command did not request GPUs, and inspection shows DeviceRequests is empty. The platform's installed container runtime is configured to provide GPUs only when explicitly requested. The image manifest records a CUDA-enabled framework build with a CUDA runtime supported by the installed host driver; this compatibility has been verified separately for this exact image digest. The workload should receive GPU 1 only, and GPU 0 is reserved for the unrelated service.

Diagnose the strongest supported cause, and propose a corrected launch or equivalent runtime configuration. Describe how device identity should be verified inside and outside the container, including the possibility that the assigned physical device appears as device zero inside. Give a staged validation plan before restarting the full workload.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Preserve the GPU 0 reservation and do not reset GPUs or reinstall drivers as a first step.
- Do not treat CUDA_VISIBLE_DEVICES as a mechanism that grants host device access.
- State the container engine assumption when giving an exact launch command.
- Do not claim commands have been run; provide expected observations.

# Evaluation criteria

1. Distinguishes host driver health from container device exposure.
2. Uses the runtime inspection evidence to identify the missing configuration.
3. Restricts access to the intended physical GPU.
4. Explains visibility and device-index remapping accurately.
5. Validates runtime access and a small computation before full inference.
