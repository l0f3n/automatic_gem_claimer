#installkeybdhook
#UseHook
^LButton::
GetKeyState, state, ScrollLock, T

if (state = "D") ;if scrollLock is toggled
{
	Loop
	{
		Sleep, -0.1
		Click
		
		GetKeyState, state, LButton, P
		if(state == "U")
		{
			break
		}	
	}
}
return

