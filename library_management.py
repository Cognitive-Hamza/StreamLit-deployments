import streamlit as st

# Function to check availability status
def check_availability(copies):
    match copies:
        case c if c >= 5:
            return "Highly Available", "🟢"
        case c if c >= 3:
            return "Available", "🟡"
        case c if c >= 1:
            return "Low Stock", "🟠"
        case _:
            return "Out of Stock", "🔴"

# Function to validate if string is a valid positive number
def validate_number(num_str):
    try:
        num = int(num_str)
        return num >= 0
    except:
        return False

# Function to find book by ID
def find_book(book_id, book_list):
    for book in book_list:
        if book['id'] == book_id:
            return book
    return None

# Initialize session state
if 'book_list' not in st.session_state:
    st.session_state.book_list = []
if 'used_ids' not in st.session_state:
    st.session_state.used_ids = set()

# Page configuration
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        padding: 20px;
        background: linear-gradient(90deg, #E3F2FD 0%, #BBDEFB 100%);
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .stat-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
    }
    .book-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📚 School Library Management System</div>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📋 Navigation")
menu = st.sidebar.radio(
    "Select Option:",
    ["🏠 Home", "➕ Add Book", "📖 View All Books", "🔍 Search Book", 
     "📤 Borrow Book", "📥 Return Book", "⚠️ Low Stock Books", "📊 Statistics"]
)

