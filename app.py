import streamlit as st
import subprocess
import os

# Page Title
st.title("🧪 QsarDB Web Application")

# --- AUTOMATIC MAVEN COMPILER ON STREAMLIT ---
@st.cache_resource
def build_project_directly():
    st.info("🔄 First time initialization: Compiling Java QSARDB project... (Please wait 1-2 minutes)")
    try:
        # Streamlit server par hi project build karne ki command
        subprocess.run(["mvn", "clean", "package", "-DskipTests"], capture_output=True, text=True)
        return True
    except Exception as e:
        st.error(f"Maven error: {str(e)}")
        return False

# Build trigger karna
build_project_directly()

# Pure project se automatic built jar file dhoondna
def find_jar():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".jar") and "original" not in file.lower():
                if "target" in root: # target folder ke andar se dhoondna
                    return os.path.join(root, file)
    return None

jar_path = find_jar()

if jar_path:
    st.success(f"✅ Backend Connected: {os.path.basename(jar_path)}")
else:
    st.warning("⚠️ Waiting for build to finish... Please refresh in a moment.")

# --- SIMPLE FORM LAYOUT ---
st.subheader("📋 Registry & Details")
molecule_id = st.text_input("Compound Id", value="Fisetin-Ligand")
name = st.text_input("Name *", value="")
description = st.text_area("Description", value="")
smiles = st.text_input("SMILES String", value="C1=CC=C(C=C1)C2=C(C(=O)C3=CC=CC=C3O2)O")

st.markdown("---")

# --- EXECUTE BUTTON ---
if st.button("Run / Save Analysis"):
    if jar_path is None:
        st.error("Error: Compiled file still not found. Make sure 'packages.txt' is added.")
    else:
        st.info(f"Executing payload on backend...")
        try:
            result = subprocess.run(
                ["java", "-jar", jar_path, "--id", molecule_id, "--smiles", smiles], 
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
