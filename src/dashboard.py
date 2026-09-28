from rich.console import Console
from rich.table import Table

def dashboard(resultats: list[dict]):
    """Calcule et affiche les statistiques des tickets."""
    
    if not resultats:
        return

    categories_number = {}
    severity_sum = 0
    valid_tickets = []

    for item in resultats:
        analyse = item.get("analysis", {})
        
        if analyse.get("status") == "to_check":
            continue
            
        categorie = analyse.get("categorie", "Inconnu")
        severite = analyse.get("severite", 1)
        resume = analyse.get("resume", "Pas de résumé")
        ticket_id = item["initial_ticket"]["id"]
        
        if categorie in categories_number:
            categories_number[categorie] += 1
        else:
            categories_number[categorie] = 1
            
        severity_sum += severite
        
        valid_tickets.append({"id": ticket_id, "severite": severite, "resume": resume})

    valid_ticket_count = len(valid_tickets)
    if valid_ticket_count == 0:
        print("\n Tous les tickets sont en erreur, impossible d'afficher des statistiques.")
        return

    severity_mean = severity_sum / valid_ticket_count

    valid_tickets.sort(key=lambda x: x["severite"], reverse=True)
    top_3 = valid_tickets[:3]

    console = Console()
    
    table = Table(title="\n DASHBOARD TRIAGEBOT", show_header=True, header_style="bold magenta")
    table.add_column("Métrique", style="cyan")
    table.add_column("Valeur", justify="right", style="green")
    
    table.add_row("Total des tickets analysés", str(valid_ticket_count))
    table.add_row("Tickets en échec (to_check)", str(len(resultats) - valid_ticket_count))
    table.add_row("Sévérité moyenne", f"{severity_mean:.1f} / 5")
    table.add_section()
    
    for cat, count in categories_number.items():
        table.add_row(f"Catégorie : {cat}", str(count))
        
    console.print(table)
    
    console.print("\n[bold red] TOP 3 DES URGENCES [/bold red]")
    for index, ticket in enumerate(top_3, start=1):
        console.print(f"{index}. [Ticket #{ticket['id']}] (Sévérité {ticket['severite']}) : {ticket['resume']}")
    print("\n")