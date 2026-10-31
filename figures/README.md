# Figures

Every figure in the paper should be reproducible from this folder. Small processed data live in `data/`; plotting is done by one script (or notebook) per figure.

| Paper figure | Content | Script | Data |
|---|---|---|---|
| Fig. 1 | Geometry and surface structures | – (drawing) | – |
| Fig. … | Validation against experiment | `fig_validation.py` | `data/validation_*.csv` |
| Fig. … | Gas accumulation, baseline vs. structures | `fig_accumulation.py` | `data/accumulation_*.csv` |
| Fig. … | Bubble size (d₃₂) / population-balance rates | `fig_pbm.py` | `data/pbm_*.csv` |

The paper figures were made with pgfplots/TikZ; the `.tex` sources can live here too (`tikz/`), reading the same CSV files.
