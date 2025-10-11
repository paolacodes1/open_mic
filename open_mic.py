#!/usr/bin/env python3
"""
Free Voice Transcriber - Permission Fix Version
Helps diagnose and fix the exact auto-paste permission issue
"""
import ssl
import urllib.request
import whisper
import sounddevice as sd
import rumps
import threading
import time
import subprocess
import numpy as np
from pynput import keyboard
import os

# SSL workaround
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
original_urlopen = urllib.request.urlopen
urllib.request.urlopen = lambda url, **kwargs: original_urlopen(url, context=ssl_context, **kwargs)

class WhisperPermissionApp(rumps.App):
    def __init__(self):
        super(WhisperPermissionApp, self).__init__(
            "🎤",
            title="🎤",
            menu=[
                "Status: Loading...",
                "💡 Press Ctrl+Space to record",
                None,
                "📝 Last Transcription",
                "📋 Copy Last Text",
                None,
                "✨ Auto-Paste: ON",
                "🔧 Open System Settings",
                "🧪 Test Auto-Paste Now",
                None,
                "ℹ️ About",
                "🚪 Quit"
            ]
        )

        # State variables
        self.model = None
        self.is_recording = False
        self.audio_chunks = []
        self.sample_rate = 16000
        self.last_transcription = ""
        self.auto_paste_enabled = True
        self.recording_stream = None
        self.listener = None
        self.recording_timer = None
        self.currently_pressed = set()

        # Setup callbacks
        self.menu["📋 Copy Last Text"].set_callback(self.copy_last_text)
        self.menu["✨ Auto-Paste: ON"].set_callback(self.toggle_auto_paste)
        self.menu["🔧 Open System Settings"].set_callback(self.open_system_settings)
        self.menu["🧪 Test Auto-Paste Now"].set_callback(self.test_auto_paste)
        self.menu["ℹ️ About"].set_callback(self.show_about)

        # Load model and setup hotkeys
        threading.Thread(target=self.load_model, daemon=True).start()

    def load_model(self):
        """Load Whisper model in background"""
        try:
            self.model = whisper.load_model("base")
            self.title = "🎤"
            self.setup_hotkeys()

            rumps.notification(
                title="🎤 Voice Transcriber Ready",
                subtitle="Press Ctrl+Space to record",
                message="Click '🔧 Open System Settings' if auto-paste fails"
            )

        except Exception as e:
            print(f"Model loading error: {e}")

    def setup_hotkeys(self):
        """Setup global hotkey listener using regular Listener"""
        def on_press(key):
            try:
                # Check if Control key is being held and Space is pressed
                if hasattr(key, 'name') and key.name == 'space':
                    # Check if ctrl is in currently_pressed
                    if keyboard.Key.ctrl_l in self.currently_pressed or keyboard.Key.ctrl in self.currently_pressed:
                        self.toggle_recording()
            except Exception as e:
                print(f"Key press error: {e}")

        def on_release(key):
            try:
                if key in self.currently_pressed:
                    self.currently_pressed.remove(key)
            except:
                pass

        def on_press_track(key):
            try:
                self.currently_pressed.add(key)
                on_press(key)
            except Exception as e:
                print(f"Track error: {e}")

        try:
            # Initialize set to track pressed keys
            self.currently_pressed = set()

            # Stop existing listener if any
            if self.listener:
                try:
                    self.listener.stop()
                except:
                    pass
                self.listener = None

            # Create new listener with on_press and on_release
            self.listener = keyboard.Listener(
                on_press=on_press_track,
                on_release=on_release
            )
            self.listener.start()
            print("✅ Hotkey listener started successfully")

        except Exception as e:
            print(f"Hotkey setup error: {e}")

    def audio_callback(self, indata, frames, time, status):
        """Callback for audio recording"""
        if self.is_recording:
            self.audio_chunks.append(indata.copy())

    def toggle_recording(self):
        """Toggle recording on/off via hotkey"""
        if not self.model:
            return

        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """Start recording audio"""
        try:
            # Make sure we're not already recording
            if self.is_recording:
                print("Already recording, ignoring start request")
                return

            # Clean up any existing stream first
            if self.recording_stream:
                try:
                    self.recording_stream.stop()
                    self.recording_stream.close()
                except:
                    pass
                self.recording_stream = None

            # Start fresh recording
            self.is_recording = True
            self.audio_chunks = []
            self.title = "🔴"

            self.recording_stream = sd.InputStream(
                callback=self.audio_callback,
                channels=1,
                samplerate=self.sample_rate,
                dtype='float32'
            )
            self.recording_stream.start()
            print("🎙️ Recording started")

            # Auto-stop after 5 minutes (300 seconds) to allow longer recordings
            self.recording_timer = threading.Timer(300.0, self.auto_stop)
            self.recording_timer.start()

            rumps.notification(
                title="🎙️ Recording",
                subtitle="Press Ctrl+Space to stop",
                message=""
            )

        except Exception as e:
            print(f"Recording error: {e}")
            self.is_recording = False
            self.title = "🎤"

    def stop_recording(self):
        """Stop recording and transcribe"""
        if not self.is_recording:
            return

        try:
            self.is_recording = False
            self.title = "🟠"

            # Cancel timer first
            if self.recording_timer:
                self.recording_timer.cancel()
                self.recording_timer = None

            # Properly close audio stream
            if self.recording_stream:
                try:
                    self.recording_stream.stop()
                    self.recording_stream.close()
                except Exception as stream_error:
                    print(f"Stream cleanup error: {stream_error}")
                finally:
                    self.recording_stream = None

            # Process audio if we have any
            if self.audio_chunks:
                threading.Thread(target=self.transcribe_audio, daemon=True).start()
            else:
                # Reset icon if no audio was captured
                self.title = "🎤"

        except Exception as e:
            print(f"Stop recording error: {e}")
            self.title = "🎤"

    def auto_stop(self):
        """Auto-stop recording after timeout"""
        if self.is_recording:
            self.stop_recording()

    def transcribe_audio(self):
        """Transcribe recorded audio"""
        try:
            if not self.audio_chunks:
                return

            audio_data = np.concatenate(self.audio_chunks, axis=0).flatten()
            self.audio_chunks = []

            if len(audio_data) < self.sample_rate * 0.3:
                print("Recording too short")
                self.title = "🎤"
                return

            # Transcribe
            result = self.model.transcribe(audio_data)
            text = result["text"].strip()

            if text:
                self.last_transcription = text
                print(f"Transcribed: {text}")

                # Copy to clipboard FIRST
                self.copy_text_to_clipboard(text)

                # Auto-paste if enabled
                if self.auto_paste_enabled:
                    success = self.paste_text_with_feedback()
                    if success:
                        self.title = "✅"
                        rumps.notification(
                            title="✅ Auto-Pasted!",
                            subtitle=text[:50],
                            message=""
                        )
                    else:
                        self.title = "📋"
                        rumps.notification(
                            title="📋 Permission Needed",
                            subtitle="Click '🔧 Open System Settings'",
                            message="Text copied to clipboard - use Cmd+V"
                        )
                else:
                    self.title = "📋"

                # Reset after 3 seconds
                threading.Timer(3.0, lambda: setattr(self, 'title', '🎤')).start()

            else:
                print("No speech detected")
                self.title = "🎤"

        except Exception as e:
            print(f"Transcription error: {e}")
            self.title = "🎤"

    def paste_text_with_feedback(self):
        """Paste text and provide detailed feedback about what failed"""
        print("🔄 Testing auto-paste...")

        try:
            result = subprocess.run([
                'osascript', '-e',
                'tell application "System Events" to keystroke "v" using command down'
            ], check=True, timeout=3, capture_output=True, text=True)
            print("✅ Auto-paste SUCCESS!")
            return True

        except subprocess.CalledProcessError as e:
            if "1002" in str(e.stderr):
                print("❌ ERROR: osascript is not allowed to send keystrokes")
                print("🔧 SOLUTION: Need to add Terminal to Accessibility permissions")
                print("   1. Click '🔧 Open System Settings' in menu")
                print("   2. Go to Privacy & Security > Accessibility")
                print("   3. Click '+' and add Terminal")
                print("   4. Restart this app")
            else:
                print(f"❌ Auto-paste failed with error: {e.stderr}")
            return False

        except Exception as e:
            print(f"❌ Auto-paste failed: {e}")
            return False

    def test_auto_paste(self, sender):
        """Test auto-paste functionality"""
        # Put some test text in clipboard
        self.copy_text_to_clipboard("🧪 AUTO-PASTE TEST - This should appear where your cursor is!")

        # Try to paste it
        success = self.paste_text_with_feedback()

        if success:
            rumps.alert(
                title="✅ Auto-Paste Working!",
                message="Great! Auto-paste is working correctly.\n\nThe test text should have appeared where your cursor was."
            )
        else:
            rumps.alert(
                title="❌ Auto-Paste Not Working",
                message="Auto-paste failed. Please:\n\n" +
                       "1. Click '🔧 Open System Settings'\n" +
                       "2. Go to Privacy & Security > Accessibility\n" +
                       "3. Add Terminal to allowed apps\n" +
                       "4. Restart this app\n\n" +
                       "Test text is in your clipboard - try Cmd+V"
            )

    def open_system_settings(self, sender):
        """Open System Settings to Accessibility page"""
        try:
            # Try to open directly to Accessibility settings
            subprocess.run([
                'open', 'x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility'
            ], check=True)

            rumps.notification(
                title="🔧 System Settings Opened",
                subtitle="Add Terminal to Accessibility",
                message="Look for Terminal in the list and enable it"
            )
        except Exception as e:
            # Fallback: just open System Settings
            subprocess.run(['open', '/System/Applications/System Preferences.app'])
            rumps.alert(
                title="🔧 Manual Steps",
                message="Please navigate to:\n\n" +
                       "Privacy & Security > Accessibility\n\n" +
                       "Then add Terminal to the allowed apps list."
            )

    def copy_text_to_clipboard(self, text):
        """Copy text to system clipboard"""
        try:
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            print(f"📋 Copied to clipboard: {text}")
        except Exception as e:
            print(f"Clipboard error: {e}")

    def copy_last_text(self, sender):
        """Copy last transcription to clipboard"""
        if self.last_transcription:
            self.copy_text_to_clipboard(self.last_transcription)
            rumps.notification(
                title="📋 Copied",
                subtitle="Last transcription copied",
                message=""
            )
        else:
            rumps.alert("No transcription to copy!")

    def toggle_auto_paste(self, sender):
        """Toggle auto-paste"""
        self.auto_paste_enabled = not self.auto_paste_enabled

        if self.auto_paste_enabled:
            self.menu["✨ Auto-Paste: ON"].title = "✨ Auto-Paste: ON"
        else:
            self.menu["✨ Auto-Paste: ON"].title = "✨ Auto-Paste: OFF"

    def show_about(self, sender):
        """Show about"""
        rumps.alert(
            title="🎤 Free Voice Transcriber",
            message="FREE offline voice transcription\n\n" +
                   "• Press Ctrl+Space to record\n" +
                   "• Auto-paste to any app\n" +
                   "• No API keys needed\n" +
                   "• Click '🧪 Test Auto-Paste Now' to diagnose issues\n\n" +
                   "Powered by OpenAI Whisper"
        )

    def clean_up(self):
        """Clean up resources"""
        self.is_recording = False
        if self.listener:
            self.listener.stop()
        if self.recording_timer:
            self.recording_timer.cancel()
        if self.recording_stream:
            try:
                self.recording_stream.stop()
                self.recording_stream.close()
            except:
                pass

if __name__ == "__main__":
    print("🎤 Starting Permission Fix Voice Transcriber...")
    print("🔧 If auto-paste doesn't work, click '🔧 Open System Settings' in menu")
    print("🧪 Use '🧪 Test Auto-Paste Now' to check if permissions work")
    print("📱 Look for 🎤 in menu bar")
    print()

    app = WhisperPermissionApp()
    try:
        app.run()
    finally:
        app.clean_up()