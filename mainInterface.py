from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse
import serial.tools.list_ports

app = FastAPI()

def list_available_ports():
    ports = serial.tools.list_ports.comports()
    available_ports = []
    for port in ports:
        available_ports.append({
            "device": port.device,
            "name": port.name,
            "description": port.description,
            "hwid": port.hwid,
            "vid": port.vid,
            "pid": port.pid,
            "serial_number": port.serial_number,
            "location": port.location,
            "manufacturer": port.manufacturer,
            "product": port.product,
            "interface": port.interface
        })
    return available_ports

@app.get("/")
def read_root():
    with open("templates/index.html", "r") as f:
        content = f.read()
    return HTMLResponse(content)


@app.get("/getPorts")
def getPorts():
    ports = list_available_ports()
    if not ports:
        raise HTTPException(status_code=404, detail="No USB ports found")
    return {"status": 200, "ports": ports}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)