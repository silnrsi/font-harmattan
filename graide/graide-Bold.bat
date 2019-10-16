set ver=0_8_80

@echo off

@rem get source file if not present
if not exist ..\results\generated\Harmattan-Bold.xml (
	echo "file ..\results\generated\Harmatta-Regular.xml is missing ... please build font first."
) else (
	if not exist ..\results\Harmattan-Bold-graide.ttf psfufo2ttf ..\source\Harmattan-Bold.ufo ..\results\Harmattan-Bold-graide.ttf
	py -3 C:\SRC\GitHub\graide\graide -p Harmattan-Bold.cfg
	@rem graide%ver%_console.exe -p Harmattan-Bold.cfg 
)