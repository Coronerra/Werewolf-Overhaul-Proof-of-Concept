Scriptname BA_Main extends Quest
{Beast Aware - tells SkyrimNet NPCs when the player shifts into or out of beast form. by coronerra}

bool Property ModEnabled = true Auto
bool Property AnnounceShift = true Auto      ; event when shifting in
bool Property AnnounceRevert = true Auto     ; event when shifting back
bool Property NpcsReact = true Auto          ; true = DirectNarration (NPCs may react), false = silent persistent event
bool Property StateContext = true Auto       ; keep a "currently in beast form" note in scene context
bool Property DebugMessages = false Auto

int Property CurrentForm = 0 Auto Hidden     ; 0 none, 1 werewolf, 2 vampire lord, 3 werebear/other
Race WerewolfRace
Race VampireLordRace
float RefreshInterval = 30.0

Event OnInit()
	Maintenance()
EndEvent

Function Maintenance()
	WerewolfRace = Game.GetFormFromFile(0x000CDD84, "Skyrim.esm") as Race
	VampireLordRace = Game.GetFormFromFile(0x0000283A, "Dawnguard.esm") as Race
	CheckForm(true)
EndFunction

int Function DetectForm()
	Actor p = Game.GetPlayer()
	Race r = p.GetRace()
	if WerewolfRace && r == WerewolfRace
		return 1
	elseif VampireLordRace && r == VampireLordRace
		return 2
	endif
	; catch-all for overhaul races (werebears etc.) by name
	string n = r.GetName()
	if StringUtil.Find(n, "Werewolf") >= 0
		return 1
	elseif StringUtil.Find(n, "Werebear") >= 0
		return 3
	elseif StringUtil.Find(n, "Vampire Lord") >= 0
		return 2
	endif
	return 0
EndFunction

string Function BeastDesc(int f)
	if f == 2
		return "a towering, leathery-winged Vampire Lord, a grey-skinned monster with claws and fangs"
	elseif f == 3
		return "a massive, shaggy, bear-like werebear"
	endif
	return "a massive, hairy werewolf"
EndFunction

string Function FormName(int f)
	if f == 2
		return "Vampire Lord form"
	elseif f == 3
		return "werebear form"
	endif
	return "werewolf form"
EndFunction

string Function StateBody(int f)
	if f == 2
		return "a towering, leathery-winged monster, far too large for any clothing or armor to fit"
	elseif f == 3
		return "a massive, shaggy, bear-like beast, far too large for any clothing or armor to fit"
	endif
	return "a towering, fur-covered beast far too large for any clothing or armor to fit"
EndFunction

string Function SeenAs(int f)
	if f == 2
		return "a huge, leathery-winged Vampire Lord"
	elseif f == 3
		return "a huge, shaggy werebear"
	endif
	return "a huge, hairy werewolf"
EndFunction

string Function ShiftText(int f, string nm)
	return nm + " tore free of their clothes as their body swelled and twisted, stripping them off before they could rip, and grew into " + BeastDesc(f) + "."
EndFunction

string Function StateText(int f, string nm)
	return nm + " is in " + FormName(f) + ": " + StateBody(f) + ". Being unclothed is natural for this form, and their body is fully exposed. Anyone nearby sees " + SeenAs(f) + " and reacts to that (fear, awe, desire, or whatever fits them), and would not scold them for lacking clothes the way they would a naked human."
EndFunction

string Function RevertText(int f, string nm)
	string back = "human form"
	if f == 2
		back = "mortal form"
	endif
	return nm + " shrank back into " + back + ", left standing naked and exhausted among the remains of the change."
EndFunction

; onLoad = true: quiet resync after loading a save (no announcement)
Function CheckForm(bool onLoad)
	int f = DetectForm()
	int old = CurrentForm
	CurrentForm = f
	if f == old
		if f > 0 && StateContext
			PushState()
			RegisterForSingleUpdate(RefreshInterval)
		endif
		return
	endif
	if !ModEnabled
		return
	endif
	Actor p = Game.GetPlayer()
	string nm = p.GetDisplayName()
	if f > 0 && old == 0
		if AnnounceShift && !onLoad
			Send(ShiftText(f, nm))
		endif
		if StateContext
			PushState()
			RegisterForSingleUpdate(RefreshInterval)
		endif
		Dbg("shift detected: form " + f)
	elseif f == 0 && old > 0
		if AnnounceRevert && !onLoad
			Send(RevertText(old, nm))
		endif
		UnregisterForUpdate()
		Dbg("revert detected")
	else
		; switched between two beast forms
		if AnnounceShift && !onLoad
			Send(ShiftText(f, nm))
		endif
		Dbg("form changed: " + f)
	endif
EndFunction

Function Send(string content)
	Actor p = Game.GetPlayer()
	int rc
	if NpcsReact
		rc = SkyrimNetApi.DirectNarration(content, None, None)
	else
		rc = SkyrimNetApi.RegisterPersistentEvent(content, p, None)
	endif
	Dbg("event sent (rc " + rc + ")")
EndFunction

Function PushState()
	if !ModEnabled || CurrentForm == 0
		return
	endif
	Actor p = Game.GetPlayer()
	string d = StateText(CurrentForm, p.GetDisplayName())
	SkyrimNetApi.RegisterShortLivedEvent("beastaware_player_form", "beastaware_form", d, "", 45000, p, None)
EndFunction

Event OnUpdate()
	; safety net in case a race switch event was missed
	CheckForm(false)
EndEvent

Function Dbg(string s)
	if DebugMessages
		Debug.Notification("Beast Aware: " + s)
	endif
EndFunction
