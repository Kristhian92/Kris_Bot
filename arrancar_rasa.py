import asyncio
import sys
from rasa.__main__ import main

# Obligamos a Windows a usar el Event Loop clásico y estable
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Encendemos Rasa
if __name__ == "__main__":
    main()
