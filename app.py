# app.py - Main application file for ERWIQ Airlines Support Agent

import os
import json
import time
import base64
import glob
from typing import List, Dict, Tuple, Optional

import gradio as gr
from openai import OpenAI
import anthropic
import google.generativeai as genai

from config import (
    OPENAI_API_KEY,
    ANTHROPIC_API_KEY,
    GOOGLE_API_KEY,
    OPENAI_MODEL,
    CLAUDE_MODEL,
    GEMINI_MODEL,
    SYSTEM_MESSAGE
)
from tools import TOOLS, execute_tool
from knowledge_base import (
    initialize_knowledge_base,
    embed_knowledge_base,
    search_airline_policies,
    RAG_TOOL,
    load_knowledge_base
)
from utils import (
    log_interaction,
    get_analytics_display,
    get_logs_display,
    send_notification
)


# Initialize API clients
print("🚀 Initializing ERWIQ Airlines Support Agent...")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

claude_client = None
if ANTHROPIC_API_KEY:
    claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    print("✅ Claude client initialized")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    print("✅ Gemini configured")

# Combine all tools
all_tools = TOOLS + [RAG_TOOL]

## Initialize knowledge base
print("📚 Setting up knowledge base...")
initialize_knowledge_base()

loaded = load_knowledge_base("knowledge_base.json")

if not loaded:
    print("📊 Embedding knowledge base (first run)...")
    embed_knowledge_base(openai_client)
    save_knowledge_base("knowledge_base.json")
else:
    print("✅ Loaded pre-embedded knowledge base")

print("✅ Agent ready!\n")


# ============================================
# Chat Functions
# ============================================

def chat_openai(user_message: str, history: List = None) -> str:
    """Basic chat with OpenAI (no tools)."""
    history = history or []
    
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
    messages += history
    messages.append({"role": "user", "content": user_message})
    
    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages
    )
    
    return response.choices[0].message.content


def chat_claude(user_message: str, history: List = None) -> str:
    """Basic chat with Claude (no tools)."""
    if not claude_client:
        raise Exception("Claude client not initialized")
    
    history = history or []
    messages = history + [{"role": "user", "content": user_message}]
    
    response = claude_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        system=SYSTEM_MESSAGE,
        messages=messages
    )
    
    return response.content[0].text


def chat_gemini(user_message: str, history: List = None) -> str:
    """Basic chat with Gemini (no tools)."""
    if not GOOGLE_API_KEY:
        raise Exception("Gemini not configured")
    
    history = history or []
    
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=SYSTEM_MESSAGE
    )
    
    full_prompt = ""
    for msg in history:
        role = "User" if msg["role"] == "user" else "Assistant"
        full_prompt += f"{role}: {msg['content']}\n"
    full_prompt += f"User: {user_message}"
    
    response = model.generate_content(full_prompt)
    return response.text


def execute_tool_call(tool_name: str, tool_arguments: str) -> str:
    """Execute a tool, handling special cases."""
    if tool_name == "search_airline_policies":
        args = json.loads(tool_arguments)
        return search_airline_policies(args.get("query", ""), openai_client)
    elif tool_name == "get_destination_image":
        return execute_tool(tool_name, tool_arguments, openai_client)
    else:
        return execute_tool(tool_name, tool_arguments)


def chat_with_tools(user_message: str, history: List = None) -> Tuple[str, List[str]]:
    """
    Chat with OpenAI including tool support.
    Returns: (response_text, list_of_tools_used)
    """
    history = history or []
    tools_used = []
    
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
    messages += history
    messages.append({"role": "user", "content": user_message})
    
    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        tools=all_tools
    )
    
    response_message = response.choices[0].message
    
    # Handle tool calls
    if response.choices[0].finish_reason == "tool_calls":
        messages.append(response_message)
        
        for tool_call in response_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = tool_call.function.arguments
            tools_used.append(tool_name)
            
            print(f"🔧 Calling tool: {tool_name}")
            result = execute_tool_call(tool_name, tool_args)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
        
        # Get final response
        final_response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages
        )
        
        return final_response.choices[0].message.content, tools_used
    
    return response_message.content, tools_used


