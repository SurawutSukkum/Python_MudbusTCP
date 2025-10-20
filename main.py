from pyModbusTCP.client import ModbusClient
from time import sleep
while True:
    client = ModbusClient(host="192.168.3.20", port=502, unit_id=1, auto_open=True)

    if client.open():
        #print("Connection successful")
        # Read 4 digital outputs (coils)
        start=0
        outputs = client.read_holding_registers(start, 1)
        
        if outputs:
            value = outputs[0]
            bits = [int(b) for b in format(value, '08b')]  # 16-bit binary
            print("\nBits0 :", bits[7])
            print("Bits1 :", bits[6])
            print("Bits2 :", bits[5])
            print("Bits3 :", bits[4])
            print("Bits4 :", bits[3])
            print("Bits5 :", bits[2])
            print("Bits6 :", bits[1])
            print("Bits7 :", bits[0])



        # Write to 4 digital outputs
        output_values = [True, False, False, False]
        for i, val in enumerate(output_values):
            success = client.write_single_coil(0 + i, val)
            #print(f"Write to coil {0 + i}: {'Success' if success else 'Failed'}")
        sleep(1)
        # Read 4 digital outputs (coils)
        outputs = client.read_coils(0, 4)
        sleep(1)
    else:
        print("Connection failed")