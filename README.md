# API de Recetas 

Una API RESTful desarrollada con FastAPI para la gestión de recetas culinarias y sus categorías. Este proyecto prioriza la arquitectura de backend con un modelo de base de datos relacional, e incluye un cliente web ligero para documentar, visualizar y consumir la información gestionada.

## Tecnologías

**Backend:**
* **Framework:** FastAPI (Python)
* **Base de Datos:** SQLite
* **ORM:** SQLAlchemy
* **Validación de Datos:** Pydantic

**Herramientas & Metodologías:**
* Git & Gitflow para control de versiones.
* Diseño UI/UX en Figma.
* Código bajo estándar PEP 8.

---

## Diagrama Entidad-Relación (DER)

El modelo de datos implementa una relación de uno a muchos (1:M) entre **Categorías** y **Recetas**.

```mermaid
erDiagram
    CATEGORIA ||--o{ RECETA : "tiene"
    
    CATEGORIA {
        int id PK
        string nombre
        string descripcion
    }
    
    RECETA {
        int id PK
        string titulo
        text ingredientes
        text instrucciones
        int categoria_id FK
    }
