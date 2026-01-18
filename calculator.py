import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Simple Calculator",
    page_icon="🔢",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem;
        font-size: 1.1rem;
        border-radius: 8px;
        border: none;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .result-box {
        padding: 1.5rem;
        background-color: #ffffff;
        border: 2px solid #4CAF50;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    .operation-label {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Title and header
st.title("🔢 Simple Calculator")
st.markdown("---")

# Session state initialization
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'num1' not in st.session_state:
    st.session_state.num1 = None
if 'num2' not in st.session_state:
    st.session_state.num2 = None
if 'num3' not in st.session_state:
    st.session_state.num3 = None
if 'result' not in st.session_state:
    st.session_state.result = None

# Step 1: Name input
if st.session_state.step == 1:
    st.subheader("👋 Welcome!")
    name = st.text_input("Enter your name:", key="name_input")
    
    if st.button("Continue"):
        if name.replace(" ", "").isalpha() and name.strip():
            st.session_state.name = name
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("❌ Please enter a valid name (letters only)")

# Step 2: Number inputs
elif st.session_state.step == 2:
    st.subheader(f"Hello, {st.session_state.name}! 👋")
    st.write("Enter your numbers below:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num1 = st.number_input("First number:", value=0.0, key="num1_input")
    
    with col2:
        num2 = st.number_input("Second number:", value=0.0, key="num2_input")
    
    num3 = st.number_input("Third number (optional):", value=None, key="num3_input")
    
    if st.button("Next"):
        st.session_state.num1 = num1
        st.session_state.num2 = num2
        st.session_state.num3 = num3
        st.session_state.step = 3
        st.rerun()

# Step 3: First operation
elif st.session_state.step == 3:
    st.subheader("Choose your operation")
    
    st.markdown(f"**Calculate:** `{st.session_state.num1}` ⚡ `{st.session_state.num2}`")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Add", use_container_width=True):
            st.session_state.operation1 = "add"
            st.session_state.step = 4
            st.rerun()
    
    with col2:
        if st.button("➖ Subtract", use_container_width=True):
            st.session_state.operation1 = "subtract"
            st.session_state.step = 4
            st.rerun()
    
    with col3:
        if st.button("✖️ Multiply", use_container_width=True):
            st.session_state.operation1 = "multiply"
            st.session_state.step = 4
            st.rerun()
    
    with col4:
        if st.button("➗ Divide", use_container_width=True):
            st.session_state.operation1 = "divide"
            st.session_state.step = 4
            st.rerun()

# Step 4: Show result and optional second operation
elif st.session_state.step == 4:
    # Calculate first result
    num1 = st.session_state.num1
    num2 = st.session_state.num2
    operation = st.session_state.operation1
    
    if operation == "add":
        result = num1 + num2
        op_symbol = "+"
    elif operation == "subtract":
        result = num1 - num2
        op_symbol = "-"
    elif operation == "multiply":
        result = num1 * num2
        op_symbol = "×"
    elif operation == "divide":
        if num2 == 0:
            st.error("❌ Cannot divide by zero!")
            result = 0
        else:
            result = num1 / num2
        op_symbol = "÷"
    
    st.session_state.result = result
    
    # Display result
    st.success(f"### Result: `{num1}` {op_symbol} `{num2}` = **{result}**")
    
    # If third number exists, offer second operation
    if st.session_state.num3 is not None:
        st.markdown("---")
        st.subheader("Continue with second operation?")
        st.markdown(f"**Calculate:** `{result}` ⚡ `{st.session_state.num3}`")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("➕ Add", key="add2", use_container_width=True):
                st.session_state.operation2 = "add"
                st.session_state.step = 5
                st.rerun()
        
        with col2:
            if st.button("➖ Subtract", key="sub2", use_container_width=True):
                st.session_state.operation2 = "subtract"
                st.session_state.step = 5
                st.rerun()
        
        with col3:
            if st.button("✖️ Multiply", key="mul2", use_container_width=True):
                st.session_state.operation2 = "multiply"
                st.session_state.step = 5
                st.rerun()
        
        with col4:
            if st.button("➗ Divide", key="div2", use_container_width=True):
                st.session_state.operation2 = "divide"
                st.session_state.step = 5
                st.rerun()
    
    st.markdown("---")
    if st.button("🔄 Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Step 5: Final result
elif st.session_state.step == 5:
    # Calculate second result
    result = st.session_state.result
    num3 = st.session_state.num3
    operation = st.session_state.operation2
    
    if operation == "add":
        final_result = result + num3
        op_symbol = "+"
    elif operation == "subtract":
        final_result = result - num3
        op_symbol = "-"
    elif operation == "multiply":
        final_result = result * num3
        op_symbol = "×"
    elif operation == "divide":
        if num3 == 0:
            st.error("❌ Cannot divide by zero!")
            final_result = result
        else:
            final_result = result / num3
        op_symbol = "÷"
    
    # Display calculation history
    st.success("### ✅ Calculation Complete!")
    
    # Get operation symbols for display
    if st.session_state.operation1 == "add":
        op1_symbol = "+"
    elif st.session_state.operation1 == "subtract":
        op1_symbol = "-"
    elif st.session_state.operation1 == "multiply":
        op1_symbol = "×"
    elif st.session_state.operation1 == "divide":
        op1_symbol = "÷"
    
    st.markdown(f"""
    <div class='result-box'>
        <h4 style='color: #333;'>First Operation:</h4>
        <p style='font-size:1.2rem; color: #000;'>{st.session_state.num1} {op1_symbol} {st.session_state.num2} = <b>{result}</b></p>
        <h4 style='color: #333;'>Second Operation:</h4>
        <p style='font-size:1.2rem; color: #000;'>{result} {op_symbol} {num3} = <b style='color:#4CAF50; font-size:1.5rem;'>{final_result}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.balloons()
    
    st.markdown("---")
    if st.button("🔄 Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Made with ❤️ using Streamlit</p>",
    unsafe_allow_html=True
)