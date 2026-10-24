# Cookie Agent official skills

Skills that [Cookie Agent](https://github.com/cookie-agent/cookie-agent) keeps up
to date on every daemon that enables them (`[skills] official = true`, the
default). They are served from GitHub Pages at
<https://cookie-agent.github.io/skills/>, a URL that carries no version: each
skill in `index.json` states the Cookie Agent versions it works with
(`requires_cookie`), and a daemon only installs the skills its version
satisfies.

- `index.json` lists every skill with its version, `requires_cookie` range,
  and the SHA-256 of each file.
- `<name>/SKILL.md` is the skill itself.

A daemon fetches the index at start and then daily, downloads changed files,
checks their hashes, and keeps them in `official_skills/` in the daemon's data root (`~/.cookie-agent/official_skills/` by default). A
user skill with the same name always wins.

Every push is checked by CI against the newest Cookie Agent release, nightly builds included: each
skill must parse, name only `cookie` subcommands that exist, and link only to
documentation pages that exist.

## Changing a skill

Edit `<name>/SKILL.md`, bump the skill's `version` in `index.json` (and its
`requires_cookie` when it starts relying on a newer Cookie Agent), then run
`scripts/update-index.py` to refresh the hashes and `cookie skills check .`
to validate it (`--docs <cookie-agent>/docs/site` checks links against a
docs checkout instead of the published site).
