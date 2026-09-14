def rcas_assemble(source_code):
    binary_stream = ""
    q_map = {"Q0": "00", "Q1": "01", "Q2": "10", "Q3": "11"}

    lines = source_code.strip().split('\n')
    for line in lines:
        parts = line.replace(',', '').replace('[', '').replace(']', '').split()
        if not parts or parts[0].startswith(';'): 
            continue
            
        cmd = parts[0]
        
        # 4-битные команды
        if cmd == "INIT":
            binary_stream += "00" + q_map[parts[1]]
        elif cmd == "HAD":
            binary_stream += "01" + q_map[parts[1]]
            
        # 16-битные команды
        elif cmd == "MEAS":
            binary_stream += "1000" + q_map[parts[1]] + "00" + format(int(parts[2]), '08b')
        elif cmd == "QEC.CHK":
            binary_stream += "1001" + q_map[parts[1]] + "00" + "00000000"
        elif cmd == "JNC":
            binary_stream += "1010" + "0000" + format(int(parts[1]), '08b')
            
        # 32-битные команды
        elif cmd == "ADD.M":
            binary_stream += "11000000" + format(int(parts[1]), '08b') + format(int(parts[2]), '08b') + format(int(parts[3]), '08b')
        elif cmd == "AND.M":
            binary_stream += "11010000" + format(int(parts[1]), '08b') + format(int(parts[2]), '08b') + format(int(parts[3]), '08b')
            
    return binary_stream

if __name__ == "__main__":
    source = """
    INIT Q0        
    HAD Q0         
    QEC.CHK Q0     
    JNC 44         
    INIT Q0        
    HAD Q0
    MEAS Q0, [15]  
    """
    print("Компиляция программы RCAS v1.0")
    bin_code = rcas_assemble(source)
    
    # Записываем бинарник в файл для процессора
    with open("program.bin", "w") as f:
        f.write(bin_code)
        
    print(f"Бинарный код сохранен в 'program.bin'")
    print(f"Размер прошивки: {len(bin_code)} бит ({len(bin_code)//8} байт)")
