import qrcode
from gtts import gTTS
import streamlit as st
from io import BytesIO
import uuid

# QR GENERATION FUNCTION
def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


# STREAMLIT UI
st.set_page_config(page_title="Metro Ticket Booking", page_icon="🚆")
st.title("🚆 Metro Ticket Booking System with QR Code + Auto Voice")

stations = ["Ameerpet", "Miyapur", "LB Nagar", "KPHB", "JNTU"]

name = st.text_input("Passenger Name")
source = st.selectbox("Source Station", stations)
destination = st.selectbox("Destination Station", stations)
no_tickets = st.number_input("Number of Tickets", min_value=1, value=1)

price_per_ticket = 30
total_amount = no_tickets * price_per_ticket
st.info(f"Total Amount: ₹{total_amount}")

# BOOKING BUTTON
if st.button("Book Ticket"):
    if name.strip() == "":
        st.error("Please enter passenger name.")
    elif source == destination:
        st.error("Source and Destination cannot be same.")
    else:
        booking_id = str(uuid.uuid4())[:8]

        qr_data = (
            f"Booking ID: {booking_id}\n"
            f"Name: {name}\n"
            f"From: {source}\n"
            f"To: {destination}\n"
            f"Tickets: {no_tickets}\n"
            f"Amount: ₹{total_amount}"
        )

        qr_img = generate_qr(qr_data)

        buf = BytesIO()
        qr_img.save(buf, format="PNG")
        qr_bytes = buf.getvalue()

        # Voice generation
        voice_text = f"Ticket booked successfully. {name}, your journey from {source} to {destination}. Total amount {total_amount} rupees."
        tts = gTTS(voice_text)
        audio_buf = BytesIO()
        tts.write_to_fp(audio_buf)
        audio_buf.seek(0)

        st.success("Ticket Booked Successfully!")
        st.subheader("🎫 Ticket Details")
        st.write(f"**Booking ID:** {booking_id}")
        st.write(f"**Passenger:** {name}")
        st.write(f"**From:** {source}")
        st.write(f"**To:** {destination}")
        st.write(f"**Tickets:** {no_tickets}")
        st.write(f"**Amount:** ₹{total_amount}")

        st.image(qr_bytes, width=250)
        st.audio(audio_buf, format="audio/mp3")
