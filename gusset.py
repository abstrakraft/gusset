import cairo
import math

x_border = 0.5
y_border = 0.5

# Gusset parameters (in inches & degrees)
gusset_angle_deg = 90.0
hypotenuse = 5.0
# height of the bend area
bend_height = 2.35
# radius of cutout at the sides of the bend area
bend_radius = 2.5

dimple_diameter = 1.25

gusset_angle = math.radians(gusset_angle_deg)
gusset_width = 2 * hypotenuse * math.sin(gusset_angle/2)
gusset_height = hypotenuse * math.cos(gusset_angle/2)

base_to_dimple_center = math.tan((math.pi - gusset_angle)/4) * gusset_width/2
point_to_dimple_center = gusset_height - base_to_dimple_center

points_per_inch = 72
# in points
width = (gusset_width + x_border) * points_per_inch
height = (2 * gusset_height + bend_height + y_border) * points_per_inch

ps = cairo.PDFSurface('gusset.pdf', width, height)
ctx = cairo.Context(ps)

ctx.scale(points_per_inch, points_per_inch)

ctx.translate(x_border, y_border)

#Top triangle
ctx.move_to(gusset_width/2, 0)
ctx.line_to(gusset_width, gusset_height)
ctx.line_to(0, gusset_height)
ctx.line_to(gusset_width/2, 0)
ctx.close_path()

#Left arc
ctx.move_to(0, gusset_height)
center_offset = math.sqrt(bend_radius**2 - (bend_height/2)**2)
bend_half_angle = math.asin(bend_height/2/bend_radius)
ctx.arc(-center_offset, gusset_height + bend_height/2, bend_radius, -bend_half_angle, bend_half_angle)
ctx.close_path()

#Right arc
ctx.move_to(gusset_width, gusset_height)
ctx.arc(gusset_width + center_offset, gusset_height + bend_height/2, bend_radius, -bend_half_angle + math.pi, bend_half_angle + math.pi)
ctx.close_path()

# Top Dimple
ctx.move_to(gusset_width/2 + dimple_diameter/2, point_to_dimple_center)
ctx.arc(gusset_width/2, point_to_dimple_center, dimple_diameter/2, 0, math.pi*2)
ctx.move_to(gusset_width/2 + 0.01, point_to_dimple_center)
ctx.arc(gusset_width/2, point_to_dimple_center, 0.01, 0, math.pi*2)
ctx.close_path()

# Bottom triangle
ctx.translate(0, gusset_height + bend_height)
ctx.move_to(0, 0)
ctx.line_to(gusset_width, 0)
ctx.line_to(gusset_width/2, gusset_height)
ctx.line_to(0, 0)
ctx.close_path()

# Bottom dimple
ctx.move_to(gusset_width/2 + dimple_diameter/2, base_to_dimple_center)
ctx.arc(gusset_width/2, base_to_dimple_center, dimple_diameter/2, 0, math.pi*2)
ctx.move_to(gusset_width/2 + 0.01, base_to_dimple_center)
ctx.arc(gusset_width/2, base_to_dimple_center, 0.01, 0, math.pi*2)
ctx.close_path()

ctx.set_source_rgb(0, 0, 0)
ctx.set_line_width(0.02)
ctx.stroke()

ctx.show_page()

#surface.write_to_png('test.png')
