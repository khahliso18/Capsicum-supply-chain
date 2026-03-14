import streamlit as st
import hashlib
from datetime import datetime
import qrcode
from io import BytesIO

st.set_page_config(page_title="Blockchain Supply Chain", layout="wide")

st.title("🌶️ Blockchain Supply Chain Explorer")
st.write("Simulation of a blockchain ledger for Capsicum traceability")

# Blockchain storage
if "blockchain" not in st.session_state:
    st.session_state.blockchain = []

# Hash function
def create_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

# QR generator
def generate_qr(data):
    qr = qrcode.make(data)
    buf = BytesIO()
    qr.save(buf)
    return buf.getvalue()

# Input form
st.subheader("Add Supply Chain Transaction")

col1, col2 = st.columns(2)

with col1:
    actor = st.text_input("Actor (Farmer, Transporter, Distributor)")
    activity = st.text_input("Activity (Harvested, Transported, Sold)")

with col2:
    product = st.text_input("Product Name", value="Capsicum")
    product_id = st.text_input("Product ID")

if st.button("➕ Add Block"):

    block_number = len(st.session_state.blockchain) + 1
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    prev_hash = "0"
    if st.session_state.blockchain:
        prev_hash = st.session_state.blockchain[-1]["hash"]

    data = f"{block_number}{actor}{activity}{product}{product_id}{timestamp}{prev_hash}"
    current_hash = create_hash(data)

    block = {
        "number": block_number,
        "actor": actor,
        "activity": activity,
        "product": product,
        "product_id": product_id,
        "timestamp": timestamp,
        "prev_hash": prev_hash,
        "hash": current_hash
    }

    st.session_state.blockchain.append(block)

# Display Blockchain
st.subheader("🔗 Blockchain Ledger")

for i, block in enumerate(st.session_state.blockchain):

    # Verify block
    data_check = f"{block['number']}{block['actor']}{block['activity']}{block['product']}{block['product_id']}{block['timestamp']}{block['prev_hash']}"
    recalculated_hash = create_hash(data_check)

    verified = recalculated_hash == block["hash"]

    color = "#d4edda" if verified else "#f8d7da"

    st.markdown(
        f"""
        <div style="
        background:{color};
        padding:20px;
        border-radius:10px;
        margin-bottom:10px;
        border:2px solid #444">

        <h4>Block {block['number']}</h4>

        <b>Actor:</b> {block['actor']} <br>
        <b>Activity:</b> {block['activity']} <br>
        <b>Product:</b> {block['product']} <br>
        <b>Product ID:</b> {block['product_id']} <br>
        <b>Timestamp:</b> {block['timestamp']} <br>

        <b>Previous Hash:</b><br>
        <small>{block['prev_hash']}</small><br>

        <b>Current Hash:</b><br>
        <small>{block['hash']}</small>

        </div>
        """,
        unsafe_allow_html=True
    )

    # QR Code
    qr = generate_qr(block["product_id"])
    st.image(qr, width=120, caption="Product QR Trace")

    # Arrow between blocks
    if i < len(st.session_state.blockchain) - 1:
        st.markdown(
            "<h2 style='text-align:center'>⬇️</h2>",
            unsafe_allow_html=True
        )
