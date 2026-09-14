import random
import math

class RCAS_Processor:
    def __init__(self):
        self.classic_ram = [0] * 256
        self.qubits = {'00': [0.0, 0.0], '01': [0.0, 0.0], '10': [0.0, 0.0], '11': [0.0, 0.0]}
        self.q_names = {'00': 'Q0', '01': 'Q1', '10': 'Q2', '11': 'Q3'}
        self.ERR = 0 # Аппаратный флаг ошибки: 0 - стабильно, 1 - сбой

    def execute_binary(self, binary_stream):
        pc = 0  # Program Counter (Счетчик битов)
        print("\n=== ВЫПОЛНЕНИЕ БИНАРНОГО КОДА НА ПРОЦЕССОРЕ ===")
        
        max_cycles = 30 
        cycles = 0
        
        while pc < len(binary_stream) and cycles < max_cycles:
            cycles += 1
            prefix = binary_stream[pc]
            
            # Группа 0: 4 бита (INIT, HAD)
            if prefix == '0':
                opcode, q = binary_stream[pc:pc+2], binary_stream[pc+2:pc+4]
                if opcode == "00": 
                    self.qubits[q] = [1.0, 0.0]
                    print(f"[-] {self.q_names[q]} -> |0>")
                elif opcode == "01": 
                    self.qubits[q] = [0.707, 0.707]
                    print(f"[~] {self.q_names[q]} -> Суперпозиция")
                pc += 4
                
            # Группа 10: 16 бит (MEAS, QEC.CHK, JNC)
            elif binary_stream[pc:pc+2] == '10':
                opcode = binary_stream[pc+2:pc+4]
                
                if opcode == "00": # MEAS
                    q, addr = binary_stream[pc+4:pc+6], int(binary_stream[pc+8:pc+16], 2)
                    prob_0 = self.qubits[q][0]**2
                    res = 0 if random.random() < prob_0 else 1
                    self.qubits[q] = [1.0, 0.0] if res == 0 else [0.0, 1.0]
                    self.classic_ram[addr] = res
                    print(f"[!] {self.q_names[q]} коллапс -> {res}. Записано в RAM[{addr}]")
                    
                elif opcode == "01": # QEC.CHK
                    q = binary_stream[pc+4:pc+6]
                    self.ERR = 1 if random.random() < 0.4 else 0 
                    status = "ОШИБКА ШУМА!" if self.ERR else "Стабильно"
                    print(f"[?] QEC.CHK {self.q_names[q]}: {status}")
                    
                elif opcode == "10": # JNC
                    jump_addr = int(binary_stream[pc+8:pc+16], 2)
                    if self.ERR == 0:
                        print(f"[>] JNC: Ошибок нет. Прыжок на бит {jump_addr}")
                        pc = jump_addr
                        continue 
                    else:
                        print("[>] JNC: Обнаружена ошибка. Прыжок отменен, сброс флага.")
                        self.ERR = 0
                pc += 16
                
            # Группа 11: 32 бита (ADD.M, AND.M)
            elif binary_stream[pc:pc+2] == '11':
                opcode = binary_stream[pc+2:pc+4]
                a, b, c = int(binary_stream[pc+8:pc+16], 2), int(binary_stream[pc+16:pc+24], 2), int(binary_stream[pc+24:pc+32], 2)
                
                if opcode == "00": # ADD.M
                    self.classic_ram[c] = self.classic_ram[a] + self.classic_ram[b]
                    print(f"[+] RAM[{a}] + RAM[{b}] = {self.classic_ram[c]} -> RAM[{c}]")
                elif opcode == "01": # AND.M
                    self.classic_ram[c] = self.classic_ram[a] & self.classic_ram[b]
                    print(f"[&] RAM[{a}] AND RAM[{b}] = {self.classic_ram[c]} -> RAM[{c}]")
                pc += 32
                
        if cycles >= max_cycles:
            print("... (Программа остановлена по лимиту циклов) ...")

if __name__ == "__main__":
    try:
        # Процессор считывает скомпилированный бинарный файл
        with open("program.bin", "r") as f:
            bin_code = f.read()
            
        cpu = RCAS_Processor()
        print(f"Загружен бинарный поток: {bin_code}")
        
        for i in range(1, 3):
            print(f"\n--- ТАКТОВЫЙ ЗАПУСК {i} ---")
            cpu.execute_binary(bin_code)
            
    except FileNotFoundError:
        print("[-] Ошибка: файл 'program.bin' не найден! Сначала запусти assembler.py")