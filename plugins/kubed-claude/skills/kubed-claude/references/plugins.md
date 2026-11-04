# Plugins

A plugin is a folder Claude Code installs from a marketplace (a git repository
with `.claude-plugin/marketplace.json`). Add one with `/plugin marketplace add
<owner>/<repo>`; a plugin installs as `<plugin>@<marketplace>`.

```
plugins/<plugin>/
  .claude-plugin/plugin.json   name, version, description
  skills/<skill>/SKILL.md      /<plugin>:<skill>, and the model can load it
  commands/<name>.md           /<plugin>:<name>
  agents/<name>.md             subagents, with fields ignored (below)
  hooks/, .mcp.json            hooks and MCP servers for every session it is on in
```

- **Bump `version`** in `plugin.json` when a change should reach installed
  copies.
- **Names are policed.** `claude plugin validate <dir>` refuses a third-party name
  that is `claude`, `claude-code`, `anthropic`…, or starts with `claude-`,
  `anthropic-` or `cc-plugin-`; one that merely contains `claude` passes with a
  warning. It also warns when there's no icon. Run it before the first push.
  (Tested 2.1.316.) A reserved name still loads with `--plugin-dir` and installs
  from a marketplace today; only `validate` refuses it, so don't count on that lasting.
- `${CLAUDE_PLUGIN_ROOT}` in a body is the plugin's folder. kubed-io/mcp-kb
  rewrites it to `skill://<library>` when it serves the plugin.
- **A plugin's `bin/`** is on the Bash tool's `PATH` only. An MCP `headersHelper` in
  the plugin's `.mcp.json` must say `${CLAUDE_PLUGIN_ROOT}/bin/<tool> <args>`; the bare
  name never ran and its server never connected. The helper gets `CLAUDE_PLUGIN_ROOT`
  and `CLAUDE_CODE_MCP_SERVER_NAME` (`plugin:<plugin>:<server>`). **tested** 2.1.316
  One plugin's `${CLAUDE_PLUGIN_ROOT}` can't name another's folder. A symlink to a
  file outside the plugin is copied into the cache as the real file. **tested** 2.1.316
- **`defaultEnabled: false`** in `plugin.json` keeps the plugin off under `--plugin-dir`
  too: `--agent <plugin>:x` is "not found" until `--settings` sets
  `"<plugin>@inline": true`. **tested** 2.1.316
- A plugin's MCP servers load into the **main** session. For a server only one
  agent should have, use a user or project agent with inline `mcpServers`.

## What a plugin agent ignores

Docs: `mcpServers`, `hooks` and `permissionMode` (and `initialPrompt`) in a
plugin's `agents/*.md`. Two ways round it:

- A mod in the plugin registers the agent at `session.start` with
  `$.agent.register`; its inline `mcpServers` connect. **tested** 2.1.316
  ([hooks.md](hooks.md)).
- The agent lives in `.claude/agents/` or the user's `agents/`, or comes in
  with `--agents`.

## Ways a plugin loads

No marketplace is needed for most of them. **docs** (`plugins/loading`)

| How | Id | Notes |
|---|---|---|
| `claude plugin install <name>@<marketplace>` | `@<marketplace>` | Copied into `cache/<marketplace>/<plugin>/<version>/` |
| `--plugin-dir <dir or .zip>` (repeatable) | `@inline` | This session only, loaded in place. Wins a name clash with an installed plugin, silently |
| `--plugin-url <https .zip>` | `@inline` | Downloaded at startup, this session only |
| `CLAUDE_CODE_PLUGIN_DIRS` | `@inline` | Same, for when you can't pass a flag (2.1.280+) |
| A folder with `.claude-plugin/plugin.json` under `~/.claude/skills/` or the project's `.claude/skills/` | `@skills-dir` | Every session, no install. `claude plugin init` makes one. A project one needs workspace trust |
| On for your claude.ai account | `@synced` | Downloaded once per start |
| `extraKnownMarketplaces` with a `settings` source | `@<name>` | The catalog written inline in settings; object sources only |

**Install scopes, tested** 2.1.316. `claude plugin install <id> --scope
user|project|local` changes only which settings file gets `enabledPlugins`. The
files always go to `<config dir>/plugins/cache/` (or `CLAUDE_CODE_PLUGIN_CACHE_DIR`),
and `installed_plugins.json` records the scope and `projectPath`. A project
install doesn't put the marketplace in the repository. For teammates, run
`claude plugin marketplace add … --scope project` too.

