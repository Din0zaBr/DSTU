from TheoryOfInformation.lab1.utils_for_analyze import analyze
from TheoryOfInformation.lab1.utils_for_encode_decode import huffman_encode, huffman_decode, lz77_encode, lzw_encode
from TheoryOfInformation.lab1.utils_for_matrix_representation_of_block_codes import main_new
import tkinter as tk
from tkinter import ttk
import threading


def main():
    # Создание графического интерфейса
    root = tk.Tk()
    root.title('File Analyzer')

    file_label = tk.Label(root, text='Enter file path:')
    file_label.grid(row=0, column=0, padx=10, pady=10)

    file_entry = tk.Entry(root, width=50)
    file_entry.grid(row=0, column=1, padx=10, pady=10)

    entropy_label = tk.Label(root, text='')
    entropy_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    progress_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
    progress_bar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    results_table = ttk.Treeview(root, columns=('Parameter', 'Value'), show='headings')
    results_table.heading('Parameter', text='Parameter')
    results_table.heading('Value', text='Value')
    results_table.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    loading_label = tk.Label(root, text='')
    loading_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    analyze_button = tk.Button(root, text='Analyze file', command=lambda: threading.Thread(target=analyze,
                                                                                           args=(file_entry,
                                                                                                 entropy_label,
                                                                                                 progress_bar,
                                                                                                 results_table,
                                                                                                 loading_label,
                                                                                                 root)).start())
    analyze_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    encode_decode_button = tk.Button(root, text='Encode/Decode file', command=lambda: open_encode_decode_window(root))
    encode_decode_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
    block_codes_button = tk.Button(root, text='Block codes', command=lambda: threading.Thread(target=block_code()))
    block_codes_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
    root.mainloop()


def open_encode_decode_window(root):
    global encode_decode_window

    if 'encode_decode_window' in globals():
        encode_decode_window.lift()
        return

    encode_decode_window = tk.Toplevel(root)
    encode_decode_window.title('Encode/Decode file')

    algorithm_label = tk.Label(encode_decode_window, text='Select algorithm:')
    algorithm_label.grid(row=0, column=0, padx=10, pady=10)

    algorithm_var = tk.StringVar(encode_decode_window)
    algorithm_var.set('Huffman')  # default value

    algorithm_menu = ttk.OptionMenu(encode_decode_window, algorithm_var, 'Huffman', "Huffman", 'LZ77', 'LZW')
    algorithm_menu.grid(row=0, column=1, padx=10, pady=10)

    file_label = tk.Label(encode_decode_window, text='Enter file path:')
    file_label.grid(row=1, column=0, padx=10, pady=10)

    file_entry = tk.Entry(encode_decode_window, width=50)
    file_entry.grid(row=1, column=1, padx=10, pady=10)

    encode_button = tk.Button(encode_decode_window, text='Encode', command=lambda: threading.Thread(target=encode_file,
                                                                                                    args=(
                                                                                                        algorithm_var.get(),
                                                                                                        file_entry)).start())
    encode_button.grid(row=2, column=0, padx=10, pady=10)

    decode_button = tk.Button(encode_decode_window, text='Decode', command=lambda: threading.Thread(target=decode_file,
                                                                                                    args=(
                                                                                                        algorithm_var.get(),
                                                                                                        file_entry)).start())
    decode_button.grid(row=2, column=1, padx=10, pady=10)


def encode_file(algorithm, file_entry):
    file_path = file_entry.get()

    if algorithm == 'Huffman':
        huffman_encode(file_path)
    elif algorithm == 'LZ77':
        lz77_encode(file_path)
    elif algorithm == 'LZW':
        lzw_encode(file_path)


def decode_file(algorithm, file_entry):
    file_path = file_entry.get()

    if algorithm == 'Huffman':
        huffman_decode(file_path)


def block_code():
    main_new()


if __name__ == "__main__":
    main()
