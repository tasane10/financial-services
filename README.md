# Claude for Financial Services

Reference agents, skills, and data connectors for the financial-services workflows we see most — investment banking, equity research, private equity, and wealth management.

Everything here is available **two ways from one source**: install it as a [Claude Cowork](https://claude.com/product/cowork) plugin, or deploy it through the [Claude Managed Agents API](https://docs.claude.com/en/api/managed-agents) behind your own workflow engine. Same system prompt, same skills — you choose where it runs.

> [!IMPORTANT]
> Nothing in this repository constitutes investment, legal, tax, or accounting advice. These agents draft analyst work product — models, memos, research notes, reconciliations — for review by a qualified professional. They do not make investment recommendations, execute transactions, bind risk, post to a ledger, or approve onboarding; every output is staged for human sign-off. You are responsible for verifying outputs and for compliance with the laws and regulations that apply to your firm.

> [!NOTE]
> **Personal fork:** I'm primarily using this for equity research workflows (Market Researcher + Earnings Reviewer). The IB/PE agents are largely untouched. See my notes in [`./notes/personal-setup.md`](./notes/personal-setup.md) for my local config.
>
> **My active agents:** Market Researcher, Earnings Reviewer
> **Sectors I cover:** semiconductors, cloud infrastructure, enterprise software

What's in the repo:

- **[Agents](#agents)** — named, end-to-end workflow agents (Pitch Agent, Market Researcher, GL Reconciler, …). Each ships as a Cowork plugin **and** as a [Claude Managed Agent template](./managed-agent-cookbooks) you deploy via `/v1/agents`.
- **[Vertical plugins](#vertical-plugins)** — the underlying skills, slash commands, and data connectors, bundled by FSI vertical. Install these on their own if you just want `/comps`, `/dcf`, `/earnings` and the connectors without a full agent.

## Agents

Each agent is named for the workflow it runs. They're starting points: install the ones that match your work, then tune the prompts, skills, and connectors to how your firm does it.

Each agent plugin is **self-contained** — it bundles the skills it uses, so installing the agent is all you need.

| Function | Agent | What it does |
|---|---|---|
| **Coverage & advisory** | **[Pitch Agent](./plugins/agent-plugins/pitch-agent)** | Comps, precedents, LBO → branded pitch deck, end to end |
| | **[Meeting Prep Agent](./plugins/agent-plugins/meeting-prep-agent)** | Briefing pack before every client meeting |
| **Research & modeling** | **[Market Researcher](./plugins/agent-plugins/market-researcher)** | Sector or theme → industry overview, competitive landscape, peer comps, ideas shortlist |
| | **[Earnings Reviewer](./plugins/agent-plugins/earnings-reviewer)** | Earnings call + filings → model update → note draft |
| | **[Model Builder](./plugins/agent-plugins/model-builder)** | DCF, LBO, 3-statement, comps — live in Excel |
| **Fund admin & finance ops** | **[Valuation Reviewer](./plugins/agent-plugins/valuation-reviewer)** | Ingests GP packages, runs val
