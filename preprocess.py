import mne
import numpy as np
from scipy.signal import welch

print("Loading EEG files...")
files = [
    'data/S001R04.edf',
    'data/S001R06.edf',
    'data/S001R08.edf'
]
raws = [mne.io.read_raw_edf(f, preload=True, verbose=False) for f in files]
raw  = mne.concatenate_raws(raws)

print("Filtering signal...")
raw.filter(8.0, 30.0, fir_design='firwin', verbose=False)

print("Extracting events...")
events, event_id = mne.events_from_annotations(raw, verbose=False)
print(f"Events: {event_id}")

print("Creating epochs...")
epochs = mne.Epochs(
    raw, events, event_id=event_id,
    tmin=0.0, tmax=4.0,
    baseline=None, preload=True, verbose=False
)

print(f"Total epochs: {len(epochs)}")

# ── Better feature extraction ──────────────────
def extract_band_power(epochs):
    data     = epochs.get_data()
    sfreq    = epochs.info['sfreq']
    features = []

    for epoch in data:
        epoch_features = []
        for channel in epoch:
            # Alpha band (8-13 Hz)
            freqs, psd = welch(channel, sfreq, nperseg=256)
            alpha_idx  = np.where((freqs >= 8)  & (freqs <= 13))[0]
            beta_idx   = np.where((freqs >= 13) & (freqs <= 30))[0]
            gamma_idx  = np.where((freqs >= 30) & (freqs <= 45))[0]

            alpha_power = np.mean(psd[alpha_idx])
            beta_power  = np.mean(psd[beta_idx])
            gamma_power = np.mean(psd[gamma_idx])

            epoch_features.extend([alpha_power, beta_power, gamma_power])

        features.append(epoch_features)

    return np.array(features)

print("Extracting band power features (this takes 1-2 mins)...")
X = extract_band_power(epochs)
y = epochs.events[:, 2]

print(f"Feature matrix shape : {X.shape}")
print(f"Labels shape         : {y.shape}")
print(f"Unique labels        : {np.unique(y)}")

np.save('data/X_features.npy', X)
np.save('data/y_labels.npy',   y)

print("\nPhase 2 updated! ✅")