# Claude for Office — Direct Cloud Setup

Admin tooling for configuring the Claude Office add-in to call your own cloud
(Vertex AI, Bedrock, or an LLM gateway) instead of Anthropic's API.

> **Personal note:** I'm using this with AWS Bedrock. The `setup` wizard handles
> most of the heavy lifting — just make sure your IAM role has `bedrock:InvokeModel`
> permissions before running it.
>
> **Tip:** If you're in `us-east-1` like me, set `AWS_DEFAULT_REGION=us-east-1` in
> your environment before running `setup` — the wizard doesn't always pick it up
> automatically and will prompt you for it mid-run.

## Install

```bash
claude plugin marketplace add anthropics/financial-services-plugins
claude plugin install claude-for-msft-365-install@financial-services-plugins
```

Then inside the session: `/claude-for-msft-365-install:setup`

## Commands

| Command | What it does |
|---|---|
| `/claude-for-msft-365-install:setup` | Interactive wizard — provisions cloud resources, admin consent, writes manifest |
| `/claude-for-msft-365-install:manifest` | Generate the customized add-in manifest XML |
| `/claude-for-msft-365-install:consent` | Azure admin consent URL for the add-in's app registration |
| `/claude-for-msft-365-install:update-user-attrs` | Write per-user config via Microsoft Graph extension attributes |
| `/claude-for-msft-365-install:bootstrap` | Build the bootstrap endpoint — per-user MCP servers, skills, dynamic config |