# HOME PAGE
if menu == "🏠 Home":
    st.subheader("Welcome to the Library Management System!")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_books = sum(book['copies'] for book in st.session_state.book_list)
        st.markdown(f"""
            <div class="stat-card">
                <h3 style="color: #1E88E5;">📚 Total Books</h3>
                <h1 style="color: #1E88E5;">{total_books}</h1>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_titles = len(st.session_state.book_list)
        st.markdown(f"""
            <div class="stat-card">
                <h3 style="color: #43A047;">📖 Total Titles</h3>
                <h1 style="color: #43A047;">{total_titles}</h1>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        available = sum(1 for book in st.session_state.book_list if book['copies'] > 0)
        st.markdown(f"""
            <div class="stat-card">
                <h3 style="color: #FB8C00;">✅ Available</h3>
                <h1 style="color: #FB8C00;">{available}</h1>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        low_stock = sum(1 for book in st.session_state.book_list if 1 <= book['copies'] <= 2)
        st.markdown(f"""
            <div class="stat-card">
                <h3 style="color: #E53935;">⚠️ Low Stock</h3>
                <h1 style="color: #E53935;">{low_stock}</h1>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("👈 Use the sidebar to navigate through different features!")
    
    if st.session_state.book_list:
        st.subheader("📋 Recent Books")
        recent_books = st.session_state.book_list[-3:][::-1]
        for book in recent_books:
            status, icon = check_availability(book['copies'])
            st.markdown(f"""
                <div class="book-card">
                    <b>{icon} {book['title']}</b> - ID: {book['id']} | Copies: {book['copies']} | Status: {status}
                </div>
            """, unsafe_allow_html=True)

# ADD BOOK
elif menu == "➕ Add Book":
    st.subheader("➕ Add New Book to Library")
    
    with st.form("add_book_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            book_id = st.text_input("📌 Book ID (numbers only)", placeholder="e.g., 101")
            title = st.text_input("📖 Book Title", placeholder="e.g., Python Basics")
        
        with col2:
            copies = st.number_input("📚 Number of Copies", min_value=0, value=1, step=1)
        
        submitted = st.form_submit_button("✅ Add Book", use_container_width=True)
        
        if submitted:
            # Validation
            if not book_id:
                st.error("❌ Book ID cannot be empty!")
            elif not book_id.isdigit():
                st.error("❌ Book ID must contain only numbers!")
            elif book_id in st.session_state.used_ids:
                st.error("❌ This Book ID already exists!")
            elif not title.strip():
                st.error("❌ Book title cannot be empty!")
            else:
                status, icon = check_availability(copies)
                
                book = {
                    'id': book_id,
                    'title': title.strip(),
                    'copies': copies,
                    'status': status
                }
                
                st.session_state.book_list.append(book)
                st.session_state.used_ids.add(book_id)
                
                st.success(f"✅ Book '{title}' added successfully!")
                st.balloons()

# VIEW ALL BOOKS
elif menu == "📖 View All Books":
    st.subheader("📖 All Books in Library")
    
    if not st.session_state.book_list:
        st.warning("📭 No books in the library yet. Add some books first!")
    else:
        # Search and filter
        search_term = st.text_input("🔍 Search by Title or ID", placeholder="Type to search...")
        
        filtered_books = st.session_state.book_list
        if search_term:
            filtered_books = [
                book for book in st.session_state.book_list 
                if search_term.lower() in book['title'].lower() or search_term in book['id']
            ]
        
        # Display books in cards
        for book in filtered_books:
            status, icon = check_availability(book['copies'])
            
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### {icon} {book['title']}")
                st.caption(f"Book ID: {book['id']}")
            
            with col2:
                st.metric("Copies Available", book['copies'])
            
            with col3:
                st.markdown(f"**{status}**")
            
            st.markdown("---")
        
        if not filtered_books and search_term:
            st.info("🔍 No books found matching your search.")

# SEARCH BOOK
elif menu == "🔍 Search Book":
    st.subheader("🔍 Search Book by ID")
    
    search_id = st.text_input("Enter Book ID", placeholder="e.g., 101")
    
    if st.button("🔍 Search", use_container_width=True):
        if not search_id:
            st.warning("⚠️ Please enter a Book ID!")
        else:
            found = find_book(search_id, st.session_state.book_list)
            
            if found:
                st.success("✅ Book Found!")
                status, icon = check_availability(found['copies'])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                        <div class="book-card">
                            <h3>{icon} {found['title']}</h3>
                            <p><b>Book ID:</b> {found['id']}</p>
                            <p><b>Copies Available:</b> {found['copies']}</p>
                            <p><b>Status:</b> {status}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if found['copies'] > 0:
                        st.success("✅ This book is available for borrowing!")
                    else:
                        st.error("❌ This book is currently out of stock!")
            else:
                st.error("❌ Book not found with this ID!")

# BORROW BOOK
elif menu == "📤 Borrow Book":
    st.subheader("📤 Borrow a Book")
    
    if not st.session_state.book_list:
        st.warning("📭 No books available in the library!")
    else:
        # Show available books
        available_books = [book for book in st.session_state.book_list if book['copies'] > 0]
        
        if not available_books:
            st.error("❌ No books are currently available for borrowing!")
        else:
            book_options = {f"{book['id']} - {book['title']} ({book['copies']} copies)": book['id'] 
                          for book in available_books}
            
            selected = st.selectbox("Select Book to Borrow:", list(book_options.keys()))
            
            if st.button("📤 Borrow Book", use_container_width=True):
                borrow_id = book_options[selected]
                found = find_book(borrow_id, st.session_state.book_list)
                
                if found and found['copies'] > 0:
                    found['copies'] -= 1
                    found['status'], _ = check_availability(found['copies'])
                    st.success(f"✅ Book '{found['title']}' borrowed successfully!")
                    st.info(f"📚 Remaining copies: {found['copies']}")
                    st.balloons()
                else:
                    st.error("❌ This book is out of stock!")

# RETURN BOOK
elif menu == "📥 Return Book":
    st.subheader("📥 Return a Book")
    
    if not st.session_state.book_list:
        st.warning("📭 No books in the library!")
    else:
        book_options = {f"{book['id']} - {book['title']}": book['id'] 
                      for book in st.session_state.book_list}
        
        selected = st.selectbox("Select Book to Return:", list(book_options.keys()))
        
        if st.button("📥 Return Book", use_container_width=True):
            return_id = book_options[selected]
            found = find_book(return_id, st.session_state.book_list)
            
            if found:
                found['copies'] += 1
                found['status'], _ = check_availability(found['copies'])
                st.success(f"✅ Book '{found['title']}' returned successfully!")
                st.info(f"📚 Total copies now: {found['copies']}")
                st.balloons()

# LOW STOCK BOOKS
elif menu == "⚠️ Low Stock Books":
    st.subheader("⚠️ Low Stock Books (1-2 copies)")
    
    low_stock_books = [book for book in st.session_state.book_list 
                       if 1 <= book['copies'] <= 2]
    
    if not low_stock_books:
        st.success("✅ No books are low in stock!")
    else:
        st.warning(f"⚠️ Found {len(low_stock_books)} book(s) with low stock!")
        
        for book in low_stock_books:
            status, icon = check_availability(book['copies'])
            st.markdown(f"""
                <div class="book-card">
                    <h4>{icon} {book['title']}</h4>
                    <p><b>Book ID:</b> {book['id']}</p>
                    <p><b>Copies:</b> {book['copies']}</p>
                    <p style="color: #E53935;"><b>⚠️ Low Stock Alert!</b></p>
                </div>
            """, unsafe_allow_html=True)

# STATISTICS
elif menu == "📊 Statistics":
    st.subheader("📊 Library Statistics")
    
    if not st.session_state.book_list:
        st.warning("📭 No data available yet!")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Book Status Distribution")
            status_count = {
                "Highly Available": 0,
                "Available": 0,
                "Low Stock": 0,
                "Out of Stock": 0
            }
            
            for book in st.session_state.book_list:
                status_count[book['status']] += 1
            
            for status, count in status_count.items():
                st.metric(status, count)
        
        with col2:
            st.markdown("### 📚 Top 5 Books by Copies")
            sorted_books = sorted(st.session_state.book_list, 
                                key=lambda x: x['copies'], reverse=True)[:5]
            
            for i, book in enumerate(sorted_books, 1):
                st.markdown(f"**{i}. {book['title']}** - {book['copies']} copies")
        
        st.markdown("---")
        
        total_books = sum(book['copies'] for book in st.session_state.book_list)
        avg_copies = total_books / len(st.session_state.book_list) if st.session_state.book_list else 0
        
        col3, col4, col5 = st.columns(3)
        
        with col3:
            st.metric("📚 Total Books", total_books)
        
        with col4:
            st.metric("📖 Total Titles", len(st.session_state.book_list))
        
        with col5:
            st.metric("📊 Avg Copies/Title", f"{avg_copies:.1f}")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>📚 School Library Management System | Built with Streamlit</p>
    </div>
""", unsafe_allow_html=True)
