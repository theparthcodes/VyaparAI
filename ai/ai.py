import datetime
import streamlit as st


def show_chatbot():

    st.markdown(
        """
        <style>
        .stTextArea textarea {
            background-color: #2b2b2b !important;
            color: #ffffff !important;
            font-family: 'Arial', sans-serif !important;
            font-size: 14px !important;
        }

        div[data-testid="stForm"] {
            background-color: #1e1e1e !important;
            border: 2px solid #4CAF50 !important;
            border-radius: 8px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("VyaparAI")

    # =====================================================
    # CHAT HISTORY
    # =====================================================

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = [

            "VyaparAI: Welcome! Type commands like "
            "'calculate gst' or 'check discount'.\n"
            "-------------------------------------------------------------\n"

        ]

    # =====================================================
    # DISPLAY CHAT
    # =====================================================

    chat_text_block = "\n".join(
        st.session_state.chat_history
    )

    st.text_area(
        label="Terminal Logs",
        value=chat_text_block,
        height=380,
        disabled=True,
        label_visibility="collapsed"
    )

    # =====================================================
    # CHATBOT LOGIC
    # =====================================================

    def answer_question(user_text):

        if user_text.strip() == "":

            return ""

        q = user_text.lower()

        bot_reply = ""

        words = q.split()

        numbers = []

        for w in words:

            clean_w = (
                w.replace(",", "")
                 .replace("₹", "")
            )

            try:

                numbers.append(float(clean_w))

            except ValueError:

                continue

        # =================================================
        # EXISTING TEAMMATE LOGIC
        # =================================================

        if "profit target" in q:

            if len(numbers) < 3:

                bot_reply = (
                    "Error: Please enter Cost Price, "
                    "Selling Price, and Target Profit."
                )

            else:

                cp = numbers[0]

                sp = numbers[1]

                target = numbers[2]

                margin = sp - cp

                if margin <= 0:

                    bot_reply = (
                        "Error: Selling price must "
                        "be higher than cost price."
                    )

                else:

                    total_units = (
                        int(target / margin) + 1
                    )

                    bot_reply = (
                        "You need to sell " +
                        str(total_units) +
                        " units to hit profit target."
                    )

        elif "pricing suggestion" in q:

            if len(numbers) < 1:

                bot_reply = (
                    "Error: Please supply "
                    "the product cost price."
                )

            else:

                item_cost = numbers[0]

                final_suggested = item_cost * 1.30

                bot_reply = (
                    "Suggested selling price is: Rs. " +
                    str(round(final_suggested, 2))
                )

        elif "loss recovery" in q:

            if len(numbers) < 2:

                bot_reply = (
                    "Error: Enter total loss "
                    "and profit per unit."
                )

            else:

                total_loss = numbers[0]

                unit_profit = numbers[1]

                if unit_profit <= 0:

                    bot_reply = (
                        "Error: Profit per unit "
                        "must be greater than zero."
                    )

                else:

                    required_units = (
                        int(total_loss / unit_profit) + 1
                    )

                    bot_reply = (
                        "You need to sell " +
                        str(required_units) +
                        " extra items to recover loss."
                    )

        elif "gst" in q:

            if len(numbers) < 2:

                bot_reply = (
                    "Error: Please supply "
                    "base amount and GST %."
                )

            else:

                base_val = numbers[0]

                gst_rate = numbers[1]

                tax_added = (
                    base_val +
                    (base_val * gst_rate / 100.0)
                )

                bot_reply = (
                    "Total price after GST is: Rs. " +
                    str(round(tax_added, 2))
                )

        elif "discount" in q:

            if len(numbers) < 2:

                bot_reply = (
                    "Error: Please enter amount "
                    "and discount %."
                )

            else:

                base_price = numbers[0]

                disc_rate = numbers[1]

                reduced_price = (
                    base_price -
                    (base_price * disc_rate / 100.0)
                )

                bot_reply = (
                    "Final price after discount is: Rs. " +
                    str(round(reduced_price, 2))
                )

        elif "stock" in q or "inventory" in q:

            bot_reply = (
                "Inventory Advice: Keep minimum "
                "safety stock and check weekly."
            )

        elif "hello" in q or "hi" in q:

            bot_reply = (
                "Hello! I am VyaparAI. "
                "Ask me a business math question."
            )

        elif "time" in q or "date" in q:

            bot_reply = (
                "Time: " +
                datetime.datetime.now().strftime(
                    "%d/%m/%Y %H:%M:%S"
                )
            )

        else:

            bot_reply = (
                "Query not recognized. "
                "Try typing 'gst' or 'discount'."
            )

        return bot_reply

    # =====================================================
    # INPUT FORM
    # =====================================================

    with st.form(
        "vyapar_panel",
        clear_on_submit=True
    ):

        col_input, col_btn = st.columns([5, 1])

        with col_input:

            user_input = st.text_input(
                "Input Field",
                placeholder=(
                    "Type 'calculate gst' or "
                    "'calculate discount'..."
                ),
                label_visibility="collapsed"
            )

        with col_btn:

            submitted = st.form_submit_button(
                "Send"
            )

        if submitted:

            if user_input.strip() != "":

                reply = answer_question(
                    user_input
                )

                st.session_state.chat_history.append(
                    "You: " + user_input
                )

                st.session_state.chat_history.append(
                    "VyaparAI: " + reply + "\n"
                )

                st.rerun()