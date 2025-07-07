import json
import os
import sys
from pynput.keyboard import Controller, Key
import time

# Caminho do arquivo JSON para salvar sequências
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "sequences.json")
keyboard = Controller()

# Mapeia nomes legíveis para teclas especiais
SPECIAL_KEYS = {
    "space": Key.space,
    "enter": Key.enter,
    "tab": Key.tab,
    "esc": Key.esc,
    "shift": Key.shift,
    "ctrl": Key.ctrl,
    "alt": Key.alt
}

DEFAULT_HOLD = 0.1
DEFAULT_WAIT = 0.1

def load_sequences():
    """Carrega sequências do arquivo JSON"""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_sequences(sequences):
    """Salva sequências no arquivo JSON"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(sequences, f, indent=4)

def parse_token(token: str):
    """Analisa um token: tecla:hold:wait"""
    parts = token.strip().lower().split(":")
    key_str = parts[0]
    key = SPECIAL_KEYS.get(key_str, key_str)
    hold_time = float(parts[1]) if len(parts) > 1 else DEFAULT_HOLD
    wait_time = float(parts[2]) if len(parts) > 2 else DEFAULT_WAIT
    return key, hold_time, wait_time

def run_sequence(tokens, repeat=False):
    """Executa uma sequência"""
    try:
        count = 1
        while True:
            print(f"\n▶ Executando sequência (passo {count})")
            for key, hold, wait in tokens:
                print(f"  ↳ {key}  pressionado {hold}s  espera {wait}s")
                keyboard.press(key)
                time.sleep(hold)
                keyboard.release(key)
                time.sleep(wait)
            if not repeat:
                break
            count += 1
    except KeyboardInterrupt:
        print("\n⏹️  Sequência interrompida pelo usuário.\n")

def main_menu():
    sequences = load_sequences()
    while True:
        print("\n=== AUTO KEYS MENU ===")
        print("1. Listar sequências salvas")
        print("2. Criar nova sequência")
        print("3. Executar uma sequência")
        print("4. Excluir uma sequência")
        print("5. Sair")
        choice = input("Escolha uma opção (1-5): ").strip()

        if choice == "1":
            if not sequences:
                print("⚠️ Nenhuma sequência salva.")
            else:
                print("📄 Sequências salvas:")
                for name in sequences:
                    print(f" - {name}")

        elif choice == "2":
            name = input("Nome da sequência: ").strip()
            seq = input("Cole a sequência (formato: w:0.2:0.3, a, space): ").strip()
            sequences[name] = seq
            save_sequences(sequences)
            print(f"✅ Sequência '{name}' salva com sucesso!")

        elif choice == "3":
            if not sequences:
                print("⚠️ Nenhuma sequência para executar.")
                continue
            print("📄 Sequências disponíveis:")
            for name in sequences:
                print(f" - {name}")
            name = input("Digite o nome da sequência para executar: ").strip()
            if name not in sequences:
                print("❌ Sequência não encontrada.")
                continue
            repeat = input("Repetir infinitamente? (s/n): ").strip().lower() == "s"
            try:
                tokens = [parse_token(tok) for tok in sequences[name].split(",")]
                run_sequence(tokens, repeat)
            except Exception as e:
                print(f"❌ Erro na sequência: {e}")

        elif choice == "4":
            if not sequences:
                print("⚠️ Nenhuma sequência para excluir.")
                continue
            name = input("Digite o nome da sequência para excluir: ").strip()
            if name in sequences:
                del sequences[name]
                save_sequences(sequences)
                print(f"🗑️ Sequência '{name}' excluída.")
            else:
                print("❌ Sequência não encontrada.")

        elif choice == "5":
            print("👋 Saindo...")
            break

        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main_menu()
