import streamlit as st  
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import base64

# --- PAGE CONFIG ---
st.set_page_config(page_title="CMALT - Composite Tool", layout="wide")

# --- SESSION STATE INIT ---
if "name_entered" not in st.session_state:
    st.session_state["name_entered"] = False

# --- FRONT PAGE (NAME ENTRY) ---
if not st.session_state["name_entered"]:

    def show_logo_centered(image_path, width=200):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            st.markdown(
                f"""
                <div style='text-align: center; padding-top: 10px; padding-bottom: 10px;'>
                    <img src='data:image/png;base64,{encoded}' width='{width}'>
                </div>
                """,
                unsafe_allow_html=True
            )

    show_logo_centered("cmalt_logo.png", width=220)

    st.markdown("""
        <h3 style="text-align:center; font-size: 24px; color: #333;">
            <strong>Composite Micromechanical Analysis Learning Tool</strong>
        </h3>
    """, unsafe_allow_html=True)

    with st.expander("📘 Learn More about CMALT"):
        st.markdown("""
        **CMALT** (Composite Micromechanical Analysis Learning Tool) is developed to provide users with an intuitive interface for understanding composite micromechanics, specifically the calculation of elastic properties such as **E₁ (longitudinal modulus)** and **E₂ (transverse modulus)**.

        🔹 **Why CMALT?**
        - Supports engineering education and composite design.
        - Visualizes how fiber and matrix properties affect stiffness.
        - Provides side-by-side comparison for two composite cases.

        🔹 **Who is it for?**
        - Engineering students  
        - Academic instructors  
        - Industry engineers needing quick estimations

        CMALT bridges theory and application — making composite learning interactive, fast, and fun.
        """)

    name = st.text_input("👤 Enter your name:", key="username_input")
    if st.button("➡️ Proceed"):
        if name.strip() != "":
            st.session_state["name_entered"] = True
            st.session_state["username"] = name.strip()
            st.rerun()
        else:
            st.warning("Please enter your name before proceeding.")

