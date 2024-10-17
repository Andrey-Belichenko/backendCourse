from fastapi import FastAPI, Query, Body
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn

app = FastAPI(docs_url=None)

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]


@app.get("/hotels")
def get_hotels(id: int | None = Query(default=None, description="Identifier"),
               title: str | None = Query(default=None, description="Hotel name"),):
    """ Getting all list of hotels from 'db' """
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    return hotels_


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    """ Deleting hotel using hotel id from 'db' """
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.post("/hotels")
def create_hotel(title: str = Body(embed=True), name: str = Body(embed=True)):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
        })
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def put_hotel(hotel_id: int, title: str = Body(embed=True), name: str = Body(embed=True)):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK"}
    return {"status:": "ID ERROR"}


@app.patch("/hotels/{hotel_id}")
def patch_hotel(hotel_id: int, title: str | None = Body(None), name: str | None = Body(None)):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name

            return {"status": "OK"}
    return {"status:": "ID ERROR"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Fix long loading time for swagger docs """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
