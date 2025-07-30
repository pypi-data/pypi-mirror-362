import numpy as np


def stretch(y: np.ndarray, stretch_factor: float, window_size: int=2048) -> np.ndarray:
    
    # prepare input buffer
    
    x = y.copy()

    if len(x.shape) == 1:
        x = np.expand_dims(x, axis=1)

    transpose = False
    if x.shape[0] < x.shape[1]:
        transpose = True
        x = x.T
    
    # prepare output buffer
        
    n_channels = x.shape[1]
    output_length = int(np.ceil(x.shape[0] * stretch_factor))
    n_frames = int(output_length // (0.5 * window_size))
    full_output_length = (n_frames + 1) * int(0.5 * window_size)
    output_buffer = np.zeros_like(x, shape=(full_output_length, n_channels))
    
    # calculate window

    window = np.power(1.0-np.power(np.linspace(-1.0 , 1.0, window_size), 2), 1.25)
    window = np.expand_dims(window, axis=1)
    window = np.tile(window, (1, n_channels))
    
    # process frames

    for n in range(int(n_frames)): 
        output_i = int(n * window_size * 0.5)
        input_i = int(np.round(output_i / stretch_factor))

        frame = x[input_i:input_i+window_size].copy()
        
        # extend incomplete last frame to fill entire window
        if frame.shape[0] < window_size:
            frame = x[input_i:].copy()
            pad_amount = window_size - frame.shape[0]
            frame = np.pad(frame, ((0, pad_amount), (0, 0)))

        frame *= window

        fft = np.fft.rfft(frame, axis=0)

        random_phases = np.random.uniform(-np.pi, np.pi, size=fft.shape[0])
        random_phases = np.expand_dims(random_phases, axis=1)
        random_phases = np.tile(random_phases, (1, n_channels))

        fft *= np.exp(1.j * random_phases) 

        frame = np.fft.irfft(fft, axis=0)

        frame *= window

        output_buffer[output_i:output_i+window_size] += frame

    if transpose:
        output_buffer = output_buffer.T

    return output_buffer