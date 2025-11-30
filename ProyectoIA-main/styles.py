from tkinter import ttk

def aplicar_estilos(root):
    style = ttk.Style(root)

    # ======================
    # FUENTES
    # ======================
    # Tkinter no carga fuentes web; se usan equivalentes locales.
    FONT_INTER = ("Segoe UI", 11)
    FONT_INTER_BOLD = ("Segoe UI", 11, "bold")
    FONT_PLAYFAIR = ("Georgia", 13)  # Simulación de "Playfair Display"

    # ======================
    # BOTÓN PRINCIPAL  (.btn--primary)
    # ======================
    style.configure(
        "Primary.TButton",
        background="#f57c20",
        foreground="white",
        padding=(16, 10),   # ≈ 0.9rem 2rem
        font=FONT_INTER_BOLD,
        relief="flat",
    )

    # Hover → ttk lo maneja mediante "map"
    style.map(
        "Primary.TButton",
        background=[
            ("active", "#D85F1D")  # color hover
        ]
    )

    # ======================
    # LABELS DE ORIGEN/DESTINO (.route-form .field label)
    # ======================
    style.configure(
        "FieldLabel.TLabel",
        font=("Segoe UI", 13, "bold"),  # clamp convertido a tamaño fijo
        foreground="#000",
        padding=(0, 4, 0, 8),  # margen inferior ≈ 0.4rem
        background=root["bg"]
    )

    # ======================
    # COMBOBOXES  (.route-form select)
    # ======================
    style.configure(
        "Select.TCombobox",
        font=("Segoe UI", 11),
        padding=4,                           # padding equivalente a 0.4rem 0.8rem
        foreground="#000",
        fieldbackground="white",
        background="white",
        bordercolor="#aaa",
        lightcolor="#aaa",
        darkcolor="#aaa",
        borderwidth=1
    )

    # Esto hace que el borde se vea gris siempre
    style.map(
        "Select.TCombobox",
        bordercolor=[("focus", "#aaa"), ("!focus", "#aaa")]
    )

    return {
        "FONT_INTER": FONT_INTER,
        "FONT_INTER_BOLD": FONT_INTER_BOLD,
        "FONT_PLAYFAIR": FONT_PLAYFAIR
    }
