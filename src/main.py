from ticket_manager import detect_prompt_injection, load_tickets, clean_tickets
from llm_engine import analyze_ticket_with_ollama
import json
from datetime import datetime
from dashboard import dashboard
from pathlib import Path

RESULT_FILE_PATH = Path("output/results.json")
def main():
    print("Chargement des tickets depuis tickets.json...")
    tickets_path = "data/tickets.json"
    raw_tickets = load_tickets(tickets_path)
    tickets = clean_tickets(raw_tickets)
    
    if not tickets:
        print("Aucun ticket à analyser. Veuillez vérifier le fichier tickets.json.")
        return
    
    print(f"Analyse de {len(tickets)} tickets...")
    
    results = []
    for ticket in tickets:
        message = ticket["message"]
        if detect_prompt_injection(message):
            print(f" [SÉCURITÉ] Injection détectée sur le ticket #{ticket['id']} ! Blocage immédiat.")
            formated_analyze = {
                "categorie": "toxicity",
                "severite": 1,
                "sentiment": "negative",
                "resume": "[BLOQUÉ] Tentative d'injection de prompt."
            }
        else:
            analysis = analyze_ticket_with_ollama(message)
            if isinstance(analysis, dict):
                formated_analyze = analysis
            else:
                formated_analyze = analysis.model_dump(mode="json")
        ticket_handled = {
            "initial_ticket": ticket,
            "analysis": formated_analyze
        }
        
        results.append(ticket_handled)
        category = formated_analyze.get("categorie", "N/A")
        severity = formated_analyze.get("severite", "N/A")
        
        print(f"Ticket {ticket['id']} analysé : Catégorie - {category}, Sévérité - {severity}")
        
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data = {
        "derniere_maj": date,
        "total_tickets": len(results),
        "tickets": results
    }
    RESULT_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    print("\n Sauvegarde des résultats dans 'results.json'...")
    with open(RESULT_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print("Triage terminé !")
    dashboard(results)
if __name__ == "__main__":
    main()