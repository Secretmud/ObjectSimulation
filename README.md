# Simulating movement of a object

This is a 10 ECTS weight course. The main objective of this course is to learn to work on a project,
either a practical project with a company or a project with weight on research.

## Idea

Simulate how an object acts and moves in different planes.

### Examples

- Simulate breaking distance on different surfaces
- Simulate how a object would slide down a slope, and how far it would go.
	- Simulating using different algorithms Euler Cromer, Heun's method, Runge Kutta 4 etc. 

## Language

I've chosen to go with python just for the ease of prototyping. I've already come across a few speed issues using Euler-Cromer, with small step sizes the plotting becomes extremely slow, I will probably reimplement this project in a language with more memory control, much like C/C++. I can imagine that reading a plot from a CSV-file or the likes will increase the overall feel of the end product.

I've also chosen to use matplotlib for it's excellent plotting interface, and for the current iteration I use numpy and I will probably continue using it.

## Before running

```
pip install -r requirements.txt
```


## Todo

Create a GUI for creating simulations and saving simulation setups. 
