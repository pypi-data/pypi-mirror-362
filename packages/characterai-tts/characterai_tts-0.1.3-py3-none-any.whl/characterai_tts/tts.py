import asyncio
from PyCharacterAI import Client
from PyCharacterAI.exceptions import AuthenticationError, SessionClosedError 
import logging
import io

try:
    import pygame
    _pygame_available = True
except ImportError:
    _pygame_available = False
    logging.warning("pygame library not found. Audio playback feature will be disabled. Install with 'pip install pygame' or 'pip install tulgatts[audio]'.")

class TTS:
    """
    Synthesizes speech using a single, pre-configured Character ID 
    but allows selecting from multiple defined Voice IDs for that character.
    Leverages the PyCharacterAI library.
    """

    _FIXED_CHAR_ID = '2WPyJRflV_4nTx6_-tuNrhkiiqhDyOsn9O25BR1sDO8'

    def __init__(self, 
                 api_token: str | None = None,
                 voice: str | None = None):
        """
        Initializes the CharacterTTS client for the fixed character, with selectable voices.

        Args:
            api_token (str | None): The Character AI API token. If None, tries env var.
            voice (str | None): The voice name (key from VOICES) to use. 
                                If None, uses the first voice in VOICES.

        Raises:
            ValueError: If api_token is needed but not found, or if VOICES is empty.
            KeyError: If the specified voice is not found in VOICES.
        """
        if api_token is None:
            raise ValueError("API token not provided and CHARACTER_AI_TOKEN environment variable not set.")

        self.api_token = api_token
        self.client = Client()
        self._authenticated = False
        self._is_authenticating = False
        self.auth_lock = asyncio.Lock()
        self.voice = voice
        # Add this line to allow direct voice id usage without VOICES dict
        self.VOICES = {}

        if _pygame_available:
            try:
                pygame.mixer.init()
                self._pygame_available = True
            except Exception as e:
                logging.error(f"Failed to initialize pygame mixer: {e}. Audio playback disabled.")
                self._pygame_available = False
        else:
            self._pygame_available = False

        self._current_chat = None
        self._current_chat_id = None

    async def _ensure_authenticated(self):
        async with self.auth_lock:
            if self._authenticated or self._is_authenticating:
                return True
            self._is_authenticating = True
            try:
                logging.info("Authenticating PyCharacterAI client...")
                await self.client.authenticate(self.api_token)
                self._authenticated = True
                return True
            except AuthenticationError as e:
                logging.error(f"PyCharacterAI Authentication failed: {e}")
                self._authenticated = False
                raise ConnectionError("Authentication failed. Check your API token.") from e
            except Exception as e:
                logging.error(f"An unexpected error occurred during authentication: {e}")
                self._authenticated = False
                raise ConnectionError(f"Authentication failed unexpectedly: {e}") from e
            finally:
                self._is_authenticating = False

    async def list_voices(self) -> list[str]:
         return list(self.VOICES.keys())

    async def _synthesize_internal(self, text: str, voice_name: str) -> bytes | None:
        char_id = self._FIXED_CHAR_ID

        # Allow direct voice id usage if not in VOICES
        if hasattr(self, "VOICES") and self.VOICES and voice_name in self.VOICES:
            voice_id = self.VOICES[voice_name]
        else:
            # Assume user passed a voice_id directly
            voice_id = voice_name

        if not voice_id:
            logging.error(f"Voice ID is missing or invalid for voice '{voice_name}'.")
            raise ValueError(f"Invalid configuration for voice '{voice_name}'.")

        try:
            if not await self._ensure_authenticated():
                return None

            if len(text) > 4096:
                raise ValueError("Greeting text must not exceed 2048 characters!")

            character = await self.client.character.fetch_character_info(char_id)
            
            await self.client.character.edit_character(
                character_id=char_id,
                name=character.name,
                greeting=text,
                title=character.title,
                description=character.description,
                definition=character.definition,
                copyable=character.copyable,
                visibility=character.visibility,
                avatar_rel_path=""
            )

            chat_obj, greeting_message = await self.client.chat.create_chat(char_id)

            turn_id = greeting_message.turn_id
            primary_candidate = greeting_message.get_primary_candidate()
            if not primary_candidate:
                logging.error(f"No primary candidate found for greeting message with char ID '{char_id}'.")
                return None
            candidate_id = primary_candidate.candidate_id

            speech_bytes = await self.client.utils.generate_speech(
                chat_id=chat_obj.chat_id,
                turn_id=turn_id,
                candidate_id=candidate_id,
                voice_id=voice_id
            )
            return speech_bytes

        except AuthenticationError as e:
            logging.error(f"Auth error during internal synth for fixed char: {e}")
            self._authenticated = False 
            raise ConnectionError("Authentication failed during synthesis.") from e
        except SessionClosedError as e:
            logging.error(f"Session closed during internal synth for fixed char: {e}")
            self._authenticated = False
            raise ConnectionError("Session closed during synthesis.") from e
        except KeyError as e:
            logging.error(f"Internal Error: {e}")
            raise
        except ValueError as e:
            logging.error(f"Internal Error: {e}")
            raise
        except Exception as e:
            logging.exception(f"Unexpected error during internal synthesis for fixed char: {type(e).__name__} - {e}")
            raise RuntimeError(f"Unexpected error during synthesis for fixed char.") from e

    async def say_async(self,
                text: str,
                voice: str | None = None,
                output_file: str | None = None,
                play_audio: bool = True) -> str | None:
        used_voice = voice or self.voice
        
        audio_bytes = None
        try:
            audio_bytes = await self._synthesize_internal(text, used_voice)
        except (KeyError, ValueError, ConnectionError, RuntimeError) as e:
             logging.error(f"Synthesis failed for voice '{used_voice}': {e}")
             raise e 
        except Exception as e:
             logging.exception(f"Unexpected error during synthesis call for voice '{used_voice}': {e}")
             raise RuntimeError(f"An unexpected error occurred during synthesis for voice '{used_voice}'.") from e

        if not audio_bytes:
            logging.error("Synthesis returned no audio bytes without raising an exception. This indicates an issue.")
            return None

        saved_path = None
        if output_file:
            try:
                with open(output_file, "wb") as f:
                    f.write(audio_bytes)
                saved_path = output_file
            except IOError as e:
                logging.error(f"Failed to save audio to {output_file}: {e}")

        if play_audio:
            if self._pygame_available:
                if not pygame.mixer.get_init():
                    logging.warning("pygame mixer not initialized. Attempting reinit.")
                    try: pygame.mixer.init()
                    except Exception: self._pygame_available = False
                if pygame.mixer.get_init():
                    try:
                        sound = pygame.mixer.Sound(io.BytesIO(audio_bytes))
                        sound.play()
                        while pygame.mixer.get_busy():
                            await asyncio.sleep(0.1)
                    except Exception as e:
                        logging.error(f"Error during pygame audio playback: {e}")
            else:
                logging.warning("Audio playback requested but pygame is not available or failed to initialize.")

        return saved_path
    
    def say(self,
                 text: str,
                 voice: str | None = None, 
                 output_file: str | None = None,
                 play_audio: bool = True) -> str | None:
        used_voice = voice or self.voice
        
        try:
            result = asyncio.run(self.say_async(text, used_voice, output_file, play_audio))
            return result
        except RuntimeError as e:
            if "cannot be called from a running event loop" in str(e):
                 logging.error("say_sync cannot be called from a running event loop. Use `await self.say()` instead.")
                 raise TypeError("say_sync cannot be called from a running event loop.") from e
            else: raise
        except Exception as e:
            logging.error(f"Error during say_sync execution: {type(e).__name__} - {e}")
            raise e