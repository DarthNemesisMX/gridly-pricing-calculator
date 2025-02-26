import streamlit as st


def calculate_gridly_pricing(plan, modules, total_platform_seats, total_translation_seats, billing_cycle):
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
    
    module_pricing = {
        "CMS": {"fee": {"BASIC": 99, "TEAM": 249, "ENT 1": 460, "ENT 2": 460, "ENT 3": 460, "ENT 4": 460, "ENT 5": 460, "LSP": 460},
                 "included_seats": {"BASIC": 3, "TEAM": 5, "ENT 1": 10, "ENT 2": 10, "ENT 3": 10, "ENT 4": 10, "ENT 5": 10, "LSP": 10},
                 "extra_seat_fee": {"BASIC": 29, "TEAM": 29, "ENT 1": 46, "ENT 2": 46, "ENT 3": 46, "ENT 4": 46, "ENT 5": 46, "LSP": 46}},
        "TMS": {"fee": {"BASIC": 50, "TEAM": 125, "ENT 1": 230, "ENT 2": 230, "ENT 3": 230, "ENT 4": 230, "ENT 5": 230, "LSP": 230},
                 "included_seats": {"BASIC": 1, "TEAM": 2, "ENT 1": 5, "ENT 2": 5, "ENT 3": 5, "ENT 4": 5, "ENT 5": 5, "LSP": 5},
                 "extra_seat_fee": {"BASIC": 29, "TEAM": 29, "ENT 1": 46, "ENT 2": 46, "ENT 3": 46, "ENT 4": 46, "ENT 5": 46, "LSP": 46}},
        "CAT": {"fee": {"BASIC": 140, "TEAM": 280, "ENT 1": 700, "ENT 2": 700, "ENT 3": 700, "ENT 4": 700, "ENT 5": 700, "LSP": 0},
                 "included_seats": {"BASIC": 10, "TEAM": 20, "ENT 1": 50, "ENT 2": 50, "ENT 3": 50, "ENT 4": 50, "ENT 5": 50, "LSP": 0},
                 "extra_seat_fee": {"BASIC": 14, "TEAM": 14, "ENT 1": 14, "ENT 2": 14, "ENT 3": 14, "ENT 4": 14, "ENT 5": 14, "LSP": 14}}
    }
    
    plan_data = pricing_data.get(plan, {})
    if not plan_data:
        return "Invalid Plan Selected"
    
    included_platform_seats = sum(module_pricing[module]["included_seats"].get(plan, 0) for module in modules if module in ["CMS", "TMS"])
    included_translation_seats = sum(module_pricing[module]["included_seats"].get(plan, 0) for module in modules if module == "CAT")
    
    extra_platform_seats = max(total_platform_seats - included_platform_seats, 0)
    extra_translation_seats = max(total_translation_seats - included_translation_seats, 0)
    
    total_monthly_fee = plan_data["platform_fee"]
    
    for module in modules:
        if module in module_pricing:
            module_data = module_pricing[module]
            base_fee = module_data["fee"].get(plan, 0)
            total_monthly_fee += base_fee
    
    if extra_platform_seats > 0:
        seat_fee = 35 if billing_cycle == "Monthly" and plan in ["BASIC", "TEAM"] else module_pricing["CMS"]["extra_seat_fee"].get(plan, 0)
        total_monthly_fee += extra_platform_seats * seat_fee
    if extra_translation_seats > 0:
        seat_fee = 16 if billing_cycle == "Monthly" and plan in ["BASIC", "TEAM"] else module_pricing["CAT"]["extra_seat_fee"].get(plan, 0)
        total_monthly_fee += extra_translation_seats * seat_fee
    
    return round(total_monthly_fee, 2), included_platform_seats, extra_platform_seats, included_translation_seats, extra_translation_seats

st.title("Gridly Pricing Calculator")

plan = st.selectbox("Select Plan", ["BASIC", "TEAM", "ENT 1", "ENT 2", "ENT 3", "ENT 4", "ENT 5", "LSP"])
billing_cycle_options = ["Annually"] if plan in ["ENT 1", "ENT 2", "ENT 3", "ENT 4", "ENT 5", "LSP"] else ["Annually", "Monthly"]
billing_cycle = st.radio("Billing Cycle", billing_cycle_options)
modules = st.multiselect("Select Modules", ["CMS", "TMS", "CAT"], default=["CMS", "TMS"])
total_platform_seats = st.number_input("Total Platform Seats", min_value=0, value=0)
total_translation_seats = st.number_input("Total Translation Seats", min_value=0, value=0)

if st.button("Calculate Pricing"):
    monthly_fee, included_platform_seats, extra_platform_seats, included_translation_seats, extra_translation_seats = calculate_gridly_pricing(plan, modules, total_platform_seats, total_translation_seats, billing_cycle)
    st.write(f"### Total Monthly Fee: €{monthly_fee}")
    st.write(f"Plan: {plan}")
    st.write(f"Billing Cycle: {billing_cycle}")
    st.write(f"Selected Modules: {', '.join(modules)}")
    st.write(f"Included Platform Seats: {included_platform_seats}")
    st.write(f"Extra Platform Seats: {extra_platform_seats}")
    st.write(f"Included Translation Seats: {included_translation_seats}")
    st.write(f"Extra Translation Seats: {extra_translation_seats}")
