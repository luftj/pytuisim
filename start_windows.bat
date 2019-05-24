echo Starting...

python --version | findstr /C:"2.7.">nul && (
    echo.python 2 installed
    python -m pip install -r requirements.txt
    python -m pip install -r CSL_Hamburg_Noise/requirements.txt

    start cmd /k "cd CSL_Hamburg_Noise &  java -cp bin/*;bundle/*;sys-bundle/* org.h2.tools.Server -pg & exit"
    start cmd /k "python main.py & exit"
) || (
    echo."python 3 installed"
    py -2 -m pip install -r requirements.txt
    py -2 -m pip install -r CSL_Hamburg_Noise/requirements.txt

    start cmd /k "cd CSL_Hamburg_Noise &  java -cp bin/*;bundle/*;sys-bundle/* org.h2.tools.Server -pg & exit"
    start cmd /k "py -2 main.py & exit"
)

pause