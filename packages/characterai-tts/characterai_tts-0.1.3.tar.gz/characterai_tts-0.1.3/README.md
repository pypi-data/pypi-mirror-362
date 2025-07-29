
````markdown
# CharacterAI TTS
**CharacterAI TTS - A library for synthesizing text-to-speech character.ai**

---
## 🚀 What's New
### v0.1.3
- ✅ **Increased character limit from 2048 to 4096 characters per request!**
- ⚠️ Long texts may take more time depending on CharacterAI server load.
### v0.1.2
- ℹ️ Maximum character limit was **2048 characters**.
---
## Installation
```bash
# Via pip (in the future)
pip install characterai-tts
# For audio playback (optional):
pip install -e .[audio]
```
## Documentation
See the full documentation and usage instructions here:
[https://github.com/dauitsuragan002/characterai-tts#readme](https://github.com/dauitsuragan002/characterai-tts#readme)

### The simplest usage
```python
from characterai_tts import TTS
# Create a client (default voice – your_voice_id)
client = TTS(api_token="CHARACTER_AI_TOKEN", voice="your_voice_id")
# Speak with the default voice and save to file
client.say("This is an example created with this class")
```
Note: Sometimes CharacterTTS may not synthesize your expected text. This issue is being worked on.

Special thanks to [PyCharacterAI](https://github.com/Xtr4F/PyCharacterAI) for enabling TTS with Character AI voices.
And special thanks to [CharacterAI](https://github.com/kramcat/CharacterAI) for the authentication script.

## Authors
* David Suragan (CharacterTTS)
* Gemini AI
## License

MIT

````