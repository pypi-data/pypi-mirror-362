# PyXplore

**PyXplore** is a comprehensive Python package for crystal structure determination and refinement. Developed by Mr. Bin Cao since 2020, this toolkit has undergone five years of continuous development and evolution. It is part of a larger AI-driven research initiative for automated crystal analysis.

## Overview

PyXplore is designed to support the refinement and analysis of various spectroscopic data, including:

- **X-ray Diffraction (XRD)**
- **X-ray Photoelectron Spectroscopy (XPS)**
- **Extended X-ray Absorption Fine Structure (EXAFS)**

It provides a unified framework for integrating experimental and simulated data, machine learning-based identification, and physics-based structural refinement.

## Features

- Raw powder XRD database construction:
  - **Simulated data**: SimXRD-4M (*ICLR*, 2025)
  - **Experimental data**: Opxrd (*Advanced Intelligent Discovery*, 2025)
- Pattern recognition:
  - **CPICANN** (*IUCrJ*, 2024)
- Crystal structure phase identification system:
  - **XQueryer** (2025)
- Structure refinement module:
  - **WPEM** (to be published, expected 2026)

## Installation

You can install PyXplore via pip:

```bash
pip install pyxplore
