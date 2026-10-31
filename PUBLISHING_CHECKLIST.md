# Before making this repository public

Check each item, then delete this file.

## Permissions

- [ ] **Co-authors (M. Mansour, D. Thévenin, R. Skoda)** agree to the repository, in particular to showing the experimental data and shadowgraphy images (they are already public in the SSRN preprint, but confirm).
- [ ] **Project agreement** (BMWE/IGF 01IF 23051 N, VDMA Pumps + Systems) allows publishing this material. Only the generic diffuser geometry is included; no partner pump data.
- [ ] **Journal policy:** once the paper is accepted, check that the licence lets you keep the figures, graphical abstract and extracted data here (authors can usually reuse their own figures, but confirm), and add the journal reference and DOI to `README.md` and `CITATION.cff`.

## Content

- [ ] Facts and numbers in `docs/` match the final version of the paper.
- [ ] If you want them named, add the exact solver variant and inflow boundary condition used for the paper to `cases/README.md`.
- [ ] No absolute paths, cluster usernames or account names in any file (`grep -rn "/home/\|/hsm" .`).
- [ ] `python figures/make_figures.py` and `python postprocessing/tests/test_postprocessing.py` run cleanly.
