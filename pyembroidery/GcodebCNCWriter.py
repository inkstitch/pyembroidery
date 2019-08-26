try:
	import webcolors
except ImportError:
	print('''Module "webcolors" not found. 
This module enables better thread color names.
Install with 
python -m pip install webcolors''')


	class webcolors:
		@staticmethod
		def hex_to_name(name):
			return name

from .EmbConstant import *
from .WriteHelper import write_string_utf8

STRIP_SPEEDS = True
SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_STITCH
MAX_JUMP_DISTANCE = float('inf')
MAX_STITCH_DISTANCE = float('inf')


def write(pattern, f, settings=None):
	if settings is None:
		settings = {}

	flip_x = settings.get('flip_x', False)
	flip_y = settings.get('flip_y', True)
	stitch_z_travel = settings.get('stitch_z_travel', 3.6)
	stitch_z_thread_free = settings.get('stitch_z_thread_free', 0.1)
	is_drilling = settings.get('drilling_cycle', False)
	feed_rate = settings.get('feed_rate', -1)

	stitch_z_travel -= stitch_z_thread_free
	if stitch_z_travel < 0:
		stitch_z_travel = 0

	# pyembroidery natively uses tenths of a millimeter
	extents = [extent / 10.0 for extent in pattern.extents()]
	width = extents[2] - extents[0]
	height = extents[3] - extents[1]

	header_block(f, feed_rate, pattern.count_stitches())

	z = 0
	stitching = False
	thread_id = -1
	thread_list = pattern.threadlist
	num_col_changes = 0
	for x, y, command in pattern.stitches:
		if command == COLOR_CHANGE:
			num_col_changes += 1

	for x, y, command in pattern.stitches:
		# embroidery G-code discussion: https://github.com/inkstitch/inkstitch/issues/335
		if x is not None:
			if flip_x:
				x = -x
			# pyembroidery natively uses tenths of a millimeter
			x /= 10.0
		if y is not None:
			if flip_y:
				y = -y
			# pyembroidery natively uses tenths of a millimeter
			y /= 10.0

		if command == COLOR_CHANGE:
			if thread_id < 0:
				thread_id = 0
			switch_thread(f, thread_id, thread_list)
			thread_id += 1

		if command == JUMP:
			if thread_id < 0:
				thread_id = 0 if num_col_changes < len(thread_list) else -1
				switch_thread(f, thread_id, thread_list)
				thread_id += 1
			write_string_utf8(f, "G0 X%.3f Y%.3f\r\n" % (x, y))

		if command == STITCH:
			if thread_id < 0:
				thread_id = 0 if num_col_changes < len(thread_list) else -1
				switch_thread(f, thread_id, thread_list)
				thread_id += 1
			if is_drilling:
				write_string_utf8(f, "G80 X%.3f Y%.3f Z%.3f R%.3f (stitch cycle)\r\n" % (x, y, stitch_z_travel, stitch_z_thread_free))
			else:
				zcmd = ''
				if stitch_z_thread_free > 0:
					z += stitch_z_thread_free
					zcmd = " Z%.3f" % z
				write_string_utf8(f, "G1 X%.3f Y%.3f%s\r\n" % (x, y, zcmd))
				if stitch_z_travel > 0:
					z += stitch_z_travel
					write_string_utf8(f, "G1 Z%.1f\r\n" % z)
	footer_block(f)


def footer_block(f):
	write_string_utf8(f, "(Block-name: Footer)\r\n");
	write_string_utf8(f, "(Block-expand: 0)\r\n");
	write_string_utf8(f, "(Block-enable: 1)\r\n");
	write_string_utf8(f, "G0 X0.0 Y0.0 (Go to origin)\r\n")
	write_string_utf8(f, "M18 (Disable all stepper motors)\r\n")
	write_string_utf8(f, "M30 (End of program)\r\n")


