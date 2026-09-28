from ticket_manager import load_tickets, clean_tickets
from llm_engine import analyze_ticket_with_ollama
import json
from datetime import datetime

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
        analysis = analyze_ticket_with_ollama(message)
        if isinstance(analysis, dict):
            formated_analyze = analysis
        else:
            formated_analyze = analysis.model_dump()
        ticket_handled = {
            "initial_ticket": ticket,
            "analysis": formated_analyze
        }
        
        results.append(ticket_handled)
        categorie = formated_analyze.get("category", "N/A")
        severite = formated_analyze.get("severity", "N/A")
        
        print(f"Ticket {ticket['id']} analysé : Catégorie - {categorie}, Sévérité - {severite}")
        
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data = {
        "derniere_mise_a_jour": date,
        "total_tickets": len(results),
        "tickets": results
    }
    print("\n💾 Sauvegarde des résultats dans 'results.json'...")
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print("Triage terminé !")

if __name__ == "__main__":
    main()