from app.core.memory_manager import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT username FROM user_state")
print(cursor.fetchall())

conn.close()