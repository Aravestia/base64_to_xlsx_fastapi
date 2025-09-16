from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import base64
import io

app = FastAPI()

@app.post("/")
async def convert_base64_to_xlsx(request: Request):
    data = await request.json()
    base64_str = data.get("base64")

    if not base64_str:
        return {"error": "Missing base64 string in request."}

    try:
        # Decode the base64 string
        xlsx_bytes = base64.b64decode(base64_str)
        xlsx_stream = io.BytesIO(xlsx_bytes)

        # Return the XLSX file as a downloadable response
        return StreamingResponse(
            xlsx_stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=converted.xlsx"}
        )
    except Exception as e:
        return {"error": str(e)}
