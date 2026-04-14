import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = 'data/nolimits_ai.db'

def mock_cancellations():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all active student IDs
    cursor.execute("SELECT id, data_inicio FROM vinculos WHERE status = 'ativo'")
    rows = cursor.fetchall()
    
    # Choose about 25% to cancel
    to_cancel = random.sample(rows, int(len(rows) * 0.28)) # Using 28% to match the suggestion's target
    
    print(f"Cancelling {len(to_cancel)} students...")
    
    for v_id, data_inicio in to_cancel:
        # Generate a data_fim that is at least 30 days after data_inicio and before today
        start_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        # Random cancel date between 30 and 150 days after start
        cancel_days = random.randint(30, 150)
        cancel_dt = start_dt + timedelta(days=cancel_days)
        
        # Ensure it's not in the future relative to the project context (2025-11-28 is the 'data_maxima')
        if cancel_dt > datetime(2025, 11, 28):
            cancel_dt = datetime(2025, 11, 28)
            
        cursor.execute("""
            UPDATE vinculos 
            SET status = 'cancelado', data_fim = ? 
            WHERE id = ?
        """, (cancel_dt.strftime("%Y-%m-%d"), v_id))

    conn.commit()
    conn.close()
    print("Mocks applied successfully.")

if __name__ == "__main__":
    mock_cancellations()
