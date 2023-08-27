from dotenv import load_dotenv

from lab_1.main import lab_1_search

# Load .env variables to be used on the functions and componentes.
load_dotenv()

lab_1_search()

# asyncio.run(async_lab_1_search(data_amount=1000, page_size=50))
