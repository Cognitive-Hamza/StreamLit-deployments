import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Fast Food Ordering System",
    page_icon="🍔",
    layout="wide"
)

# Custom CSS for beautiful styling that works in both light and dark mode
st.markdown("""
    <style>
    /* Main button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #ff6b35 0%, #ff4757 100%);
        color: white !important;
        border: none;
        padding: 15px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 18px;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 25px rgba(255, 71, 87, 0.4);
    }
    
    /* Menu card styling - adapts to theme */
    .menu-card {
        background: color-mix(in srgb, var(--background-color) 95%, var(--text-color) 5%);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 1px solid color-mix(in srgb, var(--background-color) 80%, var(--text-color) 20%);
        margin: 10px 0;
        transition: all 0.3s;
    }
    .menu-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(255, 107, 53, 0.2);
        border-color: #ff6b35;
    }
    
    /* Price tag */
    .price-tag {
        color: #ff6b35;
        font-size: 24px;
        font-weight: bold;
    }
    
    /* Total box */
    .total-box {
        background: linear-gradient(135deg, #ff6b35 0%, #ff4757 100%);
        color: white !important;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3);
    }
    
    /* Receipt box - adapts to theme */
    .receipt-box {
        background: color-mix(in srgb, var(--background-color) 98%, var(--text-color) 2%);
        padding: 30px;
        border-radius: 20px;
        border: 3px dashed #ff6b35;
        box-shadow: 0 10px 30px rgba(255, 107, 53, 0.2);
    }
    
    /* Welcome box - adapts to theme */
    .welcome-box {
        background: color-mix(in srgb, var(--background-color) 95%, var(--text-color) 5%);
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 10px 30px rgba(255, 107, 53, 0.15);
        border: 2px solid color-mix(in srgb, var(--background-color) 85%, var(--text-color) 15%);
        margin-top: 50px;
    }
    
    /* Header card - adapts to theme */
    .header-card {
        background: color-mix(in srgb, var(--background-color) 95%, var(--text-color) 5%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 1px solid color-mix(in srgb, var(--background-color) 80%, var(--text-color) 20%);
    }
    
    /* Cart badge */
    .cart-badge {
        background: linear-gradient(135deg, #ff6b35 0%, #ff4757 100%);
        color: white !important;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(255, 107, 53, 0.3);
    }
    
    /* Subtotal box */
    .subtotal-box {
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.15) 0%, rgba(255, 71, 87, 0.15) 100%);
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin-top: 10px;
        border: 1px solid rgba(255, 107, 53, 0.3);
    }
    
    /* Summary box */
    .summary-box {
        background: color-mix(in srgb, var(--background-color) 95%, var(--text-color) 5%);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 1px solid color-mix(in srgb, var(--background-color) 80%, var(--text-color) 20%);
    }
    
    /* Title colors that adapt */
    .primary-title {
        color: #ff4757;
        text-align: center;
        font-size: 60px;
        text-shadow: 0 2px 10px rgba(255, 71, 87, 0.2);
    }
    
    .secondary-title {
        color: #ff6b35;
    }
    
    /* Text input styling */
    .stTextInput input {
        border-radius: 10px;
        border: 2px solid color-mix(in srgb, var(--background-color) 70%, var(--text-color) 30%);
        padding: 12px;
    }
    .stTextInput input:focus {
        border-color: #ff6b35 !important;
        box-shadow: 0 0 0 2px rgba(255, 107, 53, 0.2);
    }
    
    /* Divider line */
    .divider {
        border: 1px dashed color-mix(in srgb, var(--background-color) 60%, var(--text-color) 40%);
        margin: 20px 0;
    }
    
    .divider-bold {
        border: 2px solid #ff6b35;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'name_submitted' not in st.session_state:
    st.session_state.name_submitted = False
if 'customer_name' not in st.session_state:
    st.session_state.customer_name = ""
if 'cart' not in st.session_state:
    st.session_state.cart = {
        'tikka': 0,
        'burger': 0,
        'club_sandwich': 0,
        'broast': 0
    }
if 'show_receipt' not in st.session_state:
    st.session_state.show_receipt = False

# Menu items configuration
menu_items = {
    'tikka': {'name': 'Tikka', 'price': 300, 'emoji': '🍖'},
    'burger': {'name': 'Burger', 'price': 400, 'emoji': '🍔'},
    'club_sandwich': {'name': 'Club Sandwich', 'price': 450, 'emoji': '🥪'},
    'broast': {'name': 'Broast', 'price': 550, 'emoji': '🍗'}
}

def validate_name(name):
    return name != "" and name.replace(" ", "").isalpha()

def calculate_total():
    total = 0
    for item_id, quantity in st.session_state.cart.items():
        total += quantity * menu_items[item_id]['price']
    return total

def get_total_items():
    return sum(st.session_state.cart.values())

# Main App Logic
if not st.session_state.name_submitted:
    # Welcome Screen
    st.markdown("<h1 class='primary-title'>🍔 Fast Food Ordering System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; opacity: 0.7;'>Welcome! Please enter your name to start ordering</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='welcome-box'>", unsafe_allow_html=True)
        
        name_input = st.text_input("👤 Enter Your Name", placeholder="John Doe", key="name_input")
        st.caption("Letters only, no numbers or special characters")
        
        if st.button("🚀 Start Ordering"):
            if validate_name(name_input):
                st.session_state.customer_name = name_input
                st.session_state.name_submitted = True
                st.rerun()
            else:
                st.error("❌ Invalid name! Name must contain letters only and cannot be empty.")
        
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.show_receipt:
    # Receipt Screen
    st.markdown("<h1 class='primary-title'>🧾 RECEIPT</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("<div class='receipt-box'>", unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='opacity: 0.7;'>Customer Name:</h3>", unsafe_allow_html=True)
        st.markdown(f"<h2>{st.session_state.customer_name}</h2>", unsafe_allow_html=True)
        
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("<h3 style='opacity: 0.7;'>Items Ordered:</h3>", unsafe_allow_html=True)
        
        for item_id, quantity in st.session_state.cart.items():
            if quantity > 0:
                item = menu_items[item_id]
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"<p style='font-size: 18px;'>{item['emoji']} {item['name']} x {quantity}</p>", unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"<p style='font-size: 18px; text-align: right; font-weight: bold;'>Rs {quantity * item['price']}</p>", unsafe_allow_html=True)
        
        st.markdown("<hr class='divider-bold'>", unsafe_allow_html=True)
        
        col_x, col_y = st.columns([2, 1])
        with col_x:
            st.markdown("<h2>Total Bill:</h2>", unsafe_allow_html=True)
        with col_y:
            st.markdown(f"<h2 class='secondary-title' style='text-align: right;'>Rs {calculate_total()}</h2>", unsafe_allow_html=True)
        
        st.markdown("<p style='text-align: center; font-size: 20px; margin-top: 30px; color: #ff6b35;'>🎉 Thank you for ordering! 🎉</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔄 Place New Order"):
            st.session_state.name_submitted = False
            st.session_state.customer_name = ""
            st.session_state.cart = {'tikka': 0, 'burger': 0, 'club_sandwich': 0, 'broast': 0}
            st.session_state.show_receipt = False
            st.rerun()

else:
    # Ordering Screen
    # Header
    st.markdown("<h1 class='primary-title'>🍔 Fast Food Ordering System</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"<div class='header-card'><h3>👤 Welcome, {st.session_state.customer_name}!</h3></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='cart-badge'><h3 style='color: white; margin: 0;'>🛒 Cart: {get_total_items()} items</h3></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Menu Section
    st.markdown("<h2 class='secondary-title'>📋 Menu</h2>", unsafe_allow_html=True)
    
    # Display menu items in a 2x2 grid
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    columns = [row1_col1, row1_col2, row2_col1, row2_col2]
    
    for idx, (item_id, item) in enumerate(menu_items.items()):
        with columns[idx]:
            st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
            
            st.markdown(f"<h2>{item['emoji']} {item['name']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p class='price-tag'>Rs {item['price']}</p>", unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            
            with col_a:
                if st.button("➖", key=f"minus_{item_id}", disabled=st.session_state.cart[item_id] == 0):
                    st.session_state.cart[item_id] -= 1
                    st.rerun()
            
            with col_b:
                st.markdown(f"<h1 style='text-align: center;'>{st.session_state.cart[item_id]}</h1>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; opacity: 0.6; font-size: 12px;'>of 10 max</p>", unsafe_allow_html=True)
            
            with col_c:
                if st.button("➕", key=f"plus_{item_id}", disabled=st.session_state.cart[item_id] == 10):
                    if st.session_state.cart[item_id] < 10:
                        st.session_state.cart[item_id] += 1
                        st.rerun()
                    else:
                        st.warning(f"Cannot order more than 10 {item['name']} in total.")
            
            if st.session_state.cart[item_id] > 0:
                subtotal = st.session_state.cart[item_id] * item['price']
                st.markdown(f"<div class='subtotal-box'><p style='font-weight: bold; margin: 0;'>Subtotal: Rs {subtotal}</p></div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Order Summary
    st.markdown("<h2 class='secondary-title'>🛒 Order Summary</h2>", unsafe_allow_html=True)
    
    if get_total_items() == 0:
        st.info("Your cart is empty. Add items from the menu above!")
    else:
        st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
        
        for item_id, quantity in st.session_state.cart.items():
            if quantity > 0:
                item = menu_items[item_id]
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"<p style='font-size: 18px;'>{item['emoji']} {item['name']} x {quantity}</p>", unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"<p style='font-size: 18px; text-align: right; font-weight: bold;'>Rs {quantity * item['price']}</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='total-box'><h1 style='color: white; margin: 0;'>Grand Total: Rs {calculate_total()}</h1></div>", unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🗑️ Clear Cart"):
                st.session_state.cart = {'tikka': 0, 'burger': 0, 'club_sandwich': 0, 'broast': 0}
                st.rerun()
        with col_btn2:
            if st.button("✅ Finish Order"):
                st.session_state.show_receipt = True
                st.rerun()
