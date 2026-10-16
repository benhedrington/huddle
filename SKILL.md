---
name: huddle
description: Use when someone says "huddle PROJ-123", "collaborate on PROJ-123", or "huddle PROJ". Finds or creates one shared Confluence page per ticket where PM, engineering, design and architecture build the problem together, or lists the huddles in a Jira project.
---

# huddle

One shared page per ticket, built by the PM, engineer, designer and architect together, before the problem is written up and handed off.

## When to use

- The user says "huddle <ticket>" or "collaborate <ticket>" (one ticket: open or create).
- The user says "huddle <PROJECT>" with letters only and no number (list the huddles in that project).
- A problem is still disputed, or two or more roles have open questions.
- Skip it for known fixes and small papercuts. A known fix does not need three people in a document.

## Exact names (use these verbatim when creating)

When creating, use exactly these. Do not vary case, spacing, or wording. `<KEY>` is the ticket key as written in Jira (for example `PROJ-123`). `<key>` is the same key in lowercase (`proj-123`).

| Thing | Exact value |
|---|---|
| Page title | `[<KEY>] Huddle` |
| Page labels (both, always) | `huddle` and `huddle-<key>` |
| Ticket label (on the Jira issue) | `huddle` |
| Ticket link text | `Huddle` |
| Ticket link target | the page URL |
| Ticket comment (first line, verbatim) | `Huddle page opened: <page URL>` |

The ticket link is a remote link titled `Huddle`. If remote links are not available, use the ticket label `huddle` plus the pinned comment above, and treat that comment as the link.

Lookup is flexible. Match on any of these values, and also on a close variant (a page titled differently that carries the ticket key, a similar label, a comment that links a Confluence page). Strict naming applies to what the skill creates, so its own pages are always easy to find.

## Flow

1. **Read the ticket.** Look for a remote link titled `Huddle`, a comment starting `Huddle page opened:`, or the ticket label `huddle`. Accept close variants, such as any remote link or comment pointing at a Confluence page that mentions the ticket.
2. **If found:** open the page. Summarize it through the user's role lens (below). Show open questions and any empty sections. Stop.
3. **If not found:** search Confluence for the page label `huddle-<key>`, then for the title `[<KEY>] Huddle`, then loosely for pages that mention the ticket key. This catches a page whose ticket link was lost. If one is found, repair the ticket link and label (step 6), then open it. Do not create a new page.
4. **If still not found:** check the ticket level. If it is a story or a small fix, say so and suggest the parent epic. Otherwise resolve the space and hub (see Where pages live), then ask in one question: "No huddle page for <KEY>. Create one in the Huddles space (<space key>), under <hub page>?"
5. **On yes:** search once more right before creating, in case a teammate just did. Then create the page from `templates/page.md` under the hub page in `HUDDLE_SPACE` (see Where pages live; the confirmation named the space and hub), with the exact title and both labels from the table. Fill `Opened by` with the current user's display name, resolved with `getJiraCurrentUser` (reached through `discover`, then `executeRead`). Do not rely on `atlassianUserInfo`: it returns only the account ID. Treat the connector's logged-in user as the person running the skill. If the name cannot be resolved, write `Opened by: (name not available), <date>` and mention this in the reply. Do not touch permissions.
6. **After creating (or repairing):** read back who can view and edit the page (see Permissions). Only if the other roles can open it, on the Jira issue, add the label `huddle`, add the remote link titled `Huddle`, and post the comment `Huddle page opened: <page URL>`, followed by a line mentioning the PM, engineer, designer and architect on the ticket if they are known. That comment's timestamp records when the page opened.

Always ask before creating. Never create a second page for a ticket that already has one.

## Where pages live

Convention: the organization has a Confluence space named `Huddles`, with a hub page titled `Huddles` labelled `huddle-hub`. Admins set this up once (see Admin setup). Do not hardcode a company-specific space; the `Huddles` convention is the default and the search by that name is discovery, not a fixed value.

Settings (reused for the session):

- `HUDDLE_SPACE`: the space key where huddle pages are created.
- `HUDDLE_HUB`: the hub page inside that space.

Optional: a `config.md` next to `SKILL.md` may set `HUDDLE_SPACE` and `HUDDLE_HUB` for an organization without editing the skill.

Finding the space:

1. If `HUDDLE_SPACE` is already set (by the user or a config), use it.
2. Otherwise search for a non-personal space named exactly `Huddles` (case-insensitive).
   - Exactly one match: propose it and ask the user to confirm, naming the key. Example: "No huddle page for <KEY>. Create one in the Huddles space (<space key>), under <hub page>?"
   - No match, more than one, or only close variants (for example `Team Huddles`): ask "Which Confluence space should huddle pages live in?" Do not guess.
3. Once confirmed, reuse the answer for the session.

Finding the hub:

1. Within `HUDDLE_SPACE`, look for the page labelled `huddle-hub`.
2. If none, look for a page titled `Huddles` in that space. If it is the space home page, ask whether to use it as the hub. Do not edit its content.
3. If neither exists, ask before creating a hub. Create it with the title `Huddles`, the label `huddle-hub`, a short note ("Collaboration pages, one per ticket. Created by the huddle skill."), and a Content by Label list for the label `huddle`.
4. Always identify the hub by space plus page, never by title alone. Titles repeat across spaces.

Rules:

1. Create every huddle page as a child of the hub in `HUDDLE_SPACE`. Never create in a personal space.
2. Name the exact space and hub page when asking for confirmation to create.
3. If the hub exists but has no Content by Label list, say so and offer to add it. Ask before editing an existing page.
4. List mode (`huddle PROJ`) searches within `HUDDLE_SPACE` first, then everywhere if nothing is found.

## Admin setup (once per organization)

1. Create a Confluence space named `Huddles`. Give everyone who collaborates on tickets (PM, engineering, design, architecture) access that allows viewing and editing pages.
2. Create a page titled `Huddles` in that space with the label `huddle-hub`. Add a Content by Label list for the label `huddle`.
3. Do not restrict the hub page or the space beyond that audience. Huddle pages inherit space permissions, and the skill never changes them.

## Permissions

The skill does not set or change permissions. A huddle page inherits the space's permissions.

- Never widen who can view a page. Early problem framing and open disagreements may be sensitive, and the skill cannot tell.
- Never add page restrictions either. Unrestricted inside the space is the intended state, so everyone with space access can view and edit.
- **Never call** `setConfluenceContentRestrictionState`, `addConfluenceContentPermissions`, `removeConfluenceContentPermissions`, `replaceConfluenceContentPermissions`, `enableConfluencePublicLink` or `disableConfluencePublicLink`. They exist in the toolset; this skill reads access and never changes it.
- **After creating, read back access** with `getConfluenceContentRestrictionState` (OPEN, EDIT_RESTRICTED or fully restricted) and `getConfluenceContentPermissions`. Report in one line who can view and edit the page (space-level or restricted). Example: "Created [PROJ-123] Huddle in <space>. Inherits space permissions: viewable and editable by <group or 'everyone with space access'>."
- **If the read-back is not possible**, say so. Do not claim access is fine.
- **If the audience looks too narrow** for the roles on the ticket (for example the architect or designer is not in the space), tell the user and ask what to do. Do not fix it yourself. Suggest they ask a space admin or choose a different space.
- **If the page turns out restricted** (a space or parent default), say so plainly and stop before announcing it on the ticket. A page the other roles cannot open should not be linked as the team's collaboration surface.

## Finding huddles in a project

Trigger: the user gives a project key with no number, such as `huddle PROJ`.

1. **Search Confluence** for pages labelled `huddle` whose title starts with `[PROJ-`. Also accept pages labelled `huddle-proj-*`. If label search is unavailable, search Jira for issues in the project with the label `huddle` and follow their `Huddle` links.
2. **For each page found**, read the title, last-updated date, last editor, and the count of unchecked items under Open questions.
3. **Show a short list**, most recently updated first:

   `[PROJ-123] Huddle | updated 2 days ago by <name> | 3 open questions | <ticket status>`

4. **Flag**, without being asked:
   - Pages with no update in 14 days (possibly stalled).
   - Pages where every contribution comes from one person (not yet a huddle).
   - Pages whose ticket is closed or done.
5. **Then ask** which one to open. Opening one follows the normal flow above.

If nothing is found, say so and offer `huddle PROJ-<number>` for a specific ticket. Do not create anything in this mode.

If the user gives several projects, or says "my area", ask which project keys, or use the keys they have stated earlier in the conversation.

## Page sections (by purpose, not by role)