def chat_with_fallback(
    user_message: str,
    history: List = None,
    preferred_model: str = "openai"
) -> Tuple[str, str, List[str]]:
    """
    Chat with automatic fallback to other models on failure.
    Returns: (response, model_used, tools_used)
    """
    history = history or []
    models_to_try = [preferred_model]
    
    # Add fallback models
    all_models = ["openai", "claude", "gemini"]
    for model in all_models:
        if model not in models_to_try:
            models_to_try.append(model)
    
    last_error = None
    tools_used = []
    
    for model in models_to_try:
        try:
            print(f"🔄 Trying {model}...")
            start_time = time.time()
            
            if model == "openai":
                response, tools_used = chat_with_tools(user_message, history)
            elif model == "claude":
                response = chat_claude(user_message, history)
                tools_used = []
            elif model == "gemini":
                response = chat_gemini(user_message, history)
                tools_used = []
            else:
                continue
            
            response_time = time.time() - start_time
            
            # Log successful interaction
            log_interaction(
                user_message=user_message,
                assistant_response=response,
                tools_used=tools_used,
                model=model,
                response_time=response_time
            )
            
            print(f"✅ {model} responded in {response_time:.2f}s")
            return response, model, tools_used
            
        except Exception as e:
            last_error = str(e)
            print(f"❌ {model} failed: {last_error}")
            continue
    
    # All models failed
    error_response = "I apologize, but I'm experiencing technical difficulties. Please try again later or contact ERWIQ Airlines support at 1800-ERWIQ-AIR."
    log_interaction(
        user_message=user_message,
        assistant_response=error_response,
        error=last_error
    )
    send_notification("All Models Failed", last_error, level="error")
    
    return error_response, "none", []


# ============================================
# Voice Functions
# ============================================

