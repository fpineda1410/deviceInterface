from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import time
import serial
import threading
from fastapi.middleware.cors import CORSMiddleware
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

# Define a list of origins that are allowed to make requests to your API
origins = [
    "*",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
    # Add any other origins you want to allow
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allow only specified origins
    allow_credentials=True,           # Allow cookies and authentication credentials
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],              # Allow all headers
)


@app.get("/devicehandler/{comPort}/{filename}")
def beginMeasurement(comPort: str, filename: str):
    
    if comPort and filename:
        
        def read_serial():
            serial_port = comPort.replace("dev","/dev/")  # Replace with your serial port
            baud_rate = 2000000  # Match the baud rate with Arduino
            output_file = filename
            buffer_size = 100  # Adjust buffer size as needed
            print(output_file)
            buffer = []
            try:
                with serial.Serial(serial_port, baud_rate) as ser, open(output_file, 'w+') as f:
                    f.write('red,ir,green\n')
                    start_time = time.time()
                    while True:
                        line = ser.readline().decode('utf-8').strip()
                        buffer.append(line)
                        if len(buffer) >= buffer_size:
                            f.write('\n'.join(buffer) + '\n')
                            f.flush()
                            buffer = []
                        
                        # Check if 3 minutes have passed
                        if time.time() - start_time > 180:  # 3 minutes = 180 seconds
                            break

                    # Write any remaining data in the buffer
                    if buffer:
                        f.write('\n'.join(buffer) + '\n')
                        f.flush()
            except Exception as e:
                print(f"Error: {e}")
        
        # Create a thread to handle the serial reading
        thread = threading.Thread(target=read_serial)
        thread.start()
        thread.join()  # Wait for the thread to complete

        return {"status": "Measurement completed", "filename": filename}
    else:
        raise HTTPException(status_code=400, detail="comPort format missing or incorrect")

@app.get("/getPorts")
def getPorts():
    ports = list_available_ports()
    if not ports:
        raise HTTPException(status_code=404, detail="No USB ports found")
    return {"status": 200, "ports": ports}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
