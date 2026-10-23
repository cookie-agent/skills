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
checks their hashes, and keeps them in `~/.cookie-agent/managed/skills/`. A
user skill with the same name always wins.

Every push is checked by CI against the latest Cookie Agent release: each
skill must parse, name only `cookie` subcommands that exist, and link only to
documentation pages that exist.
