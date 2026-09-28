import json
from pathlib import Path

def load_tickets(filepath: str) -> list[dict]:
    """Charge les tickets depuis tickets.json."""
    file_path = Path(filepath)
    
    if not file_path.exists():
        print(f"Erreur : Le fichier {filepath} n'existe pas.")
        return []
        
    try:
        with open(file_path, "r", encoding="utf-8") as df:
            data = json.load(df)
            return data
            
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier {filepath} est mal formaté. Ce n'est pas un JSON valide.")
        return []
        
    except Exception as e:
        print(f"Une erreur inattendue est survenue lors de la lecture : {e}")
        return []