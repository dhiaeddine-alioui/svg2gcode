# SVG2GCODE

- This software converts SVG files to GCode executable on 3D printers. 

## How it works ? 

- Parse the SVG file to SVGElements shapes
- Render some SVGElements shapes like Arc, Cubicbeizer and Quadratic Beizer to points in a euclidean plane, Othe shapes like Line or Polygon are already rendered
- Generate the Infill of shapes by finding the intersection points
- Use Matplotlib to display a preview of the drawing

## TO DO : 

- Add Infill with different angle lines, not only vertical lines
- Parse more the SVG file and get more useful information about the drawing
