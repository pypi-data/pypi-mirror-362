# PRISM OLE Handler

[![CI](https://github.com/armish/prism-ole-handler/actions/workflows/ci.yml/badge.svg)](https://github.com/armish/prism-ole-handler/actions/workflows/ci.yml)

Extract and insert GraphPad PRISM objects from Microsoft Office documents (PowerPoint, Word, Excel) on macOS.

## Background

Microsoft Office for Mac doesn't support direct editing of embedded PRISM objects (OLE), unlike Windows. This package provides tools to extract embedded PRISM objects from Office documents so they can be edited in PRISM and re-embedded.

Currently supports:
- **PowerPoint** (.pptx) - Full support
- **Word** (.docx) - Planned
- **Excel** (.xlsx) - Planned

## Installation

### From PyPI (recommended)
```bash
pip install prism-ole-handler
```

### From source
```bash
git clone https://github.com/armish/prism-ole-handler.git
cd prism-ole-handler
pip install -e .
```

### Development installation
```bash
pip install -e ".[dev]"

# Install Git hooks for code quality checks
./scripts/install-hooks.sh
```

## Usage

### Extraction:
```bash
# Extract from all slides
prism-extract presentation.pptx -o output_folder

# Extract from specific slide
prism-extract presentation.pptx --slide 2 -o output_folder

# Extract from multiple slides
prism-extract presentation.pptx --slide 2 --slide 3 --slide 5 -o output_folder

# Extract from multiple slides (comma-separated)
prism-extract presentation.pptx --slides 2,3,5 -o output_folder

# Customize filename padding (default is 3 digits)
prism-extract presentation.pptx -o output_folder --padding 2  # slide06_object04_prism.pzfx
prism-extract presentation.pptx -o output_folder --padding 1  # slide6_object4_prism.pzfx
```

This provides:
- Selective extraction by slide number
- Better OLE compound document parsing
- Slide number tracking for each object
- More detailed extraction information

## Output

Extracted files will be saved with descriptive names:
- `slide001_object001.pzfx` - PRISM file from slide 1 (default 3-digit padding)
- `slide02_object01.pzfx` - With 2-digit padding (`--padding 2`)
- `slide2_object1.pzfx` - With 1-digit padding (`--padding 1`)
- `object001_stream_Package.bin` - Extracted OLE stream for investigation

## How it works

1. PPTX files are ZIP archives containing XML and embedded objects
2. Embedded objects are stored in `ppt/embeddings/` as .bin files
3. These .bin files are often OLE compound documents containing PRISM data
4. The tool extracts and identifies PRISM XML data from these containers

## Insertion

To re-insert updated PRISM objects back into PowerPoint:

```bash
# Update an existing slide (replace existing embedding)
prism-insert presentation.pptx --slide 2 --prism updated_graph.pzfx

# Insert into empty slide
prism-insert presentation.pptx --slide 3 --prism new_graph.pzfx

# Create new slide with PRISM object
prism-insert presentation.pptx --slide 10 --prism graph.pzfx --create-new

# Update multiple slides
prism-insert presentation.pptx --slide 2 --prism graph1.pzfx --slide 3 --prism graph2.pzfx

# Add to slides that already have embeddings
prism-insert presentation.pptx --slide 2 --prism additional_graph.pzfx --force-insert
```

The insertion tool:
- **Replaces** existing embeddings by default
- **Inserts** into empty slides automatically
- **Creates new slides** with `--create-new` flag
- **Adds multiple objects** to slides with `--force-insert`
- Creates a backup of the original file
- Updates the OLE containers with new PRISM data
- Preserves the visual representation streams
- Maintains all PowerPoint relationships

## Complete Workflow

1. **Extract PRISM objects from PowerPoint:**
   ```bash
   prism-extract presentation.pptx -o extracted_files
   ```

2. **Edit the extracted .pzfx files in GraphPad PRISM**

3. **Insert the updated files back into PowerPoint:**
   ```bash
   # Replace existing object
   prism-insert presentation.pptx --slide 2 --prism extracted_files/slide2_updated.pzfx
   
   # Add to new slide
   prism-insert presentation.pptx --slide 10 --prism extracted_files/new_graph.pzfx --create-new
   ```

## Python API

You can also use the package programmatically:

```python
from prism_ole_handler import PrismExtractor, PrismInserter

# Extract PRISM objects from PowerPoint
extractor = PrismExtractor("presentation.pptx")
extractor.extract_prism_objects("output_folder", selected_slides=[2, 3])

# Customize filename padding
extractor.extract_prism_objects("output_folder", padding=2)  # slide06_object04_prism.pzfx

# Insert PRISM objects into PowerPoint
inserter = PrismInserter("presentation.pptx")
inserter.insert_prism_object(slide_num=2, prism_file_path="graph.pzfx")
```

## Limitations

- OLE files have size constraints - very large PRISM files may not fit
- Complex OLE structures may require manual investigation
- Visual representation is preserved but may not reflect all changes
- Only `.pzfx` format supported for insertion (not `.prism` files)

## File Format Notes

- **Extraction**: Creates `.pzfx` files that can be opened in PRISM
- **Insertion**: Requires `.pzfx` files (not `.prism` files)
- **Conversion**: Open `.prism` files in PRISM and save as `.pzfx` format

## Development

### Setting up for development

1. Clone the repository and install in editable mode:
```bash
git clone https://github.com/armish/prism-ole-handler.git
cd prism-ole-handler
pip install -e ".[dev]"
```

2. Install Git hooks for code quality checks:
```bash
./scripts/install-hooks.sh
```

### Code Quality

The project uses several tools to maintain code quality:

- **Black**: Code formatting
- **pytest**: Unit testing
- **Git hooks**: Automatic pre-push checks

Before pushing changes, the pre-push hook will automatically:
- Check code formatting with Black
- Run all unit tests  
- Verify package imports

### Running tests locally

```bash
# Run all tests
python -m pytest tests/ -v

# Check code formatting
black --check prism_ole_handler/ tests/

# Auto-fix formatting
black prism_ole_handler/ tests/
```

### Manual quality checks

If you prefer to run checks manually before committing:

```bash
# Format code
black prism_ole_handler/ tests/

# Run tests
python -m pytest tests/ -v

# Verify everything is ready
black --check prism_ole_handler/ tests/
```