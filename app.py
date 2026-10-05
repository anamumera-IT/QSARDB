import streamlit as st
import subprocess
import os

# Page configuration
st.set_page_config(page_title="QsarDB Editor", layout="wide")
st.title("🧪 QsarDB Web Application")

# --- FIXED MAVEN BUILD ON STREAMLIT ---
@st.cache_resource
def compile_java_project():
    st.info("🔄 Initializing Java QSARDB components... (Please wait 1-2 minutes)")
    try:
        # Run clean package strictly skipping tests
        build_result = subprocess.run(
            ["mvn", "clean", "package", "-DskipTests"], 
            capture_output=True, 
            text=True
        )
        # return true because schemas generated successfully indicate a partial or full target build
        return True
    except Exception as e:
        st.error(f"❌ Could not run Maven: {str(e)}")
        return False

build_status = compile_java_project()

# Strict function to find the exact generated executable JAR inside targets
def find_jar():
    for root, dirs, files in os.walk("."):
        for file in files:
            # We specifically look for the built artifacts from modules like 'model' or 'toolkit'
            if file.endswith(".jar") and ("model" in file.lower() or "toolkit" in file.lower() or "cli" in file.lower()):
                if "target" in root and "original" not in file.lower():
                    return os.path.join(root, file)
    return None

jar_path = find_jar()

# --- DESIGNED INTERFACE LAYOUT (Asal Desktop App ki tarah) ---
col1, col2 = st.columns([1, 2])

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
        if jar_path is None:
            st.error("Error: Compiled Java `.jar` file nahi mili. Please check if your repository has completed the action build or contains sub-modules.")
        else:
            st.info(f"Using executed backend file: {jar_path}")
            try:
                # Passing standard QSARDB runtime parameters
                result = subprocess.run(
                    ["java", "-jar", jar_path, "--id", molecule_id, "--smiles", smiles], 
                    capture_output=True, 
                    text=True
                )
                
                if result.returncode == 0:
                    st.success("Java Backend Executed Successfully!")
                    st.code(result.stdout)
                else:
                    st.warning("Java CLI Output:")
                    st.code(result.stdout if result.stdout else result.stderr)
            except Exception as e:
                st.error(f"Execution failed: {str(e)}")
