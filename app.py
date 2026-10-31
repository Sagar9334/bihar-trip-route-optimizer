from flask import Flask, render_template, request, redirect, url_for
import heapq

app = Flask(__name__)

# =========================================================
# 1. GRAPH DATA STRUCTURE (Bihar Inter-District Network)
# =========================================================
graph = {
    "Patna": [
        {"node": "Vaishali", "mode": "Bus", "cost": 80},
        {"node": "Nalanda", "mode": "Train/Bus", "cost": 120},
        {"node": "Bodh Gaya", "mode": "Train", "cost": 150},
        {"node": "Sasaram", "mode": "Train", "cost": 140},
        {"node": "Valmiki Nagar", "mode": "Train/Bus", "cost": 250},
        {"node": "Sitamarhi", "mode": "Bus", "cost": 130}
    ],
    "Nalanda": [
        {"node": "Rajgir", "mode": "Auto/Bus", "cost": 30},
        {"node": "Pawapuri", "mode": "Auto/E-Rickshaw", "cost": 25},
        {"node": "Patna", "mode": "Train/Bus", "cost": 120}
    ],
    "Rajgir": [
        {"node": "Nalanda", "mode": "Auto/Bus", "cost": 30},
        {"node": "Bodh Gaya", "mode": "Taxi/Bus", "cost": 180},
        {"node": "Pawapuri", "mode": "Auto", "cost": 40}
    ],
    "Pawapuri": [
        {"node": "Nalanda", "mode": "Auto", "cost": 25},
        {"node": "Rajgir", "mode": "Auto", "cost": 40}
    ],
    "Bodh Gaya": [
        {"node": "Rajgir", "mode": "Taxi/Bus", "cost": 180},
        {"node": "Patna", "mode": "Train", "cost": 150},
        {"node": "Sasaram", "mode": "Train", "cost": 110}
    ],
    "Sasaram": [
        {"node": "Kaimur", "mode": "Bus/Cab", "cost": 90},
        {"node": "Patna", "mode": "Train", "cost": 140},
        {"node": "Bodh Gaya", "mode": "Train", "cost": 110}
    ],
    "Kaimur": [
        {"node": "Sasaram", "mode": "Bus/Cab", "cost": 90}
    ],
    "Vaishali": [
        {"node": "Patna", "mode": "Bus", "cost": 80},
        {"node": "Sitamarhi", "mode": "Bus", "cost": 110}
    ],
    "Sitamarhi": [
        {"node": "Vaishali", "mode": "Bus", "cost": 110},
        {"node": "Patna", "mode": "Bus", "cost": 130}
    ],
    "Valmiki Nagar": [
        {"node": "Patna", "mode": "Train/Bus", "cost": 250}
    ]
}

# =========================================================
# 2. 5 DEDICATED TRAVEL CIRCUITS DATA
# =========================================================
circuits_list = [
    {
        "id": 1,
        "title": "Circuit 1: Spiritual & Heritage Trail",
        "days": "4 to 5 Days",
        "tag": "Buddhist & Jain Pilgrimage",
        "route": ["Patna", "Vaishali", "Nalanda", "Pawapuri", "Rajgir", "Bodh Gaya"],
        "highlights": "Mahabodhi Temple, Nalanda University Ruins, Jal Mandir & Glass Bridge"
    },
    {
        "id": 2,
        "title": "Circuit 2: Eco-Adventure & Wildlife",
        "days": "3 Days",
        "tag": "Nature & Wildlife",
        "route": ["Patna", "Valmiki Nagar", "Rajgir"],
        "highlights": "Valmiki Tiger Reserve, Jungle Safari, River Trekking & Zoo Safari"
    },
    {
        "id": 3,
        "title": "Circuit 3: Waterfalls & Historical Forts",
        "days": "2 to 3 Days",
        "tag": "Scenic & Monuments",
        "route": ["Patna", "Sasaram", "Kaimur"],
        "highlights": "Tomb of Sher Shah Suri, Telhar Kund Waterfall & Karkat Waterfall"
    },
    {
        "id": 4,
        "title": "Circuit 4: Ramayana & Culture Trail",
        "days": "2 Days",
        "tag": "Mythological & History",
        "route": ["Patna", "Sitamarhi", "Vaishali"],
        "highlights": "Mata Sita Janmasthali (Janaki Temple), Ashokan Pillar & Relic Stupa"
    },
    {
        "id": 5,
        "title": "Circuit 5: Patna Capital Experience",
        "days": "1 to 2 Days",
        "tag": "Urban Exploration",
        "route": ["Patna", "Vaishali"],
        "highlights": "Golghar, Bihar Museum, Takht Sri Patna Sahib & JP Ganga Path"
    }
]

