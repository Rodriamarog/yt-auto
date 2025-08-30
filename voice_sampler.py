import sounddevice as sd
import soundfile as sf
import os

# Set PulseAudio to use AudioBox monitor as the recording source
os.environ['PULSE_SOURCE'] = 'alsa_output.usb-PreSonus_AudioBox_USB_96_000000000000-00.iec958-stereo.monitor'

monitor_device = 'pulse'
print("Using AudioBox USB 96 monitor via PulseAudio")

# Try common sample rates in order of preference
sample_rates = [44100, 48000, 22050, 16000]
chosen_rate = None

for rate in sample_rates:
    try:
        # Test if this sample rate works
        sd.check_input_settings(device=monitor_device, channels=1, samplerate=rate)
        chosen_rate = rate
        print(f"Using sample rate: {rate} Hz")
        break
    except Exception as e:
        continue

if chosen_rate is None:
    chosen_rate = 44100  # Default fallback
    print(f"Fallback to {chosen_rate} Hz")

# Record 20 seconds from system audio
print("Recording system audio... (play something in Firefox)")
audio = sd.rec(int(20 * chosen_rate), samplerate=chosen_rate, channels=1, device=monitor_device)
sd.wait()
sf.write('reference_voice.wav', audio, chosen_rate)
print("Recording saved to reference_voice.wav")