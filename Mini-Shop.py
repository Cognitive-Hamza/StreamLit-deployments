import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Student Mini-Shop",
    page_icon="🛍️",
    layout="wide"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-weight: bold;
        font-size: 16px;
    }
    .item-card {
        background: white !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
        border-left: 5px solid;
    }
    .item-card h3 {
        margin: 0 !important;
        color: #000000 !important;
        text-shadow: none !important;
        display: block !important;
        visibility: visible !important;
    }
    .item-card p {
        margin: 5px 0 0 0 !important;
        color: #000000 !important;
        font-size: 1.1em;
        text-shadow: none !important;
        font-weight: 600 !important;
        display: block !important;
        visibility: visible !important;
    }
    .item-card * {
        color: #000000 !important;
    }
    .success-box {
        background: #d4edda;
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    .error-box {
        background: #f8d7da;
        border: 2px solid #dc3545;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        animation: shake 0.5s;
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    .budget-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }
    .budget-card h2, .budget-card h3 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .cart-item {
        background: #ffffff !important;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    .cart-item h4 {
        color: #000000 !important;
        margin: 0;
        text-shadow: none !important;
    }
    .cart-item p {
        color: #333333 !important;
        margin: 5px 0 0 0;
        text-shadow: none !important;
    }
    .cart-item * {
        color: #000000 !important;
    }
    h1 {
        color: #ffffff !important;
        text-align: center;
        font-size: 3em !important;
        margin-bottom: 10px !important;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.8), -2px -2px 4px rgba(255,255,255,0.5);
        font-weight: bold;
    }
    .subtitle {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        font-weight: 500;
    }
    h2, h3 {
        color: #667eea !important;
    }
    .stMarkdown h2, .stMarkdown h3 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
    }
    .section-header {
        background: rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .section-header h2 {
        margin: 0 !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'budget' not in st.session_state:
    st.session_state.budget = 0
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'error_message' not in st.session_state:
    st.session_state.error_message = ""
if 'show_receipt' not in st.session_state:
    st.session_state.show_receipt = False

# Shop items
shop_items = {
    1: {"name": "Pencil", "price": 10, "emoji": "✏️", "color": "#ffc107"},
    2: {"name": "Eraser", "price": 5, "emoji": "🧹", "color": "#e91e63"},
    3: {"name": "Notebook", "price": 25, "emoji": "📓", "color": "#2196f3"},
    4: {"name": "Juice", "price": 30, "emoji": "🧃", "color": "#ff9800"},
    5: {"name": "Sandwich", "price": 50, "emoji": "🥪", "color": "#4caf50"}
}

def calculate_total():
    return sum(item['price'] for item in st.session_state.cart)

def add_to_cart(item_id):
    item = shop_items[item_id]
    
    if st.session_state.budget == 0:
        st.session_state.error_message = "⚠️ Please set your budget first!"
        return
    
    new_total = calculate_total() + item['price']
    if new_total > st.session_state.budget:
        shortage = new_total - st.session_state.budget
        st.session_state.error_message = f"⚠️ Budget exceeded! Cannot add {item['name']}. You need Rs. {shortage} more."
        return
    
    st.session_state.cart.append(item.copy())
    st.session_state.error_message = ""

def get_cart_summary():
    """Returns cart items with quantities"""
    from collections import Counter
    item_counts = Counter(item['name'] for item in st.session_state.cart)
    summary = []
    for item_name, count in item_counts.items():
        item_data = next(item for item in st.session_state.cart if item['name'] == item_name)
        summary.append({
            'name': item_name,
            'emoji': item_data['emoji'],
            'price': item_data['price'],
            'quantity': count,
            'total': item_data['price'] * count
        })
    return summary

def remove_from_cart(item_name):
    """Remove one instance of an item from cart"""
    for idx, item in enumerate(st.session_state.cart):
        if item['name'] == item_name:
            st.session_state.cart.pop(idx)
            break

def generate_receipt():
    if len(st.session_state.cart) == 0:
        st.session_state.error_message = "⚠️ Your cart is empty! Please add items first."
        return
    
    st.session_state.show_receipt = True
    st.session_state.error_message = ""

def download_receipt():
    total = calculate_total()
    remaining = st.session_state.budget - total
    cart_summary = get_cart_summary()
    
    receipt_text = "STUDENT MINI-SHOP RECEIPT\n"
    receipt_text += "═" * 40 + "\n\n"
    receipt_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    receipt_text += "Purchased Items:\n"
    
    for idx, item in enumerate(cart_summary, 1):
        receipt_text += f"{idx}. {item['name']} x{item['quantity']} - Rs. {item['price']} each = Rs. {item['total']}\n"
    
    receipt_text += "\n" + "─" * 40 + "\n"
    receipt_text += f"Total: Rs. {total}\n"
    receipt_text += f"Budget: Rs. {st.session_state.budget}\n"
    receipt_text += f"Balance: Rs. {remaining}\n\n"
    receipt_text += f"Total Items: {len(st.session_state.cart)}\n"
    receipt_text += f"Different Items: {len(cart_summary)}\n"
    receipt_text += "\nThank you for shopping with us!\n"
    
    return receipt_text

# Header
st.markdown("<h1>🛍️ Student Mini-Shop</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle' style='text-align: center; font-size: 1.2em;'>Shop within your budget and download receipts!</p>", unsafe_allow_html=True)

# Error message display
if st.session_state.error_message:
    st.markdown(f"""
    <div class="error-box">
        <h3 style="color: #dc3545 !important; margin: 0;">❌ Error!</h3>
        <p style="margin: 5px 0 0 0; color: #721c24;">{st.session_state.error_message}</p>
    </div>
    """, unsafe_allow_html=True)

# Budget Section
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div class="section-header">
        <h2>💰 Set Your Budget</h2>
    </div>
    """, unsafe_allow_html=True)
    budget_input = st.number_input("Enter amount", min_value=0, value=0, step=10, label_visibility="collapsed")
    
    if st.button("Set Budget", type="primary"):
        if budget_input > 0:
            st.session_state.budget = budget_input
            st.session_state.error_message = ""
            st.success(f"✅ Budget set to Rs. {budget_input}")
        else:
            st.session_state.error_message = "⚠️ Please enter a valid budget amount!"

# Display current budget
if st.session_state.budget > 0:
    remaining = st.session_state.budget - calculate_total()
    st.markdown(f"""
    <div class="budget-card">
        <h2 style="color: white !important; margin: 0;">Total Budget: Rs. {st.session_state.budget}</h2>
        <h3 style="color: {'#90EE90' if remaining >= 0 else '#FFB6C1'} !important; margin: 10px 0 0 0;">
            Remaining: Rs. {remaining}
        </h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main content - Shop Items and Cart
col_left, col_right = st.columns(2)

# Left Column - Shop Items
with col_left:
    st.markdown("""
    <div class="section-header">
        <h2>🛒 Available Items</h2>
    </div>
    """, unsafe_allow_html=True)
    
    for item_id, item in shop_items.items():
        col_item, col_button = st.columns([3, 1])
        
        with col_item:
            st.markdown(f"""
            <div class="item-card" style="border-left-color: {item['color']}; background-color: white !important;">
                <h3 style="color: #000000 !important; margin: 0; display: block; visibility: visible; font-size: 1.3em;">
                    <span style="font-size: 1.5em;">{item['emoji']}</span> <span style="color: #000000 !important;">{item['name']}</span>
                </h3>
                <p style="color: #000000 !important; margin: 5px 0 0 0; font-weight: 700; display: block; visibility: visible; font-size: 1.2em;">
                    Rs. {item['price']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_button:
            st.write("")
            st.write("")
            if st.button("➕", key=f"add_{item_id}"):
                add_to_cart(item_id)
                st.rerun()

# Right Column - Cart
with col_right:
    st.markdown("""
    <div class="section-header">
        <h2>🛍️ Your Cart</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.cart) == 0:
        st.markdown("""
        <div style="text-align: center; padding: 60px 20px; color: #ccc;">
            <h2 style="color: #ccc !important;">🛒</h2>
            <p>Your cart is empty</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        cart_summary = get_cart_summary()
        
        for item in cart_summary:
            col_cart_item, col_remove = st.columns([4, 1])
            
            with col_cart_item:
                quantity_text = f" x{item['quantity']}" if item['quantity'] > 1 else ""
                st.markdown(f"""
                <div class="cart-item">
                    <h4>{item['emoji']} {item['name']}{quantity_text}</h4>
                    <p>Rs. {item['price']} each | Total: Rs. {item['total']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_remove:
                st.write("")
                if st.button("🗑️", key=f"remove_{item['name']}"):
                    remove_from_cart(item['name'])
                    st.rerun()
        
        # Total and Generate Receipt
        total = calculate_total()
        st.markdown(f"""
        <div style="background: #ffffff !important; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="text-align: center; color: #000000 !important; margin: 0;">Total: Rs. {total}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📄 Generate Receipt", type="primary", use_container_width=True):
            generate_receipt()
            st.rerun()

# Receipt Modal
if st.session_state.show_receipt:
    st.markdown("---")
    st.markdown("""
    <div class="section-header">
        <h2>✅ Receipt Generated Successfully!</h2>
    </div>
    """, unsafe_allow_html=True)
    
    total = calculate_total()
    remaining = st.session_state.budget - total
    cart_summary = get_cart_summary()
    
    st.markdown("""
    <div class="success-box">
        <h3 style="color: #155724 !important; margin: 0 0 15px 0;">Purchase Successful! 🎉</h3>
    """, unsafe_allow_html=True)
    
    st.markdown("**Purchased Items:**")
    for idx, item in enumerate(cart_summary, 1):
        st.write(f"{idx}. {item['name']} x{item['quantity']} - Rs. {item['price']} each = Rs. {item['total']}")
    
    st.markdown("---")
    st.markdown(f"**Total Items:** {len(st.session_state.cart)}")
    st.markdown(f"**Different Items:** {len(cart_summary)}")
    st.markdown(f"**Total Amount:** Rs. {total}")
    st.markdown(f"**Budget:** Rs. {st.session_state.budget}")
    st.markdown(f"**Balance:** Rs. {remaining}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Download button
    receipt_content = download_receipt()
    st.download_button(
        label="📥 Download Receipt",
        data=receipt_content,
        file_name=f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        type="primary",
        use_container_width=True
    )
    
    col_reset1, col_reset2 = st.columns(2)
    with col_reset1:
        if st.button("🔄 New Shopping", use_container_width=True):
            st.session_state.cart = []
            st.session_state.show_receipt = False
            st.rerun()
    
    with col_reset2:
        if st.button("❌ Close Receipt", use_container_width=True):
            st.session_state.show_receipt = False
            st.rerun()

# Footer
st.markdown("---")
st.markdown("<p class='subtitle' style='text-align: center;'>Made with ❤️ for Students</p>", unsafe_allow_html=True)