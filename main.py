from fastapi import FastAPI
from models.SQL_models import session_manager, Incident, Status
from models.pydantic_models import Pydantic_Incident, Pydantic_Incident_Updater
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.encoders import jsonable_encoder

app = FastAPI()


def check_status(status_id: int | None) -> bool:
    # Проверка существования статуса
    with session_manager() as session:
        if status_id is None or session.query(Status).where(Status.id == status_id).one_or_none():
            return True
        else:
            return False


@app.get("/api/incident")  # /api/incident/?status=
def get_incidents(status_id: int | None = None) -> JSONResponse:
    # Вывод всех инцидентов, а так-же фильтрация
    try:
        if not check_status(status_id):
            return JSONResponse(status_code=404, content={"message": "Not correct status_id!"})

        with session_manager() as session:
            if status_id is None:
                result = session.query(Incident).all()
            else:
                result = session.query(Incident).where(Incident.status_id == status_id).all()

            incident_pydantic_list = [Pydantic_Incident.from_orm(obj, ) for obj in result]
            return JSONResponse(status_code=200, content={"message": jsonable_encoder(incident_pydantic_list)})

    except Exception as exp:
        return JSONResponse(status_code=500, content={
            "message": f"Problem with your data! - {exp}"})  # вывод эксепшена сделан для примера, в обычном проекте это логируется


@app.put("/api/incident/refresh")
def refresh_incident(incident: Pydantic_Incident_Updater) -> JSONResponse:
    # обновление статуса инцидента
    try:
        if not check_status(incident.status_id):
            return JSONResponse(status_code=404, content={"message": "Not correct status_id!"})

        with session_manager() as session:
            existing_incident = session.query(Incident).where(Incident.id == incident.id).one_or_none()
            if not existing_incident:
                return JSONResponse(status_code=404, content={"message": "Incident not found"})

            existing_incident.status_id = incident.status_id
            session.commit()

        return JSONResponse(status_code=200, content={"message": "Incident updated successfully!"})
    except Exception as exp:
        return JSONResponse(status_code=500, content={"message": f"Problem with your data! - {exp}"})


@app.post("/api/incident")
def post_incident(incident: Pydantic_Incident) -> JSONResponse:
    # Добавление данных
    try:
        if not check_status(incident.status_id):
            return JSONResponse(status_code=404, content={"message": "Not correct status_id!"})

        with session_manager() as session:
            incident = Incident(description=incident.description, status_id=incident.status_id,
                                source=incident.source, created_at=incident.created_at)
            session.add(incident)
            session.commit()

        return JSONResponse(status_code=200, content={"message": "success!"})
    except Exception as exp:
        return JSONResponse(status_code=500, content={"message": f"Problem with your data! - {exp}"})


if __name__ == "__main__":
    # Тестировалось на python3.10
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
