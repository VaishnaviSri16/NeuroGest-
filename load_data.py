import mne
import numpy as np
import matplotlib.pyplot as plt

print("Loading EEG data...")
raw = mne.io.read_raw_edf('data/S001R04.edf', preload=True, verbose=False)

print("\n====== DATASET INFO ======")
print(f"Number of channels : {len(raw.ch_names)}")
print(f"Duration           : {raw.times[-1]:.1f} seconds")
print(f"Sample rate        : {raw.info['sfreq']} Hz")

events, event_id = mne.events_from_annotations(raw, verbose=False)
print("\n====== EVENT LABELS ======")
print(event_id)
print(f"Total events found : {len(events)}")

for label, code in event_id.items():
    count = np.sum(events[:, 2] == code)
    print(f"  {label} → {count} occurrences")

print("\n====== GAME COMMAND MAPPING ======")
print("T0 (rest)       → FORWARD")
print("T1 (left fist)  → LEFT")
print("T2 (right fist) → RIGHT")

print("\nPhase 1 complete! ✅")