A plugin in the **user's** skills folder (`$CLAUDE_CONFIG_DIR/skills/<folder>/`) did
load under `claude -p`: no marketplace, no install, no trust check. Its agents
appeared as `<plugin>:<agent>`, and it loads in place, so a `git pull` there is the
update. **tested** 2.1.316, `/claude/skills` on the pod.

A plugin kept in a repository's `.claude/skills/<plugin>/` did **not** load
under `claude -p`: there's no trust dialog. For a runner, use `--plugin-dir` on
the checkout instead. **tested** 2.1.316. `claude plugin install <package>@npm`
installs from npm with no marketplace (CLI help).

Claude Code never scans a project's `.claude/plugins/`. Edits reach a running
session after `/reload-plugins`. A plugin in a marketplace added from a local
directory loads in place, so it needs no version bump.

## How dynamic a plugin can be

- **`command` source.** The entry runs a command that prints a plugin directory.
  It runs again once per session, in the background; when the output's hash
  changes, the new version loads into the running session. The user approves the
  command at install. **docs**
- **A mod** registers tools, commands and agents in code at each start ([hooks.md](hooks.md)).
- **A `SessionStart` hook** writes skill files and returns `reloadSkills: true`.
  A new file in an existing `agents/` folder is picked up by itself.

## What an install fetches

| Source | Fetches |
|---|---|
| Marketplace from GitHub or git | A clone of the repository: all of it, unless added with `--sparse <dirs>` (`sparsePaths`). Submodules only where plugin files are (2.1.295+) |
| Marketplace from a URL | `marketplace.json` alone, so a relative entry fails at install ("a relative entry in a url-catalog marketplace"). **tested** 2.1.316 |
| A zip as a marketplace | Not a thing: the add treats the URL as a git repo and fails. Only plugins come as zips. **tested** 2.1.316 |
| Plugin, relative path | Only the plugin's folder is copied to the cache. A file above it (`../shared`) is not there |
| Plugin, `github` or `url` | That whole repository |
| Plugin, `git-subdir` (`url`, `path`) | One folder, by sparse partial clone |
| Plugin, `npm`, `archive` (https zip, `sha256`), `command` | The package, the zip, or the printed folder |

**`--sparse`, tested** 2.1.316 (`marketplace add kubed-io/skills --sparse
.claude-plugin plugins/drawio`, in a scratch `CLAUDE_CONFIG_DIR`):

- It's a shallow, `blob:none` partial clone with a cone-mode sparse checkout.
  Files at the repository root (README, LICENSE) always come too.
- The paths are saved as `sparsePaths` in `extraKnownMarketplaces` and
  `known_marketplaces.json`.
- The catalog still lists every plugin. Installing one outside the paths fails
  with `Source path does not exist`. Keep `.claude-plugin` in the list.

**`archive`, tested** 2.1.316: a GitHub source zip
(`github.com/<owner>/<repo>/archive/<sha>.zip`) installs through its redirect to
codeload, with the plugin one folder down. The version came from `plugin.json`.
A wrong `sha256` refuses the install and prints the real digest.
A release asset (`releases/download/<tag>/<file>.zip`) downloads through its
redirect to `release-assets.githubusercontent.com`. A zip with no plugin at the
top, or inside one wrapper folder, is refused as "no plugin content".

Adding a marketplace only fetches its catalog. `claude plugin install
<name>@<marketplace>` installs that one plugin and nothing else. A plugin that
lives in another project's repository, beside the server it talks to, is best
listed in our marketplace as a `git-subdir` entry: no second repository, and
users fetch only that folder.

## Configuring a plugin

A plugin asks for settings through `userConfig` in `plugin.json`: typed options
(`string`, `number`, `boolean`, `directory`, `file`) with `title`, `description`,
`default`, `required`, `options` (a picker), `multiple`, and `sensitive`. **docs**
(`plugins/manifest-reference`)

| Where the user sets them | How |
|---|---|
| `/plugin` install or enable, `/plugin configure <id>` | A dialog for options not yet set |
| `/config` | One row per option, except sensitive and `multiple` ones |
| VS Code Manage plugins | A form after install; the gear icon reopens it |
| Shell | `claude plugin install <id> --config KEY=VALUE`, or JSON on stdin to `claude plugin configure <id> --values-stdin`. `claude plugin install` alone never asks |
| A headless run | `--settings <file or JSON>` with `{"pluginConfigs":{"<id>":{"options":{...}}}}` works, though the docs list only user and managed settings. **tested** 2.1.316 |
| A project's `.claude/settings.json` or `settings.local.json` | **Ignored**: the defaults came through. A repository can't configure a plugin, but its local settings can enable one that user settings configure. **tested** 2.1.316 |

