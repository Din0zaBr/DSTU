from tkinter import *
import numpy as np

def more():
    window.geometry("1000x700")

def create_G_s(arr, k):
    I_k = np.eye(k)
    P = arr
    return np.hstack((I_k, P))

def create_H_s(arr, n, k):
    P_t = arr.transpose()
    I_n_k = np.eye(n - k)
    return np.hstack((P_t, I_n_k))

def create_info_code_table(G_s, k):
    t_i = np.zeros(k)
    t_c = np.zeros(G_s.shape[1])
    for i in range(1, 2 ** k):
        bin_i = bin(i)
        bin_arr = "0" * (k - len(bin_i[2:])) + bin_i[2:]
        t_i_new = [int(numeric_string) for numeric_string in list(bin_arr)]
        t_i = np.vstack((t_i, t_i_new))
        t_c_new = np.dot(np.hstack(t_i[i]), G_s)
        for j in range(len(t_c_new)):
            t_c_new[j] = t_c_new[j] % 2
        t_c = np.vstack((t_c, t_c_new))
    w_h = np.sum(t_c, axis=1)
    return t_i, t_c, w_h

def create_error_syndrome_table(H_s, n):
    E = np.zeros(n)
    for i in range(1, n + 1):
        new_line = [1 if (i + j) == n else 0 for j in range(n)]
        E = np.vstack((E, new_line))
    S = np.dot(E[0], H_s.transpose())
    for i in range(1, E.shape[0]):
        s_i = np.dot(E[i], H_s.transpose())
        for j in range(len(s_i)):
            s_i[j] = s_i[j] % 2
        S = np.vstack((S, s_i))
    return S, E

def rasch():
    global n, k, H_s, G_s, t_i, t_c, corr, finds
    st = text_box.get("1.0", END)
    step1 = st.split('\n')
    step2 = []
    for i in range(len(step1) - 1):
        step2.append([int(numeric_string) for numeric_string in step1[i].split(" ")])
    arr = np.array(step2)
    arr_copy = np.array(step2)
    c = arr.shape  # (строки, столбцы)
    n = c[1]
    k = c[0] if typematr.get() == "born" else c[1] - c[0]
    out1 = "n = " + str(n) + " ; k = " + str(k)

    kol_of_del = 0
    for i in range(c[1]):
        c0 = 0
        c1 = 0
        for j in range(c[0]):
            if arr_copy[j][i] == 1:
                c1 += 1
            if arr_copy[j][i] == 0:
                c0 += 1
        if c1 == 1:
            arr = np.delete(arr, i - kol_of_del, 1)
            kol_of_del += 1

    if typematr.get() == "born":
        G_s = create_G_s(arr, k)
        H_s = create_H_s(arr, n, k)
    elif typematr.get() == "check":
        H_s = create_H_s(arr.transpose(), n, k)
        G_s = create_G_s(arr.transpose(), k)

    t_i, t_c, w_h = create_info_code_table(G_s, k)
    out3 = "    i                  c                  w_h \n"
    for i in range(len(t_c)):
        out3 += str(t_i[i]) + "  " + str(t_c[i]) + "  " + str(w_h[i]) + "\n"

    filtered_w_h = np.fromiter(
        (w_h_el for w_h_el in w_h if w_h_el > 0),
        dtype=w_h.dtype
    )
    Dmin = np.min(filtered_w_h)
    finds = Dmin - 1
    corr = 0
    while True:
        if not (Dmin < 2 * corr + 1):
            corr += 1
            break
    out4 = "Dmin = " + str(Dmin) + "\nНаходит - " + str(finds) + "\n Исправляет - " + str(corr)

    ans1.configure(text=out1)
    ans2.configure(text=G_s if typematr.get() == "born" else H_s)
    ans3.configure(text=out3)
    ans4.configure(text=out4)

