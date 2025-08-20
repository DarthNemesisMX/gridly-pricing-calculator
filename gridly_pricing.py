import streamlit as st

def money(x, currency):
    symbol = "€" if currency == "EUR" else "$"
    return f"{symbol}{x:,.2f}"

def calculate_gridly_pricing(plan, modules, total_platform_seats, total_translation_seats, billing_cycle, currency):
    # Platform fees (monthly), same in both currencies unless you give USD values
    pricing_data = {
        "BASIC": {"platform_fee": 0},
        "TEAM": {"platform_fee": 0},
        "ENT 1": {"platform_fee": 0},
        "ENT 2": {"platform_fee": 370},
        "ENT 3": {"platform_fee": 740},
        "ENT 4": {"platform_fee": 1110},
        "ENT 5": {"platform_fee": 1480},
        "LSP": {"platform_fee": 915}
    }

    # === EUR tables ===
    module_pricing_EUR = {
        "CMS": {
            "fee": {"BASIC": 99, "TEAM": 249, "ENT 1": 460, "ENT 2": 460, "ENT 3": 460, "ENT 4": 460, "ENT 5": 460, "LSP": 460},
            "included_seats": {"BASIC": 3, "TEAM": 5, "ENT 1": 10, "ENT 2": 10, "ENT 3": 10, "ENT 4": 10, "ENT 5": 10, "LSP": 10},
            "extra_seat_fee": {"BASIC": 29, "TEAM": 29, "ENT 1": 46, "ENT 2": 46, "ENT 3": 46, "ENT 4": 46, "ENT 5": 46, "LSP": 46}
        },
        "TMS": {
            "fee": {"BASIC": 50, "TEAM": 125, "ENT 1": 230, "ENT 2": 230, "ENT 3": 230, "ENT 4": 230, "ENT 5": 230, "LSP": 230},
            "included_seats": {"BASIC": 1, "TEAM": 2, "ENT 1": 5, "ENT 2": 5, "ENT 3": 5, "ENT 4": 5, "ENT 5": 5, "LSP": 5},
            "extra_seat_fee": {"BASIC": 29, "TEAM": 29, "ENT 1": 46, "ENT 2": 46, "ENT 3": 46, "ENT 4": 46, "ENT 5": 46, "LSP": 46}
        },
        "CAT": {
            "fee": {"BASIC": 140, "TEAM": 280, "ENT 1": 700, "ENT 2": 700, "ENT 3": 700, "ENT 4": 700, "ENT 5": 700, "LSP": 0},
            "included_seats": {"BASIC": 10, "TEAM": 20, "ENT 1": 50, "ENT 2": 50, "ENT 3": 50, "ENT 4": 50, "ENT 5": 50, "LSP": 0},
            "extra_seat_fee": {"BASIC": 14, "TEAM": 14, "ENT 1": 14,
