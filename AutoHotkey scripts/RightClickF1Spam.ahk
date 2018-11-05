#installkeybdhook
#UseHook
^F1::
GetKeyState, state, ScrollLock, T

if (state = "D") ;if scrollLock is toggled
{
	Loop
	{
		send, {RButton}
		Sleep, -0.1
		send, {F1}
		
		GetKeyState, state, F1, P
		if(state == "U")
		{
			break
		}	
	}
}
return