def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio file to text using Whisper."""
    if audio_path is None:
        return ""
    
    try:
        with open(audio_path, "rb") as audio_file:
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        return ""


def text_to_speech(text: str, voice: str = "nova") -> Optional[str]:
    """Convert text to speech, return path to audio file."""
    try:
        response = openai_client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text[:4000]  # TTS has length limit
        )
        
        output_path = "response_audio.mp3"
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        return output_path
    except Exception as e:
        print(f"❌ TTS failed: {e}")
        return None


# ============================================
# Gradio Chat Handler
# ============================================

def gradio_chat(
    message: str,
    history: List,
    model_choice: str,
    enable_voice: bool
) -> Tuple[str, Optional[str], Optional[str]]:
    """
    Main chat function for Gradio interface.
    Returns: (response_text, audio_path, image_path)
    """
    if not message.strip():
        return "", None, None
    
    # Convert Gradio history to our format
    formatted_history = []
    for msg in history:
        formatted_history.append({"role": msg["role"], "content": msg["content"]})
    
    # Map model choice
    model_map = {
        "OpenAI (GPT-4o-mini)": "openai",
        "Claude (Sonnet)": "claude",
        "Gemini (Flash)": "gemini"
    }
    preferred = model_map.get(model_choice, "openai")
    
    # Get response
    response, model_used, tools_used = chat_with_fallback(
        message,
        formatted_history,
        preferred_model=preferred
    )
    
    # Generate audio if enabled
    audio_path = None
    if enable_voice:
        audio_path = text_to_speech(response)
    
    # Check if image was generated
    image_path = None
    if "get_destination_image" in tools_used:
        images = glob.glob("destination_*.png")
        if images:
            image_path = max(images, key=os.path.getctime)
    
    # Add model info to response
    tools_info = ', '.join(tools_used) if tools_used else 'None'
    #model_info = f"\n\n---\n*🤖 Model: {model_used} | 🔧 Tools: {tools_info}*"
    
    return response , audio_path, image_path


# ============================================
# Build Gradio App
# ============================================

def build_app():
    """Build the complete Gradio application."""
    
    with gr.Blocks(
        title="ERWIQ Airlines Support",
        #theme=gr.themes.Soft(),
    ) as app:
        
        # Header
        gr.Markdown("""
        # ✈️ ERWIQ Airlines Customer Support Agent
        """)
        # Welcome! I can help you with:
        # - 🎫 **Flight bookings and prices** - Check fares to Indian cities
        # - 📋 **Booking lookups** - Try PNR: ABC123, XYZ789, DEF456, PQR999, LMN555
        # - ✈️ **Flight status** - Try: EQ101, EQ202, EQ404, EQ505, EQ606
        # - 💰 **Refunds and cancellations**
        # - 📜 **Policies** - Baggage, check-in, pets, wheelchair, loyalty program
        # - 🖼️ **Destination images** - See beautiful Indian cities!
        
        with gr.Tabs():
            
            # ========== Chat Tab ==========
            with gr.TabItem("💬 Chat"):
                with gr.Row():
                    with gr.Column(scale=2):
                        chatbot = gr.Chatbot(
                            height=450,
                            #type="messages",
                            label="Conversation",
                            avatar_images=(None, "https://api.dicebear.com/7.x/bottts/svg?seed=erwiq")
                        )
                        
                        with gr.Row():
                            msg_input = gr.Textbox(
                                label="Your message",
                                placeholder="Type your question here... (e.g., 'What's the price to Goa?')",
                                scale=4,
                                lines=1
                            )
                            send_btn = gr.Button("Send ✈️", variant="primary", scale=1)
                        
                        with gr.Row():
                            voice_input = gr.Audio(
                                sources=["microphone"],
                                type="filepath",
                                label="🎤 Or speak your question"
                            )
                            transcribe_btn = gr.Button("Transcribe 🎙️", scale=1)
                        
                        with gr.Row():
                            model_choice = gr.Dropdown(
                                choices=[
                                    "OpenAI (GPT-4o-mini)",
                                    "Claude (Sonnet)",
                                    "Gemini (Flash)"
                                ],
                                value="OpenAI (GPT-4o-mini)",
                                label="🤖 Model",
                                scale=2
                            )
                            enable_voice = gr.Checkbox(
                                label="🔊 Enable voice response",
                                value=False,
                                scale=1
                            )
                            clear_btn = gr.Button("🗑️ Clear Chat", scale=1)
                    
                    with gr.Column(scale=1):
                        audio_output = gr.Audio(
                            label="🔊 Voice Response",
                            type="filepath"
                        )
                        image_output = gr.Image(
                            label="🖼️ Generated Image",
                            type="filepath"
                        )
            
            # ========== Analytics Tab ==========
            with gr.TabItem("📊 Analytics"):
                analytics_display = gr.Markdown(get_analytics_display())
                refresh_analytics_btn = gr.Button("🔄 Refresh Analytics")
            
            # ========== Logs Tab ==========
            with gr.TabItem("📝 Audit Logs"):
                logs_display = gr.Markdown(get_logs_display())
                refresh_logs_btn = gr.Button("🔄 Refresh Logs")
            
            # ========== Help Tab ==========
            with gr.TabItem("❓ Help"):
                gr.Markdown("""
                ## 🛫 How to Use ERWIQ Airlines Support Agent
                
                ### Sample Queries to Try:
                
                **💰 Booking & Prices:**
                - "How much is a business class ticket to Mumbai?"
                - "What's the price for economy to Goa?"
                - "Show me prices to Bangalore"
                
                **📋 Booking Lookup:**
                - "Look up booking ABC123"
                - "Check my reservation XYZ789"
                - "What's the status of booking DEF456?"
                
                **✈️ Flight Status:**
                - "Is flight EQ101 on time?"
                - "What's the status of EQ404?"
                - "Check flight EQ505"
                
                **📜 Policies:**
                - "What's the baggage allowance?"
                - "Can I bring my pet on the plane?"
                - "What's your refund policy?"
                - "Tell me about the loyalty program"
                - "What ID do I need for domestic travel?"
                
                **💸 Refunds:**
                - "I want to cancel booking ABC123"
                - "Process refund for XYZ789, plans changed"
                
                **🖼️ Images:**
                - "Show me what Goa looks like"
                - "Generate an image of Jaipur"
                
                ---
                
                ### 🎯 Features:
                - 🎤 **Voice input** via microphone
                - 🔊 **Voice output** (enable checkbox)
                - 🔄 **Multi-model support** with automatic fallback
                - 📊 **Analytics tracking**
                - 📝 **Full audit logging**
                
                ---
                
                ### 📞 Contact:
                For issues not resolved here, call **1800-ERWIQ-AIR** (toll-free)
                """)
        
        # ========== Event Handlers ==========
        
        def respond(message, history, model, voice):
            if not message.strip():
                return history, "", None, None
            
            # Add user message
            history = history + [{"role": "user", "content": message}]
            
            # Get response
            response, audio, image = gradio_chat(message, history[:-1], model, voice)
            
            # Add assistant response
            history = history + [{"role": "assistant", "content": response}]
            
            return history, "", audio, image
        
        def transcribe_and_fill(audio):
            if audio is None:
                return ""
            return transcribe_audio(audio)
        
        def clear_chat():
            return [], None, None
        
        # Wire up events
        send_btn.click(
            respond,
            inputs=[msg_input, chatbot, model_choice, enable_voice],
            outputs=[chatbot, msg_input, audio_output, image_output]
        )
        
        msg_input.submit(
            respond,
            inputs=[msg_input, chatbot, model_choice, enable_voice],
            outputs=[chatbot, msg_input, audio_output, image_output]
        )
        
        transcribe_btn.click(
            transcribe_and_fill,
            inputs=[voice_input],
            outputs=[msg_input]
        )
        
        clear_btn.click(
            clear_chat,
            outputs=[chatbot, audio_output, image_output]
        )
        
        refresh_analytics_btn.click(
            lambda: get_analytics_display(),
            outputs=[analytics_display]
        )
        
        refresh_logs_btn.click(
            lambda: get_logs_display(),
            outputs=[logs_display]
        )
    
    return app


# ============================================
# Main Entry Point
# ============================================

if __name__ == "__main__":
    app = build_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        share=False
    )