Plain values land in user `settings.json` under `pluginConfigs."<id>".options`;
sensitive ones in the keychain or `.credentials.json`. **tested** 2.1.316.

How components read them: `${user_config.KEY}` in MCP and LSP server config,
exec-form hook `args`, and skill, command and agent text (**tested** 2.1.316:
all three substituted; a sensitive one becomes `[sensitive option 'token' not
available in skill content]`); `CLAUDE_PLUGIN_OPTION_<KEY>` in
hook processes; a mod gets them as `register(on, options)`, defaults filled in.
**tested** 2.1.316: a `multiple` value saved through `--values-stdin` reaches
the mod as a JSON **string**, so parse it when it isn't an array.

## Install by declaring it

Settings with `extraKnownMarketplaces` (the source, optional `sparsePaths`,
`autoUpdate`) and `enabledPlugins` are enough: no install command is needed.
Claude Code clones and caches in the background after a session starts.
**tested** 2.1.316, `claude -p --settings` with `CLAUDE_CODE_PLUGIN_CACHE_DIR`
in scratch:

- Run 1 cloned the catalog.
- Run 2 cached the plugin.
- Run 3 loaded it.

Interactive sessions offer `/reload-plugins` instead. A runner that must have it
on its first run installs explicitly, mounts a seed
(`CLAUDE_CODE_PLUGIN_SEED_DIR`, built with `CLAUDE_CODE_PLUGIN_CACHE_DIR`), or
uses `--plugin-dir`. A plugin enabled only in a project's settings isn't
fetched.

## Private repositories

**tested** 2.1.316, adding the private `kubed-io/github`: the SSH key on the pod
cloned it, and so did HTTPS with `GH_TOKEN` through `gh auth git-credential`.
With no credential, HTTPS failed at once (`unable to get password`) rather than
hanging. **docs** (`plugins/host-marketplace`). Everything git-based works the same on a
private repository, `--sparse` and `git-subdir` included, because Claude Code
runs the user's own `git` with prompts off. Nothing in `marketplace.json` holds a
token.

- **`owner/repo`** tries SSH first (a key in `ssh-agent`), then HTTPS.
  `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` skips the SSH probe; `/plugin` and updates
  don't fall back on their own.
- **HTTPS** needs a stored credential: `gh auth login` then `gh auth setup-git`.
  `GITHUB_TOKEN` alone does nothing without a helper that reads it.
- **Background auto-update** that can't authenticate fails quietly, or re-clones.
  `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1` keeps the old checkout.
- **A private `archive`** needs `headers` or a `headersHelper`:
  - The entry must set `strict: false`.
  - The user accepts the command at install.
  - Auto-update skips the plugin.
  - Headers are dropped on a redirect to another origin.

## Marketplace or plugin

A marketplace is a catalog, not a plugin that holds plugins. It contributes no
skills, agents or hooks of its own. Only a marketplace can:

- Name the namespace after the `@`, and be the unit people trust, block,
  allow (`strictKnownMarketplaces`) and auto-update.
- Add to an entry: components appended to its `plugin.json` (`strict`, the
  default), `displayName`, `category`, `tags`, `defaultEnabled`, `relevance`,
  `dependencies`, archive `headers`.
- Manage the catalog: `renames`, `forceRemoveDeletedPlugins`,
  `allowCrossMarketplaceDependenciesOn`, `metadata.pluginRoot`.

A plugin can't contain plugins; the nearest is `dependencies`. One repository
can be both: an entry with `"source": "./"`.

## Where to keep agents

| Agents for | Keep them in | Because |
|---|---|---|
| One repository | `.claude/agents/`, committed | Versioned with the code they serve |
| You, everywhere on one machine or shared config dir | `$CLAUDE_CONFIG_DIR/agents/` (or `~/.claude/agents/`) | Every session and every headless job sharing that config dir sees them. Keeps `mcpServers` and `hooks` |
| Anyone, anywhere | A plugin | Installable and versioned, but loses `mcpServers`, `hooks`, `permissionMode` |
| One CI job | `--agents '<json>'` built from a file | Highest priority below managed settings; no file left behind |

A config dir is live state, not history: keep the agent files in a repository
and copy them in. Never commit the config dir itself (`.credentials.json`,
`.claude.json` hold secrets).

Agents written for a job (they read job files, never commit, answer in a schema)
mislead in a chat. Keep job agents with the job and chat agents in the shared
dir. An `--agent` main session with `tools: Agent(a, b)` keeps the rest of the
shared dir out of its reach ([agents.md](agents.md)).
