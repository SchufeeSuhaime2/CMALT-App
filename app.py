import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import base64

# --- Streamlit Page Config ---
st.set_page_config(page_title="CMALT - Composite Tool", layout="centered")

# --- Logo Function ---
def show_logo_centered(image_path, width=220):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
        st.markdown(
            f"<div style='text-align: center;'><img src='data:image/png;base64,{encoded}' width='{width}'></div>",
            unsafe_allow_html=True,
        )

# --- Session State Initialization ---
if "entered" not in st.session_state:
    st.session_state["entered"] = False

for case in ["1", "2"]:
    st.session_state.setdefault(f"preset{case}", "Custom Input")
    st.session_state.setdefault(f"last_preset{case}", "Custom Input")
    for key in ["Ef", "Em", "Vf"]:
        st.session_state.setdefault(f"{key}{case}", 0.0)
    st.session_state.setdefault(f"calc{case}", False)

# --- Front Page ---
if not st.session_state["entered"]:
    show_logo_centered("cmalt_logo.png")
    st.markdown("<h2 style='text-align: center;'>Composite Micromechanical Analysis Learning Tool</h2>", unsafe_allow_html=True)

    with st.expander("📘 Learn More about CMALT"):
        st.markdown("""
**CMALT** (Composite Micromechanical Analysis Learning Tool) is a Python-based interactive web application designed to support the understanding of micromechanical behavior in composite materials through two simultaneous case studies.

🔹 **Purpose**
- To help users **visualize the influence** of fiber and matrix properties on the overall elastic moduli of a composite lamina.
- To serve as a **teaching and self-learning aid** for students and educators in the subject of composite materials.

🔹 **Features**
- **Dual Case Study Comparison**: Analyze and compare two different composite material configurations side by side.
- **Real-Time Graph Plotting**: View how E₁ (longitudinal modulus) and E₂ (transverse modulus) vary with fiber volume fraction (Vf).
- **Rule of Mixtures Implementation**:
    - E₁ is calculated as:  
      $$E_1 = E_f V_f + E_m V_m$$  
    - E₂ is calculated as:  
      $$E_2 = \\frac{E_f E_m}{V_m E_f + V_f E_m}$$
- **Predefined Materials**: Includes options like Glass Fiber, Carbon Fiber, and Natural Fiber composites with default mechanical properties.
- **Custom Input Support**: Manually adjust Ef, Em, and Vf to simulate real-world materials or experimental data.
- **Auto Calculation and Reset**: Quickly compute or clear values with button interactions for each case.
- **Observation Generator**: Automatically compares results and provides interpretation for better understanding.
        """)

    if st.button("🚀 Proceed to Simulation"):
        st.session_state["entered"] = True
        st.rerun()

    st.markdown("<hr><p style='text-align: center;'>© 2025 Developed by S. A. Suhaime, F. R. Rosli, M. N. A. Ab Patar, M. S. Ismail, and J. Mahmud</p>", unsafe_allow_html=True)
    st.stop()

# === Main Simulation Starts ===
st.markdown("## Composite Micromechanical Analysis Learning Tool (CMALT)")
st.markdown("Compare two different composite configurations based on elastic modulus prediction.")
st.markdown("---")

with st.expander("📘 Theory: Composite Micromechanical Analysis"):
    st.markdown("""
Composite micromechanics helps predict the overall mechanical behavior of a composite lamina based on the individual properties of the fiber and matrix materials.

#### 🔹 Key Parameters:
- **Ef**: Modulus of Elasticity of the Fiber (GPa)  
- **Em**: Modulus of Elasticity of the Matrix (GPa)  
- **Vf**: Volume Fraction of Fiber  
- **Vm**: Volume Fraction of Matrix = 1 − Vf

#### 🔹 Elastic Moduli of the Composite:
1. **E₁ – Longitudinal Modulus**  
   Describes stiffness **along the fiber direction**:  
   $$E_1 = E_f V_f + E_m V_m$$

2. **E₂ – Transverse Modulus**  
   Describes stiffness **perpendicular to the fiber direction**:  
   $$E_2 = \\frac{E_f E_m}{V_m E_f + V_f E_m}$$

#### 🔹 Observations:
- Increasing **Vf** generally raises **E₁**, making the composite stiffer in the fiber direction.
- **E₂** is influenced by both fiber and matrix stiffness; increasing **Em** can improve transverse stiffness.
- The total volume fraction is always conserved:  
  $$V_f + V_m = 1$$

These relationships assume aligned continuous fibers, uniform distribution, and ideal bonding between the fiber and matrix.
""")

