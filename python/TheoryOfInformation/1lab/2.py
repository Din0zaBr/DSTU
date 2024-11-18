from tkinter import *
import numpy as np


def more():
    window.geometry("1000x700")


def rasch():
    global n, k, H_s, G_s, t_i, t_c, corr, finds
    st = text_box.get("1.0", END)
    # st = "1 1 1 1 0 0 0\n0 0 1 1 1 1 0\n0 1 0 1 1 0 1"
    # v = "0010110"
    step1 = st.split('\n')
    step2 = []
    for i in range(len(step1) - 1):
        step2.append([int(numeric_string) for numeric_string in step1[i].split(" ")])
    arr = np.array(step2)
    arr_copy = np.array(step2)
    c = ()
    if typematr.get() == "born":
        c = arr.shape  # (строки, столбцы)
        n = c[1]
        k = c[0]
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
        I_k = np.eye(k)
        P = arr
        G_s = np.hstack((I_k, P))
        print("G_sys")
        print(G_s)
        out2 = G_s
        P_t = P.transpose()
        I_n_k = np.eye(n - k)
        H_s = np.hstack((P_t, I_n_k))
        print("H_sys")
        print(H_s)
        t_i = np.zeros(k)
        t_c = np.zeros(n)
        w_h = []
        for i in range(1, 2 ** k):
            bin_i = bin(i)
            bin_arr = "0" * (k - len(bin_i[2:])) + bin_i[2:]
            t_i_new = [int(numeric_string) for numeric_string in list(bin_arr)]
            t_i = np.vstack((t_i, t_i_new))
        for i in range(1, 2 ** k):
            t_c_new = np.dot(np.hstack(t_i[i]), G_s)
            for j in range(len(t_c_new)):
                t_c_new[j] = t_c_new[j] % 2
            t_c = np.vstack((t_c, t_c_new))
        w_h = np.sum(t_c, axis=1)
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
    elif typematr.get() == "check":
        c = arr.shape  # (строки, столбцы)
        n = c[1]
        k = c[1] - c[0]
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
        P = arr.transpose()
        I_n_k = np.eye(c[0])
        H_s = np.hstack((arr, I_n_k))
        print("H_sys")
        print(H_s)
        out2 = H_s
        I_k = np.eye(k)
        G_s = np.hstack((I_k, P))
        print("G_sys")
        print(G_s)
        t_i = np.zeros(k)
        t_c = np.zeros(n)
        w_h = []
        for i in range(1, 2 ** k):
            bin_i = bin(i)
            bin_arr = "0" * (k - len(bin_i[2:])) + bin_i[2:]
            t_i_new = [int(numeric_string) for numeric_string in list(bin_arr)]
            t_i = np.vstack((t_i, t_i_new))
        for i in range(1, 2 ** k):
            t_c_new = np.dot(np.hstack(t_i[i]), G_s)
            for j in range(len(t_c_new)):
                t_c_new[j] = t_c_new[j] % 2
            t_c = np.vstack((t_c, t_c_new))
        w_h = np.sum(t_c, axis=1)
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
    ans2.configure(text=out2)
    ans3.configure(text=out3)
    ans4.configure(text=out4)


# РАБОТА С ВЕКТОРОМ
def vector():
    v = (txt.get())
    if corr == 0:
        warn.configure(text="Код не исправляет ошибок.")
    else:
        vec = [int(numeric_string) for numeric_string in list(v)]
        vect = np.array(vec)
        H_s_T = H_s.transpose()
        E = np.zeros(n)
        for i in range(1, n + 1):
            new_line = []
            for j in range(n):
                if (i + j) == n:
                    new_line.append(1)
                else:
                    new_line.append(0)
            new = np.array(new_line)
            E = np.vstack((E, new))
        e_case = ()
        e_case = E.shape  # (строки, столбцы)
        S = np.dot(E[0], H_s_T)
        for i in range(1, e_case[0]):
            s_i = np.dot(E[i], H_s_T)
            for j in range(len(s_i)):
                s_i[j] = s_i[j] % 2
            S = np.vstack((S, s_i))
        s_clear = S
        e_clear = E
        del_count = 0
        meet_count = []
        if e_case[0] > 2 ** (1):
            for i in range(len(E)):
                if str(S[i]) in meet_count:
                    s_clear = np.delete(s_clear, i - del_count, 0)
                    e_clear = np.delete(e_clear, i - del_count, 0)
                    del_count += 1
                else:
                    meet_count.append(str(S[i]))
        out7 = "S                     E \n"
        for i in range(len(s_clear)):
            out7 += str(s_clear[i]) + "  " + str(e_clear[i]) + "\n"
        s_in = np.dot(vect, H_s_T)
        for j in range(len(s_in)):
            s_in[j] = s_in[j] % 2

        for i in range(len(S)):
            if str(s_in) == str(S[i]):
                e_in = E[i]
        c_word = vect + e_in
        for j in range(len(c_word)):
            c_word[j] = c_word[j] % 2
        for i in range(len(t_c[i])):
            if str(c_word) == str(t_c[i]):
                word = t_i[i]
        out8 = "Cиндром введённого вектора: " + str(s_in) + "\nCоотвествующий вектор ошибок: " + str(
            e_in) + "\nЗакодированное слово без ошибок:" + str(c_word) + "\nРаскодированное слово" + str(word)
        ans7.configure(text=out7)
        ans8.configure(text=out8)


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
