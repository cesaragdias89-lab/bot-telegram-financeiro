\
    @echo off
    REM === Preparar ambiente e rodar o bot no Telegram ===
    cd /d %~dp0
    if not exist .venv (
        python -m venv .venv
    )
    call .venv\Scripts\activate
    pip install -r requirements.txt
    if not exist data mkdir data
    if not exist .env (
        echo Copie .env.example para .env e edite seu TELEGRAM_TOKEN.
        pause
        exit /b 1
    )
    python main.py telegram
