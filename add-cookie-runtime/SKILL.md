---
name: add-cookie-runtime
description: "Add another machine to cookie agent as a runtime, over ssh or by dialing in, so sessions and subagents can work there."
when_to_use: Use when the user wants work done on another machine, or gives you ssh access to one (a host, a user, a key or an ssh alias).
---
A runtime lets cookie read, write, and run commands on another machine.
Read the linked pages before you change anything; this is only the outline.

## Two ways

- **A template the daemon starts over ssh** (preferred when the daemon's
  machine can ssh there without a password): a `[runtimes.<id>]` table in
  the daemon's `config.toml` whose `command` is
  `["ssh", "-o", "BatchMode=yes", "<host>", "cookie", "runtime", "serve", "--stdio"]`.
  It needs `cookie` on the remote; nothing stays running there while no
  session uses it. See
  https://cookie-agent.github.io/doc/dev/runtimes/templates/
- **A runtime that dials in**, run on the remote as
  `cookie runtime serve --daemon <daemon url> --token <token>`: for a
  machine the daemon cannot reach over ssh, or one that should stay
  connected. Temporary in a shell or tmux, or permanent as a service. The
  daemon must listen where the remote reaches it (`cookie daemon --listen`).
  See https://cookie-agent.github.io/doc/dev/runtimes/dial-in/ and
  https://cookie-agent.github.io/doc/dev/runtimes/service/

## Steps

1. Check the remote: `ssh <host> cookie --version`. If cookie is missing,
   ask the user before installing it; the installer is one command, see
   https://cookie-agent.github.io/doc/dev/install/
2. Add the template with the daemon's own tools, not by editing files:
   `cookie config edit` (or `cookie config set` per key). `runtimes`
   changes need a restart: `cookie daemon restart`, after telling the user,
   since this session runs on that daemon too.
3. Verify: `list_runtimes` (or `cookie machine list`) shows the runtime and
   its machine.
4. Use it (https://cookie-agent.github.io/doc/dev/runtimes/ explains
   capabilities and workspaces): delegate to a subagent with `capabilities` naming
   `<runtime_id>/coding` and a `workspace` on that machine, or attach it to
   a session with `/runtime`. See
   https://cookie-agent.github.io/doc/dev/sessions/delegation/

## Safety

- Ask before installing software or leaving a service running on the
  user's machine.
- Never print the daemon's token in the transcript or in a command the user
  sees; pass it through `COOKIE_DAEMON_TOKEN` or a file only the user reads.
- Remove what you set up for a one-off task when it is done: stop a
  temporary dial-in, and remove a template you no longer need.
