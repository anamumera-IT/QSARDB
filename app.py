import streamlit as st
import subprocess
import os

# Page Title
st.title("🧪 QsarDB Web Application")

# --- JAR FILE FINDER ---
def find_jar():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".jar") and "original" not in file.lower():
                return os.path.join(root, file)
    return None

jar_path = find_jar()

if jar_path:
    st.success(f"Backend Active: {os.path.basename(jar_path)}")
else:
    st.warning("Looking for JAR file... System template active.")

# --- SIMPLE FORM LAYOUT ---
st.subheader("📋 Registry & Details")
molecule_id = st.text_input("Compound Id", value="Fisetin-Ligand")
name = st.text_input("Name *", value="")
description = st.text_area("Description", value="")
smiles = st.text_input("SMILES String", value="C1=CC=C(C=C1)C2=C(C(=O)C3=CC=CC=C3O2)O")

st.markdown("---")

# --- EXECUTE BUTTON ---
if st.button("Run / Save Analysis"):
    # Agar automatic jar nahi mili to default hardcoded path use karein
    executable_path = jar_path if jar_path else "./model/target/qsardb-model.jar"
    
    st.info(f"Executing: {executable_path}")
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