with st.expander("🧠 Example Practice Questions"):
    st.markdown("""
Test your understanding of micromechanical analysis using the following practice problems:

1. **Elastic Moduli Calculation**  
   A unidirectional composite is made from fibers with modulus **Ef = 70 GPa** and a matrix with **Em = 3.5 GPa**. If the fiber volume fraction is **Vf = 0.6**, calculate the longitudinal modulus (**E₁**) and transverse modulus (**E₂**) of the composite.

2. **Material Comparison**  
   Two composites are fabricated using different fibers:
   - **Material A**: Glass Fiber, **Vf = 0.55**
   - **Material B**: Carbon Fiber, **Vf = 0.40**  
   Assuming suitable values of Ef and Em for each material, determine which composite exhibits higher stiffness in the fiber direction (**E₁**).

3. **Prediction of Composite Moduli**  
   Given: **Ef = 12 GPa**, **Em = 2.5 GPa**, and **Vf = 0.5**.  
   Calculate the expected values of **E₁** and **E₂**.

4. **Effect of Fiber Volume Fraction**  
   Analyze and compare the elastic moduli for two fiber volume fraction scenarios:  
   - Case 1: **Vf = 0.75**  
   - Case 2: **Vf = 0.25**  
   Assume the same Ef and Em for both cases.

5. **Matrix Modulus Sensitivity**  
   Explain the effect on **E₂** when the matrix modulus (**Em**) is increased, while keeping **Ef** and **Vf** constant. Justify your answer using the E₂ formula.
""")

# --- Predefined Options ---
predefined = {
    "Custom Input": {"Ef": 0.0, "Em": 0.0, "Vf": 0.0},
    "Glass Fiber Composite": {"Ef": 70, "Em": 3.5, "Vf": 0.6},
    "Carbon Fiber Composite": {"Ef": 230, "Em": 3.0, "Vf": 0.65},
    "Natural Fiber Composite": {"Ef": 12, "Em": 2.5, "Vf": 0.5}
}

def reset_case(case):
    for key in ["Ef", "Em", "Vf"]:
        st.session_state[f"{key}{case}"] = 0.0
    st.session_state[f"calc{case}"] = False
    st.session_state[f"preset{case}"] = "Custom Input"
    st.session_state[f"last_preset{case}"] = "Custom Input"

# --- Layout ---
col1, col2 = st.columns(2)
fig, ax = plt.subplots()
plot_ready = False

# === CASE 1 ===
with col1:
    st.markdown("### 🧪Case Study 1")
    preset1 = st.selectbox("📁 Predefined Case 1", options=predefined.keys(), key="preset1")

    if st.session_state["last_preset1"] != preset1:
        for key, val in predefined[preset1].items():
            st.session_state[f"{key}1"] = val
        st.session_state["last_preset1"] = preset1

    Ef1 = st.number_input("Fiber Modulus Ef1 (GPa)", min_value=0.0, key="Ef1")
    Em1 = st.number_input("Matrix Modulus Em1 (GPa)", min_value=0.0, key="Em1")
    Vf1 = st.number_input("Fiber Volume Fraction Vf1", min_value=0.0, max_value=1.0, key="Vf1")
    Vm1 = 1 - Vf1
    st.write(f"**Matrix Volume Fraction Vm1:** {Vm1:.2f}")

    c1a, c1b = st.columns(2)
    with c1a:
        if st.button("✅ Enter Case 1"):
            if Ef1 > 0 and Em1 > 0 and Vf1 > 0:
                st.session_state["calc1"] = True
            else:
                st.warning("Please fill in all values for Case 1.")
    with c1b:
        st.button("🔄 Reset Case 1", on_click=lambda: reset_case("1"))

    if st.session_state["calc1"]:
        E1_1 = Ef1 * Vf1 + Em1 * Vm1
        denom1 = Vm1 * Ef1 + Vf1 * Em1
        E2_1 = (Ef1 * Em1 / denom1) if denom1 != 0 else 0
        st.markdown("### 📤 Results for Case 1")
        st.write(f"**E₁:** {E1_1:.2f} GPa")
        st.write(f"**E₂:** {E2_1:.2f} GPa")
        vf = np.linspace(0, 1, 100)
        vm = 1 - vf
        ax.plot(vf, Ef1 * vf + Em1 * vm, label="E₁ Case 1", color="blue")
        ax.plot(vf, (Ef1 * Em1) / (vm * Ef1 + vf * Em1 + 1e-6), label="E₂ Case 1", color="orange")
        plot_ready = True

