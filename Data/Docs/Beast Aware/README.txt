Beast Aware v1.1 - by That Guy (Coronerra)
SkyrimNet NPCs notice when you are a werewolf / Vampire Lord, and see the beast in front of them.

Requirements: SkyrimNet (built against beta28 API), SkyUI (MCM). SKSE. Dawnguard (vanilla) for Vampire Lord detection.
Optional/compatible: OStim Beast Form, Growl, ABC. Touches no vanilla records.

What it does
1. BeastAware.esp (ESL-flagged): a player alias catches OnRaceSwitchComplete (and re-checks on load
   and every 30s while transformed). On shifting in/out it sends a SkyrimNet event:
   - "NPCs react out loud" ON  -> SkyrimNetApi.DirectNarration (nearby NPCs may comment)
   - OFF -> SkyrimNetApi.RegisterPersistentEvent (remembered silently)
   While transformed it keeps a RegisterShortLivedEvent "beastaware_player_form" (45s TTL, refreshed)
   in scene context.
2. SKSE/Plugins/SkyrimNet/external/coronerra.beastaware/: additive prompt submodule
   character_bio/0405_beastaware_form.prompt. It does not replace any SkyrimNet file; it adds a
   "Current Form" section (beast far too large for any clothing to fit) to any actor's profile whose race is Werewolf, Werebear or Vampire Lord.

MCM: "Beast Aware" - Enabled, Announce transforming, Announce changing back, NPCs react out loud,
Keep beast form in scene context, Debug notifications. All on except debug.
