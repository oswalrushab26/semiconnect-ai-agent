# features/reporting.py
from datetime import datetime
from typing import List

class ReportGenerator:
    def __init__(self):
        pass
    
    def generate_weekly_brief(self, watchlist: List[str]) -> str:
        date = datetime.now().strftime("%Y-%m-%d")
        report = f"""
# Weekly Semiconductor Market Brief
**Week Ending:** {date}

## Market Overview
This week's semiconductor market shows mixed signals with ongoing supply chain adjustments.

## Companies in Focus
"""
        for company in watchlist:
            report += f"\n### {company}\n"
            report += f"- **Status:** Active monitoring\n"
            report += f"- **Key Events:** No major announcements this week\n"
            report += f"- **Outlook:** Neutral\n"
        
        report += """
## Supply Chain Update
- OSAT capacity: Stable
- Material availability: Moderate constraints
- Equipment lead times: Extended

## Key Trends
1. AI chip demand continues to drive growth
2. Supply chain diversification efforts ongoing
3. Government incentives boosting domestic production

## Recommendations
1. Monitor OSAT capacity for potential bottlenecks
2. Evaluate alternative suppliers for critical materials
3. Consider strategic inventory building
"""
        return report
    
    def generate_competitor_analysis(self, company: str, competitors: List[str]) -> str:
        """Generate competitor analysis report"""
        date = datetime.now().strftime("%Y-%m-%d")
        report = f"""
# Competitor Analysis Report
**Company:** {company}
**Analysis Date:** {date}

## Competitor Overview
"""
        for comp in competitors:
            report += f"""
### {comp}
- **Market Position:** Major player
- **Strengths:** Strong R&D, established customer base
- **Weaknesses:** High operating costs, limited diversification
- **Recent Developments:** Investing in new technologies
- **Threat Level:** Medium
"""
        
        report += """
## Comparative Analysis
| Metric | Target | Competitor Avg | Gap |
|--------|--------|----------------|-----|
| Market Share | 15% | 20% | -5% |
| R&D Spend | 12% | 10% | +2% |
| Revenue Growth | 8% | 6% | +2% |

## Recommendations
1. Focus on differentiation
2. Accelerate R&D in emerging areas
3. Consider strategic partnerships
"""
        return report
    
    def generate_supply_chain_report(self) -> str:
        """Generate supply chain health report"""
        date = datetime.now().strftime("%Y-%m-%d")
        return f"""
# Supply Chain Health Report
**Date:** {date}

## Risk Assessment Summary
- **Overall Risk Level:** Moderate
- **Critical Risks:** 2
- **High Risks:** 3
- **Medium Risks:** 5
- **Low Risks:** 8

## Key Risks
1. **Geopolitical Tensions**
   - Impact: High
   - Likelihood: Moderate
   - Mitigation: Diversify suppliers

2. **Material Shortages**
   - Impact: High
   - Likelihood: High
   - Mitigation: Strategic inventory

3. **Logistics Constraints**
   - Impact: Medium
   - Likelihood: High
   - Mitigation: Multiple shipping routes

## Recommendations
1. Establish dual sourcing for critical components
2. Increase inventory buffer for high-risk items
3. Invest in supply chain visibility tools
4. Build relationships with alternative suppliers
"""
    
    