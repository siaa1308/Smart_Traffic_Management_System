import tkinter as tk
import random
import socket
import threading

WIDTH, HEIGHT = 1000, 200
LANE_Y = HEIGHT // 2
SIGNAL_X = WIDTH // 2
VEHICLE_SIZE = 30
VEHICLE_GAP = 10

class TrafficSim:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Traffic Management System (Pedestrian Fix)")

        self.vehicle_count_label = tk.Label(root, text="Vehicles: 0", font=("Arial", 12))
        self.vehicle_count_label.pack()

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="lightgray")
        self.canvas.pack()

        self.canvas.create_rectangle(0, LANE_Y - 50, WIDTH, LANE_Y + 50, fill="gray", outline="black")
        self.canvas.create_line(0, LANE_Y, WIDTH, LANE_Y, fill="white", dash=(4, 4))

        self.signal_color = "red"
        self.signal = self.canvas.create_oval(SIGNAL_X - 10, LANE_Y - 40, SIGNAL_X + 10, LANE_Y - 20, fill=self.signal_color)

        self.vehicles = []
        self.vehicle_types = ['car', 'truck', 'ambulance']
        self.ambulance_count = 0

        self.pedestrians = []

        # Socket setup
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', 12345))

        threading.Thread(target=self.signal_update_loop, daemon=True).start()

        self.spawn_vehicle()
        self.spawn_pedestrian()
        self.move_vehicles()
        self.move_pedestrians()

    def spawn_vehicle(self):
        x = 0
        y = LANE_Y - VEHICLE_SIZE // 2
        vehicle_type = random.choices(self.vehicle_types, weights=[4, 2, 4])[0]
        if vehicle_type == 'ambulance' and self.ambulance_count >= 2:
            vehicle_type = 'car'
        if vehicle_type == 'ambulance':
            self.ambulance_count += 1

        color = {'car': 'blue', 'truck': 'orange', 'ambulance': 'white'}[vehicle_type]
        text = 'AMB' if vehicle_type == 'ambulance' else ''
        rect = self.canvas.create_rectangle(x, y, x + VEHICLE_SIZE, y + VEHICLE_SIZE, fill=color, outline='black')
        label = self.canvas.create_text(x + VEHICLE_SIZE // 2, y + VEHICLE_SIZE // 2, text=text)
        self.vehicles.append({'id': rect, 'label': label, 'type': vehicle_type, 'x': x})

        self.root.after(random.randint(1000, 2000), self.spawn_vehicle)

    def spawn_pedestrian(self):
        x = SIGNAL_X + random.randint(-30, 30)
        y = LANE_Y + 60  # Start just below the road
        circle = self.canvas.create_oval(x, y, x + 15, y + 15, fill='purple', outline='black')
        self.pedestrians.append({'id': circle, 'x': x, 'y': y, 'crossing': False})
        self.root.after(random.randint(3000, 5000), self.spawn_pedestrian)

    def signal_update_loop(self):
        while True:
            waiting = sum(1 for v in self.vehicles if v['x'] + VEHICLE_SIZE < SIGNAL_X)
            ambulance_present = any(v['type'] == 'ambulance' and v['x'] < SIGNAL_X for v in self.vehicles)
            data = f"{waiting},{int(ambulance_present)}"
            try:
                self.sock.sendall(data.encode())
                response = self.sock.recv(1024).decode()
                self.signal_color = response
            except:
                self.signal_color = "red"

            self.root.after(0, lambda: self.update_signal_display(waiting))
            threading.Event().wait(1)

    def update_signal_display(self, waiting):
        label_color = "green" if waiting > 10 else "black"
        self.vehicle_count_label.config(text=f"Vehicles before signal: {waiting}", fg=label_color)
        self.canvas.itemconfig(self.signal, fill=self.signal_color)

    def move_vehicles(self):
        updated_vehicles = []
        for vehicle in self.vehicles:
            x = vehicle['x']
            vehicle_type = vehicle['type']
            vehicle_id = vehicle['id']
            label_id = vehicle['label']

            speed = 4 if vehicle_type == 'car' else 3
            speed = 6 if vehicle_type == 'ambulance' else speed
            vehicle_front = x + VEHICLE_SIZE
            stop_line = SIGNAL_X - VEHICLE_SIZE - 5

            should_stop = (
                vehicle_front < stop_line and
                self.signal_color == 'red' and
                vehicle_type != 'ambulance'
            )

            collision = False
            for other in self.vehicles:
                if other == vehicle:
                    continue
                if 0 < other['x'] - x < VEHICLE_SIZE + VEHICLE_GAP:
                    collision = True
                    break

            if not should_stop and not collision:
                self.canvas.move(vehicle_id, speed, 0)
                self.canvas.move(label_id, speed, 0)
                x += speed

            if x < WIDTH:
                vehicle['x'] = x
                updated_vehicles.append(vehicle)
            else:
                self.canvas.delete(vehicle_id)
                self.canvas.delete(label_id)
                if vehicle_type == 'ambulance':
                    self.ambulance_count -= 1

        self.vehicles = updated_vehicles
        self.root.after(50, self.move_vehicles)

    def move_pedestrians(self):
        new_peds = []
        for ped in self.pedestrians:
            x, y = ped['x'], ped['y']
            circle_id = ped['id']

            # Start crossing if signal is red and pedestrian hasn't started
            if self.signal_color == 'red' and not ped['crossing']:
                ped['crossing'] = True

            if ped['crossing']:
                self.canvas.move(circle_id, 0, -2)
                y -= 2

            if y > -20:
                ped['y'] = y
                new_peds.append(ped)
            else:
                self.canvas.delete(circle_id)

        self.pedestrians = new_peds
        self.root.after(50, self.move_pedestrians)

root = tk.Tk()
app = TrafficSim(root)
root.mainloop()