def vector():
    v = (txt.get())
    if corr == 0:
        warn.configure(text="Код не исправляет ошибок.")
    else:
        vec = [int(numeric_string) for numeric_string in list(v)]
        vect = np.array(vec)
        S, E = create_error_syndrome_table(H_s, n)
        s_clear, e_clear = clean_error_syndrome_table(S, E)
        out7 = "S                     E \n"
        for i in range(len(s_clear)):
            out7 += str(s_clear[i]) + "  " + str(e_clear[i]) + "\n"
        s_in = np.dot(vect, H_s.transpose())
        for j in range(len(s_in)):
            s_in[j] = s_in[j] % 2
        e_in = E[np.where(np.all(S == s_in, axis=1))[0][0]]
        c_word = (vect + e_in) % 2
        word = t_i[np.where(np.all(t_c == c_word, axis=1))[0][0]]
        out8 = "Cиндром введённого вектора: " + str(s_in) + "\nCоотвествующий вектор ошибок: " + str(
            e_in) + "\nЗакодированное слово без ошибок:" + str(c_word) + "\nРаскодированное слово" + str(word)
        ans7.configure(text=out7)
        ans8.configure(text=out8)

def clean_error_syndrome_table(S, E):
    s_clear = S
    e_clear = E
    del_count = 0
    meet_count = []
    if E.shape[0] > 2 ** (1):
        for i in range(len(E)):
            if str(S[i]) in meet_count:
                s_clear = np.delete(s_clear, i - del_count, 0)
                e_clear = np.delete(e_clear, i - del_count, 0)
                del_count += 1
            else:
                meet_count.append(str(S[i]))
    return s_clear, e_clear

born = "born"
check = "check"

# ОКНО 1
typematr = ""
window = Tk()
window.title("Lab 2")
window.geometry("1000x50")
lbl1 = Label(window, text="Выберете алгоритм")
lbl1.grid(column=0, row=0)
typematr = StringVar(value="check")
born_btn = Radiobutton(text="Порождающая", value=born, variable=typematr)
born_btn.grid(column=0, row=1)
check_btn = Radiobutton(text="Проверочная", value=check, variable=typematr)
check_btn.grid(column=2, row=1)
btn0 = Button(window, text="Дальше", command=more)
btn0.grid(column=3, row=1)

# пункт 2
lbl2 = Label(window, text="Введите матрицу:")
lbl2.grid(column=0, row=2)
text_box = Text(height=13, width=30)
text_box.grid(column=0, row=3)
btn1 = Button(window, text="Подтвердить", command=rasch)
btn1.grid(column=0, row=4)
lbl3 = Label(window, text="Параметры:")  # n , k
lbl3.grid(column=1, row=2)
ans1 = Label(window, text="")
ans1.grid(column=1, row=3)
lbl4 = Label(window, text="Матрица в систематическом виде")
lbl4.grid(column=1, row=4)
ans2 = Label(window, text="")
ans2.grid(column=1, row=5)

lbl5 = Label(window, text="Таблица информационных и кодовых слов")
lbl5.grid(column=2, row=2)
ans3 = Label(window, text="")
ans3.grid(column=2, row=3)
lbl6 = Label(window, text="Вес Хемминга и  информация по ошибкам")
lbl6.grid(column=2, row=4)
ans4 = Label(window, text="")
ans4.grid(column=2, row=5)

# Пункт 3
lbl7 = Label(window, text="Введите вектор:")
lbl7.grid(column=1, row=9)
txt = Entry(window, width=30)
txt.grid(column=1, row=10)
btn2 = Button(window, text="Подтвердить", command=vector)
btn2.grid(column=1, row=11)
warn = Label(window, text="")
warn.grid(column=1, row=12)
lbl8 = Label(window, text="Таблица векторов ошибок и синдромов")  # n , k
lbl8.grid(column=3, row=9)
ans7 = Label(window, text="")
ans7.grid(column=3, row=10)
lbl9 = Label(window, text="Лидерное декодирование")
lbl9.grid(column=3, row=11)
ans8 = Label(window, text="")
ans8.grid(column=3, row=12)

window.mainloop()
