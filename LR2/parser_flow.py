import tkinter as tk
from tkinter import messagebox
import re

def analyze_code():
    code = text_input.get("1.0", tk.END)
    if not code.strip():
        messagebox.showwarning("Внимание", "Введите код для анализа!")
        return

    clean_code = re.sub(r'//.*', '', code)
    clean_code = re.sub(r'/\*.*?\*/', '', clean_code, flags=re.DOTALL)
    
    cl_ifs = len(re.findall(r'\bif\b', clean_code))
    cl_fors = len(re.findall(r'\bfor\b', clean_code))
    cl_cases = len(re.findall(r'\bcase\b', clean_code))
    
    CL = cl_ifs + cl_fors + cl_cases

    lines =[l.strip() for l in clean_code.split('\n') if l.strip()]
    statements = [l for l in lines if l not in['{', '}'] and not l.startswith('package ') and not l.startswith('import ')]
    N = len(statements)
    cl_rel = CL / N if N > 0 else 0

    code_no_str = re.sub(r'".*?"', '""', clean_code)
    tokens = re.findall(r'\bif\b|\bfor\b|\bswitch\b|\belse\b|\bcase\b|\bdefault\b|\{|\}', code_no_str)
    
    stack =[]
    current_depth = 0
    max_depth = 0
    
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in ['if', 'for']:
            stack.append('ctrl')
            current_depth += 1
            if current_depth > max_depth: max_depth = current_depth
            while i + 1 < len(tokens) and tokens[i+1] not in['{', '}', 'if', 'for', 'switch', 'else']:
                i += 1
            if i + 1 < len(tokens) and tokens[i+1] == '{': i += 1
                
        elif t == 'switch':
            stack.append('ctrl')
            current_depth += 1
            
            cases = 0
            braces = 0
            j = i + 1
            while j < len(tokens) and tokens[j] != '{': j += 1
            if j < len(tokens):
                braces = 1
                j += 1
                while j < len(tokens) and braces > 0:
                    if tokens[j] == '{': braces += 1
                    elif tokens[j] == '}': braces -= 1
                    elif tokens[j] in['case', 'default'] and braces == 1:
                        cases += 1
                    j += 1
                    
            added_depth = max(0, cases - 2)
            if current_depth + added_depth > max_depth:
                max_depth = current_depth + added_depth
                
            while i + 1 < len(tokens) and tokens[i+1] != '{': i += 1
            if i + 1 < len(tokens) and tokens[i+1] == '{': i += 1
                
        elif t == 'else':
            if i + 1 < len(tokens) and tokens[i+1] == 'if':
                pass 
            else:
                stack.append('ctrl')
                current_depth += 1
                if current_depth > max_depth: max_depth = current_depth
                while i + 1 < len(tokens) and tokens[i+1] != '{': i += 1
                if i + 1 < len(tokens) and tokens[i+1] == '{': i += 1
                    
        elif t == '{':
            stack.append('normal')
        elif t == '}':
            if stack:
                if stack.pop() == 'ctrl': current_depth -= 1
        i += 1

    CLI = max_depth

    ZG = CL + 1

    lbl_cl.config(text=f"Абсолютная сложность (CL): {CL}")
    lbl_n.config(text=f"Количество строк/операторов (N): {N}")
    lbl_cl_rel.config(text=f"Относительная сложность (cl): {cl_rel:.2f}")
    lbl_cli.config(text=f"Макс. уровень вложенности (CLI): {CLI}")
    lbl_zg.config(text=f"Метрика Маккейба Z(G): {ZG}")

root = tk.Tk()
root.title("Анализатор метрик потока управления (Джилб, Маккейб)")
root.geometry("600x450")

tk.Label(root, text="Вставьте код (Go) для анализа:", font=('Arial', 12, 'bold')).pack(pady=10)
text_input = tk.Text(root, height=12, width=70)
text_input.pack(padx=10)

tk.Button(root, text="Рассчитать метрики", command=analyze_code, bg="lightblue", font=('Arial', 12, 'bold')).pack(pady=15)

frame_res = tk.Frame(root)
frame_res.pack(fill=tk.BOTH, expand=True, padx=20)

lbl_cl = tk.Label(frame_res, text="Абсолютная сложность (CL): 0", font=('Arial', 11))
lbl_cl.pack(anchor='w')
lbl_n = tk.Label(frame_res, text="Количество строк/операторов (N): 0", font=('Arial', 11))
lbl_n.pack(anchor='w')
lbl_cl_rel = tk.Label(frame_res, text="Относительная сложность (cl): 0.0", font=('Arial', 11))
lbl_cl_rel.pack(anchor='w')
lbl_cli = tk.Label(frame_res, text="Макс. уровень вложенности (CLI): 0", font=('Arial', 11, 'bold'), fg="darkred")
lbl_cli.pack(anchor='w', pady=5)
lbl_zg = tk.Label(frame_res, text="Метрика Маккейба Z(G): 0", font=('Arial', 11, 'bold'), fg="darkblue")
lbl_zg.pack(anchor='w')

root.mainloop()