# cbusbot — Requirements & Context

> Drop this file in the repo root as `REQUIREMENTS.md`. Goal: **rewrite in Python**.

## Purpose
Discord bot for the Cbus (Columbus) server Reggie helps run.

## Current state (Claude Code: verify)
- Existing implementation in another language (inventory features from the code)
- Related TickTick items for the server: bring back the **inspirePics** bot feature limited to its own new channel; old organizer roles / self-roles channels need cleanup (manual, but the bot may help)
- There are JIRA exports (cbusBotJira.csv, cbusServerJira.csv attached to a TickTick task) containing old backlog items to be converted back into TickTick — worth importing as GitHub issues for bot-related ones instead

## Requirements
- **Functional:** Feature parity with the current bot where features are still wanted (inventory first, then decide); inspirePics revival in a dedicated channel; whatever role-management helpers make the manual cleanup easier
- **Non-functional:** Python (discord.py or nextcord — evaluate current state of libraries); config-driven; deployable on Reggie's home server; secrets via env file
- **Migration:** Run old and new in parallel briefly if feasible

## First session objectives
1. Analyze existing code; produce feature inventory with keep/drop recommendations
2. Scaffold Python bot with one trivial command working end-to-end
3. Open issues per feature; label one `next` (suggest: inspirePics, since it's explicitly wanted)
