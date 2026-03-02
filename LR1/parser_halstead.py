import tkinter as tk
from tkinter import ttk, messagebox
import re
import math

GO_KEYWORDS = {
    'break', 'default', 'func', 'interface', 'select', 'case', 'defer', 'go', 'map', 'struct',
    'chan', 'else', 'goto', 'package', 'switch', 'const', 'fallthrough', 'if', 'range', 'type',
    'continue', 'for', 'import', 'return', 'var'
}

GO_SYMBOLS =[
    '<<=', '>>=', '&^=', '&=', '|=', '^=', ':=', '...', '==', '!=', '<=', '>=', '&&', '||', '<-',
    '++', '--', '+=', '-=', '*=', '/=', '%=', '&^', '+', '-', '*', '/', '%', '&', '|', '^', '<<', '>>', 
    '=', '<', '>', '!', '.', '~', ':'
]

def analyze_code():
    code = text_input.get("1.0", tk.END)
    if not code.strip():
        messagebox.showwarning("Внимание", "Введите код для анализа!")
        return

    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

    operators_count = {}
    operands_count = {}

    strings = re.findall(r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\'', code)
    for s in strings:
        operands_count[s] = operands_count.get(s, 0) + 1
        code = code.replace(s, ' ')

    numbers = re.findall(r'\b\d+(?:\.\d+)?\b', code)
    for n in numbers:
        operands_count[n] = operands_count.get(n, 0) + 1
        code = re.sub(rf'\b{n}\b', ' ', code, count=1)

    total_ifs = len(re.findall(r'\bif\b', code))
    else_ifs = len(re.findall(r'\belse\s+if\b', code))
    actual_ifs = total_ifs - else_ifs
    
    if actual_ifs > 0:
        operators_count['if...else if...else'] = actual_ifs

    switches = len(re.findall(r'\bswitch\b', code))
    if switches > 0:
        operators_count['switch...case...default'] = switches


    func_names = set(re.findall(r'\b([a-zA-Z_]\w*)\s*\(', code))
    func_names -= GO_KEYWORDS 

    words = re.findall(r'\b[a-zA-Z_]\w*\b', code)
    for word in words:
        if word in['if', 'else', 'switch', 'case', 'default']:
            continue 
        elif word in GO_KEYWORDS:
            operators_count[word] = operators_count.get(word, 0) + 1
        elif word in func_names: 
            operators_count[word] = operators_count.get(word, 0) + 1
        else: 
            operands_count[word] = operands_count.get(word, 0) + 1

    
    for sym in GO_SYMBOLS:
        count = code.count(sym)
        if count > 0:
            operators_count[sym] = operators_count.get(sym, 0) + count
            code = code.replace(sym, ' ') 

    pairs = {'( )': ('(', ')'), '{ }': ('{', '}'), '[ ]': ('[', ']')}
    for pair_name, (open_br, close_br) in pairs.items():
        count = min(code.count(open_br), code.count(close_br))
        if count > 0:
            operators_count[pair_name] = count

    update_tables(operators_count, operands_count)

def update_tables(operators, operands):
    for row in tree_operators.get_children(): tree_operators.delete(row)
    for row in tree_operands.get_children(): tree_operands.delete(row)

    n1, n2 = 0, 0
    for idx, (op, count) in enumerate(sorted(operators.items()), 1):
        tree_operators.insert('', 'end', values=(idx, op, count))
        n1 += count
    
    for idx, (op, count) in enumerate(sorted(operands.items()), 1):
        tree_operands.insert('', 'end', values=(idx, op, count))
        n2 += count

    eta1 = len(operators)
    eta2 = len(operands)

    eta = eta1 + eta2
    N = n1 + n2
    V = N * math.log2(eta) if eta > 0 else 0

    lbl_basic.config(text=f"Базовые метрики:\nη1 (Уникальных операторов) = {eta1}\nη2 (Уникальных операндов) = {eta2}\n"
                          f"N1 (Всего операторов) = {n1}\nN2 (Всего операндов) = {n2}")
    
    lbl_extended.config(text=f"Расширенные метрики:\nСловарь программы (η) = {eta}\n"
                             f"Длина программы (N) = {N}\nОбъем программы (V) = {V:.2f} бит")

root = tk.Tk()
root.title("Парсер метрик Холстеда")
root.geometry("800x650")

frame_top = tk.Frame(root)
frame_top.pack(pady=10, fill=tk.BOTH, expand=True)

tk.Label(frame_top, text="Вставьте код (Go) для анализа:").pack()
text_input = tk.Text(frame_top, height=12)
text_input.pack(fill=tk.BOTH, expand=True, padx=10)

tk.Button(frame_top, text="Анализировать код", command=analyze_code, bg="lightblue", font=('Arial', 12, 'bold')).pack(pady=5)

frame_middle = tk.Frame(root)
frame_middle.pack(fill=tk.BOTH, expand=True, padx=10)

frame_op1 = tk.Frame(frame_middle)
frame_op1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
tk.Label(frame_op1, text="Операторы (j | Оператор | f1j)").pack()
tree_operators = ttk.Treeview(frame_op1, columns=("j", "operator", "f1j"), show="headings", height=10)
tree_operators.heading("j", text="j")
tree_operators.heading("operator", text="Оператор")
tree_operators.heading("f1j", text="f1j")
tree_operators.column("j", width=30, anchor='center')
tree_operators.column("f1j", width=50, anchor='center')
tree_operators.pack(fill=tk.BOTH, expand=True)

frame_op2 = tk.Frame(frame_middle)
frame_op2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
tk.Label(frame_op2, text="Операнды (i | Операнд | f2i)").pack()
tree_operands = ttk.Treeview(frame_op2, columns=("i", "operand", "f2i"), show="headings", height=10)
tree_operands.heading("i", text="i")
tree_operands.heading("operand", text="Операнд")
tree_operands.heading("f2i", text="f2i")
tree_operands.column("i", width=30, anchor='center')
tree_operands.column("f2i", width=50, anchor='center')
tree_operands.pack(fill=tk.BOTH, expand=True)

frame_bottom = tk.Frame(root)
frame_bottom.pack(pady=10, fill=tk.X, padx=10)

lbl_basic = tk.Label(frame_bottom, text="Базовые метрики:\nη1 = 0\nη2 = 0\nN1 = 0\nN2 = 0", font=('Arial', 11), justify=tk.LEFT)
lbl_basic.pack(side=tk.LEFT, padx=20)

lbl_extended = tk.Label(frame_bottom, text="Расширенные метрики:\nСловарь (η) = 0\nДлина (N) = 0\nОбъем (V) = 0", font=('Arial', 11, 'bold'), justify=tk.LEFT, fg="darkblue")
lbl_extended.pack(side=tk.RIGHT, padx=20)

root.mainloop()