# Destination cards & cost lookup
destinations = [
    {"id": "bodhgaya", "name": "Bodh Gaya", "description": "Mahabodhi Temple, Bodhi Tree & 80ft Buddha Statue", "circuit": "Circuit 1", "low_food": 300, "low_hotel": 500, "med_food": 700, "med_hotel": 1500, "high_food": 1500, "high_hotel": 4000},
    {"id": "rajgir", "name": "Rajgir", "description": "Glass Bridge, Zoo Safari, Ropeway & Vishwa Shanti Stupa", "circuit": "Circuit 1", "low_food": 250, "low_hotel": 400, "med_food": 600, "med_hotel": 1200, "high_food": 1200, "high_hotel": 3500},
    {"id": "nalanda", "name": "Nalanda", "description": "Ancient Nalanda University Ruins & Hiuen Tsang Hall", "circuit": "Circuit 1", "low_food": 200, "low_hotel": 400, "med_food": 500, "med_hotel": 1000, "high_food": 1000, "high_hotel": 2500},
    {"id": "pawapuri", "name": "Pawapuri", "description": "Jal Mandir Lotus Temple (Nirvana Sthan)", "circuit": "Circuit 1", "low_food": 200, "low_hotel": 350, "med_food": 450, "med_hotel": 900, "high_food": 900, "high_hotel": 2000},
    {"id": "valmiki", "name": "Valmiki Nagar", "description": "Tiger Reserve, Jungle Safari & River Trekking", "circuit": "Circuit 2", "low_food": 350, "low_hotel": 600, "med_food": 800, "med_hotel": 1800, "high_food": 1500, "high_hotel": 4000},
    {"id": "sasaram", "name": "Sasaram", "description": "Tomb of Sher Shah Suri in Artificial Lake", "circuit": "Circuit 3", "low_food": 200, "low_hotel": 400, "med_food": 500, "med_hotel": 1100, "high_food": 1000, "high_hotel": 2500},
    {"id": "kaimur", "name": "Kaimur", "description": "Telhar Kund, Karkat Waterfall & Wildlife Sanctuary", "circuit": "Circuit 3", "low_food": 200, "low_hotel": 400, "med_food": 500, "med_hotel": 1000, "high_food": 1000, "high_hotel": 2200},
    {"id": "sitamarhi", "name": "Sitamarhi", "description": "Mata Sita Janmasthali & Janaki Temple", "circuit": "Circuit 4", "low_food": 200, "low_hotel": 350, "med_food": 450, "med_hotel": 900, "high_food": 900, "high_hotel": 2000},
    {"id": "vaishali", "name": "Vaishali", "description": "Ashokan Pillar, World's First Republic & Stupas", "circuit": "Circuit 4", "low_food": 200, "low_hotel": 400, "med_food": 500, "med_hotel": 1000, "high_food": 1000, "high_hotel": 2500},
    {"id": "patna", "name": "Patna", "description": "Golghar, Bihar Museum, Takht Sri Patna Sahib & Ganga Drive", "circuit": "Circuit 5", "low_food": 300, "low_hotel": 600, "med_food": 800, "med_hotel": 1800, "high_food": 1800, "high_hotel": 4500}
]

