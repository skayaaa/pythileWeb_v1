# -*- coding: utf-8 -*-
import asyncio
import asyncpg

async def test_connection():
    try:
        # PostgreSQL baðlantý bilgileri
        conn = await asyncpg.connect(
            user="postgres",  # PostgreSQL kullanýcý adý
            password="1921",  # PostgreSQL þifresi
            database="pythile_db",  # Veritabaný adý
            host="localhost",  # Veritabaný sunucusu (ör. localhost)
            port=5432  # PostgreSQL portu (varsayýlan 5432)
        )
        print("Connection successful!")
        await conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

# Test fonksiyonunu çalýþtýr
if __name__ == "__main__":
    asyncio.run(test_connection())