else:
    st.markdown(f"<h3 style='text-align:center;'>👋 Welcome, {st.session_state['username']}!</h3>", unsafe_allow_html=True)

    defaults = {
        "Ef1": 0.0, "Em1": 0.0, "Vf1": 0.0, "calc1": False,
        "Ef2": 0.0, "Em2": 0.0, "Vf2": 0.0, "calc2": False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    def reset_case1():
        st.session_state["Ef1"] = 0.0
        st.session_state["Em1"] = 0.0
        st.session_state["Vf1"] = 0.0
        st.session_state["calc1"] = False

    def reset_case2():
        st.session_state["Ef2"] = 0.0
        st.session_state["Em2"] = 0.0
        st.session_state["Vf2"] = 0.0
        st.session_state["calc2"] = False

    with st.expander("📘 Theory: What Are E₁ and E₂?"):
        st.markdown("""
        - **E₁ (Longitudinal Modulus)**: Stiffness along the fiber direction.  
        - **E₂ (Transverse Modulus)**: Stiffness perpendicular to the fiber.
        """)
        st.latex(r"E_1 = E_f V_f + E_m V_m")
        st.latex(r"E_2 = \frac{E_f E_m}{V_m E_f + V_f E_m}")

    # --- LAYOUT ---
    col1, col2 = st.columns(2)
    fig, ax = plt.subplots()
    plot_ready = False

    # === CASE STUDY 1 ===
    with col1:
        st.markdown("### 🧪 Case Study 1")
        st.number_input("Fiber Modulus Ef1 (GPa)", min_value=0.0, key="Ef1")
        st.number_input("Matrix Modulus Em1 (GPa)", min_value=0.0, key="Em1")
        st.number_input("Fiber Volume Fraction Vf1", min_value=0.0, max_value=1.0, key="Vf1")
        Vm1 = 1 - st.session_state["Vf1"]
        st.write(f"**Matrix Volume Fraction Vm1:** {Vm1:.2f}")
        c1a, c1b = st.columns(2)
        with c1a:
            if st.button("✅ Enter Case 1"):
                if all([st.session_state["Ef1"] > 0, st.session_state["Em1"] > 0, st.session_state["Vf1"] > 0]):
                    st.session_state["calc1"] = True
                else:
                    st.warning("Please fill in all input values before entering Case 1.")
        with c1b:
            st.button("🔄 Reset Case 1", on_click=reset_case1)

        if st.session_state["calc1"]:
            Ef1, Em1, Vf1 = st.session_state["Ef1"], st.session_state["Em1"], st.session_state["Vf1"]
            E1 = Ef1 * Vf1 + Em1 * Vm1
            E2 = (Ef1 * Em1) / (Vm1 * Ef1 + Vf1 * Em1)
            st.markdown("### 📤 Results for Case Study 1")
            st.write(f"**E₁ (Longitudinal Modulus):** {E1:.2f} GPa")
            st.write(f"**E₂ (Transverse Modulus):** {E2:.2f} GPa")
            vf = np.linspace(0, 1, 100)
            vm = 1 - vf
            ax.plot(vf, Ef1 * vf + Em1 * vm, label="E₁ Case 1", color="blue")
            ax.plot(vf, (Ef1 * Em1) / (vm * Ef1 + vf * Em1), label="E₂ Case 1", color="orange")
            plot_ready = True

    # === CASE STUDY 2 ===
    with col2:
        st.markdown("### 🧪 Case Study 2 (Optional)")
        st.number_input("Fiber Modulus Ef2 (GPa)", min_value=0.0, key="Ef2")
        st.number_input("Matrix Modulus Em2 (GPa)", min_value=0.0, key="Em2")
        st.number_input("Fiber Volume Fraction Vf2", min_value=0.0, max_value=1.0, key="Vf2")
        Vm2 = 1 - st.session_state["Vf2"]
        st.write(f"**Matrix Volume Fraction Vm2:** {Vm2:.2f}")
        c2a, c2b = st.columns(2)
        with c2a:
            if st.button("✅ Enter Case 2"):
                if all([st.session_state["Ef2"] > 0, st.session_state["Em2"] > 0, st.session_state["Vf2"] > 0]):
                    st.session_state["calc2"] = True
                else:
                    st.warning("Please fill in all input values before entering Case 2.")
        with c2b:
            st.button("🔄 Reset Case 2", on_click=reset_case2)

        if st.session_state["calc2"]:
            Ef2, Em2, Vf2 = st.session_state["Ef2"], st.session_state["Em2"], st.session_state["Vf2"]
            E1 = Ef2 * Vf2 + Em2 * Vm2
            E2 = (Ef2 * Em2) / (Vm2 * Ef2 + Vf2 * Em2)
            st.markdown("### 📤 Results for Case Study 2")
            st.write(f"**E₁ (Longitudinal Modulus):** {E1:.2f} GPa")
            st.write(f"**E₂ (Transverse Modulus):** {E2:.2f} GPa")
            vf = np.linspace(0, 1, 100)
            vm = 1 - vf
            ax.plot(vf, Ef2 * vf + Em2 * vm, "--", label="E₁ Case 2", color="blue")
            ax.plot(vf, (Ef2 * Em2) / (vm * Ef2 + vf * Em2), "--", label="E₂ Case 2", color="orange")
            plot_ready = True

    # === COMBINED PLOT ===
    if plot_ready:
        st.markdown("### 📈 Modulus Variation with Fiber Volume Fraction")
        ax.set_xlabel("Fiber Volume Fraction (Vf)")
        ax.set_ylabel("Elastic Modulus (GPa)")
        ax.set_title("Comparison of E₁ and E₂ vs. Vf")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

# === FOOTER ===
st.markdown("""
<hr style="margin-top: 50px;">
<p style='text-align: center; font-size: 14px; color: gray;'>
    Developed by S. A. Suhaime, F. R. Rosli, M. N. A. Ab Patar, M. S. Ismail, and J. Mahmud – 2025
</p>
""", unsafe_allow_html=True)
