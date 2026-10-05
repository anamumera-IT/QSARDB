import streamlit as st
import subprocess
import os

# Page layout ko wide karna taake asal app jaisa bada interface dikhay
st.set_page_config(page_title="QsarDB Editor", layout="wide")

st.title("🧪 QsarDB Web Application")

# Pata lagana ke jar file pooray project mein kahan chhupi hui hai
def find_jar():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".jar") and "cli" in file.lower() or "toolkit" in file.lower() or "model" in file.lower():
                return os.path.join(root, file)
    return None

jar_path = find_jar()

# Asal App jaisa Left aur Right interface banane ke liye Columns use karna
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("📋 Registry")
    # Left Panel jahan molecules ki list aati hai
    molecule_id = st.text_input("Id", value="Fisetin-Ligand")
    st.selectbox("Select Compound:", [molecule_id, "New Compound..."])

with col2:
    st.subheader("📝 Compound Details")
    
    # Asal app ke mutabiq input fields
    name = st.text_input("Name *", value="")
    description = st.text_area("Description", value="")
    
    col_left, col_right = st.columns(2)
    with col_left:
        labels = st.text_input("Labels")
        cas = st.text_input("CAS")
    with col_right:
        inchi = st.text_input("InChi")
        smiles = st.text_input("SMILES String", value="C1=CC=C(C=C1)C2=C(C(=O)C3=CC=CC=C3O2)O") # Example structure

    st.markdown("---")
    st.subheader("🚀 Execute QSAR Action")
    
    # Run karne ka process
    if st.button("Run / Save Analysis"):
        if jar_path is None:
            st.error("Error: Compiled Java JAR file pooray project mein kahin nahi mili! Meharbani karke check karein ke GitHub Actions ka build kamyab hua tha ya nahi.")
        else:
            st.info(f"Using executed file: {jar_path}")
            try:
                # Java program ko backend mein inputs pass karna
                result = subprocess.run(
                    ["java", "-jar", jar_path, "--id", molecule_id, "--smiles", smiles], 
                    capture_output=True, 
                    text=True
                )
                
                if result.returncode == 0:
                    st.success("Java Backend Executed Successfully!")
                    st.code(result.stdout)
                else:
                    st.warning("Java ran but returned an alert:")
                    st.code(result.stderr)
            except Exception as e:
                st.error(f"Execution failed: {str(e)}")
