Scriptname BA_PlayerAlias extends ReferenceAlias
{Beast Aware - forwards player race switches and game loads to BA_Main.}

Event OnPlayerLoadGame()
	(GetOwningQuest() as BA_Main).Maintenance()
EndEvent

Event OnRaceSwitchComplete()
	(GetOwningQuest() as BA_Main).CheckForm(false)
EndEvent