def header_block(f, feed_rate=-1, num_stitches=-1):
	write_string_utf8(f, "(Block-name: Header)\r\n")
	write_string_utf8(f, "(Block-expand: 0)\r\n")
	write_string_utf8(f, "(Block-enable: 1)\r\n")
	if num_stitches > 0:
		write_string_utf8(f, '(STITCH_COUNT:%d)\r\n' % num_stitches)
	write_string_utf8(f, '(EXTENTS_LEFT:[xmin])\r\n')
	write_string_utf8(f, '(EXTENTS_TOP:[ymin])\r\n')
	write_string_utf8(f, '(EXTENTS_RIGHT:[xmax])\r\n')
	write_string_utf8(f, '(EXTENTS_BOTTOM:[ymax])\r\n')
	write_string_utf8(f, '(EXTENTS_WIDTH:[xmax-xmin])\r\n')
	write_string_utf8(f, '(EXTENTS_HEIGHT:[ymax-ymin])\r\n')
	write_string_utf8(f, "G90 (use absolute coordinates)\r\n")
	write_string_utf8(f, "G21 (coordinates will be specified in millimeters)\r\n")
	write_string_utf8(f, "G92 X0.0 Y0.0 Z0.0 (current position is the origin)\r\n")
	if feed_rate > 0:
		write_string_utf8(f, "G1 X0.0 Y0.0 F%d\r\n" % (feed_rate))
		write_string_utf8(f, "G0 X0.0 Y0.0 F%d\r\n" % (feed_rate))
	write_string_utf8(f, "\r\n")


def closest_colour(requested_colour):
	requested_colour = webcolors.hex_to_rgb(requested_colour)
	min_colours = {}
	for key, name in webcolors.css3_hex_to_names.items():
		r_c, g_c, b_c = webcolors.hex_to_rgb(key)
		rd = (r_c - requested_colour[0]) ** 2
		gd = (g_c - requested_colour[1]) ** 2
		bd = (b_c - requested_colour[2]) ** 2
		min_colours[(rd + gd + bd)] = name
	return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
	try:
		closest_name = actual_name = webcolors.hex_to_name(requested_colour)
	except ValueError:
		closest_name = closest_colour(requested_colour)
		actual_name = None
	return actual_name, closest_name


def dump_thread_data(f, selected_thread):
	thread_attrs = [a for a in dir(selected_thread) if not a.startswith('__') and not callable(getattr(selected_thread, a))]
	for variable in thread_attrs:
		if variable.upper() == 'COLOR':
			_, thread_color = get_colour_name(selected_thread.hex_color())
			varvalue = thread_color.title() + ' <' + selected_thread.hex_color() + '>'
		else:
			varvalue = getattr(selected_thread, variable)
			if varvalue == 'None':
				varvalue = None
		if varvalue:
			readable = variable.replace('_', ' ').capitalize().strip()
			if readable:
				write_string_utf8(f, '(%s: %s)\r\n' % (readable, varvalue))


def switch_thread(f, thread_id, threads_list):
	if thread_id < 0:
		thread_id = len(threads_list)
	if len(threads_list) <= thread_id:
		write_string_utf8(f, "(Block-name: Default Thread)\r\n")
		write_string_utf8(f, "(Block-expand: 0)\r\n")
		write_string_utf8(f, "(Block-enable: 1)\r\n")
	else:
		selected_thread = threads_list[thread_id]
		_, thread_color = get_colour_name(selected_thread.hex_color())
		thread_desc = ", Color: %s" % thread_color.title()
		if selected_thread.catalog_number == 'None':
			selected_thread.catalog_number = None
		thread_desc += (', Catalog number: %s' % selected_thread.catalog_number) if selected_thread.catalog_number else ""
		write_string_utf8(f, "(Block-name: Thread #%d%s)\r\n" % (thread_id, thread_desc))
		write_string_utf8(f, "(Block-expand: 0)\r\n")
		write_string_utf8(f, "(Block-enable: 1)\r\n")
		write_string_utf8(f, "(Block-color: %s)\r\n" % selected_thread.hex_color())
		dump_thread_data(f, selected_thread)
		write_string_utf8(f, "%wait\r\n")
		thread_catalog_id = (",ID:%s"%selected_thread.catalog_number) if selected_thread.catalog_number else ""
		write_string_utf8(f, "%%msg (Change%d)New color:%s%s\r\n" % (thread_id, thread_color.title(),thread_catalog_id))
		write_string_utf8(f, "M0 (pause)\r\n")
