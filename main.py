from fastapi import FastAPI
from database import init_db
from routes import read, create, update, delete, analytics

app = FastAPI(
    title="Waste Management API",
    description="API Python for Waste Management Data & Analysis",
)

init_db()

app.include_router(read.router)
app.include_router(create.router)
app.include_router(update.router)
app.include_router(delete.router)
app.include_router(analytics.router)


if __name__ == "__main__":
    import uvicorn
    import os

    class Style:
        GREEN = "\033[92m"
        BOLD = "\033[1m"
        RESET = "\033[0m"

    os.system("cls" if os.name == "nt" else "clear")

    print(f"  {Style.GREEN}{Style.BOLD}ONLINE{Style.RESET}")

    print(
        f"  API Data (JSON)    : {Style.GREEN}http://127.0.0.1:8000/data{Style.RESET}"
    )
    print(
        f"  Swagger UI (Docs)  : {Style.GREEN}http://127.0.0.1:8000/docs{Style.RESET}"
    )

    print("  Tekan CTRL+C untuk berhenti...\n")

    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")
    except KeyboardInterrupt:
        print("\nServer berhenti.")
