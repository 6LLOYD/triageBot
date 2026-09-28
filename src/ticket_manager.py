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
    
def clean_tickets(raw_tickets: list[dict])->list[dict]:
    """Filtre les tickets vides et suprimme les doublons"""
    cleaned_tickets = []
    seen_tickets = set()
    print("Nettoyage des tickets...")
    
    for ticket in raw_tickets:
        joueur = ticket.get("player")
        message = ticket.get("message", "")
        if message.strip() == "":
            print(f"Ticket vide détecté pour le joueur {joueur}. Ignoré.")
            continue
        signature = (joueur, message)
        
        if signature in seen_tickets:
            print(f"Doublon détecté pour le joueur {joueur}. Ignoré.")
            continue
        
        seen_tickets.add(signature)
        cleaned_tickets.append(ticket)
        
    print(f"Nettoyage terminé : {len(cleaned_tickets)} tickets conservés sur {len(raw_tickets)}.\n")
    return cleaned_tickets

def detect_prompt_injection(message: str) -> bool:
    """
    Agit comme un antivirus. Détecte les tentatives de manipulation du LLM.
    """
    msg_min = message.lower()
    
    restricted_terms = [
        "ignore",
        "instructions précédentes",
        "previous instructions",
        "system override",
        "tu es maintenant",
        "you are now",
        "oublie tout",
        "bypass"
    ]
    
    for word in restricted_terms:
        if word in msg_min:
            return True
            
    return False