# === CASE 2 ===
with col2:
    st.markdown("### 🧪Case Study 2 (Optional)")
    preset2 = st.selectbox("📁 Predefined Case 2", options=predefined.keys(), key="preset2")

    if st.session_state["last_preset2"] != preset2:
        for key, val in predefined[preset2].items():
            st.session_state[f"{key}2"] = val
        st.session_state["last_preset2"] = preset2

    Ef2 = st.number_input("Fiber Modulus Ef2 (GPa)", min_value=0.0, key="Ef2")
    Em2 = st.number_input("Matrix Modulus Em2 (GPa)", min_value=0.0, key="Em2")
    Vf2 = st.number_input("Fiber Volume Fraction Vf2", min_value=0.0, max_value=1.0, key="Vf2")
    Vm2 = 1 - Vf2
    st.write(f"**Matrix Volume Fraction Vm2:** {Vm2:.2f}")

    c2a, c2b = st.columns(2)
    with c2a:
        if st.button("✅ Enter Case 2"):
            if Ef2 > 0 and Em2 > 0 and Vf2 > 0:
                st.session_state["calc2"] = True
            else:
                st.warning("Please fill in all values for Case 2.")
    with c2b:
        st.button("🔄 Reset Case 2", on_click=lambda: reset_case("2"))

    if st.session_state["calc2"]:
        E1_2 = Ef2 * Vf2 + Em2 * Vm2
        denom2 = Vm2 * Ef2 + Vf2 * Em2
        E2_2 = (Ef2 * Em2 / denom2) if denom2 != 0 else 0
        st.markdown("### 📤 Results for Case 2")
        st.write(f"**E₁:** {E1_2:.2f} GPa")
        st.write(f"**E₂:** {E2_2:.2f} GPa")
        vf = np.linspace(0, 1, 100)
        vm = 1 - vf
        ax.plot(vf, Ef2 * vf + Em2 * vm, "--", label="E₁ Case 2", color="blue")
        ax.plot(vf, (Ef2 * Em2) / (vm * Ef2 + vf * Em2 + 1e-6), "--", label="E₂ Case 2", color="orange")
        plot_ready = True

# === Combined Plot and Observation ===
if plot_ready:
    st.markdown("### 📈 Modulus Variation with Fiber Volume Fraction")
    ax.set_xlabel("Fiber Volume Fraction (Vf)")
    ax.set_ylabel("Elastic Modulus (GPa)")
    ax.set_title("Comparison of E₁ and E₂ vs. Vf")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    c1 = st.session_state["calc1"]
    c2 = st.session_state["calc2"]

    if c1 and c2:
        obs = "**📝 Observation:**\n\n"
        obs += f"Based on the calculated values, the comparison between Case Study 1 and Case Study 2 reveals the following insights:\n\n"

        # Longitudinal modulus comparison
        if E1_1 > E1_2:
            obs += f"- **Case Study 1** exhibits a higher longitudinal modulus (**E₁ = {E1_1:.2f} GPa**) than Case Study 2 (**E₁ = {E1_2:.2f} GPa**), indicating better stiffness along the fiber direction.\n"
        elif E1_2 > E1_1:
            obs += f"- **Case Study 2** exhibits a higher longitudinal modulus (**E₁ = {E1_2:.2f} GPa**) than Case Study 1 (**E₁ = {E1_1:.2f} GPa**), indicating better stiffness along the fiber direction.\n"
        else:
            obs += f"- Both case studies have the same longitudinal modulus (**E₁ = {E1_1:.2f} GPa**).\n"

        # Transverse modulus comparison
        if E2_1 > E2_2:
            obs += f"- **Case Study 1** also shows a higher transverse modulus (**E₂ = {E2_1:.2f} GPa**) compared to Case Study 2 (**E₂ = {E2_2:.2f} GPa**), suggesting improved stiffness perpendicular to the fiber.\n"
        elif E2_2 > E2_1:
            obs += f"- **Case Study 2** also shows a higher transverse modulus (**E₂ = {E2_2:.2f} GPa**) compared to Case Study 1 (**E₂ = {E2_1:.2f} GPa**), suggesting improved stiffness perpendicular to the fiber.\n"
        else:
            obs += f"- Both case studies have the same transverse modulus (**E₂ = {E2_1:.2f} GPa**).\n"

        st.markdown(obs)

    elif c1:
        st.markdown("**📝 Observation:**\n\nOnly Case Study 1 has been simulated. Observe how variations in fiber volume fraction affect both E₁ and E₂.")

    elif c2:
        st.markdown("**📝 Observation:**\n\nOnly Case Study 2 has been simulated. Observe how variations in fiber volume fraction affect both E₁ and E₂.")

# --- Footer ---
st.markdown("<hr><p style='text-align: center; font-size: 14px; color: gray;'>© 2025 Developed by S. A. Suhaime, F. R. Rosli, M. N. A. Ab Patar, M. S. Ismail, and J. Mahmud</p>", unsafe_allow_html=True)