# =========================================================
# 3. INTER-STATE TRANSIT COST ENGINE
# =========================================================
def get_transit_to_patna(source, budget_level):
    parts = [p.strip() for p in source.split(',')]
    district = parts[0]
    state = parts[1] if len(parts) > 1 else "Bihar"
    budget = budget_level.lower()

    if district.lower() == "patna":
        return None

    if state.lower() == "bihar":
        if budget == "low":
            return {"node": "Patna (Transit Hub)", "mode": "Local Express Train / Bus", "cost": 120}
        elif budget in ["med", "medium"]:
            return {"node": "Patna (Transit Hub)", "mode": "AC Intercity / AC Bus", "cost": 300}
        else:
            return {"node": "Patna (Transit Hub)", "mode": "Private Intercity Cab", "cost": 1400}

    # Neighboring States
    neighbor_states = ["jharkhand", "uttar pradesh", "west bengal"]
    if any(ns in state.lower() for ns in neighbor_states):
        if budget == "low":
            return {"node": "Patna (Gateway)", "mode": "Express Train (Sleeper)", "cost": 350}
        elif budget in ["med", "medium"]:
            return {"node": "Patna (Gateway)", "mode": "Superfast Train (3AC)", "cost": 1050}
        else:
            return {"node": "Patna (Gateway)", "mode": "Direct Flight / AC Cab", "cost": 3200}

    # Rest of India (Haryana, Delhi, Punjab, Maharashtra, Rajasthan, Gujarat, etc.)
    if budget == "low":
        return {"node": "Patna (Gateway)", "mode": "Superfast Express Train (Sleeper)", "cost": 650}
    elif budget in ["med", "medium"]:
        return {"node": "Patna (Gateway)", "mode": "Superfast / Rajdhani Express (3AC)", "cost": 1950}
    else:
        return {"node": "Patna (Gateway)", "mode": "Direct Flight to Patna Airport", "cost": 5200}

# =========================================================
# 4. DIJKSTRA ROUTE CALCULATOR (Single & Multi-Hop)
# =========================================================
def calculate_dijkstra_route(source, end_destination, budget_level="low"):
    parts = [p.strip() for p in source.split(',')]
    start_clean = parts[0]
    end_clean = end_destination.strip()

    extra_cost = 0
    transit_step = None

    # Agar source direct Bihar graph network me nahi hai (jaise Palwal, Mumbai, Delhi)
    if start_clean not in graph:
        transit_step = get_transit_to_patna(source, budget_level)
        real_start = "Patna"
        if transit_step:
            extra_cost = transit_step["cost"]
    else:
        real_start = start_clean

    if real_start.lower() == end_clean.lower():
        if transit_step:
            return {"total_travel_cost": extra_cost, "path": [transit_step]}
        return {"total_travel_cost": 0, "path": []}

    pq = [(0, real_start, [])]
    visited = set()

    while pq:
        cost, current, path = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)

        if current.lower() == end_clean.lower():
            final_path = path
            if transit_step:
                final_path = [transit_step] + final_path
            return {"total_travel_cost": cost + extra_cost, "path": final_path}

        for neighbor in graph.get(current, []):
            next_node = neighbor["node"]
            step_cost = neighbor["cost"]
            mode = neighbor["mode"]
            if next_node not in visited:
                new_step = {"node": next_node, "mode": mode, "cost": step_cost}
                heapq.heappush(pq, (cost + step_cost, next_node, path + [new_step]))

    fallback_step = {"node": end_clean, "mode": "Local Transit Bus", "cost": 150}
    final_path = [fallback_step]
    if transit_step:
        final_path = [transit_step] + final_path
    return {"total_travel_cost": 150 + extra_cost, "path": final_path}

# =========================================================
# 5. FLASK WEB ROUTES
# =========================================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/details')
def details():
    return render_template('user_details.html')

