import streamlit as st
from openai import OpenAI
import json
import os
import base64
import io
import tempfile
from bs4 import BeautifulSoup
from pypdf import PdfReader
from fpdf import FPDF
import streamlit.components.v1 as components

# Simple CSS styling
def load_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-align: center;
        color: #333;
    }

    .section-header {
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        color: #333;
    }

    .chatbot-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #e0e0e0;
    }

    .chat-message {
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
    }

    .chat-message.user {
        background: #007bff;
        color: white;
        margin-left: auto;
        margin-right: 0;
        text-align: right;
    }

    .chat-message.bot {
        background: #e9ecef;
        color: #333;
        margin-left: 0;
        margin-right: auto;
    }

    .status-success {
        background: #28a745;
        color: white;
        padding: 8px 12px;
        border-radius: 5px;
        margin: 5px 0;
        text-align: center;
    }

    .status-error {
        background: #dc3545;
        color: white;
        padding: 8px 12px;
        border-radius: 5px;
        margin: 5px 0;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)



st.set_page_config(
    page_title="Universal AI Chatbot (Multimodal)",
    layout="wide",
    page_icon="🤖",
    initial_sidebar_state="expanded"
)

# Load CSS
load_css()

# Title
st.markdown('<h1 class="main-header">🎯 Universal AI Chatbot (Multimodal)</h1>', unsafe_allow_html=True)

# Simple Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    openai_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password")

    models = {
        "Text/Vision": st.sidebar.selectbox("🧠 Text/Vision Model", ["gpt-4o", "gpt-4o-mini"], key="tv_model"),
        "STT": "whisper-1",
        "TTS": "gpt-4o-mini-tts",
        "Image Generation": st.sidebar.selectbox("🎨 Image Model", ["dall-e-3", "gpt-image-1"], key="img_model")
    }

    if not openai_key:
        st.markdown('<div class="status-error">❌ Please provide OpenAI API Key</div>', unsafe_allow_html=True)
        st.stop()


# Enhanced Business Profile Setup with improved styling
st.markdown('<h2 class="section-header">🏢 Business Profile Setup</h2>', unsafe_allow_html=True)

