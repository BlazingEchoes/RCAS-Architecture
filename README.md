# RCAS (Risky Computer Architecture Set)
**Open Manifest for a Hybrid Quantum-Classical Controller Architecture**

*(Русская версия манифеста находится ниже / Russian version is below)*

## 🇬🇧 English

Modern quantum computing faces a fundamental scaling crisis: classical control systems are bulky, inefficient, and create critical latency when communicating with the quantum processor inside a cryostat.

**RCAS (Risky Computer Architecture Set)** is a conceptual hybrid controller architecture designed to manage quantum processors directly at the physical level (within cryogenic systems). It combines a highly dense, variable-length instruction set with direct hardware interaction for quantum error correction (QEC).

### Key Architectural Features
1. **Variable Instruction Length (4 bits to 32 bits):** Minimizes control code footprint. Ultra-short 4-bit instructions are dedicated to the most frequent operations (e.g., qubit initialization), saving crucial memory in cryogenic environments.
2. **Memory-to-Memory Operations:** CISC-inspired logic (`ADD.M`) allows the controller to compute pulse parameters directly in RAM without wasting cycles loading data into general-purpose registers.
3. **Hybrid Pipeline:** The classical core handles flow control and QEC stabilization, while the quantum layer operates on probabilities and matrix states.

### RCAS v1.0 Instruction Set (ISA)

| Prefix | Opcode | Length | Arguments | Command | Hardware Logic |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0` | `0` | 4 bits | `[2b: Qubit]` | **`INIT Qx`** | Hardware qubit reset to \|0>. |
| `0` | `1` | 4 bits | `[2b: Qubit]` | **`HAD Qx`** | Hadamard gate (superposition). |
| `10` | `00` | 16 bits | `[2b: Qubit] + [2b: 00] + [8b: RAM Addr]` | **`MEAS Qx, [M]`** | Measurement and state collapse to RAM. |
| `10` | `01` | 16 bits | `[2b: Qubit] + [10b: 000...]` | **`QEC.CHK Qx`** | Hardware coherence check. Raises ERR flag if noise is detected. |
| `10` | `10` | 16 bits | `[4b: 0000] + [8b: Jump Addr]` | **`JNC [Addr]`** | Jump if No Collapse (branching if ERR == 0). |
| `11` | `00` | 32 bits | `[8b: RAM A] + [8b: RAM B] + [8b: RAM C]` | **`ADD.M A, B, C`** | Direct memory addition. |
| `11` | `01` | 32 bits | `[8b: RAM A] + [8b: RAM B] + [8b: RAM C]` | **`AND.M A, B, C`** | Bitwise AND for correction masks. |

### Project Structure
This repository contains a functional Python-based proof-of-concept:
* `assembler.py` — A custom compiler that translates RCAS assembly text into a dense binary stream.
* `rcas_vm.py` — The virtual processor (hardware decoder frontend + backend execution) that reads the binary file and simulates the quantum-classical pipeline.

**How to run:**
1. Run `python assembler.py` to compile the code into `program.bin`.
2. Run `python rcas_vm.py` to execute the binary on the virtual machine.

---

## 🇷🇺 Русский

Современные квантовые вычисления сталкиваются с фундаментальным кризисом масштабирования: классические управляющие системы громоздки, неэффективны и создают критические задержки (latency) при связи с квантовым процессором.

**RCAS (Risky Computer Architecture Set)** — это концептуальная гибридная архитектура контроллера, разработанная для управления квантовыми процессорами прямо на физическом уровне (внутри криогенных систем). 

### Архитектурные особенности
1. **Переменный размер инструкций (от 4 бит до 32 бит):** Минимизирует объем кода управления. Сверхкороткие инструкции (полбайта) выделяются под самые частые операции, что критически важно для экономии памяти криостатов.
2. **Прямая работа с памятью (Memory-to-Memory):** Использование логики в стиле CISC позволяет контроллеру оперировать данными без лишних циклов загрузки в регистры, ускоряя обработку параметров.
3. **Гибридный конвейер:** Разделение труда. Классическое ядро берет на себя логику потока и стабилизацию (QEC), а квантовый уровень оперирует вероятностями.

### Базовый набор команд (ISA RCAS v1.0)

| Префикс | Опкод | Длина | Формат аргументов | Команда | Назначение (Логика в кремнии) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0` | `0` | 4 бита | `[2 бита: Кубит]` | **`INIT Qx`** | Аппаратный сброс кубита в \|0>. |
| `0` | `1` | 4 бита | `[2 бита: Кубит]` | **`HAD Qx`** | Вентиль Адамара (суперпозиция). |
| `10` | `00` | 16 бит | `[2б: Кубит] + [2б: 00] + [8б: Адрес RAM]` | **`MEAS Qx, [M]`** | Измерение с записью в RAM. |
| `10` | `01` | 16 бит | `[2б: Кубит] + [10б: 00...]`| **`QEC.CHK Qx`** | Проверка на декогеренцию. Поднимает флаг ERR при сбое. |
| `10` | `10` | 16 бит | `[4б: 0000] + [8б: Адрес перехода]` | **`JNC [Addr]`** | Переход по коду, если флаг ERR равен 0 (нет ошибок). |
| `11` | `00` | 32 бита | `[8б: RAM_A] + [8б: RAM_B] + [8б: RAM_C]` | **`ADD.M A, B, C`** | Сложение значений напрямую из памяти. |
| `11` | `01` | 32 бита | `[8б: RAM_A] + [8б: RAM_B] + [8б: RAM_C]` | **`AND.M A, B, C`** | Побитовое И (для масок коррекции). |

### Структура проекта
В репозитории представлен рабочий программный концепт:
* `assembler.py` — Кастомный компилятор, переводящий текст в плотный бинарный поток.
* `rcas_vm.py` — Виртуальный процессор (аппаратный декодер + эмулятор), который считывает скомпилированные биты и выполняет гибридную логику.

**Запуск:**
1. Выполните `python assembler.py` для генерации файла `program.bin`.
2. Выполните `python rcas_vm.py` для запуска виртуальной машины.
