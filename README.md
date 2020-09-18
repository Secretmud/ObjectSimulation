# Simulating movement of a object

This is a 10 ECTS weight course. The main objective of this course is to learn to work on a project,
either a practical project with a company or a project with weight on research.

## Information

src/sim.py - 1D simulation. Will be adding 2D later. But as of right now, y = f(x), and x is updated according to v and the current x position

src/3dsim.py - 2D simulation. This updates both x and y according to their respective speeds and theta z = f(x, y)

src/simulation.py - A file that will allow you run alltypes of simulations. This will give a greate advantage over having multiple singular files, as you can control the entire program from one runtime. 

src/lib/physics.py - A class that holds the few functions we currently need. We could just have them in the respective simulation-files, but it's a lot cleaner doing it this way.

## Idea

Simulate how an object acts and moves in different planes.

### Examples

- Simulate breaking distance on different surfaces
- Simulate how a object would slide down a slope, and how far it would go.


## Language

I've chosen to go with python just for the ease of prototyping. I've already come across a few speed issues using Euler-Cromer, with small step sizes the plotting becomes extremely slow, I will probably reimplement this project in a language with more memory control, much like C/C++. I can imagine that reading a plot from a CSV-file or the likes will increase the overall feel of the end product.

I've also chosen to use matplotlib for it's excellent plotting interface, and for the current iteration I use numpy and I will probably continue using it.

## Before running

```
pip install -r requirements.txt
```
