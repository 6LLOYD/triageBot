from ticket_manager import load_tickets
from llm_engine import analyze_ticket_with_ollama
import json

def main():
    print("Chargement des tickets depuis tickets.json...")
    tickets_path = "data/tickets.json"
    tickets = load_tickets(tickets_path)
    
    if not tickets:
        print("Aucun ticket à analyser. Veuillez vérifier le fichier tickets.json.")
        return
    
    print(f"Analyse de {len(tickets)} tickets...")
    
    results = []
    for ticket in tickets:
        message = ticket["message"]
        analysis = analyze_ticket_with_ollama(message)
        ticket_handled = {
            "initial_ticket": ticket,
            "analysis": analysis.model_dump()
        }
        
        results.append(ticket_handled)
        print(analysis.model_dump_json(indent=4, ensure_ascii=False))
        print(f"Ticket {ticket['id']} analysé : Catégorie - {analysis.category}," +
              f" Sévérité - {analysis.severity}, Sentiment - {analysis.sentiment}")
        
    print("\n💾 Sauvegarde des résultats dans 'results.json'...")
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
        
    print("Triage terminé !")

if __name__ == "__main__":
    main()