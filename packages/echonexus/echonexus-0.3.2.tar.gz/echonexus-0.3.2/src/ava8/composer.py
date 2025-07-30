import json
from pathlib import Path
from typing import List

# Tone map bundled with the package
GLYPH_TO_TONE_PATH = Path(__file__).resolve().parent / 'glyph_to_tone.json'

with open(GLYPH_TO_TONE_PATH, 'r') as f:
    GLYPH_TO_TONE = json.load(f)


def validate_glyphs(glyphs: List[str]) -> None:
    """Ensure all glyphs are known to the tone map."""
    invalid = [g for g in glyphs if g not in GLYPH_TO_TONE]
    if invalid:
        raise ValueError(f"Invalid glyphs: {', '.join(invalid)}")


def glyphs_to_tones(glyphs: List[str]) -> List[float]:
    """Convert a sequence of glyphs to MIDI note frequencies."""
    validate_glyphs(glyphs)
    tones = [GLYPH_TO_TONE[g] for g in glyphs]
    return tones


def frequency_to_midi_pitch(freq: float) -> int:
    """Convert frequency in Hz to the nearest MIDI pitch number."""
    from math import log2
    return int(round(69 + 12 * log2(freq / 440.0)))

def tones_to_midi(tones: List[float], output_file: str) -> None:
    from midiutil import MIDIFile
    """Write tones to a MIDI file."""
    midi = MIDIFile(1)
    track = 0
    midi.addTempo(track, 0, 120)
    for i, freq in enumerate(tones):
        pitch = frequency_to_midi_pitch(freq)
        midi.addNote(track, 0, pitch, i, 1, 100)
    with open(output_file, 'wb') as f:
        midi.writeFile(f)


def process_glyph_file(glyph_file: str, output_file: str) -> None:
    """Process a text file of glyphs and produce a MIDI file."""
    content = Path(glyph_file).read_text().strip().split()
    tones = glyphs_to_tones(content)
    tones_to_midi(tones, output_file)


def extract_glyphs_from_abc(abc_content: str) -> List[str]:
    """Extract glyphs from an ABC notation file, ignoring header lines."""
    glyphs: List[str] = []
    for line in abc_content.splitlines():
        if line.startswith(("X:", "T:", "L:", "M:", "K:")):
            continue
        glyphs.extend(line.split())
    return glyphs


def process_abc_file(abc_file: str, output_file: str) -> None:
    """Process an ABC file of glyphs and produce a MIDI file."""
    abc_content = Path(abc_file).read_text()
    glyphs = extract_glyphs_from_abc(abc_content)
    tones = glyphs_to_tones(glyphs)
    tones_to_midi(tones, output_file)
