# Changelog — Version History

| Version | Date | Author | Changes |
|:--------|:-----|:-------|:--------|
| v1.0 | July 2026 | Ridhi Jain | Initial repository structure and framework scaffolding |
| v1.5 | August 2026 | Ridhi Jain | Added quantitative simulation engine (Monte Carlo + Scenario Analysis) |
| v2.0 | August 2026 | Ridhi Jain | Full content population: all frameworks, roadmaps, assumptions register, SCOR diagnostic |
| v2.1 | August 2026 | Ridhi Jain | Model recalibration to 18.5% blended take rate (DRHP-consistent); chart generation added |
| v2.2 | August 2026 | Ridhi Jain | GitHub push; README navigation verified; all cross-links validated |

---

## Reproducibility

All analysis is fully reproducible:
```bash
git clone https://github.com/ridhijain709/swiggy-qcommerce-strategy-analysis
pip install pandas numpy matplotlib seaborn scipy openpyxl
python 04-analysis/models/simulation.py
```
Outputs regenerate deterministically with `seed=42`.
