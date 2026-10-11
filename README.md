# huddle

Stop handing off documents. Start building them together.

Say "huddle PROJ-123" and the skill finds, or creates, one shared Confluence page for that ticket, where the PM, engineer, designer and architect frame the problem together, with AI in the room.

## Why

A common finding in product research is that engineers are brought in after the problem is already framed. Documents written alone and handed off make that the default. A shared page that exists before the write-up makes early involvement cheap.

Source for the gap: Atlassian, State of Product 2026 (vendor survey; engineer involvement figure on p.11).
https://www.atlassian.com/software/jira/product-discovery/resources/state-of-product-2026

## Files

- `SKILL.md`: trigger, lookup flow, writing rules.
- `templates/page.md`: the page template (sections by purpose, not role).
- `scripts/build-zip.py`: builds `dist/huddle.zip` for upload to Claude (Settings > Capabilities > Skills). Rebuild after any edit to `SKILL.md` or the template.
- `dist/huddle.zip`: the built upload file.

## Status

Draft. In testing.

## Download

[`dist/huddle.zip`](dist/huddle.zip) is the ready-to-upload skill file.

## Using it in Claude

Upload `dist/huddle.zip` as a skill, and connect the Atlassian (Rovo) connector so Claude can reach Jira and Confluence. The skill asks for your Confluence space the first time.

## License

MIT. See [LICENSE](LICENSE).
