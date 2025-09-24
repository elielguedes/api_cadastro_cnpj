import csv
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import Empresa

CSV_PATH = "data/Empresas.csv"

def import_empresas():
    db: Session = SessionLocal()
    with open(CSV_PATH, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            nome = row.get("nome") or row.get("Nome") or row.get("NOME")
            if nome:
                empresa = Empresa(nome=nome)
                db.add(empresa)
        db.commit()
    db.close()
    print("Importação concluída!")

if __name__ == "__main__":
    import_empresas()
