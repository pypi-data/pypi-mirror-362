# 📦 Formulix

**Formulix** is a Python package containing essential geometry and physics formula functions. It's perfect for students, hobbyists, and developers needing fast calculations for areas, volumes, motion, and more.

---

## 🚀 Installation

Install using pip:

```bash
pip install Formulix
```

## 📊 Usage

First, import the package in your Python script:

```python
import Formulix
```

---

## 📀 Geometry Functions

### ▶️ Area Functions

```python
Formulix.rectangle_area(length, breadth)
Formulix.square_area(side)
Formulix.circle_area(radius)
Formulix.triangle_area(base, height)
Formulix.eq_triangle_area(side)
Formulix.rhombus_area(diagonal1, diagonal2)
Formulix.parallelogram_area(base, height)
Formulix.trapezium_area(base1, base2, height)
Formulix.heron_area(a, b, c)
```

### ▶️ Volume Functions

```python
Formulix.cube_volume(side)
Formulix.cuboid_volume(length, breadth, height)
Formulix.cylinder_volume(radius, height)
Formulix.cone_volume(radius, height)
Formulix.sphere_volume(radius)
```

### ▶️ Perimeter & Circumference

```python
Formulix.rectangle_perimeter(length, breadth)
Formulix.square_perimeter(side)
Formulix.triangle_perimeter(a, b, c)
Formulix.circle_circumference(radius)
Formulix.rhombus_perimeter(side)
Formulix.parallelogram_perimeter(base, side)
Formulix.trapezium_perimeter(a, b, c, d)
```

### ▶️ Pythagoras Theorem

```python
Formulix.pythagoras_hypotenuse(a, b)
Formulix.pythagoras_missing_side(hypotenuse, side)
```

---

## 🔋 Physics Functions

### ▶️ Motion

```python
Formulix.speed(distance, time)
Formulix.distance(speed, time)
Formulix.time(distance, speed)
Formulix.acceleration(final_velocity, initial_velocity, time)
```

### ▶️ Force & Weight

```python
Formulix.force(mass, acceleration)
Formulix.weight(mass, gravity=9.8)
```

---

## 🌌 Example

```python
import Formulix

print(Formulix.circle_area(7))              # 153.94...
print(Formulix.pythagoras_hypotenuse(3, 4)) # 5.0
print(Formulix.speed(100, 2))               # 50.0
```

---

## 📈 Coming Soon

* Electricity formulas
* Optics & waves
* CLI interface for command-line use

---

## ✉️ Author

**Darsh Nayak Das**


---

## 🚫 License

This project is open-source and free to use for educational purposes.
