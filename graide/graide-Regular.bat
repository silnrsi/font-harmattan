set ver=0_8_80

@echo off

@rem get source file if not present
if not exist ..\results\generated\Harmattan-Regular.xml (
	echo "file ..\results\generated\Harmatta-Regular.xml is missing ... please build font first."
) else (
	if not exist ..\results\Harmattan-Regular-graide.ttf psfufo2ttf ..\source\Harmattan-Regular.ufo ..\results\Harmattan-Regular-graide.ttf
	py -3 C:\SRC\GitHub\graide\graide -p Harmattan-Regular.cfg
	@rem graide%ver%_console.exe -p Harmattan-Regular.cfg 
)