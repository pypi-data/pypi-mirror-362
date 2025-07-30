"""Core utilities for SAOCC placeholder operations."""

def process_file(input_file: str, output_file: str) -> None:
    """A minimal passthrough that copies input to output."""
    with open(input_file, 'r') as f_in:
        content = f_in.read()
    with open(output_file, 'w') as f_out:
        f_out.write(content)
