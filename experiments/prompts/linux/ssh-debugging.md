---
benchmark: linux--ssh-debugging
version: 2
domain: linux
capability: ssh-authentication-diagnosis
jurisdiction: UK
expected_output: analysis-and-commands
scoring: qualitative
---
# Task

An operator cannot log in to a synthetic Ubuntu host as deploy using an Ed25519 key. This is a key-authentication incident; password login is intentionally disabled. They still have a separate working administrative session.

The client debug trace shows a successful TCP connection and host-key verification, then Offering public key: /home/operator/.ssh/deploy_ed25519, followed by Authentications that can continue: publickey. It never prints Server accepts key. The server journal at the same timestamp says: Authentication refused: bad ownership or modes for directory /home/deploy/.ssh.

On the server:
/home/deploy is owned by deploy:deploy, mode 0755.
/home/deploy/.ssh is owned by deploy:deploy, mode 0777.
/home/deploy/.ssh/authorized_keys is owned by deploy:deploy, mode 0600.
The administrator has independently confirmed that the offered public-key fingerprint matches the intended authorized_keys entry. The effective sshd configuration for this user has PubkeyAuthentication yes, StrictModes yes, and PasswordAuthentication no.

Explain the most likely cause and provide a minimal repair, validation, and safe retest sequence. Include what the client and server evidence has already ruled out and which additional checks would become appropriate only if the repair fails.

# Constraints

- This is a closed-book benchmark. Use the supplied evidence and rules; do not browse, run commands, or claim external verification. Any requested code or commands are proposals, not actions to execute.
- Keep the working administrative session open throughout the proposed retest.
- Do not disable StrictModes, enable passwords, or request private-key contents.
- Use commands appropriate to the stated paths and account.
- State whether your proposed permission-only repair needs an sshd restart.

# Evaluation criteria

1. Locates the failure at the authentication stage.
2. Connects the server refusal to a specific ownership or mode problem.
3. Proposes narrowly scoped permission changes preserving key security.
4. Verifies recovery from both client and server perspectives.
5. Avoids unsupported diagnoses and unnecessary service disruption.
