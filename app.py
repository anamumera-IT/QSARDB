import streamlit as st
import subprocess

# Page Setup
st.set_page_config(page_title="QsarDB Editor", layout="wide")
st.title("🧪 QsarDB Web Application")

# --- SIMPLE FORM LAYOUT ---
st.subheader("📋 Registry & Details")
molecule_id = st.text_input("Compound Id", value="Fisetin-Ligand")
name = st.text_input("Name *", value="")
description = st.text_area("Description", value="")
smiles = st.text_input("SMILES String", value="C1=CC=C(C=C1)C2=C(C(=O)C3=CC=CC=C3O2)O")

st.markdown("---")

# --- EXECUTE VIA DIRECT MAVEN PLUGIN ---
if st.button("Run / Save Analysis"):
    st.info("🔄 Processing request directly through Java runtime environment...")
    
    try:
        # Hamein .jar file ki zaroorat hi nahi hai, hum direct Maven plugin runtime logic use kar rahe hain
        # Yeh module command direct Java context ko call karegi bina kisi file dependency ke
        result = subprocess.run(
            [
                "mvn", "compile", "exec:java", 
                "-Dexec.mainClass=org.qsardb.model.Model", 
                f"-Dexec.args=--id {molecule_id} --smiles {smiles}"
            ], 
            capture_output=True, 
            text=True
        )
        
        st.subheader("🚀 Result Logs")
        
        # Display the output directly from the compiler shell
        if result.stdout:
            st.success("Analysis Complete!")
            st.code(result.stdout)
            
        if result.stderr and result.returncode != 0:
            st.warning("System Notice:")
            st.code(result.stderr)
            
    except Exception as e:
        st.error(f"Execution failed: {str(e)}")
