# Before making this repository public

This repository comes out of a funded project with industry partners and an experimental partner. Check each item and record the answer before publishing. Delete this file (or keep it private) once done.

## Permissions

- [ ] **Supervisor (Prof. Skoda)** agrees to publishing setups and scripts, and to the licence (MIT for scripts/setups).
- [ ] **Co-authors at OVGU Magdeburg (M. Mansour, D. Thévenin)** agree, in particular on how experimental data are handled.
- [ ] **Experimental data**: may processed experimental profiles used in the figures be redistributed, or only cited? If only cited, the figure scripts must load them from a local path that is not committed.
- [ ] **Project / partner confidentiality**: the project agreement allows publication of these setups. No partner geometry (pump impellers, volutes), partner operating data or internal reports are included.
- [ ] **Journal policy**: the target journal allows sharing code and data alongside the preprint (most encourage it).

## Content

- [ ] Only the generic diverging-channel geometry is included.
- [ ] No absolute paths, cluster usernames or job-script account names in any file (`grep -rn "/home/\|/hsm\|#SBATCH --account" .`).
- [ ] Large fields are on Zenodo, not in git (`git count-objects -vH` stays small; nothing over ~50 MB).
- [ ] Every paper figure has an entry in `figures/README.md` that reproduces it.
- [ ] Funding acknowledgement in `README.md` matches the paper exactly.

## After publishing

- [ ] Create a GitHub release and connect the repository to Zenodo to mint a DOI.
- [ ] Add the DOI to `CITATION.cff`, the paper (data availability statement) and the CV.
- [ ] Update the SSRN record / journal submission with the repository link if allowed.