@app.route('/trips', methods=['GET', 'POST'])
def trips():
    user_name = request.form.get('name', 'Traveler')
    user_location = request.form.get('location', 'Patna, Bihar')
    return render_template('trips.html', name=user_name, location=user_location, destinations=destinations)

@app.route('/circuits')
def circuits():
    source = request.args.get('source', 'Patna, Bihar')
    return render_template('circuits.html', circuits=circuits_list, source=source)

@app.route('/select_circuit_budget')
def select_circuit_budget():
    circuit_id = int(request.args.get('circuit_id', 1))
    source = request.args.get('source', 'Patna, Bihar')
    circuit = next((c for c in circuits_list if c['id'] == circuit_id), circuits_list[0])
    return render_template('circuit_budget.html', circuit=circuit, source=source)

@app.route('/calculate_circuit')
def calculate_circuit():
    circuit_id = int(request.args.get('circuit_id', 1))
    budget_level = request.args.get('budget', 'Low').lower()
    source = request.args.get('source', 'Patna, Bihar')

    circuit = next((c for c in circuits_list if c['id'] == circuit_id), circuits_list[0])
    route_nodes = circuit['route']

    legs = []
    total_travel_cost = 0

    # 1. State / District Transit to Patna Hub (Leg 1)
    transit_leg = get_transit_to_patna(source, budget_level)
    if transit_leg:
        legs.append({
            'from': source,
            'to': transit_leg['node'],
            'mode': transit_leg['mode'],
            'cost': transit_leg['cost']
        })
        total_travel_cost += transit_leg['cost']

    # 2. Sequential Bihar Circuit Legs
    for i in range(len(route_nodes) - 1):
        from_node = route_nodes[i]
        to_node = route_nodes[i + 1]
        
        path_res = calculate_dijkstra_route(from_node, to_node, budget_level)
        leg_cost = path_res['total_travel_cost']
        total_travel_cost += leg_cost

        mode_str = path_res['path'][0]['mode'] if path_res['path'] else 'Bus/Auto'

        legs.append({
            'from': from_node,
            'to': to_node,
            'mode': mode_str,
            'cost': leg_cost
        })

    # 3. Stay & Food calculation
    stops_breakdown = []
    total_food_cost = 0
    total_hotel_cost = 0

    for stop_name in route_nodes:
        d_info = next((d for d in destinations if d['name'].lower() == stop_name.lower()), None)
        f_cost = d_info.get(f'{budget_level}_food', 250) if d_info else 250
        h_cost = d_info.get(f'{budget_level}_hotel', 400) if d_info else 400

        total_food_cost += f_cost
        total_hotel_cost += h_cost

        stops_breakdown.append({
            'name': stop_name,
            'food_cost': f_cost,
            'hotel_cost': h_cost,
            'total_stop': f_cost + h_cost
        })

    grand_total = total_travel_cost + total_food_cost + total_hotel_cost

    return render_template(
        'circuit_result.html',
        circuit=circuit,
        source=source,
        budget=budget_level.capitalize(),
        legs=legs,
        stops_breakdown=stops_breakdown,
        total_travel_cost=total_travel_cost,
        total_food_cost=total_food_cost,
        total_hotel_cost=total_hotel_cost,
        grand_total=grand_total
    )

@app.route('/select_budget')
def select_budget():
    source = request.args.get('source', 'Patna, Bihar')
    dest = request.args.get('dest', 'Bodh Gaya')
    return render_template('budget_select.html', source=source, dest=dest)

@app.route('/calculate')
def calculate():
    source = request.args.get('source', 'Patna, Bihar')
    dest = request.args.get('dest', 'Bodh Gaya')
    budget = request.args.get('budget', 'Low')
    budget_level = budget.lower()

    dest_info = next((d for d in destinations if d['name'].lower() == dest.lower()), destinations[0])
    best_path = calculate_dijkstra_route(source, dest, budget_level)

    return render_template('result.html', source=source, dest=dest, budget=budget, best_path=best_path, dest_info=dest_info)

if __name__ == '__main__':
    app.run(debug=True)