Problem and outcome. Ideas and options. Constraints and feasibility. Decisions. Open questions. Links.

Anyone can add to any section. Roles do not own sections.

## Role lens (what to show first, never a permission)

- PM: problem and outcome, open questions.
- Engineer: constraints and feasibility, open questions.
- Designer: problem and outcome, ideas and options, open questions.
- Architect: decisions, constraints, dependencies.

The whole page is always readable and writable by everyone. If the user does not state a role, show the whole page in order.

## Writing rules

- Tag every contribution with the author's name and, optionally, their role.
- Never overwrite or delete text that another person added. Disagree with a reply or an inline comment so the discussion stays visible.
- Untouched template placeholders are not contributions. The first real contribution to a section replaces any untouched placeholder there (a placeholder task item or blank table row). "Untouched" means the text matches the template exactly. If unsure whether text is a placeholder, leave it and ask.
- Guidance text under a heading stays. Add contributions after it, never in place of it.
- Add Open questions as sibling task items in the existing task list, or as the first item if the section is empty. Never use an insert-after edit that wraps the new item in a new list; that nests it under the previous item. After the first edit on a site, read the page back to confirm the item is top-level, and fix it if nested.
- Check the page version immediately before every write (`listConfluenceContentVersions`, newest first). If it changed since you read it, read again and merge. Never replace. If a write times out, check the version before retrying so the edit is not applied twice.
- Record decisions with who agreed and the reason.
- Flag empty sections when opening the page. Do not fill them with invented content.

## Do not

- Add workflows beyond find, read, append and flag.
- Write on someone's behalf without saying so.
- Put credentials, customer data or anything confidential in the page unless the user says it belongs there.

## Tool needs

Written against the Atlassian Rovo MCP server's supported-tools page (checked Oct 2026). Refer to capabilities first; tool names below are the current catalog. Older deployments use older names (`createConfluencePage`, `searchConfluenceUsingCql`, `addCommentToJiraIssue`, `getJiraIssueRemoteIssueLinks`), so match by what a tool does.

| Need | Current tool |
|---|---|
| Site id (required for calls) | `getAccessibleAtlassianResources` (cloudId) |
| Current user display name (for `Opened by`) | `getJiraCurrentUser` (via `discover`, `executeRead`) |
| Read ticket | `getJiraIssue` |
| Read ticket remote links | `listJiraIssueRemoteIssueLinks` |
| Add remote link `Huddle` | `createJiraIssueRemoteIssueLink` |
| Add ticket label | `editJiraIssue` |
| Comment on ticket | `addOrEditJiraIssueComment` |
| Find tickets in a project | `searchJiraIssuesUsingJql` |
| Find pages (by label, title, key) | `searchConfluence` (CQL) |
| Create page | `createConfluenceContent` |
| Put page under the hub | `moveConfluenceContent` if create takes no parent |
| Add page labels | `addLabelsToConfluenceContent` |
| Read page / comments / open tasks | `getConfluenceContent`, `listConfluenceComments`, `listConfluenceTasks` |
| Edit page | `updateConfluenceContent` |
| Version before write | `listConfluenceContentVersions` |
| Access read-back | `getConfluenceContentRestrictionState`, `getConfluenceContentPermissions` |

Notes:

- The server shows only a few primary tools up front. If a tool above is not listed, use `discover` to find it.
- Write tools need the `write_jira` and `write_confluence` permission groups, granted by an org admin. If a write fails for permission, say so and stop. Do not retry another way.
- Open questions are written as Confluence tasks (`- [ ]` in the template), so `listConfluenceTasks` counts the unchecked ones for the list view.
- Last editor and last-updated for the list view come from the page or `listConfluenceContentVersions`. If not returned, show the date only.
- If a remote link cannot be added, use the label plus the pinned comment (see Exact names).
- Many of these tools are only reachable through `discover` and the `executeRead` / `executeWrite` wrappers. Pass `cloudId` at the top level and inside `inputs`. If a wrapper call fails with "Invalid URL" for the cloud ID, the top-level `cloudId` is missing.
- `editJiraIssue` sets the whole `labels` array rather than appending. Read the current labels first and send the full list.
- A write can time out without being applied. Check `listConfluenceContentVersions` before retrying.
- Not confirmed from the docs: whether `createConfluenceContent` takes a parent page and labels directly. The table assumes it may not and adds them in separate steps. Check on first run.
