import streamlit as st
import subprocess
import os

# Page Title
st.title("🧪 QsarDB Web Application")

# --- FORCE COMPILE LOGIC ---
@st.cache_resource
def force_compile():
    st.info("🔄 Checking Java environment and building submodules... Please wait.")
    try:
        # Pura clean build chalana taake modules target folders banayein
        subprocess.run(["mvn", "clean", "install", "-DskipTests"], capture_output=True, text=True)
        return True
    except Exception as e:
        st.error(f"Compilation trigger failed: {str(e)}")
        return False

force_compile()

# --- UNIVERSAL SCANNER ---
def find_compiled_artifact():
    # Pura workspace scan karna submodules (cargo, model, storage, query) k andar
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".jar") and "original" not in file.lower():
                # QSARDB ka koi bhi active component module return karna
                return os.path.join(root, file)
    return None

jar_path = find_compiled_artifact()

if jar_path:
    st.success(f"✅ Backend Connected: {os.path.basename(jar_path)}")
else:
    st.warning("⚠️ Executable binary sequence initializing... Try clicking run below.")

# --- SIMPLE FORM LAYOUT ---
st.subheader("📋 Registry & Details")
molecule_id = st.text_input("Compound Id", value="Fisetin-Ligand")
name = st.text_input("Name *", value="")
description = st.text_area("Description", value="")
smiles = st.text_input("SMILES String", value="C1=CC=C(C=C1)C2=C(C(=O)C3=CC=CC=C3O2)O")

st.markdown("---")

# --- EXECUTE BUTTON ---
if st.button("Run / Save Analysis"):
    # Agar loop bypass ho jaye to common target coordinates fallback lagana
    executable_path = jar_path if jar_path else "./model/target/qsardb-model-1.0.jar"
    
    st.info(f"Targeting active workspace: {executable_path}")
    try:
        result = subprocess.run(
            ["java", "-jar", executable_path, "--id", molecule_id, "--smiles", smiles], 
            capture_output=True, 
            text=True
        )
        
        st.subheader("🚀 Result Logs")
        if result.stdout:
            st.code(result.stdout)
        if result.stderr:
            st.code(result.stderr)
            
    except Exception as e:
        st.error(f"Execution failed: {str(e)}")
