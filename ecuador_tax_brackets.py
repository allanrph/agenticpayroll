#!/usr/bin/env python3
"""
Dummy tax bracket data for Ecuador based on the TaxBracket structure.
This data represents the 2024 Ecuadorian income tax brackets.
"""

from app.domains.country_profile import TaxBracket

# Ecuador 2024 Income Tax Brackets (Annual Income in USD)
# Based on the current Ecuadorian tax system

ECUADOR_TAX_BRACKETS = [
    # First bracket: 0 to $11,200 (exempt)
    TaxBracket(from_amount=0.0, up_to=11200.0, rate=0.0, fixed=0.0),
    # Second bracket: $11,200.01 to $14,400
    TaxBracket(from_amount=11200.01, up_to=14400.0, rate=0.05, fixed=0.0),
    # Third bracket: $14,400.01 to $18,000
    TaxBracket(from_amount=14400.01, up_to=18000.0, rate=0.10, fixed=160.0),
    # Fourth bracket: $18,000.01 to $21,600
    TaxBracket(from_amount=18000.01, up_to=21600.0, rate=0.12, fixed=520.0),
    # Fifth bracket: $21,600.01 to $24,000
    TaxBracket(from_amount=21600.01, up_to=24000.0, rate=0.15, fixed=952.0),
    # Sixth bracket: $24,000.01 to $27,600
    TaxBracket(from_amount=24000.01, up_to=27600.0, rate=0.20, fixed=1312.0),
    # Seventh bracket: $27,600.01 to $36,000
    TaxBracket(from_amount=27600.01, up_to=36000.0, rate=0.25, fixed=2024.0),
    # Eighth bracket: $36,000.01 to $48,000
    TaxBracket(from_amount=36000.01, up_to=48000.0, rate=0.30, fixed=3134.0),
    # Ninth bracket: $48,000.01 to $60,000
    TaxBracket(from_amount=48000.01, up_to=60000.0, rate=0.35, fixed=6734.0),
    # Tenth bracket: Above $60,000
    TaxBracket(
        from_amount=60000.01, up_to=None, rate=0.37, fixed=10934.0  # No upper limit
    ),
]

# Alternative representation with more detailed brackets for testing
ECUADOR_DETAILED_TAX_BRACKETS = [
    # Exempt income
    TaxBracket(from_amount=0.0, up_to=11200.0, rate=0.0, fixed=0.0),
    # 5% bracket
    TaxBracket(from_amount=11200.01, up_to=14400.0, rate=0.05, fixed=0.0),
    # 10% bracket
    TaxBracket(from_amount=14400.01, up_to=18000.0, rate=0.10, fixed=160.0),
    # 12% bracket
    TaxBracket(from_amount=18000.01, up_to=21600.0, rate=0.12, fixed=520.0),
    # 15% bracket
    TaxBracket(from_amount=21600.01, up_to=24000.0, rate=0.15, fixed=952.0),
    # 20% bracket
    TaxBracket(from_amount=24000.01, up_to=27600.0, rate=0.20, fixed=1312.0),
    # 25% bracket
    TaxBracket(from_amount=27600.01, up_to=36000.0, rate=0.25, fixed=2024.0),
    # 30% bracket
    TaxBracket(from_amount=36000.01, up_to=48000.0, rate=0.30, fixed=3134.0),
    # 35% bracket
    TaxBracket(from_amount=48000.01, up_to=60000.0, rate=0.35, fixed=6734.0),
    # 37% bracket (highest)
    TaxBracket(from_amount=60000.01, up_to=None, rate=0.37, fixed=10934.0),
]


# Sample usage and testing data
def get_ecuador_tax_brackets():
    """Return Ecuador tax brackets for use in the application."""
    return ECUADOR_TAX_BRACKETS


def get_ecuador_detailed_tax_brackets():
    """Return detailed Ecuador tax brackets for testing."""
    return ECUADOR_DETAILED_TAX_BRACKETS


# Example usage
if __name__ == "__main__":
    print("Ecuador Tax Brackets 2024:")
    print("=" * 50)

    for i, bracket in enumerate(ECUADOR_TAX_BRACKETS, 1):
        print(f"Bracket {i}:")
        print(
            f"  From: ${bracket.from_amount:,.2f}"
            if bracket.from_amount
            else "  From: $0.00"
        )
        print(
            f"  Up to: ${bracket.up_to:,.2f}" if bracket.up_to else "  Up to: No limit"
        )
        print(f"  Rate: {bracket.rate:.1%}")
        print(f"  Fixed: ${bracket.fixed:,.2f}" if bracket.fixed else "  Fixed: $0.00")
        print()
