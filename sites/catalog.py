import json,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
rows=json.loads((root/'docs/repositories.json').read_text())['repositories']
text="# Component repository directory\n\nGenerated from [repositories.json](repositories.json); regenerate with `python sites/catalog.py`. Branch links are current-source navigation, not release compatibility.\n\n| Repository / ref | Responsibility and contracts | Human documentation | Agent entry | Status |\n| --- | --- | --- | --- | --- |\n"
for r in rows:
 site=f"[Site]({r['human_site']})" if r['human_site'] else 'Not published/established at audit'
 agent=f"[Raw Markdown]({r['agent_entry']})" if r['agent_entry'] else 'Missing dedicated entry; use repository README'
 text+=f"| [{r['repository']}]({r['url']}) / `{r['ref']}` | {r['role']}; {r['contracts']} | {site} | {agent} | {r['documentation_status']} |\n"
p=root/'docs/repositories.md'
if '--check'in sys.argv:
 if not p.exists() or p.read_text()!=text:raise SystemExit('Regenerate docs/repositories.md')
else:p.write_text(text)
