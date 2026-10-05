import streamlit as st
import subprocess
import os

# Page configurations
st.set_page_config(page_title="QsarDB Editor", layout="wide")
st.title("🧪 QsarDB Web Application")

# --- GLOBAL SCANNER FOR JAVA EXECUTABLES ---
def find_any_valid_jar():
    # Poore directory tree me search karna bina targets folder ki kisi hard condition k
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".jar") and "original" not in file.lower():
                # QSARDB standard components key phrases check karna
                if any(x in file.lower() for x in ["client", "cli", "toolkit", "model", "qsardb"]):
                    return os.path.join(root, file)
    return None

jar_path = find_any_valid_jar()

# Debug component for visual validation
if jar_path is not None:
    st.sidebar.success(f"Backend Active: {os.path.basename(jar_path)}")
else:
    st.sidebar.error("Backend Alert: Looking for JAR file...")

# --- DESIGNED INTERFACE LAYOUT (Asal Desktop App ki tarah) ---
col1, col2 = st.columns()

with col1:
    st.subheader("📋 Registry")
    molecule_id = st.text_input("Id", value="Fisetin-Ligand")
    st.selectbox("Select Compound:", [molecule_id, "New Compound..."])

with col2:
    st.subheader("📝 Compound Details")
    name = st.text_input("Name *", value="")
    description = st.text_area("Description", value="")
    
    col_left, col_right = st.columns(2)
    with col_left:
        labels = st.text_input("Labels")
        cas = st.text_input("CAS")
    with col_right:
        inchi = st.text_input("InChi")
        smiles = st.text_input("SMILES String", value="C1=CC=C(C=C1)C2=C(C(=O)C3=CC=CC=C3O2)O")

    st.markdown("---")
    st.subheader("🚀 Execute QSAR Action")
    
    if st.button("Run / Save Analysis"):
        # Agar memory space me system path compile nahi mila to direct build target apply karna
        executable_path = jar_path if jar_path else "./client/target/qsardb-client-1.0.jar"
        
        st.info(f"Executing payload on: {executable_path}")
        try:
            # Passing default terminal parameters for java execution environment
            result = subprocess.run(
                ["java", "-jar", executable_path, "--id", molecule_id, "--smiles", smiles], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                st.success("Java Backend Executed Successfully!")
                st.code(result.stdout)
            else:
                st.warning("Java Process Response:")
                # Display output logs or standard terminal standard errors
                st.code(result.stdout if result.stdout else result.stderr)
        except Exception as e:
            st.error(f"Execution failed: {str(e)}")
