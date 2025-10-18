# 🤖 Universal AI Chatbot (Multimodal)

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50+-red.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-orange.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A powerful, industry-adaptive AI chatbot with multimodal capabilities including text, voice, and image processing. Built with Streamlit and integrated with OpenAI's latest models for enterprise-grade conversational AI.

![Universal AI Chatbot Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=🤖+Universal+AI+Chatbot+Demo)

## ✨ Features

### 🎯 **Multimodal AI Processing**
- **Text Conversations** - Natural language processing with context awareness
- **Voice Integration** - Speech-to-text and text-to-speech capabilities
- **Image Analysis** - Upload images and ask specific questions about them
- **Smart Responses** - Context-aware replies based on business profiles

### 🏢 **Industry-Specific Adaptation**
- **Dynamic Business Profiles** - Generate industry-specific chatbot configurations
- **Knowledge Base Integration** - Upload PDF documents for internal knowledge
- **Content Generation** - Create FAQs, product guides, and presentations
- **Multi-Industry Support** - Finance, Healthcare, Technology, and more

### 🚀 **Advanced Capabilities**
- **Custom Image Questions** - Ask specific questions about uploaded images
- **Real-time Processing** - Fast, responsive AI interactions
- **Session Management** - Persistent chat history and settings
- **Professional UI** - Clean, modern interface design

## 🎬 Demo

![App Screenshot](https://via.placeholder.com/800x400/764ba2/ffffff?text=🎯+Business+Profile+Setup)

*Universal AI Chatbot interface showing business profile generation and industry selection*

## 🛠️ Installation

### Prerequisites
- Python 3.13 or higher
- OpenAI API key
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/srinipusuluri/universal_ai_chatbot.git
   cd universal_ai_chatbot
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8502`

## 📖 Usage

### 🔑 Initial Setup

1. **Enter your OpenAI API Key** in the sidebar settings
2. **Select your industry** from the dropdown menu
3. **Generate a business profile** based on your industry requirements
4. **Upload PDF knowledge base** (optional) for internal information

### 🤖 AI Interaction

Choose your preferred input method:

#### 💬 **Text Chat**
- Type messages directly or use suggested prompts
- Context-aware responses based on your business profile

#### 🎤 **Voice Input**
- Upload audio files (WAV, MP3, M4A)
- Automatic transcription and AI response

#### 🖼️ **Image Analysis**
- Upload images (PNG, JPG, JPEG)
- **Ask specific questions** about the image content
- Get targeted responses instead of generic descriptions

### 📝 Content Generation

Generate industry-specific content:

- **📋 FAQs** - Frequently asked questions for your business
- **📖 Product Guides** - Comprehensive product documentation
- **💼 Investor Presentations** - Business pitch decks
- **🎨 Custom Styling** - Professional HTML output

## 🏗️ Project Structure

```
universal_ai_chatbot/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── docs/                          # Documentation and templates
│   ├── chatbot_industry_requirements.html
│   ├── investor_business_idea.html
│   └── universal_ai_chatbot_guide.html
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit 1.50+
- **AI Engine**: OpenAI GPT-4o, GPT-4o-mini
- **Speech Processing**: OpenAI Whisper, TTS
- **Document Processing**: PyPDF, BeautifulSoup
- **Image Processing**: PIL, OpenAI Vision
- **Data Processing**: Pandas, NumPy

## 🔧 Configuration

### Environment Variables

Create a `.streamlit/secrets.toml` file:

```toml
[openai]
api_key = "your-openai-api-key-here"
```

### Customization

The application supports extensive customization through:

- **Business Profile Settings** - Industry-specific configurations
- **AI Model Selection** - Choose between different OpenAI models
- **Content Templates** - Customizable output formats
- **UI Preferences** - Simplified, professional interface

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for their powerful AI models and APIs
- **Streamlit** for the amazing web framework
- **Python Community** for the extensive ecosystem

## 📞 Support

For support and questions:

- **Issues**: [GitHub Issues](https://github.com/srinipusuluri/universal_ai_chatbot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/srinipusuluri/universal_ai_chatbot/discussions)
- **Email**: [Contact](mailto:your-email@example.com)

## 🚀 Roadmap

- [ ] **Multi-language support** - Internationalization
- [ ] **Advanced analytics** - Usage tracking and insights
- [ ] **Plugin system** - Extensible architecture
- [ ] **Mobile optimization** - Responsive design
- [ ] **API endpoints** - RESTful API for integration
- [ ] **Database integration** - Persistent storage options

---

**⭐ If you found this project helpful, please give it a star!**

[![GitHub stars](https://img.shields.io/github/stars/srinipusuluri/universal_ai_chatbot.svg?style=social&label=Star)](https://github.com/srinipusuluri/universal_ai_chatbot)
[![GitHub forks](https://img.shields.io/github/forks/srinipusuluri/universal_ai_chatbot.svg?style=social&label=Fork)](https://github.com/srinipusuluri/universal_ai_chatbot/fork)
[![GitHub watchers](https://img.shields.io/github/watchers/srinipusuluri/universal_ai_chatbot.svg?style=social&label=Watch)](https://github.com/srinipusuluri/universal_ai_chatbot)

---

**Made with ❤️ using Streamlit and OpenAI**
