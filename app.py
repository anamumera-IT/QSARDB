import streamlit as st
import subprocess
import os

# Page layout
st.set_page_config(page_title="QsarDB Editor", layout="wide")
st.title("🧪 QsarDB Web Application")

# --- AUTO MAVEN BUILD ON STREAMLIT ---
# Yeh function Streamlit par hi Java project ko compile kar k asli JAR file bana dega
@st.cache_resource
def compile_java_project():
    st.info("🔄 First time initialization: Compiling Java QSARDB project on Streamlit Cloud... (Please wait about 1-2 minutes)")
    try:
        # Run maven build directly inside Streamlit container
        build_result = subprocess.run(
            ["mvn", "clean", "package", "-DskipTests"], 
            capture_output=True, 
            text=True
        )
        if build_result.returncode == 0:
            st.success("✅ Java Project Compiled successfully inside Streamlit!")
            return True
        else:
            st.error("❌ Maven build failed inside Streamlit:")
            st.code(build_result.stderr)
            return False
    except Exception as e:
        st.error(f"❌ Could not run Maven: {str(e)}")
        return False

# Build run karna
build_status = compile_java_project()

# Strict function compiled .jar dhoondne k liy
def find_jar():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".jar") and ("cli" in file.lower() or "toolkit" in file.lower() or "model" in file.lower() or "storage" in file.lower()):
                # ensure we are targeting a built target folder file
                if "target" in root:
                    return os.path.join(root, file)
    return None

jar_path = find_jar()

# --- INTERFACE LAYOUT ---
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
        if jar_path is None:
            st.error("Error: Compiled Java JAR file (.jar) nahi mili! Please make sure 'packages.txt' includes 'maven' and 'default-jdk'.")
        else:
            st.info(f"Using executed file: {jar_path}")
            try:
                # Running the compiled JAR file with parameters
                result = subprocess.run(
                    ["java", "-jar", jar_path, "--id", molecule_id, "--smiles", smiles], 
                    capture_output=True, 
                    text=True
                )
                
                if result.returncode == 0:
                    st.success("Java Backend Executed Successfully!")
                    st.code(result.stdout)
                else:
                    st.warning("Java program responded:")
                    st.code(result.stdout if result.stdout else result.stderr)
            except Exception as e:
                st.error(f"Execution failed: {str(e)}")
