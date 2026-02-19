# Document Summary — 3D Clinostat Research Package

---

## Paper 1: Development of an Inexpensive 3D Clinostat and Comparison with Other Microgravity Simulators Using *Mycobacterium marinum*

**Type:** Primary research article

### Overview
This paper describes the design and validation of a low-cost 3D clinostat built as an alternative to the commercially available Random Positioning Machine (RPM 2.0) for simulating microgravity conditions in biological experiments. The device uses two independently rotating frames to time-average the gravity vector experienced by a sample to near-zero, mimicking weightlessness.

### Key Methods
- An **Arduino-based accelerometer** system recorded real-time acceleration data from the clinostat during operation.
- The quality of microgravity simulation was quantified using a **distribution score** based on how evenly the acceleration vector is spread across a hemisphere. This was computed using a Fibonacci lattice of 1000 evenly-spaced points (see also Data Sheet 2, Figure 2).
- The clinostat performance was benchmarked against:
  - RPM 2.0 (via onboard accelerometer)
  - RPM 2.0 (via software data output)
  - Computer simulation
- *Mycobacterium marinum* was used as a biological model to test the biological relevance of the simulated microgravity conditions. Experiments evaluated changes in bacterial growth and antibiotic (rifampicin) resistance.

### Key Findings
- The 3D clinostat produced acceleration vector distributions **comparable to RPM 2.0**, validating it as a viable low-cost alternative.
- Operating the clinostat inside a standard incubator caused a **statistically significant temperature increase** (~36.4°C control vs ~36.9°C with clinostat running, p = 0.0327), which must be accounted for in experimental design.
- Biological experiments confirmed that the clinostat produces measurable microgravity-related effects in *M. marinum*, consistent with RPM results.

---

## Paper 2: Time-Averaged Simulated Microgravity (taSMG) Inhibits Proliferation of Lymphoma Cells, L-540 and HDLM-2, Using a 3D Clinostat

**Type:** Primary research article

### Overview
This paper investigates the biological effects of simulated microgravity — referred to as **taSMG (time-averaged simulated microgravity)** — on two Hodgkin lymphoma cell lines: **L-540** and **HDLM-2**. The same 3D clinostat platform described in Paper 1 was used.

### Key Methods
- Lymphoma cells were cultured under taSMG conditions using the 3D clinostat.
- Cell **proliferation rates** were measured and compared between taSMG-exposed and control (static) conditions.

### Key Findings
- taSMG significantly **inhibited proliferation** of both L-540 and HDLM-2 Hodgkin lymphoma cell lines.
- The results suggest that simulated microgravity may have potential relevance as a research tool for understanding cancer cell behavior and possibly informing therapeutic strategies.

---

## Data Sheet 2.PDF — Supplementary Material (for Paper 1)

**Type:** Supplementary figures and code for the clinostat development paper

### Contents
- **Figure 1 — CAD Model of 3D Clinostat v2:** Engineering design of the clinostat with three sample holder types: HARV (Horizontal Axis Rotating Vessel), T25 flask, and Flaskette. Shows the mechanical structure of inner and outer rotating frames.
- **Figure 2 — Quantitating the Distribution of the Acceleration Vector:** Describes the Python-based algorithm that uses a Fibonacci lattice (1000 points on a hemisphere) to compute a distribution score. A higher score means the acceleration vector is more uniformly spread across all directions — the ideal outcome for microgravity simulation.
- **Figure 3 — Incubator Temperature Change Due to Clinostat Operation:** Documents the temperature elevation inside the incubator caused by motor heat generation from clinostat operation, supporting the statistically significant finding reported in Paper 1.
- **Figure 4 — Path and Distribution of Acceleration Vector:** Side-by-side visual comparison of the acceleration vector paths and distribution scores between the 3D clinostat and RPM 2.0, demonstrating comparable performance.
- **Supplementary Code References:** Lists Arduino (C), Java, and Python scripts used for data acquisition and analysis.

---

## Data Sheet 1.XLSX — RPM Optimization Heat Maps and Rankings

**Type:** Computational data appendix (4 spreadsheet tabs)

### Overview
This spreadsheet contains the results of a systematic sweep of inner and outer frame RPM combinations for the 3D clinostat, evaluated at two time windows. The goal is to identify the optimal RPM settings that minimize the time-averaged acceleration magnitude (best microgravity simulation) while maximizing the distribution score (most uniform coverage).

### Sheet Structure

| Sheet | Time Window | Content |
|---|---|---|
| Heat Map (2000–3000 sec) | 33–50 min | Color-coded magnitude matrix across RPM combos |
| Heat Map (5000–6000 sec) | 83–100 min | Same, at later time window |
| Ranking (2000–3000 sec) | 33–50 min | All combos sorted by magnitude and distribution score |
| Ranking (5000–6000 sec) | 83–100 min | Same, at later time window |

### Key Findings
- RPM combinations are evaluated from **0.125 to ~4.0 RPM** for both inner and outer frames.
- The **legend** uses: Blue = best performance, Yellow = 50th percentile, Red = worst performance.
- **Best combinations by lowest magnitude:**
  - At 2000–3000 s: `0.25 : 4.0` RPM (magnitude ≈ 0.00132)
  - At 5000–6000 s: `0.125 : 4.0` RPM (magnitude ≈ 0.000591)
- **Best combinations by highest distribution score:**
  - At 2000–3000 s: `3.75 : 1.375` RPM (score = 501/1000 points)
  - At 5000–6000 s: `3.75 : 0.125` RPM (score = 509/1000 points)
- Combinations where inner and outer frame speeds are **equal produce the worst results** (diagonal of the heat map shows high magnitude values ~0.5), confirming that non-harmonic speed ratios are essential for proper microgravity simulation.

---

## Overall Summary

The documents together form a **complete research package** around a low-cost, open-source 3D clinostat for simulating microgravity:

1. **Paper 1 + Data Sheet 2** establish the device's engineering design, validation methodology, and biological proof-of-concept using *M. marinum*.
2. **Paper 2** demonstrates a direct biological application — showing taSMG inhibits lymphoma cell proliferation.
3. **Data Sheet 1** provides the computational optimization data needed to select the best operating RPM settings, with the key recommendation that **outer frame speed should be significantly higher than inner frame speed** (e.g. 0.25:4.0 or 0.125:4.0) for optimal performance.
