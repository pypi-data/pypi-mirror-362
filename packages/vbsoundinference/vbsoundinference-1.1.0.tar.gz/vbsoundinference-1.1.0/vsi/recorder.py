import sounddevice as sd
import numpy as np
import os

class RecordingSample:
    def __init__(self, recording=None, duration=1, num_samples=512, class_number=0):
        self.recording = recording or []
        self.duration = duration
        self.num_samples = num_samples
        self.class_number = class_number

class Recorder:
    def __init__(self, samplerate=44100):
        self.samplerate = samplerate

    def record_sample(self, duration=1, num_samples=512, class_number=0, input_device_index=0, normalize_range=1, precision=3):
        sd.default.device = (input_device_index, None)
        audio = sd.rec(int(duration * self.samplerate), samplerate=self.samplerate, channels=1, dtype='float64')
        sd.wait()
        audio = audio.flatten()

        # Create evenly spaced indices for resampling
        original_indices = np.linspace(0, len(audio) - 1, num=num_samples, dtype=int)
        sampled_audio = audio[original_indices]

        # Normalize to [-1.0, 1.0]
        max_val = np.max(np.abs(sampled_audio))
        if max_val > 0:
            sampled_audio = sampled_audio / max_val
        sampled_audio *= normalize_range
        sampled_audio = sampled_audio.tolist()

        sampled_audio = [round(sampled_audio, precision) for sampled_audio in sampled_audio]

        return RecordingSample(
            recording=sampled_audio,
            duration=duration,
            num_samples=num_samples,
            class_number=class_number
        )


    def record_class(self, n_recordings, duration=1, num_samples=512, class_number=0,
                     input_device_index=0, normalize_range=1, precision=3, dataset_file="test.txt", append=False, num_classes=2):
        recordings = []
        for i in range(n_recordings):
            input(f"recording class {class_number}, ({i+1}/{n_recordings}). press enter to continue...")
            sample = self.record_sample(duration=duration, num_samples=num_samples,
                                        class_number=class_number, input_device_index=input_device_index,
                                        normalize_range=normalize_range, precision=precision)
            recordings.append(sample)

            # Format: [recording.recording, recording.duration, recording.class_number, recording.num_samples]
            line = f"[{sample.recording}, {sample.duration}, {sample.class_number}, {sample.num_samples}, {num_classes}]\n"

            # Append to file
            if append or i:
                with open(dataset_file, "a") as f:
                    f.write(line)
            else:
                if not i:
                    with open(dataset_file, "w") as f:
                        f.write(line)

    def record_class_continuous(self, num_recordings=100, duration=1, num_samples=512, class_number=0, input_device_index=0, normalize_range=1, precision=3, dataset_file="test.txt", append=False, num_classes=2):
        recordings = []
        for i in range(num_recordings):
            sample = self.record_sample(duration=duration, num_samples=num_samples,
                                        class_number=class_number, input_device_index=input_device_index,
                                        normalize_range=normalize_range, precision=precision)
            recordings.append(sample)
            print(f"recording class {class_number} continuously, ({i+1}/{num_recordings}).")

            # Format: [recording.recording, recording.duration, recording.class_number, recording.num_samples]
            line = f"[{sample.recording}, {sample.duration}, {sample.class_number}, {sample.num_samples}, {num_classes}]\n"

            # Append to file
            if append or i:
                with open(dataset_file, "a") as f:
                    f.write(line)
            else:
                if not i:
                    with open(dataset_file, "w") as f:
                        f.write(line)