with st.container():
    st.markdown("""
    <div class="chatbot-container">
        <p style="font-size: 16px; margin-bottom: 20px; color: #6c757d;">
            Configure your chatbot's business profile and industry-specific settings.
        </p>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data
def load_industries():
    try:
        with open("docs/chatbot_industry_requirements.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')[1:]  # skip header
        industries = []
        for row in rows:
            cols = [col.text.strip() for col in row.find_all('td')]
            if len(cols) >= 1:
                industries.append(cols[0])
        return sorted(set(industries))  # remove duplicates and sort
    except Exception:
        return ["Finance", "Healthcare", "Technology", "Other"]

industries_list = load_industries()

col1, col2 = st.columns([2, 1])

with col1:
    industry = st.selectbox("🏢 Select Industry", industries_list, help="Choose the industry for your business")

with col2:
    st.write("")  # Spacing
    if industry:
        st.markdown(f'<div class="status-success">✅ Selected: {industry}</div>', unsafe_allow_html=True)

if industry:
    with st.expander("💡 Suggested Self-Service Use Cases", expanded=True):
        st.write("**Recommended use cases for this industry:**")
        industry_data_partial = {}
        try:
            with open("docs/chatbot_industry_requirements.html", "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, 'html.parser')
            table = soup.find('table')
            rows = table.find_all('tr')[1:]
            for row in rows:
                cols = [col.text.strip() for col in row.find_all('td')]
                if len(cols) >= 12 and cols[0] == industry:
                    product_universe = cols[11].split(', ') if cols[11] else []
                    if product_universe:
                        for case in product_universe:
                            st.markdown(f"• {case}", unsafe_allow_html=True)
                    else:
                        st.markdown("• General inquiries and support", unsafe_allow_html=True)
                    break
        except Exception:
            st.markdown("• General inquiries and support", unsafe_allow_html=True)

# Enhanced internal knowledge base upload
st.markdown('<h3 class="section-header">📚 Internal Knowledge Base</h3>', unsafe_allow_html=True)

uploaded_pdf = st.file_uploader(
    "📄 Upload internal knowledge PDF (optional)",
    type=["pdf"],
    help="Upload a PDF with your internal knowledge base"
)

if uploaded_pdf:
    try:
        reader = PdfReader(uploaded_pdf)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text() + "\n"
        st.session_state.pdf_text = pdf_text
        st.markdown('<div class="status-success">✅ PDF uploaded and processed successfully!</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="status-error">❌ Error processing PDF: {e}</div>', unsafe_allow_html=True)

# Generate and edit business profile
if st.button("🚀 Generate Business Profile", help="Generate a business profile based on the selected industry"):
    try:
        with open("docs/chatbot_industry_requirements.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')[1:]  # skip header
        industry_data = {}
        for row in rows:
            cols = [col.text.strip() for col in row.find_all('td')]
            if len(cols) == 14:
                ind = cols[0]
                industry_data[ind] = {
                    "projected_monthly_chat_volume": cols[1],
                    "must_haves": cols[2],
                    "firm_name": cols[3],
                    "assistant_name": cols[4],
                    "address": cols[5],
                    "phones": {"main": cols[6]},
                    "website": cols[7],
                    "business_hours_local": cols[8],
                    "tone": cols[9],
                    "disclaimer_text": cols[10],
                    "product_universe": cols[11].split(', ') if cols[11] else [],
                    "additional_knowledge_articles": cols[12],
                    "other_additional_info": cols[13]
                }
        if industry in industry_data:
            business_profile = industry_data[industry]
        else:
            business_profile = {"firm_name": "Generic Firm"}
    except Exception as e:
        st.error(f"Error loading industry data: {e}")
        business_profile = {"firm_name": "Generic Firm"}
    st.session_state.business_profile = business_profile
    st.markdown('<div class="status-success">✅ Business profile generated successfully!</div>', unsafe_allow_html=True)

with st.expander("📋 Business Profile Preview", expanded=False):
    if 'business_profile' in st.session_state:
        st.json(st.session_state.business_profile)
    else:
        st.info("💡 Generate a business profile first to see the preview")

if st.button("✏️ Edit Business Profile", key="edit_profile", help="Edit the generated business profile"):
    st.session_state.editing = True

if 'editing' in st.session_state and st.session_state.editing and 'business_profile' in st.session_state:
    st.markdown('<h3 class="section-header">📝 Edit Business Profile</h3>', unsafe_allow_html=True)

    with st.form("edit_business_form"):
        st.markdown("### 📊 Company Information")
        cols1, cols2 = st.columns(2)
        with cols1:
            firm_name = st.text_input("🏢 Firm Name", value=st.session_state.business_profile.get('firm_name', ''))
            assistant_name = st.text_input("🤖 Assistant Name", value=st.session_state.business_profile.get('assistant_name', ''))
            address = st.text_input("📍 Address", value=st.session_state.business_profile.get('address', ''))
            main_phone = st.text_input("📞 Main Phone", value=st.session_state.business_profile.get('phones', {}).get('main', ''))
        with cols2:
            website = st.text_input("🌐 Website", value=st.session_state.business_profile.get('website', ''))
            business_hours = st.text_input("🕒 Business Hours", value=st.session_state.business_profile.get('business_hours_local', ''))
            tone = st.text_input("💬 Tone", value=st.session_state.business_profile.get('tone', ''))

        st.markdown("### 📄 Content & Policies")
        col1, col2 = st.columns(2)
        with col1:
            disclaimer = st.text_area("⚠️ Disclaimer Text", value=st.session_state.business_profile.get('disclaimer_text', ''), height=100)
            knowledge_articles = st.text_input("📚 Knowledge Articles", value=st.session_state.business_profile.get('additional_knowledge_articles', ''))
        with col2:
            product_universe = st.text_area("🛍️ Product Universe (comma-separated)", value=", ".join(st.session_state.business_profile.get('product_universe', [])), height=80)
            other_info = st.text_area("ℹ️ Other Additional Info", value=st.session_state.business_profile.get('other_additional_info', ''), height=80)

        # Include hidden ones
        projected_vol = st.session_state.business_profile.get('projected_monthly_chat_volume', '')
        must_haves = st.session_state.business_profile.get('must_haves', '')

        submitted = st.form_submit_button("💾 Save Changes")
        if submitted:
            # Update
            st.session_state.business_profile = {
                "projected_monthly_chat_volume": projected_vol,
                "must_haves": must_haves,
                "firm_name": firm_name,
                "assistant_name": assistant_name,
                "address": address,
                "phones": {"main": main_phone},
                "website": website,
                "business_hours_local": business_hours,
                "tone": tone,
                "disclaimer_text": disclaimer,
                "product_universe": [p.strip() for p in product_universe.split(',') if p.strip()],
                "additional_knowledge_articles": knowledge_articles,
                "other_additional_info": other_info
            }
            st.session_state.editing = False
            st.markdown('<div class="status-success">✅ Business profile updated successfully!</div>', unsafe_allow_html=True)
            st.rerun()

# Initialize OpenAI client
client = OpenAI(api_key=openai_key)

# Enhanced Content Generation Section
st.markdown('<h2 class="section-header">📝 Content Generation</h2>', unsafe_allow_html=True)

st.markdown('<h3 class="section-header">💼 Investor Conference Presentation</h3>', unsafe_allow_html=True)

with st.expander("ℹ️ About Investor Presentation", expanded=False):
    st.write("""
    Generate a compelling business idea presentation for investors, including:
    - Problem statement and solution
    - Market opportunity and competitive advantages
    - Monetization strategy and growth potential
    - Funding requirements and financial projections
    """)

if st.button("📊 Generate Business Idea for Investors"):
    with st.spinner("Generating investor presentation..."):
        try:
            prompt = f"""Based on the Universal AI Chatbot (Multimodal) system:

- Multimodal capabilities: text, voice, image input/output
- Industry-specific adaptation using structured profiles
- Knowledge integration via PDFs and internal docs
- Dynamic FAQ and content generation
- Operational in {len(industries_list)}+ industries

Create a compelling business idea presentation for an investor conference, including:

1. Problem statement
2. Our innovative solution
3. Market opportunity and target audiences
4. Competitive advantages
5. Monetization strategy
6. Scalability and growth potential
7. Team and expertise needed
8. Funding ask and financial projections

Format as a rich, professional HTML presentation page suited for investor conferences."""
            response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], max_tokens=8000)
            investor_html = response.choices[0].message.content.strip()
            with open("docs/investor_business_idea.html", "w", encoding="utf-8") as f:
                f.write(investor_html)
            st.markdown('<div class="status-success">✅ Investor presentation generated and saved to docs/investor_business_idea.html!</div>', unsafe_allow_html=True)
            st.download_button(label="📥 Download Investor Presentation", data=investor_html, file_name="investor_business_idea.html", mime="text/html", key="investor_download")
        except Exception as e:
            st.markdown(f'<div class="status-error">❌ Error generating investor presentation: {e}</div>', unsafe_allow_html=True)

# Enhanced Additional Instructions
st.markdown('<h3 class="section-header">📋 Additional Bot Instructions</h3>', unsafe_allow_html=True)

additional_instructions = st.text_area(
    "🔧 Additional Instructions",
    value="""- Do not hallucinate information; stick to known facts from provided context.
- Use phrases like 'I'm not sure' or 'Please consult our official resources' when uncertain.
- Avoid discussing sensitive topics like politics, religion, or personal financial advice without disclaimers.
- Maintain confidentiality; do not share internal knowledge externally.
- Always provide accurate contact information from the business profile.
- If the query is outside scope, politely redirect to appropriate channels.
""",
    height=150,
    help="Add custom instructions for the chatbot's behavior"
)
st.session_state.additional_instructions = additional_instructions

if 'business_profile' in st.session_state:
    # Enhanced Content Generation
    st.markdown('<h2 class="section-header">🎨 Generate Content</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("❓ FAQ Generation", expanded=True):
            st.markdown("### 📋 Frequently Asked Questions")

            col_a, col_b = st.columns([1, 2])
            with col_a:
                num_faqs = st.number_input("Number of FAQs", min_value=1, max_value=50, value=5, step=1)
            with col_b:
                faq_output_format = st.radio("Output Format", ["Text Display", "PDF Download", "HTML Download"], key="faq_format")

            if st.button("🚀 Generate FAQ", help="Generate FAQs based on the business profile"):
                with st.spinner("Generating FAQs..."):
                    prompt = f"Based on this business profile for {industry}: {json.dumps(st.session_state.business_profile)} Generate {num_faqs} frequently asked questions and their detailed answers for a customer service chatbot in this industry. Format as Q1: question\nA1: answer\netc."
                    try:
                        response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], max_tokens=3000)
                        faq_text = response.choices[0].message.content.strip()

                        html_content = f"<!DOCTYPE html><html><head><title>{industry} FAQs</title></head><body><h1>{industry} FAQs</h1><pre>{faq_text}</pre></body></html>"

                        if faq_output_format == "Text Display":
                            st.text_area("Generated FAQs", value=faq_text, height=400, disabled=True)
                        elif faq_output_format == "PDF Download":
                            try:
                                pdf = FPDF()
                                pdf.add_page()
                                pdf.set_font("Arial", size=12)
                                for line in faq_text.split('\n'):
                                    safe_line = line.encode('Latin1', 'replace').decode('Latin1')
                                    pdf.cell(0, 10, safe_line, ln=True)
                                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                                    pdf.output(tmp.name)
                                    with open(tmp.name, 'rb') as f:
                                        pdf_content = f.read()
                                os.unlink(tmp.name)
                                st.download_button(label="📥 Download FAQ PDF", data=pdf_content, file_name=f"{industry}_faq.pdf", mime="application/pdf", key="faq_pdf_download")
                            except Exception as e:
                                st.markdown(f'<div class="status-error">❌ Error generating PDF: {e}</div>', unsafe_allow_html=True)
                        elif faq_output_format == "HTML Download":
                            st.download_button(label="📥 Download FAQ HTML", data=html_content, file_name=f"{industry}_faq.html", mime="text/html", key="faq_html_download")

                        st.markdown('<div class="status-success">✅ FAQ generated successfully!</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f'<div class="status-error">❌ Error generating FAQ: {e}</div>', unsafe_allow_html=True)

    with col2:
        with st.expander("📖 Product Guide Generation", expanded=True):
            st.markdown("### 🏷️ Product Guide")

            if st.button("🚀 Generate Product Guide", help="Generate a comprehensive product guide"):
                with st.spinner("Generating product guide..."):
                    try:
                        # Load all industry data
                        with open("docs/chatbot_industry_requirements.html", "r", encoding="utf-8") as f:
                            soup = BeautifulSoup(f, 'html.parser')
                        table = soup.find('table')
                        rows = table.find_all('tr')[1:]
                        industries_data = []
                        for row in rows:
                            cols = [col.text.strip() for col in row.find_all('td')]
                            if len(cols) == 14:
                                industries_data.append({
                                    "industry": cols[0],
                                    "volume": cols[1],
                                    "must_haves": cols[2],
                                    "firm_name": cols[3],
                                    "products": cols[11].split(', ') if cols[11] else []
                                })

                        prompt = f"""Based on the following industries data: {json.dumps(industries_data)}

Create a rich HTML product guide for the Universal AI Chatbot (Multimodal) assistant. The guide should include:

1. Overview of the AI assistant concept
2. Its key capabilities (multimodal input/output, industry adaptation, knowledge integration)
3. Use cases for each industry listed
4. Rich styling with sections, lists, and professional appearance

Format as complete HTML with <style> for rich look."""
                        response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], max_tokens=10000)
                        guide_html = response.choices[0].message.content.strip()
                        st.download_button(label="📥 Download Product Guide HTML", data=guide_html, file_name="universal_ai_chatbot_guide.html", mime="text/html", key="guide_download")
                        with open("docs/universal_ai_chatbot_guide.html", "w", encoding="utf-8") as f:
                            f.write(guide_html)
                        st.markdown('<div class="status-success">✅ Product guide generated and saved to docs/universal_ai_chatbot_guide.html!</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f'<div class="status-error">❌ Error generating product guide: {e}</div>', unsafe_allow_html=True)

# Enhanced AI Interaction Section
if 'business_profile' in st.session_state:
    st.markdown('<h2 class="section-header">🤖 AI Interaction</h2>', unsafe_allow_html=True)

    # Build system prompt
    system_prompt = f"""You are a customer service chatbot for {st.session_state.business_profile.get('firm_name', 'the company')}.

Industry Context:
- Projected Monthly Chat Volume: {st.session_state.business_profile.get('projected_monthly_chat_volume', '')}
- Must Haves: {st.session_state.business_profile.get('must_haves', '')}

Business Profile:
{json.dumps({k:v for k,v in st.session_state.business_profile.items() if k not in ['projected_monthly_chat_volume', 'must_haves']}, indent=2)}

Instructions:
- Base your answers on the business profile, industry context, and any uploaded FAQs or knowledge documents.
- Provide helpful, professional responses tailored to the company's services and tone.
- Include the disclaimer where appropriate.
- Always maintain the specified tone: {st.session_state.business_profile.get('tone', '')}

Additional Instructions:
{st.session_state.additional_instructions}
"""
    if 'pdf_text' in st.session_state:
        system_prompt += f"\nInternal Knowledge from Uploaded PDF:\n{st.session_state.pdf_text}\n"

    # Display system prompt
    with st.expander("📋 Complete System Prompt", expanded=False):
        st.text_area("System Prompt (for reference)", value=system_prompt, height=300, disabled=True)

    # Enhanced interaction settings
    st.markdown("### ⚙️ Interaction Settings")

    col1, col2 = st.columns(2)
    with col1:
        input_channel = st.radio("📥 Input Channel", ["Text", "Voice", "Image"], help="Choose how you want to communicate with the bot")
    with col2:
        output_channel = st.radio("📤 Output Channel", ["Text", "Voice", "Image"], help="Choose how the bot responds")

    # Initialize chat history if not exists
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Enhanced input handling based on channel
    user_message = None
    if input_channel == "Text":
        st.markdown("### 💬 Chat Interface")

        # Show suggested prompts
        with st.expander("💡 Suggested Prompts", expanded=True):
            prompt_options = [
                "What are the business hours?",
                "How can I contact customer support?",
                f"Tell me about {industry} products",
                "What is the company address?",
                "What services do you offer?",
                "How to make a complaint?"
            ]
            selected_prompt = st.selectbox("Select a suggested prompt or type your own:", options=[""] + prompt_options, key="prompt_select")
            user_text = st.text_input("Or type your own message:", key="user_input", help="Enter your message to the chatbot")
            if selected_prompt and selected_prompt != "":
                user_message = selected_prompt
            elif user_text:
                user_message = user_text

    elif input_channel == "Voice":
        st.markdown("### 🎤 Voice Input")
        audio_file = st.file_uploader("🎵 Upload audio for speech-to-text", type=["wav", "mp3", "m4a"], help="Upload an audio file and it will be transcribed")
        if audio_file:
            with open("temp_audio", "wb") as f:
                f.write(audio_file.getvalue())
            with open("temp_audio", "rb") as f:
                transcript = client.audio.transcriptions.create(model=models["STT"], file=f)
            user_message = transcript.text
            os.remove("temp_audio")
            st.markdown(f'<div class="status-success">✅ Transcribed: <strong>{user_message}</strong></div>', unsafe_allow_html=True)
            st.session_state.chat_history.append({"role": "user", "content": f"🎵 [Voice]: {user_message}", "type": "voice"})

    elif input_channel == "Image":
        st.markdown("### 🖼️ Image Input")
        with st.form("image_form"):
            image_file = st.file_uploader("📷 Upload image", type=["png", "jpg", "jpeg"], help="Upload an image to analyze")
            image_question = ""
            if image_file:
                st.image(image_file, caption="Uploaded Image", width=300)
                image_question = st.text_input("❓ Ask a question about this image:", key="image_question", help="Enter your specific question about the image")

            submitted = st.form_submit_button("🚀 Ask About Image")
            if submitted and image_file:
                if image_question:
                    user_message = {"file": image_file, "question": image_question}
                    st.session_state.chat_history.append({"role": "user", "content": f"🖼️ [Image]: {image_question}", "type": "image"})
                else:
                    user_message = {"file": image_file, "question": "Describe this image"}
                    st.session_state.chat_history.append({"role": "user", "content": image_file, "type": "image"})

    # Process message button and response
    if user_message and st.button("🚀 Process Message", help="Send your message to the chatbot"):
        with st.spinner("🤖 Thinking..."):
            try:
                # Generate AI response
                messages = [{"role": "system", "content": system_prompt}]

                if input_channel == "Image":
                    # Handle custom image questions
                    if isinstance(user_message, dict):
                        question = user_message["question"]
                        image_file = user_message["file"]
                    else:
                        question = "Describe this image"
                        image_file = user_message

                    messages.append({"role": "user", "content": [
                        {"type": "text", "text": question},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(image_file.getvalue()).decode()}"}}
                    ]})
                else:
                    messages.append({"role": "user", "content": user_message})

                response = client.chat.completions.create(
                    model=models["Text/Vision"],
                    messages=messages,
                    max_tokens=500
                )
                output_text = response.choices[0].message.content

                # Add to chat history
                if input_channel == "Text":
                    st.session_state.chat_history.append({"role": "user", "content": user_message, "type": "text"})
                st.session_state.chat_history.append({"role": "bot", "content": output_text, "type": output_channel.lower()})

            except Exception as e:
                st.markdown(f'<div class="status-error">❌ Error processing message: {e}</div>', unsafe_allow_html=True)

    # Display chat history with enhanced styling
    if st.session_state.chat_history:
        st.markdown("### 💬 Conversation History")

        # Clear chat button
        if st.button("🗑️ Clear Chat", help="Clear the conversation history"):
            st.session_state.chat_history = []
            st.rerun()

        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chatbot-container">', unsafe_allow_html=True)

            for msg in st.session_state.chat_history[-10:]:  # Show last 10 messages
                if msg["role"] == "user":
                    if msg["type"] == "image":
                        st.markdown('<div class="chat-message user">🖼️ [You uploaded an image]</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-message user">{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    if msg["type"] == "voice":
                        # Generate audio response
                        try:
                            tts_response = client.audio.speech.create(
                                model=models["TTS"],
                                input=msg["content"]
                            )
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
                                tts_response.stream_to_file(tmp.name)
                                st.markdown(f'<div class="chat-message bot">{msg["content"]}</div>', unsafe_allow_html=True)
                                st.audio(tmp.name)
                                os.unlink(tmp.name)
                        except Exception as e:
                            st.markdown(f'<div class="chat-message bot">{msg["content"]}</div>', unsafe_allow_html=True)
                    elif msg["type"] == "image":
                        # Generate image response
                        try:
                            image_response = client.images.generate(
                                model=models["Image Generation"],
                                prompt=msg["content"],
                                n=1
                            )
                            st.markdown(f'<div class="chat-message bot">{msg["content"]}</div>', unsafe_allow_html=True)
                            st.image(image_response.data[0].url)
                        except Exception as e:
                            st.markdown(f'<div class="chat-message bot">{msg["content"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-message bot">{msg["content"]}</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
