import numpy as np
from music21 import converter, instrument, note, chord, stream
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint
notes = []
midi_files = ["beethoven_opus10_1 (1).mid", "beethoven_opus10_2.mid","mz_311_2.mid","pathetique_1.mid","mz_311_1.mid","beethoven_opus10_3.mid"]

for file in midi_files:
    print("Parsing:", file)
    midi = converter.parse(file)
    notes_to_parse = midi.flatten().notes

    for element in notes_to_parse:

        if isinstance(element, note.Note):
            notes.append(str(element.pitch))

        elif isinstance(element, chord.Chord):
            notes.append('.'.join(str(n) for n in element.normalOrder))

print("Total Notes:", len(notes))
sequence_length = 50

pitchnames = sorted(set(notes))

note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

network_input = []
network_output = []

for i in range(0, len(notes) - sequence_length):

    sequence_in = notes[i:i + sequence_length]
    sequence_out = notes[i + sequence_length]

    network_input.append([note_to_int[char] for char in sequence_in])
    network_output.append(note_to_int[sequence_out])

n_patterns = len(network_input)

network_input = np.reshape(
    network_input,
    (n_patterns, sequence_length, 1)
)

network_input = network_input / float(len(pitchnames))

network_output = to_categorical(network_output)

model = Sequential()

model.add(LSTM(
    256,
    input_shape=(network_input.shape[1], network_input.shape[2]),
    return_sequences=True
))

model.add(Dropout(0.3))

model.add(LSTM(256))

model.add(Dense(128, activation='relu'))

model.add(Dropout(0.3))

model.add(Dense(len(pitchnames), activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')

print("\nModel created successfully!\n")

print("training started...\n")
model.fit(
    network_input,
    network_output,
    epochs=20,
    batch_size=64
)
print("\ntraining completed!\n")
start = np.random.randint(0, len(network_input)-1)

int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

pattern = network_input[start]
prediction_output = []

for note_index in range(100):

    prediction_input = np.reshape(pattern, (1, len(pattern), 1))
    prediction_input = prediction_input / float(len(pitchnames))

    prediction = model.predict(prediction_input, verbose=0)

    index = np.argmax(prediction)

    result = int_to_note[index]

    prediction_output.append(result)

    pattern = np.append(pattern, index)
    pattern = pattern[1:]
    offset = 0
output_notes = []

for pattern in prediction_output:

    if ('.' in pattern) or pattern.isdigit():

        notes_in_chord = pattern.split('.')
        notes_list = []

        for current_note in notes_in_chord:
            new_note = note.Note(int(current_note))
            new_note.storedInstrument = instrument.Piano()
            notes_list.append(new_note)

        new_chord = chord.Chord(notes_list)
        new_chord.offset = offset
        output_notes.append(new_chord)

    else:

        new_note = note.Note(pattern)
        new_note.offset = offset
        new_note.storedInstrument = instrument.Piano()
        output_notes.append(new_note)

    offset += 0.5

midi_stream = stream.Stream(output_notes)

midi_stream.write('midi', fp='generated_music.mid')

print("Music generated successfully!")
print("Saved as generated_music.mid")