Scriptname BA_MCM extends SKI_ConfigBase

BA_Main Property Main Auto
int oidEnabled
int oidShift
int oidRevert
int oidReact
int oidState
int oidDebug

Event OnConfigInit()
	ModName = "Beast Aware"
	Pages = new string[1]
	Pages[0] = "Settings"
EndEvent

BA_Main Function M()
	if !Main
		Main = (Self as Quest) as BA_Main
	endif
	return Main
EndFunction

Event OnPageReset(string page)
	SetCursorFillMode(TOP_TO_BOTTOM)
	AddHeaderOption("SkyrimNet beast form awareness")
	oidEnabled = AddToggleOption("Enabled", M().ModEnabled)
	oidShift = AddToggleOption("Announce transforming", M().AnnounceShift)
	oidRevert = AddToggleOption("Announce changing back", M().AnnounceRevert)
	oidReact = AddToggleOption("NPCs react out loud", M().NpcsReact)
	oidState = AddToggleOption("Keep beast form in scene context", M().StateContext)
	AddHeaderOption("")
	oidDebug = AddToggleOption("Debug notifications", M().DebugMessages)
	AddTextOption("Current form", M().CurrentForm as string, OPTION_FLAG_DISABLED)
EndEvent

Event OnOptionSelect(int o)
	BA_Main m = M()
	if o == oidEnabled
		m.ModEnabled = !m.ModEnabled
		SetToggleOptionValue(o, m.ModEnabled)
	elseif o == oidShift
		m.AnnounceShift = !m.AnnounceShift
		SetToggleOptionValue(o, m.AnnounceShift)
	elseif o == oidRevert
		m.AnnounceRevert = !m.AnnounceRevert
		SetToggleOptionValue(o, m.AnnounceRevert)
	elseif o == oidReact
		m.NpcsReact = !m.NpcsReact
		SetToggleOptionValue(o, m.NpcsReact)
	elseif o == oidState
		m.StateContext = !m.StateContext
		SetToggleOptionValue(o, m.StateContext)
	elseif o == oidDebug
		m.DebugMessages = !m.DebugMessages
		SetToggleOptionValue(o, m.DebugMessages)
	endif
EndEvent

Event OnOptionHighlight(int o)
	if o == oidReact
		SetInfoText("On: shifting is narrated and nearby NPCs can respond. Off: it is silently remembered.")
	elseif o == oidState
		SetInfoText("While transformed, keeps a short note in SkyrimNet scene context (refreshed every 30s) so NPCs see you as the beast you are.")
	endif
EndEvent
