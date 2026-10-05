import streamlit as st
import subprocess
import os

st.title("🧪 QSARDB Java Runner via Streamlit")

# Check karna ke kya Java system me install hai
st.write("Java Environment aur Database ko verify kiya ja raha hai...")

# Input fields (Aap apne mutabiq inputs badal sakti hain)
command_input = st.text_input("Enter Command/SMILES for QSAR:", "query")

if st.button("Run QSAR Analysis"):
    try:
        # Background me Java JAR file ko execute karna
        # Note: 'target/your-file.jar' ki jagah build hone wali jar ka sahi naam dain
        result = subprocess.run(
            ["java", "-jar", "model/target/qsardb-model.jar", command_input], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            st.success("Java Output:")
            st.code(result.stdout)
        else:
            st.error("Error in Java Execution:")
            st.code(result.stderr)
            
    except Exception as e:
        st.error(f"Execution failed: {str(e)}")
