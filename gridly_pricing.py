import streamlit as st

def money(x, currency):
    return f"{'€' if currency == 'EUR' else '$'}{x:,.2f}"

# ---------- Pricing Tables (copy-safe; all braces closed) ----------
PLATFORM_FEES = {
    "BASIC": 0, "TEAM": 0, "ENT 1": 0, "ENT 2": 370, "ENT 3": 740, "ENT 4": 1110, "ENT 5": 1480, "LSP": 915
}

MODULES = {
    "EUR": {
        "CMS": {
            "fee": {"BASIC": 99, "TEAM": 249, "ENT 1": 460, "ENT 2": 460, "ENT 3": 460, "ENT 4": 460, "ENT 5": 460, "LSP": 460},
            "included_seats": {"BASIC": 3, "TEAM": 5, "ENT 1": 10, "ENT 2": 10, "ENT 3": 10, "ENT 4": 10, "ENT 5": 10, "LSP": 10},
            "extra_seat_fee": {"BASIC": 29, "TEAM": 29, "ENT 1": 46, "ENT 2": 46, "ENT 3": 46, "ENT 4": 46, "ENT 5": 46, "LSP": 46},
        },
        "TMS": {
            "fee": {"BASIC": 50, "TEAM": 125, "ENT 1": 230, "ENT 2": 230, "ENT 3": 230, "ENT 4": 230, "ENT 5": 230, "LSP": 230},
            "included_seats": {"BASIC": 1, "TEAM": 2, "ENT 1": 5, "ENT 2": 5, "ENT 3": 5, "ENT 4": 5, "ENT 5": 5, "LSP": 5},
            "extra_seat_fee": {"BASIC": 29, "TEAM": 29, "ENT 1": 46, "ENT 2": 46, "ENT 3": 46, "ENT 4": 46, "ENT 5": 46, "LSP": 46},
        },
        "CAT": {
            "fee": {"BASIC": 140, "TEAM": 280, "ENT 1": 700, "ENT 2": 700, "ENT 3": 700, "ENT 4": 700, "ENT 5": 700, "LSP": 0},
            "included_seats": {"BASIC": 10, "TEAM": 20, "ENT 1": 50, "ENT 2": 50, "ENT 3": 50, "ENT 4": 50, "ENT 5": 50, "LSP": 0},
            "extra_seat_fee": {"BASIC": 14, "TEAM": 14, "ENT 1": 14, "ENT 2": 14, "ENT 3": 14, "ENT 4": 14, "ENT 5": 14, "LSP": 14},
        },
    },
    "USD": {
        "CMS": {
            "fee": {"BASIC": 112, "TEAM": 281, "ENT 1": 520, "ENT 2": 520, "ENT 3": 520, "ENT 4": 520, "ENT 5": 520, "LSP": 520},
            "included_seats": {"BASIC": 3, "TEAM": 5, "ENT 1": 10, "ENT 2": 10, "ENT 3": 10, "ENT 4": 10, "ENT 5": 10, "LSP": 10},
            "extra_seat_fee": {"BASIC": 33, "TEAM": 33, "ENT 1": 52, "ENT 2": 52, "ENT 3": 52, "ENT 4": 52, "ENT 5": 52, "LSP": 52},
        },
        "TMS": {
            "fee": {"BASIC": 57, "TEAM": 141, "ENT 1": 260, "ENT 2": 260, "ENT 3": 260, "ENT 4": 260, "ENT 5": 260, "LSP": 260},
            "included_seats": {"BASIC": 1, "TEAM": 2, "ENT 1": 5, "ENT 2": 5, "ENT 3": 5, "ENT 4": 5, "ENT 5": 5, "LSP": 5},
            "extra_seat_fee": {"BASIC": 33, "TEAM": 33, "ENT 1": 52, "ENT 2": 52, "ENT 3": 52, "ENT 4": 52, "ENT 5": 52, "LSP": 52},
        },
        "CAT": {
            "fee": {"BASIC": 158, "TEAM": 317, "ENT 1": 791, "ENT 2": 791, "ENT 3": 791, "ENT 4": 791, "ENT 5": 791, "LSP": 0},
            "included_seats": {"BASIC": 10, "TEAM": 20, "ENT 1": 50, "ENT 2": 50, "ENT 3": 50, "ENT 4": 50, "ENT 5": 50, "LSP": 0},
            "extra_seat_fee": {"BASIC": 16, "TEAM": 16, "ENT 1": 16, "ENT 2": 16, "ENT 3": 16, "ENT 4": 16, "ENT 5": 16, "LSP": 16},
        },
    },
}
# -------------------------------------------------------------------

