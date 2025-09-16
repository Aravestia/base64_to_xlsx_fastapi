from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import base64
import io
import zipfile

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

        # Create an in-memory ZIP file
        zip_stream = io.BytesIO()
        with zipfile.ZipFile(zip_stream, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("converted.xlsx", xlsx_bytes)

        # Reset stream position to the beginning
        zip_stream.seek(0)

        # Return the ZIP file as a downloadable response
        return StreamingResponse(
            zip_stream,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=converted.zip"}
        )
    except Exception as e:
        return {"error": str(e)}
