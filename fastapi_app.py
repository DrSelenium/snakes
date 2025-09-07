from fastapi import FastAPI, Request
from fastapi.responses import Response
import random

app = FastAPI()

@app.post("/slpu")
async def slpu_endpoint(request: Request):
    # The body is SVG, but we don't need to parse it for this simple case
    # Just generate 6 random die rolls (1-6)
    rolls = [str(random.randint(1, 6)) for _ in range(6)]
    die_rolls = ''.join(rolls)
    
    # Return SVG response
    svg_content = f'<svg xmlns="http://www.w3.org/2000/svg"><text>{die_rolls}</text></svg>'
    return Response(content=svg_content, media_type="image/svg+xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