def calculate_gridly_pricing(plan, modules, total_platform_seats, total_translation_seats, billing_cycle, currency):
    module_pricing = MODULES[currency]

    included_platform_seats = sum(
        module_pricing[m]["included_seats"].get(plan, 0) for m in modules if m in ["CMS", "TMS"]
    )
    included_translation_seats = sum(
        module_pricing[m]["included_seats"].get(plan, 0) for m in modules if m == "CAT"
    )

    extra_platform_seats = max(total_platform_seats - included_platform_seats, 0)
    extra_translation_seats = max(total_translation_seats - included_translation_seats, 0)

    total_monthly_fee = PLATFORM_FEES.get(plan, 0)

    for m in modules:
        if m in module_pricing:
            total_monthly_fee += module_pricing[m]["fee"].get(plan, 0)

    # Base extra-seat fees from table
    base_platform_extra = module_pricing["CMS"]["extra_seat_fee"].get(plan, 0)
    base_translation_extra = module_pricing["CAT"]["extra_seat_fee"].get(plan, 0)

    # BASIC/TEAM monthly uplift (EUR 35/17; USD 39/19)
    if billing_cycle == "Monthly" and plan in ["BASIC", "TEAM"]:
        platform_extra = 35 if currency == "EUR" else 39
        translation_extra = 17 if currency == "EUR" else 19
    else:
        platform_extra = base_platform_extra
        translation_extra = base_translation_extra

    total_monthly_fee += extra_platform_seats * platform_extra
    total_monthly_fee += extra_translation_seats * translation_extra

    total_monthly_fee = round(total_monthly_fee, 2)
    total_annual_fee = round(total_monthly_fee * 12, 2)

    return (
        total_monthly_fee, total_annual_fee,
        included_platform_seats, extra_platform_seats,
        included_translation_seats, extra_translation_seats
    )

# =========================
# UI
# =========================
st.title("Gridly Pricing Calculator")

currency = st.selectbox("Currency", ["EUR", "USD"])
plan = st.selectbox("Select Plan", ["BASIC", "TEAM", "ENT 1", "ENT 2", "ENT 3", "ENT 4", "ENT 5", "LSP"])
billing_cycle_options = ["Annually"] if plan in ["ENT 1", "ENT 2", "ENT 3", "ENT 4", "ENT 5", "LSP"] else ["Annually", "Monthly"]
billing_cycle = st.radio("Billing Cycle", billing_cycle_options)
modules = st.multiselect("Select Modules", ["CMS", "TMS", "CAT"], default=["CMS", "TMS"])
total_platform_seats = st.number_input("Total Platform Seats", min_value=0, value=0)

translation_input_disabled = "CAT" not in modules
total_translation_seats = st.number_input(
    "Total Translation Seats",
    min_value=0,
    value=0,
    disabled=translation_input_disabled,
)

if st.button("Calculate Pricing"):
    (monthly_fee, annual_fee,
     included_platform_seats, extra_platform_seats,
     included_translation_seats, extra_translation_seats) = calculate_gridly_pricing(
        plan, modules, total_platform_seats, total_translation_seats, billing_cycle, currency
    )

    st.write(f"### Total Monthly Fee: {money(monthly_fee, currency)}")
    st.write(f"### Total Annual Fee: {money(annual_fee, currency)}")
    st.write(f"Plan: {plan}")
    st.write(f"Currency: {currency}")
    st.write(f"Billing Cycle: {billing_cycle}")
    st.write(f"Selected Modules: {', '.join(modules) if modules else 'None'}")
    st.write(f"Included Platform Seats: {included_platform_seats}")
    st.write(f"Extra Platform Seats: {extra_platform_seats}")
    st.write(f"Included Translation Seats: {included_translation_seats}")
    st.write(f"Extra Translation Seats: {extra_translation_seats}")
