# -*- coding: utf-8 -*-
import asyncio
import asyncpg

async def test_connection():
    try:
        # PostgreSQL ba�lant� bilgileri
        conn = await asyncpg.connect(
            user="postgres",  # PostgreSQL kullan�c� ad�
            password="1921",  # PostgreSQL �ifresi
            database="pythile_db",  # Veritaban� ad�
            host="localhost",  # Veritaban� sunucusu (�r. localhost)
            port=5432  # PostgreSQL portu (varsay�lan 5432)
        )
        print("Connection successful!")
        await conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

# Test fonksiyonunu �al��t�r
if __name__ == "__main__":
    asyncio.run(test_connection())
